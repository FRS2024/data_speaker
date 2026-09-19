"""
Prompt templates and schema context injection for the Autonomous AI Analyst.
Guarantees schema-only context boundaries, zero raw data leakage, and strict
code-backed mathematical determinism.
"""

from __future__ import annotations

from typing import Any, Dict, List
from services.api.models import DataFrameProfile

# Canonical tool definition for native LLM tool-calling
EXECUTE_PYTHON_TOOL: Dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "execute_python",
        "description": (
            "Execute Python analytical code in the stateful sandbox kernel where the "
            "active dataset is pre-loaded as `df` (and named tables as `df_<table_name>`). "
            "Captures stdout, stderr, execution duration, and interactive Plotly figures."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": (
                        "Complete, executable Python code snippet. Print key numerical findings "
                        "using print(). For charts, build interactive Plotly figures with `px` or `go`."
                    ),
                }
            },
            "required": ["code"],
        },
    },
}


def format_schema_context(profiles: List[DataFrameProfile]) -> str:
    """Format DataFrameProfile metadata into compact, grounded prompt context."""
    if not profiles:
        return "No datasets are currently loaded in this session."

    lines: List[str] = ["### Active Datasets in Session:\n"]
    for p in profiles:
        lines.append(f"#### Table: `{p.table_name}` (Active alias: `df`)")
        lines.append(f"- **Dimensions**: {p.row_count:,} rows × {p.column_count} columns")
        lines.append(f"- **Memory Footprint**: {p.memory_footprint_mb} MB")
        lines.append("- **Column Schema & Statistics**:")
        for col in p.columns:
            sample_str = ", ".join(repr(v) for v in col.sample_values[:3])
            lines.append(
                f"  - `{col.name}` ({col.dtype}): {col.null_percentage}% null | "
                f"cardinality: {col.cardinality:,} | samples: [{sample_str}]"
            )

        lines.append("\n- **Head Preview (First 5 Rows)**:")
        lines.append(p.head_preview_markdown)
        lines.append("\n" + "-" * 50 + "\n")

    return "\n".join(lines)


def build_system_prompt(profiles: List[DataFrameProfile]) -> str:
    """Construct the grounding system prompt for the AI Data Analyst."""
    schema_context = format_schema_context(profiles)

    return f"""You are the Lead Autonomous Data Analyst and Python Specialist for data_speaker.

## Core Directives & Operating Principles
1. **Mathematical Determinism**: You must NEVER guess, invent, or extrapolate numbers. Every analytical claim, statistic, aggregate, trend, or percentage MUST be calculated by executing Python code.
2. **Stateful Execution**: You are connected to a stateful IPython execution kernel. The dataset is already loaded in memory as `df` (and as individual tables `df_<name>`). Any DataFrame transformations, column additions, or aggregations you perform will persist across turns.
3. **Execution Tool**: Use the `execute_python` tool whenever you need to compute values, test hypotheses, or generate charts.
4. **Data Science Standards**:
   - Pre-installed packages: `pandas as pd`, `polars as pl`, `numpy as np`, `scipy`, `sklearn`, `statsmodels`, `plotly.express as px`, `plotly.graph_objects as go`.
   - Always print summary statistics and key metrics using `print(...)` so they appear in stdout.
   - For visualizations: ALWAYS use Plotly (`px` or `go`). Set informative titles and axis labels. The sandbox automatically intercepts any `fig` object or `fig.show()`.
5. **Data Privacy**: You only have access to structural schema profiles and small sanitized previews. Do not attempt to dump entire tables to stdout.

{schema_context}
"""


def build_reflexion_prompt(
    failed_code: str,
    error_traceback: str,
    attempt: int,
    max_attempts: int = 3,
) -> str:
    """Build the self-correction prompt for the Reflexion loop."""
    return f"""Your previous code execution failed on attempt {attempt}/{max_attempts}.

### Failed Code:
```python
{failed_code}
```

### Runtime Traceback:
```
{error_traceback}
```

### Self-Correction Instructions:
1. Carefully diagnose the error (e.g. KeyError on missing column, incorrect datatype, division by zero, syntax error).
2. Check the active column names and data types in the schema above.
3. Call the `execute_python` tool again with the corrected Python code that resolves this specific error.
"""


def build_synthesis_prompt(
    user_prompt: str,
    code: str,
    stdout: str,
    has_figures: bool,
) -> str:
    """Build prompt for conversational interpretation following successful code execution."""
    chart_note = "An interactive Plotly chart was successfully generated." if has_figures else "No chart was requested."

    return f"""The user asked: "{user_prompt}"

The analytical code was executed in the sandbox:
```python
{code}
```

Execution Output (stdout):
```
{stdout if stdout.strip() else "(Execution completed with 0 errors; no printed output)"}
```
Visualizations: {chart_note}

### Your Task:
Provide a clear, professional, and executive-ready conversational response directly answering the user's question.
- Ground your explanation strictly in the verified numbers above.
- Highlight key insights, business takeaways, trends, or notable anomalies.
- Keep the explanation concise, scannable, and engaging.
"""
