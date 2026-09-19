# Graph Report - Conversational_Data  (2026-09-19)

## Corpus Check
- 47 files · ~24,921 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .css 1, .lock 1)

## Summary
- 585 nodes · 887 edges · 34 communities (19 shown, 15 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 36 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `338ae8f5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SYSTEM ARCHITECTURE & DESIGN DOCUMENT
- TECHNICAL REQUIREMENTS DOCUMENT (TRD)
- Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)
- PRODUCT REQUIREMENTS DOCUMENT (PRD)
- main.py
- runner.py
- BaseLLMProvider
- SandboxClient
- profiler.py
- SandboxRunner
- test_agent_orchestrator.py
- rules/graphify.md
- workflows/graphify.md
- SYSTEM_DESIGN.md
- Web Application Client (`apps/web`)
- api/__init__.py
- api/README.md
- sandbox/__init__.py
- sandbox/README.md
- data-speaker
- data-speaker-api
- sandbox-runner
- package.json
- page.tsx
- session_service.py
- Session
- compilerOptions
- DataFrameProfile
- get_session
- .run_chat_stream
- next.config.mjs
- next-env.d.ts
- get_db_session

## God Nodes (most connected - your core abstractions)
1. `Session` - 22 edges
2. `SandboxClient` - 21 edges
3. `SessionService` - 17 edges
4. `LocalSandboxClient` - 17 edges
5. `compilerOptions` - 16 edges
6. `RemoteSandboxClient` - 16 edges
7. `SandboxRunner` - 16 edges
8. `DataFrameProfile` - 15 edges
9. `SYSTEM ARCHITECTURE & DESIGN DOCUMENT` - 15 edges
10. `ExecutionResult` - 14 edges

## Surprising Connections (you probably didn't know these)
- `client()` --uses--> `SandboxClient`  [INFERRED]
  tests/test_sandbox_runner.py → services/sandbox/client.py
- `test_dataframe_mutation_and_shape_tracking()` --uses--> `SandboxClient`  [INFERRED]
  tests/test_sandbox_runner.py → services/sandbox/client.py
- `test_plotly_figure_interception_via_show()` --uses--> `SandboxClient`  [INFERRED]
  tests/test_sandbox_runner.py → services/sandbox/client.py
- `test_plotly_figure_interception_without_show()` --uses--> `SandboxClient`  [INFERRED]
  tests/test_sandbox_runner.py → services/sandbox/client.py
- `test_reset_flushes_state()` --uses--> `SandboxClient`  [INFERRED]
  tests/test_sandbox_runner.py → services/sandbox/client.py

## Import Cycles
- None detected.

## Communities (34 total, 15 thin omitted)

### Community 0 - "SYSTEM ARCHITECTURE & DESIGN DOCUMENT"
Cohesion: 0.06
Nodes (34): 10.1 Predictive Warm-Pool Algorithm, 10.2 Pool State Machine, 10. Scalability & Pool Management Architecture, 11. Disaster Recovery & Business Continuity, 12. Technology Stack Evaluation Matrix, 13. System Evolution Path, 14. Architecture Decision Records (ADRs), 1.1 Architectural Vision (+26 more)

### Community 1 - "TECHNICAL REQUIREMENTS DOCUMENT (TRD)"
Cohesion: 0.08
Nodes (24): 1.1 High-Level Technical Goals, 1.2 Key Technical Constraints & Non-Negotiables, 1.3 Technology Philosophy & Engineering Principles, 1. Technical Overview, 2.1.1 REST Endpoints Specification, 2.1.2 Real-Time Event Stream (Server-Sent Events), 2.1 API Contracts & Interaction Protocols, 2.2 Domain Data Models & Database Schemas (+16 more)

### Community 2 - "Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)"
Cohesion: 0.14
Nodes (13): 1.1 Executive Summary & Core Value Proposition, 1.2 Target User Personas, 1.3 Key Features & Acceptance Criteria, 1. Product Requirements Document (PRD), 2. Technical Architecture & Component Flow, 3.1 Recommended Tech Stack, 3.2 Sandbox Execution Strategy (The Stateful Engine), 3. Technical Requirements Document (TRD) (+5 more)

### Community 3 - "PRODUCT REQUIREMENTS DOCUMENT (PRD)"
Cohesion: 0.04
Nodes (48): 1.1 One-Paragraph Vision, 1.2 Problem Statement, 1.3 Solution Overview, 1.4 Target Users & Market Segments, 1.5 Key Value Propositions, 1.6 High-Level Business & Operational Metrics, 1. Executive Summary, 2.1 Long-Term Product Vision (3–5 Years) (+40 more)

### Community 4 - "main.py"
Cohesion: 0.16
Nodes (22): fastapi_middleware_cors, fastapi_responses, chat_with_data(), create_session(), execute_code(), post, FastAPI Application Gateway for data_speaker. Exposes REST endpoints for…, Upload a tabular dataset (CSV, TSV, Parquet, Excel, JSON, SQLite).… (+14 more)

### Community 5 - "runner.py"
Cohesion: 0.10
Nodes (26): ast, concurrent_futures, contextlib, ipython_core_interactiveshell, numpy, plotly_express, plotly_graph_objects, pydantic (+18 more)

### Community 6 - "BaseLLMProvider"
Cohesion: 0.08
Nodes (18): ABC, AgentOrchestrator, Orchestrates multi-turn analytical reasoning, code generation, and Reflexion., AnthropicProvider, BaseLLMProvider, GeminiProvider, MockProvider, OpenAIProvider (+10 more)

### Community 7 - "SandboxClient"
Cohesion: 0.06
Nodes (37): argparse, httpx, pytest, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any (+29 more)

### Community 8 - "profiler.py"
Cohesion: 0.07
Nodes (45): chardet, csv, DataFrame, datetime, math, pandas, polars, re (+37 more)

### Community 9 - "SandboxRunner"
Cohesion: 0.10
Nodes (12): BaseException, Any, Inspect the current namespace variables and DataFrame dimensions., Execute a Python code string sequentially within the persistent IPython shell., Run code in the IPython shell while redirecting stdout and stderr., Collect and serialize all Plotly figures generated in this execution turn., Maintains a persistent, stateful IPython session for executing data science…, Instantiate and configure the persistent IPython InteractiveShell. (+4 more)

### Community 10 - "test_agent_orchestrator.py"
Cohesion: 0.06
Nodes (35): fastapi_testclient, io, create_db_and_tables(), Initialize all registered SQLModel tables in the database., lifespan(), FastAPI, Application lifespan: initialize database tables upon startup., fixture (+27 more)

### Community 22 - "package.json"
Cohesion: 0.04
Nodes (45): dependencies, clsx, lucide-react, @monaco-editor/react, next, plotly.js-dist-min, react, react-dom (+37 more)

### Community 23 - "page.tsx"
Cohesion: 0.10
Nodes (27): Home(), ChatPanel(), ChatPanelProps, CodeConsole(), CodeConsoleProps, FileUploadModal(), FileUploadModalProps, Navbar() (+19 more)

### Community 24 - "session_service.py"
Cohesion: 0.13
Nodes (19): asyncio, json, os, pathlib, Autonomous AI Analyst & Reflexion Orchestration Engine. Coordinates schema…, build_reflexion_prompt(), build_synthesis_prompt(), Prompt templates and schema context injection for the Autonomous AI Analyst.… (+11 more)

### Community 25 - "Session"
Cohesion: 0.14
Nodes (14): BaseSandboxClient, ChatTurn, Individual analytical turn within a session., Conversational data analysis session., Session, Path, Save uploaded file, profile all tables, record in database, and hydrate sandbox., Execute arbitrary Python analytical code inside the session's sandbox. Records… (+6 more)

### Community 26 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 27 - "DataFrameProfile"
Cohesion: 0.20
Nodes (10): build_system_prompt(), format_schema_context(), Format DataFrameProfile metadata into compact, grounded prompt context., Construct the grounding system prompt for the AI Data Analyst., DataFrameProfile, Serialize DataFrameProfile list to JSON string., Structural schema profile of a loaded dataset (privacy-safe, no raw bulk data)., File uploaded and ingested into a session. (+2 more)

### Community 28 - "get_session"
Cohesion: 0.22
Nodes (10): get_session(), get_session_schema(), health_check(), Any, get, Fetch privacy-safe schema profiles for all datasets loaded in the session. Used…, Reset the sandbox kernel state and re-hydrate loaded datasets., Health status and configuration. (+2 more)

### Community 29 - ".run_chat_stream"
Cohesion: 0.33
Nodes (5): format_sse(), Any, Synchronous non-streaming execution wrapper. Consumes the SSE stream and…, Format structured payload into a Server-Sent Event (SSE) frame., Execute an autonomous analytical turn with real-time SSE streaming. Emits…

## Knowledge Gaps
- **156 isolated node(s):** `nextConfig`, `name`, `version`, `private`, `dev` (+151 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 327 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SandboxRunner` connect `SandboxRunner` to `runner.py`, `SandboxClient`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `LocalSandboxClient` connect `SandboxClient` to `session_service.py`, `Session`, `SandboxRunner`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `get_db_session`, `main.py`, `session_service.py`, `get_session`, `.run_chat_stream`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SandboxClient` (e.g. with `main()` and `run_repl()`) actually correct?**
  _`SandboxClient` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SessionService` (e.g. with `ChatTurn` and `CodeExecutionResponse`) actually correct?**
  _`SessionService` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `LocalSandboxClient` (e.g. with `SessionService` and `ExecutionResult`) actually correct?**
  _`LocalSandboxClient` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `nextConfig`, `name`, `version` to the rest of the system?**
  _156 weakly-connected nodes found - possible documentation gaps or missing edges._