"""
Multi-Agent Swarm Coordinator for Track D.
Coordinates the collaborative loop between Analyst Agent, Statistician Critic,
Sandbox Execution Kernel, and Executive Synthesizer.
"""

from __future__ import annotations

import json
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

import pandas as pd
from sqlmodel import Session

from services.api.agent.critic import statistician_critic
from services.api.agent.prompts import (
    build_reflexion_prompt,
    build_synthesis_prompt,
    build_system_prompt,
)
from services.api.agent.providers import BaseLLMProvider, get_llm_provider
from services.api.models import (
    ChatTurn,
    CriticReview,
    DebateExchange,
    Session as DbSession,
)
from services.api.session_service import session_service


def format_sse(event: str, data: Dict[str, Any]) -> str:
    """Format structured payload into a Server-Sent Event (SSE) frame."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


class SwarmCoordinator:
    """Coordinates collaborative multi-agent execution with peer review and debate."""

    def __init__(self, provider: Optional[BaseLLMProvider] = None) -> None:
        self.provider = provider or get_llm_provider()

    async def run_swarm_turn(
        self,
        db: Session,
        session_id: str,
        user_prompt: str,
        provider_name: Optional[str] = None,
        model_name: Optional[str] = None,
        max_debate_rounds: int = 2,
    ) -> AsyncGenerator[str, None]:
        """
        Executes a peer-reviewed multi-agent analytical turn.
        Streams swarm phases, code generation, critic reviews, debate steps,
        execution results, and final synthesized takeaways.
        """
        active_provider = (
            get_llm_provider(provider_name, model_name)
            if (provider_name or model_name)
            else get_llm_provider()
        )

        session_obj = session_service.get_session(db, session_id)
        if not session_obj:
            yield format_sse("error", {"error": f"Session '{session_id}' not found."})
            return

        profiles = session_service.get_session_profiles(db, session_id)
        system_prompt = build_system_prompt(profiles)

        # ------------------------------------------------------------------
        # Phase 1: Analyst Agent Planning & Code Generation
        # ------------------------------------------------------------------
        yield format_sse(
            "swarm_phase",
            {"phase": "analyst_planning", "message": "Analyst proposing analytical plan and Python code...", "step": 1},
        )

        messages: List[Dict[str, Any]] = [{"role": "user", "content": user_prompt}]
        try:
            tool_call = await active_provider.generate_code_call(messages, system_prompt)
            executed_code = tool_call.code
        except Exception as exc:
            yield format_sse("error", {"error": f"Analyst code generation failed: {str(exc)}"})
            return

        yield format_sse(
            "code_generated",
            {"code": executed_code, "language": "python", "thought": tool_call.thought or "", "attempt": 1},
        )

        # ------------------------------------------------------------------
        # Phase 2: Critic Pre-Execution AST Screening
        # ------------------------------------------------------------------
        yield format_sse(
            "swarm_phase",
            {"phase": "critic_pre_review", "message": "Statistician pre-screening AST for data loss & methodology...", "step": 2},
        )

        pre_review = statistician_critic.pre_execute_audit(executed_code)
        yield format_sse("critic_review", pre_review.model_dump())

        debate_history: List[DebateExchange] = []

        # If Critic requests revision, enter Phase 2 Debate Loop
        if pre_review.verdict == "requires_revision":
            for d_round in range(1, max_debate_rounds + 1):
                yield format_sse(
                    "swarm_phase",
                    {"phase": "debate_turn", "message": f"Swarm Debate Round {d_round}: Analyst revising code...", "step": 2},
                )
                debate_exchange = DebateExchange(
                    turn_num=d_round,
                    speaker="critic",
                    message=f"Statistical objection: {pre_review.critique}. Suggestion: {pre_review.suggested_fix or 'Refine methodology.'}",
                )
                debate_history.append(debate_exchange)
                yield format_sse("debate_step", debate_exchange.model_dump())

                # Analyst self-correction prompt
                critic_feedback = (
                    f"Statistician peer-review rejected the code:\n"
                    f"Warning: {pre_review.statistical_warnings}\n"
                    f"Fix requirement: {pre_review.suggested_fix or 'Address mathematical fallacy.'}\n"
                    f"Please provide revised Python code."
                )
                messages.append({"role": "assistant", "content": f"```python\n{executed_code}\n```"})
                messages.append({"role": "user", "content": critic_feedback})

                try:
                    tool_call = await active_provider.generate_code_call(messages, system_prompt)
                    executed_code = tool_call.code
                except Exception:
                    break

                yield format_sse(
                    "code_generated",
                    {"code": executed_code, "language": "python", "thought": f"Analyst revision round {d_round}", "attempt": d_round + 1},
                )

                pre_review = statistician_critic.pre_execute_audit(executed_code)
                yield format_sse("critic_review", pre_review.model_dump())
                if pre_review.verdict != "requires_revision":
                    break

        # ------------------------------------------------------------------
        # Phase 3: Sandbox Execution
        # ------------------------------------------------------------------
        yield format_sse(
            "swarm_phase",
            {"phase": "sandbox_executing", "message": "Executing reviewed code in isolated kernel...", "step": 3},
        )

        exec_res = await session_service.execute_code(
            db=db,
            session_id=session_id,
            code=executed_code,
            user_prompt=user_prompt,
        )

        if exec_res.status != "success":
            yield format_sse("error", {"error": exec_res.stderr or "Code execution failed."})
            return

        yield format_sse("execution_stdout", {"stdout": exec_res.stdout})

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
            ds_data = session_service.get_dataset_data(
                db, session_id, session_obj.active_dataframe_version, limit=1000
            )
            if ds_data:
                yield format_sse("dataset", ds_data)

        # ------------------------------------------------------------------
        # Phase 4: Critic Post-Execution Statistical Audit
        # ------------------------------------------------------------------
        yield format_sse(
            "swarm_phase",
            {"phase": "critic_post_audit", "message": "Statistician auditing outputs, sample size & distribution skew...", "step": 4},
        )

        post_review = statistician_critic.post_execute_audit(
            code=executed_code,
            stdout=exec_res.stdout,
            figures=exec_res.figures,
        )
        yield format_sse("critic_review", post_review.model_dump())

        # ------------------------------------------------------------------
        # Phase 5: Executive Synthesis with Statistical Caveats
        # ------------------------------------------------------------------
        yield format_sse(
            "swarm_phase",
            {"phase": "synthesizing", "message": "Synthesizing executive findings with peer-reviewed confidence...", "step": 5},
        )

        caveats_text = ""
        if post_review.statistical_warnings:
            caveats_text = "\n\n**Statistical Peer-Review Caveats**:\n" + "\n".join(
                f"- ⚠️ {w}" for w in post_review.statistical_warnings
            )

        has_charts = bool(exec_res and exec_res.figures)
        synthesis_prompt = build_synthesis_prompt(
            user_prompt=user_prompt,
            code=executed_code,
            stdout=exec_res.stdout + caveats_text,
            has_figures=has_charts,
        )

        full_synthesis = []
        try:
            async for token in active_provider.stream_synthesis(messages, synthesis_prompt):
                full_synthesis.append(token)
                yield format_sse("token", {"token": token})
        except Exception:
            fallback = f"Analysis complete. {post_review.critique}{caveats_text}"
            yield format_sse("token", {"token": fallback})

        # Save turn to database with critic and debate payloads
        try:
            turn_record = ChatTurn(
                session_id=session_id,
                user_prompt=user_prompt,
                generated_code=executed_code,
                stdout=exec_res.stdout,
                stderr=None,
                status="success",
                critic_review_json=post_review.model_dump_json(),
                debate_history_json=json.dumps([d.model_dump() for d in debate_history]) if debate_history else None,
            )
            db.add(turn_record)
            db.commit()
        except Exception:
            pass

        yield format_sse(
            "turn_complete",
            {
                "status": "success",
                "session_id": session_id,
                "confidence_score": post_review.confidence_score,
                "critic_verdict": post_review.verdict,
            },
        )


swarm_coordinator = SwarmCoordinator()
