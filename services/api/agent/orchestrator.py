"""
Autonomous AI Analyst & Reflexion Orchestration Engine.
Coordinates schema grounding, native LLM tool-calling, automated error recovery
(Reflexion loop up to 3 retries), sandbox execution, and real-time SSE streaming.
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional

from sqlmodel import Session, select

from services.api.agent.prompts import (
    build_reflexion_prompt,
    build_synthesis_prompt,
    build_system_prompt,
)
from services.api.agent.providers import BaseLLMProvider, get_llm_provider
from services.api.models import ChatTurn, Session as DbSession
from services.api.session_service import session_service


def format_sse(event: str, data: Dict[str, Any]) -> str:
    """Format structured payload into a Server-Sent Event (SSE) frame."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


class AgentOrchestrator:
    """Orchestrates multi-turn analytical reasoning, code generation, and Reflexion."""

    def __init__(self, provider: Optional[BaseLLMProvider] = None) -> None:
        self.provider = provider or get_llm_provider()

    async def run_chat_stream(
        self,
        db: Session,
        session_id: str,
        user_prompt: str,
        max_attempts: int = 3,
        provider_name: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Execute an autonomous analytical turn with real-time SSE streaming.
        Emits token, code_generated, execution_status, execution_stdout,
        chart_generated, reflexion_step, and turn_complete events.
        """
        active_provider = (
            get_llm_provider(provider_name, model_name)
            if (provider_name or model_name)
            else get_llm_provider()
        )
        start_time = time.perf_counter()
        turn_id = f"trn_{uuid.uuid4().hex[:12]}"

        # 1. Fetch Session & Active Schema Context
        session_obj = session_service.get_session(db, session_id)
        if not session_obj:
            yield format_sse("error", {"error": f"Session '{session_id}' not found."})
            return

        profiles = session_service.get_session_profiles(db, session_id)
        system_prompt = build_system_prompt(profiles)

        # 2. Build Context Messages
        messages: List[Dict[str, Any]] = [{"role": "user", "content": user_prompt}]

        exec_res = None
        executed_code = ""
        reflexion_count = 0

        # 3. Reflexion Execution Loop (Up to max_attempts)
        for attempt in range(1, max_attempts + 1):
            yield format_sse("execution_status", {"status": "generating_code", "attempt": attempt})

            try:
                tool_call = await active_provider.generate_code_call(messages, system_prompt)
                executed_code = tool_call.code
            except Exception as exc:
                yield format_sse("error", {"error": f"LLM generation failed: {str(exc)}"})
                return

            yield format_sse(
                "code_generated",
                {
                    "code": executed_code,
                    "language": "python",
                    "thought": tool_call.thought or "",
                    "attempt": attempt,
                },
            )

            yield format_sse("execution_status", {"status": "running_sandbox", "attempt": attempt})

            # Execute code inside the isolated stateful sandbox
            exec_res = await session_service.execute_code(
                db=db,
                session_id=session_id,
                code=executed_code,
                user_prompt=user_prompt,
            )

            # Check for success
            if exec_res.status == "success":
                yield format_sse("execution_stdout", {"stdout": exec_res.stdout})

                # Stream any generated Plotly figures
                for fig in exec_res.figures:
                    yield format_sse("chart_generated", {"figure_type": "plotly", "spec": fig})

                if exec_res.has_mutated_dataframe:
                    db.refresh(session_obj)
                    yield format_sse(
                        "checkpoint_created",
                        {
                            "version_tag": session_obj.active_dataframe_version,
                            "df_shape": exec_res.df_shape,
                            "operation": user_prompt[:100],
                        },
                    )
                    # Emit dataset payload for TanStack Query cache
                    ds_data = session_service.get_dataset_data(
                        db, session_id, session_obj.active_dataframe_version, limit=1000
                    )
                    if ds_data:
                        yield format_sse("dataset", ds_data)

                break  # Successful execution, exit Reflexion loop

            # Handle execution failure (Reflexion self-correction trigger)
            reflexion_count += 1
            error_msg = exec_res.stderr.strip() or f"Execution failed with status: {exec_res.status}"
            short_error = error_msg.splitlines()[-1] if error_msg.splitlines() else error_msg

            if attempt < max_attempts:
                yield format_sse(
                    "reflexion_step",
                    {
                        "attempt": attempt,
                        "error": short_error,
                        "status": "retrying",
                    },
                )

                # Feed error feedback into conversation history
                messages.append(
                    {"role": "assistant", "content": f"Executed code:\n```python\n{executed_code}\n```"}
                )
                reflexion_feedback = build_reflexion_prompt(
                    failed_code=executed_code,
                    error_traceback=error_msg,
                    attempt=attempt,
                    max_attempts=max_attempts,
                )
                messages.append({"role": "user", "content": reflexion_feedback})
            else:
                # All attempts exhausted
                yield format_sse(
                    "error",
                    {
                        "error": "Reflexion limit reached. Code execution could not self-correct.",
                        "detail": error_msg,
                        "attempts": attempt,
                    },
                )
                return

        # 4. Conversational Interpretation Pass (Natural Language Insights)
        yield format_sse("execution_status", {"status": "synthesizing_insights"})

        has_charts = bool(exec_res and exec_res.figures)
        synthesis_prompt = build_synthesis_prompt(
            user_prompt=user_prompt,
            code=executed_code,
            stdout=exec_res.stdout if exec_res else "",
            has_figures=has_charts,
        )
        synthesis_messages = [{"role": "user", "content": synthesis_prompt}]

        full_explanation = ""
        try:
            async for token in active_provider.synthesize_explanation_stream(
                synthesis_messages, system_prompt
            ):
                full_explanation += token
                yield format_sse("token", {"token": token, "turn_id": turn_id})
        except Exception as exc:
            yield format_sse("error", {"error": f"Synthesis stream error: {str(exc)}"})

        # 4.5. Decoupled Dataset Event for TanStack Query & Table
        try:
            ds = session_service.get_dataset_data(db, session_id, limit=5000)
            if ds:
                yield format_sse("dataset", ds)
        except Exception:
            pass

        # 5. Final Turn Complete Event
        total_duration_ms = int((time.perf_counter() - start_time) * 1000)
        yield format_sse(
            "turn_complete",
            {
                "turn_id": turn_id,
                "active_version": session_obj.active_dataframe_version,
                "duration_ms": total_duration_ms,
                "reflexion_count": reflexion_count,
                "has_mutated_df": exec_res.has_mutated_dataframe if exec_res else False,
                "df_shape": exec_res.df_shape if exec_res else None,
            },
        )

    async def run_chat_sync(
        self,
        db: Session,
        session_id: str,
        user_prompt: str,
        max_attempts: int = 3,
        provider_name: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Synchronous non-streaming execution wrapper. Consumes the SSE stream
        and returns a unified turn response dictionary.
        """
        explanation = ""
        code = ""
        stdout = ""
        stderr = ""
        figures: List[Dict[str, Any]] = []
        reflexion_steps: List[Dict[str, Any]] = []
        turn_metadata: Dict[str, Any] = {}
        error_info: Optional[Dict[str, Any]] = None

        async for chunk in self.run_chat_stream(
            db=db,
            session_id=session_id,
            user_prompt=user_prompt,
            max_attempts=max_attempts,
            provider_name=provider_name,
            model_name=model_name,
        ):
            # Parse SSE lines
            lines = [line for line in chunk.strip().splitlines() if line]
            if len(lines) >= 2:
                event_type = lines[0].replace("event: ", "").strip()
                data_str = lines[1].replace("data: ", "").strip()
                try:
                    payload = json.loads(data_str)
                except Exception:
                    continue

                if event_type == "token":
                    explanation += payload.get("token", "")
                elif event_type == "code_generated":
                    code = payload.get("code", "")
                elif event_type == "execution_stdout":
                    stdout = payload.get("stdout", "")
                elif event_type == "chart_generated":
                    figures.append(payload.get("spec", {}))
                elif event_type == "reflexion_step":
                    reflexion_steps.append(payload)
                elif event_type == "turn_complete":
                    turn_metadata = payload
                elif event_type == "error":
                    error_info = payload

        if error_info:
            return {
                "status": "error",
                "error": error_info.get("error", "Unknown error"),
                "detail": error_info.get("detail", ""),
                "code": code,
                "reflexion_steps": reflexion_steps,
            }

        return {
            "status": "success",
            "turn_id": turn_metadata.get("turn_id", ""),
            "explanation": explanation.strip(),
            "code": code,
            "stdout": stdout,
            "stderr": stderr,
            "figures": figures,
            "reflexion_count": turn_metadata.get("reflexion_count", 0),
            "duration_ms": turn_metadata.get("duration_ms", 0),
            "has_mutated_df": turn_metadata.get("has_mutated_df", False),
            "df_shape": turn_metadata.get("df_shape"),
            "active_version": turn_metadata.get("active_version", "df_v0"),
        }


# Global orchestrator instance
agent_orchestrator = AgentOrchestrator()
