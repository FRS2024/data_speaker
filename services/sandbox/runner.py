"""IPython-based stateful execution runner with output interception and Plotly capture."""

from __future__ import annotations

import ast
import contextlib
import io
import json
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Any, Dict, List, Optional

from IPython.core.interactiveshell import InteractiveShell
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


class ExecutionResult:
    """Encapsulates the output of a code execution turn."""

    def __init__(
        self,
        status: str,  # "success" | "error" | "timeout"
        stdout: str = "",
        stderr: str = "",
        figures: Optional[List[Dict[str, Any]]] = None,
        duration_ms: int = 0,
        has_mutated_df: bool = False,
        df_shape: Optional[tuple[int, int]] = None,
    ) -> None:
        self.status = status
        self.stdout = stdout
        self.stderr = stderr
        self.figures = figures or []
        self.duration_ms = duration_ms
        self.has_mutated_df = has_mutated_df
        self.df_shape = df_shape

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "figures": self.figures,
            "duration_ms": self.duration_ms,
            "has_mutated_df": self.has_mutated_df,
            "df_shape": list(self.df_shape) if self.df_shape else None,
        }


class SandboxRunner:
    """Maintains a persistent, stateful IPython session for executing data science code."""

    def __init__(self, default_timeout_seconds: int = 60) -> None:
        self.default_timeout_seconds = default_timeout_seconds
        self.captured_figures: List[go.Figure] = []
        self._init_shell()

    def _init_shell(self) -> None:
        """Instantiate and configure the persistent IPython InteractiveShell."""
        # Reset any existing singleton instance
        InteractiveShell.clear_instance()
        self.shell = InteractiveShell.instance(
            history_length=0,
        )
        self.shell.colors = "nocolor"
        self._install_display_hooks()
        self._import_baseline_libraries()

    def _import_baseline_libraries(self) -> None:
        """Pre-populate the namespace with standard analytical packages."""
        baseline_code = (
            "import pandas as pd\n"
            "import numpy as np\n"
            "import plotly.express as px\n"
            "import plotly.graph_objects as go\n"
        )
        self.shell.run_cell(baseline_code, store_history=False, silent=True)

    def _install_display_hooks(self) -> None:
        """Hook into figure display calls to capture Plotly figures without a GUI."""
        runner = self

        def custom_show(fig_self: go.Figure, *args: Any, **kwargs: Any) -> None:
            runner.captured_figures.append(fig_self)

        # Monkey-patch go.Figure.show to intercept show() calls
        go.Figure.show = custom_show  # type: ignore[assignment]

    def reset(self) -> None:
        """Reset the execution namespace, flushing variables while keeping baseline imports."""
        self.captured_figures.clear()
        self._init_shell()

    def get_state(self) -> Dict[str, Any]:
        """Inspect the current namespace variables and DataFrame dimensions."""
        user_vars: Dict[str, Any] = {}
        dataframes: Dict[str, Any] = {}

        # Exclude built-in and module variables
        for name, val in self.shell.user_ns.items():
            if name.startswith("_") or name in ("In", "Out", "exit", "quit", "get_ipython"):
                continue
            if isinstance(val, (pd.DataFrame, pd.Series)):
                dataframes[name] = {
                    "type": type(val).__name__,
                    "shape": list(val.shape),
                    "memory_bytes": int(val.memory_usage(deep=True).sum()) if isinstance(val, pd.DataFrame) else int(val.memory_usage(deep=True)),
                }
            elif not callable(val) and not isinstance(val, type(sys)):
                user_vars[name] = {
                    "type": type(val).__name__,
                    "repr": repr(val)[:100],
                }

        return {
            "dataframes": dataframes,
            "variables": user_vars,
            "has_df": "df" in self.shell.user_ns and isinstance(self.shell.user_ns["df"], pd.DataFrame),
        }

    def execute(self, code: str, timeout_seconds: Optional[int] = None) -> ExecutionResult:
        """Execute a Python code string sequentially within the persistent IPython shell."""
        timeout = timeout_seconds or self.default_timeout_seconds
        start_time = time.perf_counter()

        # Track previous state of 'df' to detect mutations
        prev_df_state: Optional[tuple[int, int]] = None
        if "df" in self.shell.user_ns and isinstance(self.shell.user_ns["df"], pd.DataFrame):
            prev_df_state = self.shell.user_ns["df"].shape

        self.captured_figures = []

        # Execute using a thread pool to allow timeout enforcement
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self._run_cell_intercepted, code)
            try:
                stdout, stderr, raw_result, exc = future.result(timeout=timeout)
            except FutureTimeoutError:
                duration_ms = int((time.perf_counter() - start_time) * 1000)
                return ExecutionResult(
                    status="timeout",
                    stdout="",
                    stderr=f"Execution timed out after {timeout} seconds.",
                    duration_ms=duration_ms,
                )

        duration_ms = int((time.perf_counter() - start_time) * 1000)

        # Check for execution failure
        if exc is not None:
            return ExecutionResult(
                status="error",
                stdout=stdout,
                stderr=stderr,
                duration_ms=duration_ms,
            )

        # Extract figures from both explicit show() calls and namespace scan
        figures_json = self._extract_figures(raw_result)

        # Check for DataFrame mutations
        has_mutated = False
        current_df_shape: Optional[tuple[int, int]] = None
        if "df" in self.shell.user_ns and isinstance(self.shell.user_ns["df"], pd.DataFrame):
            current_df_shape = self.shell.user_ns["df"].shape
            if prev_df_state is None or prev_df_state != current_df_shape:
                has_mutated = True

        return ExecutionResult(
            status="success",
            stdout=stdout,
            stderr=stderr,
            figures=figures_json,
            duration_ms=duration_ms,
            has_mutated_df=has_mutated,
            df_shape=current_df_shape,
        )

    def _run_cell_intercepted(self, code: str) -> tuple[str, str, Any, Optional[BaseException]]:
        """Run code in the IPython shell while redirecting stdout and stderr."""
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        raw_result = None
        caught_exc: Optional[BaseException] = None

        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
            try:
                execution_info = self.shell.run_cell(code, store_history=True, silent=False)
                raw_result = execution_info.result

                if execution_info.error_before_exec:
                    caught_exc = execution_info.error_before_exec
                elif execution_info.error_in_exec:
                    caught_exc = execution_info.error_in_exec

                # If the last expression returned a DataFrame or series, render it as markdown table to stdout
                if raw_result is not None:
                    if isinstance(raw_result, (pd.DataFrame, pd.Series)):
                        formatted_table = raw_result.head(10).to_markdown() if hasattr(raw_result, "to_markdown") else str(raw_result.head(10))
                        print(formatted_table, file=stdout_buf)
                    elif isinstance(raw_result, go.Figure):
                        self.captured_figures.append(raw_result)

            except Exception as e:
                caught_exc = e

        stdout = stdout_buf.getvalue()
        stderr = stderr_buf.getvalue()

        if caught_exc is not None and not stderr:
            stderr = "".join(traceback.format_exception(type(caught_exc), caught_exc, caught_exc.__traceback__))

        return stdout, stderr, raw_result, caught_exc

    def _extract_figures(self, last_result: Any) -> List[Dict[str, Any]]:
        """Collect and serialize all Plotly figures generated in this execution turn."""
        figures: List[go.Figure] = list(self.captured_figures)

        # Check if the last cell expression evaluated to a Figure
        if isinstance(last_result, go.Figure) and last_result not in figures:
            figures.append(last_result)

        # Multi-strategy scan: Inspect common figure variable names in user namespace
        for candidate_name in ("fig", "figure", "chart", "plot", "output_chart"):
            candidate = self.shell.user_ns.get(candidate_name)
            if isinstance(candidate, go.Figure) and candidate not in figures:
                figures.append(candidate)

        # Also check any new go.Figure in the namespace
        for name, val in self.shell.user_ns.items():
            if not name.startswith("_") and isinstance(val, go.Figure) and val not in figures:
                figures.append(val)

        serialized: List[Dict[str, Any]] = []
        for fig in figures:
            try:
                # fig.to_json() returns a valid JSON string specification conforming to Plotly.js schema
                fig_json = json.loads(fig.to_json())
                serialized.append(fig_json)
            except Exception as ex:
                sys.stderr.write(f"Warning: Failed to serialize Plotly figure: {ex}\n")

        return serialized
