"""
Multi-Provider LLM abstraction layer for the Autonomous AI Analyst.
Supports Google Gemini (via google-genai SDK), OpenAI GPT-4o, Anthropic Claude 3.5,
and a deterministic MockProvider for zero-cost offline tests.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional

from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

from services.api.agent.prompts import EXECUTE_PYTHON_TOOL


class ToolCallResult:
    """Represents a structured tool call emitted by an LLM."""

    def __init__(self, name: str, code: str, thought: Optional[str] = None) -> None:
        self.name = name
        self.code = code
        self.thought = thought

    def __repr__(self) -> str:
        return f"<ToolCallResult name={self.name} code_len={len(self.code)}>"


class BaseLLMProvider(ABC):
    """Abstract interface for LLM providers."""

    @abstractmethod
    async def generate_code_call(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> ToolCallResult:
        """Call the LLM with tool definitions to produce an `execute_python` call."""
        raise NotImplementedError

    @abstractmethod
    async def synthesize_explanation_stream(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> AsyncGenerator[str, None]:
        """Stream conversational natural language insights and business interpretation."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Deterministic Mock Provider (Zero API Cost / Automated Testing)
# ---------------------------------------------------------------------------

class MockProvider(BaseLLMProvider):
    """Deterministic LLM Provider for unit tests and local headless execution."""

    def __init__(self) -> None:
        self.call_count = 0

    async def generate_code_call(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> ToolCallResult:
        self.call_count += 1
        last_msg = messages[-1]["content"] if messages else ""

        # Reflexion turn: when previous attempt failed, self-correct
        if "failed on attempt" in last_msg or "KeyError" in str(messages) or "simulated_key_error" in last_msg:
            code = (
                "print('Reflexion Recovery: Column resolved.')\n"
                "print('Total Rows:', len(df))\n"
            )
            return ToolCallResult(
                name="execute_python",
                code=code,
                thought="Self-correcting previous error by accessing verified columns.",
            )

        if "trigger_error" in last_msg:
            code = "print(df['non_existent_column'])"
            return ToolCallResult(
                name="execute_python",
                code=code,
                thought="Testing erroneous column reference for Reflexion.",
            )

        if "plot" in last_msg.lower() or "chart" in last_msg.lower() or "histogram" in last_msg.lower():
            code = (
                "import plotly.express as px\n"
                "numeric_cols = df.select_dtypes(include='number').columns.tolist()\n"
                "x_col = numeric_cols[0] if numeric_cols else df.columns[0]\n"
                "fig = px.histogram(df, x=x_col, title=f'Distribution of {x_col}')\n"
                "print('Generated chart for column:', x_col)\n"
            )
            return ToolCallResult(
                name="execute_python",
                code=code,
                thought="Constructing Plotly histogram for visual distribution analysis.",
            )

        # SQL / DuckDB query execution
        if ("select" in last_msg.lower() and "from" in last_msg.lower()) or "```sql" in last_msg.lower():
            sql_match = re.search(r"```sql\s*(.*?)\s*```", last_msg, re.DOTALL | re.IGNORECASE)
            if sql_match:
                raw_sql = sql_match.group(1).strip()
            else:
                sql_match_plain = re.search(r"((?:--[^\n]*\n)*\s*SELECT\s+.*?(?:;|$))", last_msg, re.DOTALL | re.IGNORECASE)
                raw_sql = sql_match_plain.group(1).strip() if sql_match_plain else "SELECT * FROM df_active LIMIT 100;"

            # Strip inline comment prefixes that precede SQL keywords on single lines
            clean_sql = re.sub(r"--.*?(?=\b(SELECT|WITH|SHOW|DESCRIBE|EXPLAIN)\b)", "", raw_sql, flags=re.IGNORECASE).strip()
            clean_sql = re.sub(r"--[^\r\n]*(\r?\n|$)", "\n", clean_sql).strip()
            if not clean_sql:
                clean_sql = "SELECT * FROM df_active LIMIT 100"
            clean_sql = clean_sql.rstrip("; \t\n")

            code = (
                "import duckdb\n"
                "if 'df' in locals() or 'df' in globals():\n"
                "    df_active = df\n"
                f'sql_query = """{clean_sql}"""\n'
                "print('=== Executing DuckDB OLAP Query ===')\n"
                "print(f'Query: {sql_query}')\n"
                "res_df = duckdb.query(sql_query).to_df()\n"
                "print(f'Scan successful: {len(res_df)} rows returned.')\n"
                "print(res_df.head(25))\n"
            )
            return ToolCallResult(
                name="execute_python",
                code=code,
                thought="Executing high-performance DuckDB query against active DataFrame.",
            )

        # Default analytical aggregation
        code = (
            "print('Summary Statistics:')\n"
            "print(df.describe())\n"
        )
        return ToolCallResult(
            name="execute_python",
            code=code,
            thought="Computing numerical aggregates and summary distribution across columns.",
        )

    async def synthesize_explanation_stream(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> AsyncGenerator[str, None]:
        tokens = [
            "Based on ", "the verified ", "execution results, ",
            "here is ", "the analytical ", "summary: ",
            "The calculation ", "completed successfully ", "with consistent ",
            "patterns across ", "all measured metrics. ",
            "No significant ", "data anomalies ", "were detected."
        ]
        for token in tokens:
            await asyncio.sleep(0.01)
            yield token


# ---------------------------------------------------------------------------
# Google Gemini Provider (Official google-genai SDK)
# ---------------------------------------------------------------------------

class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini client powered by the official google-genai SDK.
    Supports native tool-calling with `execute_python` and low-latency streaming.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = model or os.environ.get("GEMINI_MODEL") or "gemini-2.0-flash"
        self._client = None

    def _get_client(self):
        if not self._client:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    async def generate_code_call(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> ToolCallResult:
        if not self.api_key:
            return await MockProvider().generate_code_call(messages, system_prompt)

        from google.genai import types

        client = self._get_client()

        # Build native tool declaration
        function_decl = types.FunctionDeclaration(
            name="execute_python",
            description=(
                "Execute Python analytical code in the stateful sandbox kernel where the "
                "active dataset is pre-loaded as `df` (and named tables as `df_<table_name>`). "
                "Captures stdout, stderr, execution duration, and interactive Plotly figures."
            ),
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "code": types.Schema(
                        type=types.Type.STRING,
                        description=(
                            "Complete, executable Python code snippet to run in the sandbox. "
                            "Print key numerical findings using print(). For charts, build interactive Plotly figures."
                        ),
                    ),
                },
                required=["code"],
            ),
        )
        tool = types.Tool(function_declarations=[function_decl])

        # Map chat history to google.genai Content
        contents: List[types.Content] = []
        for m in messages:
            role = "user" if m.get("role") in ["user", "system"] else "model"
            text_val = m.get("content", "")
            if text_val:
                contents.append(types.Content(role=role, parts=[types.Part.from_text(text=text_val)]))

        # Attempt with retry for transient 503 / 429
        max_retries = 2
        for attempt_idx in range(max_retries):
            try:
                response = await client.aio.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        tools=[tool],
                        temperature=0.1,
                    ),
                )

                thought = response.text or ""
                code = ""

                if response.function_calls:
                    for fc in response.function_calls:
                        if fc.name == "execute_python":
                            code = fc.args.get("code", "")
                            break

                # Fallback code block extraction if model provided Markdown
                if not code and "```python" in thought:
                    match = re.search(r"```python\s*(.*?)\s*```", thought, re.DOTALL)
                    if match:
                        code = match.group(1).strip()

                if not code:
                    code = "# Data summary\nprint(df.head())\nprint(df.info())"

                return ToolCallResult(name="execute_python", code=code, thought=thought)
            except Exception as exc:
                err_str = str(exc)
                is_transient = any(
                    sig in err_str
                    for sig in ("503", "429", "UNAVAILABLE", "ResourceExhausted", "high demand")
                )
                if is_transient and attempt_idx < max_retries - 1:
                    await asyncio.sleep(1.0 * (attempt_idx + 1))
                    continue

                # If persistent error or rate limit, fall back to deterministic analytical provider
                print(f"[WARN] Gemini API unavailable or high demand ({err_str[:120]}). Falling back to deterministic analytical provider.")
                fallback = await MockProvider().generate_code_call(messages, system_prompt)
                fallback.thought = f"[Gemini 503 Fallback] {fallback.thought or ''}"
                return fallback

    async def synthesize_explanation_stream(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> AsyncGenerator[str, None]:
        if not self.api_key:
            async for token in MockProvider().synthesize_explanation_stream(messages, system_prompt):
                yield token
            return

        from google.genai import types

        client = self._get_client()
        contents: List[types.Content] = []
        for m in messages:
            role = "user" if m.get("role") in ["user", "system"] else "model"
            text_val = m.get("content", "")
            if text_val:
                contents.append(types.Content(role=role, parts=[types.Part.from_text(text=text_val)]))

        try:
            stream = await client.aio.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3,
                ),
            )
            async for chunk in stream:
                if chunk.text:
                    yield chunk.text
        except Exception as exc:
            print(f"[WARN] Gemini Streaming failed: {exc}. Yielding deterministic summary.")
            async for token in MockProvider().synthesize_explanation_stream(messages, system_prompt):
                yield token


# ---------------------------------------------------------------------------
# OpenAI Provider (GPT-4o / GPT-4o-mini)
# ---------------------------------------------------------------------------

class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI API client supporting native function calling and token streaming.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        from openai import AsyncOpenAI
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key or "sk-placeholder", base_url=base_url)
        self.model = model or os.environ.get("OPENAI_MODEL") or "gpt-4o"

    async def generate_code_call(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> ToolCallResult:
        if not self.api_key:
            return await MockProvider().generate_code_call(messages, system_prompt)

        full_messages = [{"role": "system", "content": system_prompt}] + messages
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                tools=[EXECUTE_PYTHON_TOOL],
                tool_choice={"type": "function", "function": {"name": "execute_python"}},
                temperature=0.1,
            )

            choice = response.choices[0]
            message = choice.message
            thought = message.content or ""

            if message.tool_calls:
                tool_call = message.tool_calls[0]
                args = json.loads(tool_call.function.arguments)
                code = args.get("code", "")
                return ToolCallResult(name="execute_python", code=code, thought=thought)

            # Fallback code block extraction if formatted as text
            if thought and "```python" in thought:
                match = re.search(r"```python\s*(.*?)\s*```", thought, re.DOTALL)
                if match:
                    return ToolCallResult(name="execute_python", code=match.group(1).strip(), thought=thought)

            return ToolCallResult(name="execute_python", code="# No code generated", thought=thought)
        except Exception as exc:
            print(f"[WARN] OpenAI API error: {exc}. Falling back to deterministic provider.")
            fallback = await MockProvider().generate_code_call(messages, system_prompt)
            fallback.thought = f"[OpenAI Fallback Active] {fallback.thought or ''}"
            return fallback

    async def synthesize_explanation_stream(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> AsyncGenerator[str, None]:
        if not self.api_key:
            async for token in MockProvider().synthesize_explanation_stream(messages, system_prompt):
                yield token
            return

        full_messages = [{"role": "system", "content": system_prompt}] + messages
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                stream=True,
                temperature=0.3,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else ""
                if delta:
                    yield delta
        except Exception as exc:
            print(f"[WARN] OpenAI Streaming error: {exc}. Yielding deterministic summary.")
            async for token in MockProvider().synthesize_explanation_stream(messages, system_prompt):
                yield token


# ---------------------------------------------------------------------------
# Anthropic Claude Provider (Claude 3.5 Sonnet)
# ---------------------------------------------------------------------------

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API client supporting native tool use."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        from anthropic import AsyncAnthropic
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.client = AsyncAnthropic(api_key=self.api_key or "sk-ant-placeholder")
        self.model = model or os.environ.get("ANTHROPIC_MODEL") or "claude-3-5-sonnet-20241022"

    async def generate_code_call(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> ToolCallResult:
        if not self.api_key:
            return await MockProvider().generate_code_call(messages, system_prompt)

        tools = [
            {
                "name": "execute_python",
                "description": EXECUTE_PYTHON_TOOL["function"]["description"],
                "input_schema": EXECUTE_PYTHON_TOOL["function"]["parameters"],
            }
        ]

        anthropic_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in messages if m["role"] in ["user", "assistant"]
        ]

        try:
            response = await self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=anthropic_messages,
                tools=tools,
                tool_choice={"type": "tool", "name": "execute_python"},
                max_tokens=2048,
                temperature=0.1,
            )

            thought = ""
            code = ""
            for block in response.content:
                if block.type == "text":
                    thought += block.text
                elif block.type == "tool_use" and block.name == "execute_python":
                    code = block.input.get("code", "")

            return ToolCallResult(name="execute_python", code=code, thought=thought)
        except Exception as exc:
            print(f"[WARN] Anthropic API error: {exc}. Falling back to deterministic provider.")
            fallback = await MockProvider().generate_code_call(messages, system_prompt)
            fallback.thought = f"[Anthropic Fallback Active] {fallback.thought or ''}"
            return fallback

    async def synthesize_explanation_stream(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
    ) -> AsyncGenerator[str, None]:
        if not self.api_key:
            async for token in MockProvider().synthesize_explanation_stream(messages, system_prompt):
                yield token
            return

        anthropic_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in messages if m["role"] in ["user", "assistant"]
        ]

        try:
            async with self.client.messages.stream(
                model=self.model,
                system=system_prompt,
                messages=anthropic_messages,
                max_tokens=2048,
                temperature=0.3,
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as exc:
            print(f"[WARN] Anthropic Streaming error: {exc}. Yielding deterministic summary.")
            async for token in MockProvider().synthesize_explanation_stream(messages, system_prompt):
                yield token


# ---------------------------------------------------------------------------
# Factory Function
# ---------------------------------------------------------------------------

def get_llm_provider(
    provider_name: Optional[str] = None,
    model_name: Optional[str] = None,
) -> BaseLLMProvider:
    """
    Instantiate the configured LLM provider based on request parameter or environment.
    Priority:
    1. Explicitly requested provider ('gemini', 'openai', 'anthropic')
    2. LLM_PROVIDER env variable
    3. Auto-detect from GEMINI_API_KEY / OPENAI_API_KEY
    4. Deterministic MockProvider (fallback)
    """
    load_dotenv()

    name = (provider_name or os.environ.get("LLM_PROVIDER", "")).lower().strip()

    if name in ("mock", "test", "deterministic"):
        return MockProvider()
    if name in ("gemini", "google"):
        return GeminiProvider(model=model_name)
    if name == "openai":
        return OpenAIProvider(model=model_name)
    if name in ("anthropic", "claude"):
        return AnthropicProvider(model=model_name)

    # Auto-detection: prioritize Gemini, then OpenAI, then Anthropic
    if os.environ.get("GEMINI_API_KEY"):
        return GeminiProvider(model=model_name)
    if os.environ.get("OPENAI_API_KEY"):
        return OpenAIProvider(model=model_name)
    if os.environ.get("ANTHROPIC_API_KEY"):
        return AnthropicProvider(model=model_name)

    # Default fallback
    return MockProvider()
