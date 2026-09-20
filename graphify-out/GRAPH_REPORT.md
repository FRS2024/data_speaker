# Graph Report - Conversational_Data  (2026-09-20)

## Corpus Check
- 66 files · ~85,853 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .example 1, .css 1)

## Summary
- 912 nodes · 1533 edges · 63 communities (46 shown, 17 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 64 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `40086b28`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SYSTEM ARCHITECTURE & DESIGN DOCUMENT
- TECHNICAL REQUIREMENTS DOCUMENT (TRD)
- Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)
- PRODUCT REQUIREMENTS DOCUMENT (PRD)
- models.py
- server.py
- providers.py
- SandboxClient
- test_profiler.py
- SandboxRunner
- test_agent_orchestrator.py
- rules/graphify.md
- workflows/graphify.md
- SYSTEM_DESIGN.md
- useChatStream
- api/__init__.py
- api/README.md
- sandbox/__init__.py
- sandbox/README.md
- data-speaker
- data-speaker-api
- sandbox-runner
- dependencies
- apps_web_src_lib_types_dataframeprofile
- DataFrameProfile
- SessionService
- compilerOptions
- BaseWarehouseConnector
- router.tsx
- 05_asset-st/DESIGN_SYSTEM.md
- package.json
- react
- useChatStream.ts
- Imported Screens & Assets
- Any
- runner.py
- Session
- SqlWorkspace.tsx
- .execute
- main.py
- DuckDBEngine
- apps_web_src_app_globals
- apps_web_src_lib_api_resetsession
- subprocess
- urllib_request
- devDependencies
- FileUploadModal.tsx
- test_export_engine.py
- scripts
- vite.config.ts
- tailwind.config.ts
- profiler.py
- get
- Any
- pytest
- post
- test_api_ingestion.py
- test_duckdb_sql.py
- create_db_and_tables
- SchemaMapper.tsx
- apps_web_src_lib_types
- lifespan

## God Nodes (most connected - your core abstractions)
1. `Session` - 53 edges
2. `DataFrameProfile` - 30 edges
3. `SessionService` - 30 edges
4. `SandboxClient` - 23 edges
5. `profile_dataframe()` - 20 edges
6. `LocalSandboxClient` - 20 edges
7. `compilerOptions` - 19 edges
8. `RemoteSandboxClient` - 18 edges
9. `SandboxRunner` - 18 edges
10. `BaseWarehouseConnector` - 17 edges

## Surprising Connections (you probably didn't know these)
- `Technical Stack:` --references--> `useChatStream()`  [INFERRED]
  apps/web/README.md → apps/web/src/hooks/useChatStream.ts
- `setup_database()` --calls--> `create_db_and_tables()`  [EXTRACTED]
  tests/test_agent_orchestrator.py → services/api/database.py
- `setup_db()` --calls--> `create_db_and_tables()`  [EXTRACTED]
  tests/test_duckdb_sql.py → services/api/database.py
- `test_dataset_exports()` --references--> `Session`  [EXTRACTED]
  tests/test_export_engine.py → services/api/models.py
- `test_executive_report_export()` --references--> `Session`  [EXTRACTED]
  tests/test_export_engine.py → services/api/models.py

## Import Cycles
- None detected.

## Communities (63 total, 17 thin omitted)

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

### Community 4 - "models.py"
Cohesion: 0.09
Nodes (37): datetime, decimal, duckdb, json, math, pandas, re, Autonomous AI Analyst & Reflexion Orchestration Engine. Coordinates schema… (+29 more)

### Community 5 - "server.py"
Cohesion: 0.18
Nodes (18): pydantic, CheckpointFileRequest, execute_code(), ExecuteRequest, ExecuteResponse, get_sandbox_state(), health_check(), HealthResponse (+10 more)

### Community 6 - "providers.py"
Cohesion: 0.07
Nodes (28): asyncio, dotenv, AgentOrchestrator, format_sse(), Any, Synchronous non-streaming execution wrapper. Consumes the SSE stream and…, Format structured payload into a Server-Sent Event (SSE) frame., Orchestrates multi-turn analytical reasoning, code generation, and Reflexion. (+20 more)

### Community 7 - "SandboxClient"
Cohesion: 0.05
Nodes (37): argparse, httpx, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any, Client SDK for interacting with the sandbox execution engine. (+29 more)

### Community 8 - "test_profiler.py"
Cohesion: 0.12
Nodes (25): DataFrame, detect_encoding_and_delimiter(), generate_loader_code(), Path, Ingest a file of any supported format and return a dictionary of named…, Synthesize the optimal Python code snippet to hydrate the dataset into the…, Detect character encoding via chardet and sniff tabular delimiter. Falls back…, read_file_to_dataframes() (+17 more)

### Community 9 - "SandboxRunner"
Cohesion: 0.21
Nodes (6): Hook into figure display calls to capture Plotly figures without a GUI., Reset the execution namespace, flushing variables while keeping baseline…, Maintains a persistent, stateful IPython session for executing data science…, Instantiate and configure the persistent IPython InteractiveShell., Pre-populate the namespace with standard analytical packages., SandboxRunner

### Community 10 - "test_agent_orchestrator.py"
Cohesion: 0.14
Nodes (14): fixture, Automated test suite for Phase 3: Autonomous AI Analyst & Reflexion Loop.…, Test real-time Server-Sent Events (SSE) streaming format and event multiplexing., Ensure database tables exist before each test., Create a session and upload a sample employee dataset., Test standard single-turn analytical query returning synchronous JSON., Test that chart requests produce interactive Plotly specifications., Test the Reflexion loop: 1. Attempt 1 triggers a KeyError… (+6 more)

### Community 14 - "useChatStream"
Cohesion: 0.33
Nodes (4): Technical Stack:, Web Application Client (`apps/web`), useChatStream(), RootLayout()

### Community 22 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, clsx, lucide-react, @monaco-editor/react, plotly.js-dist-min, react, react-dom, react-plotly.js (+6 more)

### Community 24 - "DataFrameProfile"
Cohesion: 0.11
Nodes (17): os, pathlib, polars, Base interface and abstractions for external cloud data warehouse connectors.…, Path, Google Cloud BigQuery Connector for data_speaker. Supports schema discovery,…, Warehouse connectors registry for data_speaker., Path (+9 more)

### Community 25 - "SessionService"
Cohesion: 0.09
Nodes (23): BaseSandboxClient, CheckpointSummaryResponse, CodeExecutionResponse, ColumnDiff, SchemaDiff, SessionRelationsResponse, Any, Path (+15 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, baseUrl, esModuleInterop, isolatedModules, jsx, lib, module (+13 more)

### Community 27 - "BaseWarehouseConnector"
Cohesion: 0.06
Nodes (18): BaseWarehouseConnector, ABC, Any, Path, Abstract interface for external analytical data warehouse connections., Return True if required environment variables or credentials exist., Return connector health and configuration metadata., Verify network connectivity and credentials with the cloud warehouse. (+10 more)

### Community 28 - "router.tsx"
Cohesion: 0.10
Nodes (19): Header(), HeaderProps, SqlPatchModal(), SqlPatchModalProps, apps_web_src_lib_api_createsession, apps_web_src_lib_api_fetchcheckpoints, apps_web_src_lib_api_fetchdatasetdata, apps_web_src_lib_api_fetchprovidersstatus (+11 more)

### Community 29 - "05_asset-st/DESIGN_SYSTEM.md"
Cohesion: 0.08
Nodes (23): 1. Primary Prompt Input Bar, 2. Buttons, 3. Filter Chips & Model Switchers, 4. Conversational Cards & Response Bubbles, 5. Checkboxes & Radio Controls, 6. Responsive Collapsible Sidebar, Ambient AI Accents & Signals, Ambient Radiant Glows (+15 more)

### Community 30 - "package.json"
Cohesion: 0.12
Nodes (16): name, private, type, version, autoprefixer, clsx, lucide-react, plotly.js-dist-min (+8 more)

### Community 31 - "react"
Cohesion: 0.18
Nodes (11): ActiveChatView(), ActiveChatViewProps, FloatingActionDock(), FloatingActionDockProps, VisualizationStudio(), VisualizationStudioProps, ZeroStateCanvas(), ZeroStateCanvasProps (+3 more)

### Community 32 - "useChatStream.ts"
Cohesion: 0.18
Nodes (10): UseChatStreamOptions, apps_web_src_index, apps_web_src_lib_queryclient, apps_web_src_lib_queryclient_queryclient, apps_web_src_lib_types_dataseteventpayload, apps_web_src_lib_types_reflexionstep, rootElement, router (+2 more)

### Community 34 - "Imported Screens & Assets"
Cohesion: 0.05
Nodes (35): 1. Primary Prompt Input Bar, 2. Buttons, 3. Filter Chips & Model Switchers, 4. Conversational Cards & Response Bubbles, 5. Checkboxes & Radio Controls, 6. Responsive Collapsible Sidebar, Ambient AI Accents & Signals, Ambient Radiant Glows (+27 more)

### Community 35 - "Any"
Cohesion: 0.17
Nodes (6): BaseException, Any, Inspect the current namespace variables and DataFrame dimensions., Atomically persist active 'df' to a Parquet file., Restore 'df' from a Parquet checkpoint file., Run code in the IPython shell while redirecting stdout and stderr.

### Community 36 - "runner.py"
Cohesion: 0.18
Nodes (10): ast, concurrent_futures, contextlib, ipython_core_interactiveshell, numpy, plotly_express, plotly_graph_objects, IPython-based stateful execution runner with output interception and Plotly… (+2 more)

### Community 37 - "Session"
Cohesion: 0.13
Nodes (13): get_db_session(), FastAPI dependency for database session injection., Generate a Markdown Executive Summary report synthesizing the dataset profile,…, Export the active DataFrame snapshot in CSV, Parquet, or Excel format. Returns:…, Generate a fully reproducible Jupyter Notebook (.ipynb) containing setup cells,…, Conversational data analysis session., Session, Create a new session record in the database. (+5 more)

### Community 38 - "SqlWorkspace.tsx"
Cohesion: 0.17
Nodes (11): SqlWorkspace(), SqlWorkspaceProps, VirtualDataTable(), VirtualDataTableProps, apps_web_src_lib_api_executesql, apps_web_src_lib_types_datasetcolumn, apps_web_src_lib_types_datasetdataresponse, apps_web_src_lib_types_sqlqueryresponse (+3 more)

### Community 39 - ".execute"
Cohesion: 0.33
Nodes (4): _df_fingerprint(), Execute a Python code string sequentially within the persistent IPython shell., Collect and serialize all Plotly figures generated in this execution turn., Generate a lightweight structural and content fingerprint of a DataFrame.

### Community 40 - "main.py"
Cohesion: 0.16
Nodes (20): fastapi_middleware_cors, fastapi_responses, services_api_connectors, execute_sql_query(), FastAPI Application Gateway for data_speaker. Exposes REST endpoints for…, Non-destructively roll back the active DataFrame to a specified checkpoint…, Execute arbitrary analytical SQL on session datasets and checkpoints via…, revert_session_version() (+12 more)

### Community 41 - "DuckDBEngine"
Cohesion: 0.16
Nodes (14): DuckDBPyConnection, SqlQueryColumn, DuckDBEngine, Any, DbSession, Execute an analytical SQL query against session tables and checkpoints. Returns…, Execute a SQL statement and materialize the result into a new Parquet…, Sanitize filename into a valid SQL identifier (lowercase, alphanumeric +… (+6 more)

### Community 46 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, @types/react-plotly.js (+3 more)

### Community 47 - "FileUploadModal.tsx"
Cohesion: 0.18
Nodes (9): FileUploadModal(), FileUploadModalProps, Sidebar(), SidebarProps, apps_web_src_lib_api, apps_web_src_lib_api_fetchsessions, apps_web_src_lib_api_uploaddataset, apps_web_src_lib_types_fileuploadresponse (+1 more)

### Community 48 - "test_export_engine.py"
Cohesion: 0.24
Nodes (9): io, sqlmodel_pool, asyncio, fixture, Tests for Phase 5: Multi-Format Export Engine., test_dataset_exports(), test_db(), test_executive_report_export() (+1 more)

### Community 49 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 50 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_node_url, vite, @vitejs/plugin-react

### Community 52 - "profiler.py"
Cohesion: 0.13
Nodes (16): chardet, csv, ColumnProfile, ForeignKeyRelation, Metadata profile of a single column., clean_table_name(), infer_foreign_key_relations(), Any (+8 more)

### Community 53 - "get"
Cohesion: 0.13
Nodes (15): export_session_data(), get_session(), get_session_dataset(), get_session_table_relations(), health_check(), list_session_checkpoints(), list_sessions(), get (+7 more)

### Community 54 - "Any"
Cohesion: 0.15
Nodes (13): get_connectors_status(), get_dataset(), get_providers_status(), get_session_schema(), Any, Fetch privacy-safe schema profiles for all datasets loaded in the session. Used…, Reset the sandbox kernel state, prune incremental checkpoints, and re-hydrate…, Retrieve high-performance tabular dataset rows and typed schema for headless… (+5 more)

### Community 55 - "pytest"
Cohesion: 0.18
Nodes (10): fastapi_testclient, pytest, Unit tests for Multi-File Relational Joins & Foreign Key Inference., Test uploading two relational tables (customers and orders), verifying foreign…, test_multi_file_relational_inference_and_join(), Unit tests for BigQuery and Snowflake Cloud Warehouse Connectors., Test inspecting BigQuery and Snowflake connector statuses., Test importing a cloud warehouse dataset query into a session as a Parquet… (+2 more)

### Community 56 - "post"
Cohesion: 0.17
Nodes (12): chat_with_data(), create_session(), execute_code(), import_warehouse_dataset(), post, Create a new data analysis session., Upload a tabular dataset (CSV, TSV, Parquet, Excel, JSON, SQLite).…, Execute arbitrary Python analytical code within the session's sandbox. Returns… (+4 more)

### Community 57 - "test_api_ingestion.py"
Cohesion: 0.17
Nodes (11): End-to-end integration tests for the API Gateway and Ingestion Flow…, Test state persistence across turns and Plotly figure interception via API., Verify API health check endpoint., Test creating a new session and querying its metadata., Test uploading a CSV dataset, extracting schema, and querying schema endpoint., Test that uploaded data is automatically hydrated and accessible as `df`., test_create_and_get_session(), test_execute_code_against_hydrated_dataframe() (+3 more)

### Community 58 - "test_duckdb_sql.py"
Cohesion: 0.18
Nodes (11): fixture, Unit tests for the embedded DuckDB SQL Execution Engine & Checkpoint…, Create a session and ingest sample transactional data., Test standard SELECT query with aggregations on uploaded orders dataset., Test querying the active dataset checkpoint via df_active or df., Test creating a new DataFrame checkpoint directly from a SQL filter query., session_with_data(), setup_db() (+3 more)

### Community 59 - "create_db_and_tables"
Cohesion: 0.22
Nodes (9): create_db_and_tables(), Initialize all registered SQLModel tables in the database., fixture, Ensure database tables exist before each test., setup_database(), fixture, setup_db(), fixture (+1 more)

### Community 60 - "SchemaMapper.tsx"
Cohesion: 0.25
Nodes (7): SchemaMapper(), SchemaMapperProps, UserJoinLink, apps_web_src_lib_api_fetchtablerelations, apps_web_src_lib_api_savesqlcheckpoint, apps_web_src_lib_types_foreignkeyrelation, apps_web_src_lib_types_schemaresponse

### Community 61 - "apps_web_src_lib_types"
Cohesion: 0.40
Nodes (4): VersionHistoryView(), VersionHistoryViewProps, apps_web_src_lib_types, apps_web_src_lib_types_checkpointsummary

### Community 62 - "lifespan"
Cohesion: 0.67
Nodes (3): lifespan(), FastAPI, Application lifespan: initialize database tables upon startup.

## Knowledge Gaps
- **221 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+216 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 493 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataFrameProfile` connect `DataFrameProfile` to `models.py`, `main.py`, `profiler.py`, `SessionService`, `BaseWarehouseConnector`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `Session` connect `Session` to `models.py`, `providers.py`, `main.py`, `DuckDBEngine`, `test_export_engine.py`, `get`, `Any`, `post`, `SessionService`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `LocalSandboxClient` connect `SandboxClient` to `SessionService`, `models.py`, `SandboxRunner`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Session` (e.g. with `list_sessions()` and `SessionService`) actually correct?**
  _`Session` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `DataFrameProfile` (e.g. with `build_system_prompt()` and `format_schema_context()`) actually correct?**
  _`DataFrameProfile` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `SessionService` (e.g. with `ChatTurn` and `CheckpointSummaryResponse`) actually correct?**
  _`SessionService` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SandboxClient` (e.g. with `main()` and `run_repl()`) actually correct?**
  _`SandboxClient` has 11 INFERRED edges - model-reasoned connections that need verification._