# Graph Report - Conversational_Data  (2026-09-19)

## Corpus Check
- 28 files · ~17,372 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: .csv 15, (none) 2, .db 1)

## Summary
- 396 nodes · 593 edges · 22 communities (11 shown, 11 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2edade0d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SYSTEM ARCHITECTURE & DESIGN DOCUMENT
- TECHNICAL REQUIREMENTS DOCUMENT (TRD)
- Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)
- PRODUCT REQUIREMENTS DOCUMENT (PRD)
- main.py
- runner.py
- 2. Product Vision & Strategy
- SandboxClient
- profiler.py
- SandboxRunner
- test_api_ingestion.py
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

## God Nodes (most connected - your core abstractions)
1. `SandboxClient` - 21 edges
2. `Session` - 18 edges
3. `SessionService` - 17 edges
4. `LocalSandboxClient` - 17 edges
5. `RemoteSandboxClient` - 16 edges
6. `SandboxRunner` - 16 edges
7. `SYSTEM ARCHITECTURE & DESIGN DOCUMENT` - 15 edges
8. `ExecutionResult` - 14 edges
9. `DataFrameProfile` - 12 edges
10. `read_file_to_dataframes()` - 12 edges

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

## Communities (22 total, 11 thin omitted)

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
Cohesion: 0.05
Nodes (40): 1.1 One-Paragraph Vision, 1.2 Problem Statement, 1.3 Solution Overview, 1.4 Target Users & Market Segments, 1.5 Key Value Propositions, 1.6 High-Level Business & Operational Metrics, 1. Executive Summary, 3.1 Primary Personas (+32 more)

### Community 4 - "main.py"
Cohesion: 0.06
Nodes (55): asyncio, BaseSandboxClient, fastapi_middleware_cors, create_session(), execute_code(), get_session(), get_session_schema(), health_check() (+47 more)

### Community 5 - "runner.py"
Cohesion: 0.10
Nodes (26): ast, concurrent_futures, contextlib, ipython_core_interactiveshell, json, numpy, plotly_express, plotly_graph_objects (+18 more)

### Community 6 - "2. Product Vision & Strategy"
Cohesion: 0.25
Nodes (8): 2.1 Long-Term Product Vision (3–5 Years), 2.2 North-Star Metric, 2.3 Positioning Statement, 2.4 Competitive Landscape & Differentiation Matrix, 2.5 Monetization & Business Model, 2.6 Go-To-Market (GTM) Strategy, 2. Product Vision & Strategy, Unit Economics & Margin Targets

### Community 7 - "SandboxClient"
Cohesion: 0.05
Nodes (38): argparse, httpx, pytest, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any (+30 more)

### Community 8 - "profiler.py"
Cohesion: 0.07
Nodes (43): chardet, csv, DataFrame, datetime, math, pandas, polars, re (+35 more)

### Community 9 - "SandboxRunner"
Cohesion: 0.11
Nodes (12): BaseException, Any, Inspect the current namespace variables and DataFrame dimensions., Execute a Python code string sequentially within the persistent IPython shell., Run code in the IPython shell while redirecting stdout and stderr., Collect and serialize all Plotly figures generated in this execution turn., Maintains a persistent, stateful IPython session for executing data science…, Instantiate and configure the persistent IPython InteractiveShell. (+4 more)

### Community 10 - "test_api_ingestion.py"
Cohesion: 0.08
Nodes (26): fastapi_testclient, io, os, pathlib, create_db_and_tables(), get_db_session(), Database configuration and session lifecycle management for services/api.…, Initialize all registered SQLModel tables in the database. (+18 more)

## Knowledge Gaps
- **95 isolated node(s):** `data-speaker`, `data-speaker-api`, `sandbox-runner`, `graphify`, `Workflow: graphify` (+90 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 220 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SandboxRunner` connect `SandboxRunner` to `runner.py`, `SandboxClient`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `LocalSandboxClient` connect `SandboxClient` to `SandboxRunner`, `main.py`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `RemoteSandboxClient` connect `SandboxClient` to `main.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SandboxClient` (e.g. with `main()` and `run_repl()`) actually correct?**
  _`SandboxClient` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SessionService` (e.g. with `ChatTurn` and `CodeExecutionResponse`) actually correct?**
  _`SessionService` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `LocalSandboxClient` (e.g. with `SessionService` and `ExecutionResult`) actually correct?**
  _`LocalSandboxClient` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `RemoteSandboxClient` (e.g. with `SessionService` and `ExecutionResult`) actually correct?**
  _`RemoteSandboxClient` has 3 INFERRED edges - model-reasoned connections that need verification._