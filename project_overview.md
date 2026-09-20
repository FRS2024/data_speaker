# Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)

This document outlines the Product Requirements Document (PRD), Technical Requirements Document (TRD), System Architecture, execution engine design, and roadmap required to build a conversational, code-interpreting data analysis platform.

---

## 1. Product Requirements Document (PRD)

### 1.1 Executive Summary & Core Value Proposition
The platform functions as an interactive, conversational data analyst. Users (both non-technical and technical) can upload datasets (CSV, XLSX, Parquet, JSON, SQLite) into a chat interface, inspect automated schema profiling, request natural-language data cleaning, perform exploratory data analysis (EDA), generate client-side interactive visualizations, and export reproducible Python/R scripts and transformed datasets.

### 1.2 Target User Personas
* **Business & Marketing Analysts:** Need rapid aggregations, churn modeling, and exportable charts without manual Pandas or SQL scripting.
* **Data Scientists & Engineers:** Leverage conversational workflows to automate boilerplate data wrangling, review generated code, and export clean Jupyter notebooks.
* **Executives & Non-Technical Founders:** Require high-level KPI summaries, anomaly detection, and natural language query capabilities directly over internal datasets.

### 1.3 Key Features & Acceptance Criteria

| Category | Capability | Acceptance Criteria |
| :--- | :--- | :--- |
| **Ingestion** | Multi-file uploads | Supports files up to 500MB (CSV, XLSX, TSV, JSON, Parquet, SQLite) with automatic MIME validation. |
| **Data Profiling** | Instant Schema & EDA | On upload, automatically extracts row/col counts, datatypes, null counts, memory footprint, and previews the first 5 rows. |
| **Cleaning** | Conversational Wrangling | User requests (e.g., *"fill missing ages with median, normalize country names"*) generate transparent code, transform the DataFrame, and display a diff summary. |
| **Versioning** | Checkpoint & Revert | Every data transformation creates an immutable revision state (`df_v0`, `df_v1`), allowing users to revert changes. |
| **Visualization** | Interactive Plots | Code outputs Plotly JSON specifications rendered client-side with zoom, pan, hover tooltips, and PNG/SVG export. |
| **Code Inspection** | Glass-Box Transparency | A collapsible code drawer displays the exact Python script executed for every step, along with stdout/stderr logs. |
| **Self-Correction** | Error Recovery Loop | If Python execution throws an exception, the orchestrator passes the stack trace back to the LLM to rewrite and re-execute (up to 3 retries). |

---

## 2. Technical Architecture & Component Flow

```
[ Client: TanStack Router + Vite + Tailwind + Plotly.js ]
                  │
                  │ WebSocket (SSE / Real-time events) + HTTPS
                  ▼
[ API Gateway / BFF: Node.js / FastAPI ] ─── Auth (JWT / Clerk / Supabase)
                  │
     ┌────────────┴─────────────────────────────┐
     ▼                                          ▼
[ Metadata & Chat Store ]             [ Object Storage: S3 / MinIO ]
(PostgreSQL + pgvector)               (Raw & Processed Datasets, Artifacts)
     │
     ▼
[ Agent Orchestrator (LangGraph / Temporal) ]
     │  - Schema Context Injection
     │  - Code Prompt Synthesis
     │  - Self-Correction Reflexion Loop
     │
     ├──► [ Multi-LLM Router ] (Gemini, Claude 3.5 Sonnet, GPT-4o)
     │
     ▼ (Dispatches execution payload)
[ Sandbox Manager / Pool Service ] (FastAPI + Redis)
     │  - Container Pooling / Warm Workers
     │  - Zero-Network Isolation (gVisor / Firecracker / E2B)
     │
     ▼
┌────────────────────────────────────────────────────────┐
│             Isolated Python Sandbox                    │
│  - Custom Kernel / Runner (IPython engine)             │
│  - Persistent Memory Session (`globals()` state)       │
│  - Pre-installed: pandas, polars, numpy, scipy, plotly │
│  - Captures: stdout, stderr, Plotly JSON, file exports │
└────────────────────────────────────────────────────────┘
```

---

## 3. Technical Requirements Document (TRD)

### 3.1 Recommended Tech Stack
* **Frontend:** TanStack Router (Vite SPA), TypeScript, Tailwind CSS, Monaco Editor (for code inspection), `react-plotly.js` or Vega-Lite.
* **Backend API & Gateway:** Python (FastAPI) or Node.js/TypeScript (Fastify/NestJS). FastAPI is recommended for clean integration with Python data structures.
* **Database & Cache:**
  * **PostgreSQL:** User accounts, chat sessions, project metadata, message logs.
  * **Redis:** Sandbox job queue, session state locks, and pub/sub token streaming.
* **Object Storage:** AWS S3 or Cloudflare R2 for storing uploaded datasets, intermediate Parquet snapshots, and generated output files (PDFs, images).
* **Sandbox Execution Infrastructure:** E2B, Modal, or self-hosted Docker containers isolated via **gVisor (`runsc`)** or **Firecracker MicroVMs**.

### 3.2 Sandbox Execution Strategy (The Stateful Engine)
Data analysis cannot run in a stateless function. If Step 1 cleans column A, Step 2 requires column A to be present in memory:
1. **Warm Pool Architecture:** Pre-spawn a pool of 5–10 idle sandboxes with standard libraries pre-imported (`pandas`, `numpy`, `plotly.express`). When a user sends a prompt, assign a container from the pool in under 150ms.
2. **Session Persistence:** Maintain a running IPython kernel process per user session. Code snippets execute via the kernel’s message loop, retaining the variable state (`df`) between chat turns.
3. **Security Constraints:**
   * Drop all container capabilities (`cap-drop=ALL`).
   * Disable outbound internet access (`network: none`) to prevent data exfiltration.
   * Apply strict resource limits: 2 vCPU, 4GB RAM, 60s hard execution timeout.
   * Run all processes under a non-root user (`uid 1000`).

---

## 4. Agent Orchestration & Execution Loop

### 4.1 Orchestration State Machine
```python
async def process_user_query(session_id: str, user_prompt: str):
    # 1. Retrieve current DataFrame metadata (columns, dtypes, nulls, head preview)
    schema_context = await get_df_metadata(session_id)
    
    # 2. Construct system prompt with schema injection (never send raw rows)
    prompt = build_prompt(schema_context, user_prompt)
    
    # 3. Stream LLM output and extract executable Python block
    code = await llm.generate_code(prompt)
    
    retries = 0
    max_retries = 3
    
    while retries < max_retries:
        # 4. Execute inside isolated persistent sandbox
        result = await sandbox_runner.execute(session_id, code)
        
        if result.status == "success":
            # Extract outputs: text, formatted markdown tables, or Plotly JSON structures
            return format_response(result.stdout, result.figures, result.modified_df)
        else:
            # 5. Reflexion Loop: LLM analyzes traceback to fix code
            retries += 1
            code = await llm.fix_code(code=code, error=result.stderr, context=schema_context)
            
    return {"error": "Failed to execute transformation after 3 attempts."}
```

### 4.2 System Prompt Specification
```markdown
You are an expert Data Analyst and Python Programmer.
You have access to a persistent Pandas DataFrame named `df`.

Current DataFrame Schema & Profile:
{dataframe_profile_json}

Rules:
1. Always write idiomatic Python using Pandas, Polars, or Plotly.
2. Store any modified dataset back into `df` unless creating a temporary pivot.
3. For visualizations, ALWAYS use Plotly Express or Graph Objects. Do NOT call `fig.show()`. 
   Instead, serialize the figure to JSON: `output_chart = fig.to_json()`.
4. Wrap table previews in `print(result_df.head(10).to_markdown())` so stdout captures formatted tables.
5. Do not hallucinate column names. Rely strictly on the columns present in the schema profile.
```

---

## 5. Implementation Roadmap (Zero to MVP)

1. **Phase 1: Isolated Sandbox (Weeks 1–2):** Build a Docker container running an IPython kernel wrapped in a lightweight FastAPI/ZeroMQ server. Ensure it accepts Python code strings, executes sequentially, preserves memory state across requests, and returns stdout/stderr/Plotly JSON.
2. **Phase 2: Ingestion & Profiling (Week 3):** Implement the S3 file upload pipeline. On upload, run an automated profiling script calculating schema types, missingness, distributions, and summary JSONs for context injection.
3. **Phase 3: Orchestration & Error Recovery (Weeks 4–5):** Integrate multi-LLM routing, markdown code extraction, sandbox dispatch, and the iterative self-healing reflection loop.
4. **Phase 4: Frontend UI/UX (Weeks 6–7):** Build the split-pane workspace: chat on the left panel, interactive data tables and Plotly visualizations on the right, with an expandable drawer for viewing raw code.
5. **Phase 5: State Versioning & Export (Week 8):** Implement automated `.to_parquet()` checkpointing after each successful mutative operation, enabling users to undo actions or branch analyses without recomputing previous steps.