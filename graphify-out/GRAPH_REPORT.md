# Graph Report - Conversational_Data  (2026-09-23)

## Corpus Check
- 87 files · ~103,325 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 3, .example 1, .ini 1)

## Summary
- 1186 nodes · 2337 edges · 96 communities (63 shown, 33 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 153 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3ccb8442`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SYSTEM ARCHITECTURE & DESIGN DOCUMENT
- TECHNICAL REQUIREMENTS DOCUMENT (TRD)
- Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)
- PRODUCT REQUIREMENTS DOCUMENT (PRD)
- session_service.py
- server.py
- orchestrator.py
- SandboxClient
- test_profiler.py
- SandboxRunner
- setup_database
- rules/graphify.md
- workflows/graphify.md
- SYSTEM_DESIGN.md
- api/diagnostics.py
- api/__init__.py
- api/README.md
- sandbox/__init__.py
- sandbox/README.md
- data-speaker
- data-speaker-api
- sandbox-runner
- dependencies
- types.ts
- DataFrameProfile
- SessionService
- compilerOptions
- typing
- api.ts
- 05_asset-st/DESIGN_SYSTEM.md
- package.json
- router.tsx
- useChatStream.ts
- design_system/DESIGN_SYSTEM.md
- ExecutionResult
- runner.py
- ExportEngine
- SqlWorkspace.tsx
- automl.py
- models.py
- DuckDBEngine
- apps_web_src_app_globals
- apps_web_src_lib_api_resetsession
- subprocess
- urllib_request
- workspaces.py
- FileUploadModal.tsx
- Session
- routers/auth.py
- test_login_and_token_lifecycles
- os
- profile_dataframe
- LocalSandboxClient
- ChatTurn
- database.py
- AuthContext
- setup_database
- session_with_data
- setup_database
- Imported Screens & Assets
- Sidebar.tsx
- main.py
- test_workspace_creation_and_listing
- SnowflakeConnector
- Components
- Components
- devDependencies
- client.py
- Colors
- Colors
- Elevation & Depth
- Layout & Spacing
- routers/__init__.py
- routers/diagnostics.py
- BigQueryConnector
- .get_status
- .ingest_file
- scripts
- vite.config.ts
- get_me
- .get_session_relations
- tailwind.config.ts
- test_chat_stream_sse_events
- test_chat_sync_successful_analytical_query
- test_chat_reflexion_self_correction
- test_multi_turn_state_and_plotly_generation
- test_create_and_get_session
- test_upload_and_profile_dataset
- test_execute_code_against_hydrated_dataframe
- test_refresh_token_rotation_and_revocation
- test_db
- test_duckdb_query_on_df_active_alias
- test_cross_tenant_session_isolation
- test_multi_file_relational_inference_and_join
- test_warehouse_connectors_status

## God Nodes (most connected - your core abstractions)
1. `Session` - 77 edges
2. `SessionService` - 32 edges
3. `DataFrameProfile` - 31 edges
4. `AuthContext` - 30 edges
5. `SandboxClient` - 23 edges
6. `create_db_and_tables()` - 22 edges
7. `User` - 22 edges
8. `authFetch()` - 21 edges
9. `WorkspaceMember` - 20 edges
10. `profile_dataframe()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `test_signup_creates_user_and_personal_workspace()` --uses--> `User`  [INFERRED]
  tests/test_auth.py → services/api/models.py
- `remote_client()` --uses--> `RemoteSandboxClient`  [INFERRED]
  tests/test_live_docker.py → services/sandbox/client.py
- `client()` --uses--> `LocalSandboxClient`  [INFERRED]
  tests/test_sandbox_runner.py → services/sandbox/client.py
- `Technical Stack:` --references--> `useChatStream()`  [INFERRED]
  apps/web/README.md → apps/web/src/hooks/useChatStream.ts
- `setup_database()` --calls--> `create_db_and_tables()`  [EXTRACTED]
  tests/test_agent_orchestrator.py → services/api/database.py

## Import Cycles
- None detected.

## Communities (96 total, 33 thin omitted)

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

### Community 4 - "session_service.py"
Cohesion: 0.13
Nodes (19): chardet, csv, datetime, decimal, duckdb, math, pandas, re (+11 more)

### Community 5 - "server.py"
Cohesion: 0.18
Nodes (18): pydantic, CheckpointFileRequest, execute_code(), ExecuteRequest, ExecuteResponse, get_sandbox_state(), health_check(), HealthResponse (+10 more)

### Community 6 - "orchestrator.py"
Cohesion: 0.06
Nodes (39): asyncio, dotenv, json, AgentOrchestrator, format_sse(), Any, Autonomous AI Analyst & Reflexion Orchestration Engine. Coordinates schema…, Synchronous non-streaming execution wrapper. Consumes the SSE stream and… (+31 more)

### Community 7 - "SandboxClient"
Cohesion: 0.10
Nodes (20): Base interface for sandbox interaction., SandboxClient, client(), fixture, Comprehensive test suite verifying the stateful execution sandbox engine., Verify that runaway or infinite loops are halted cleanly at the timeout…, Verify that reset clears custom variables while keeping baseline imports…, Verify that variable state survives sequential execution turns. (+12 more)

### Community 8 - "test_profiler.py"
Cohesion: 0.13
Nodes (23): detect_encoding_and_delimiter(), generate_loader_code(), DataFrame, Path, Ingest a file of any supported format and return a dictionary of named…, Synthesize the optimal Python code snippet to hydrate the dataset into the…, Detect character encoding via chardet and sniff tabular delimiter. Falls back…, read_file_to_dataframes() (+15 more)

### Community 9 - "SandboxRunner"
Cohesion: 0.19
Nodes (7): Hook into figure display calls to capture Plotly figures without a GUI., Reset the execution namespace, flushing variables while keeping baseline…, Restore 'df' from a Parquet checkpoint file., Maintains a persistent, stateful IPython session for executing data science…, Instantiate and configure the persistent IPython InteractiveShell., Pre-populate the namespace with standard analytical packages., SandboxRunner

### Community 10 - "setup_database"
Cohesion: 0.40
Nodes (5): fixture, Ensure database tables exist before each test., Create a session and upload a sample employee dataset., session_with_data(), setup_database()

### Community 14 - "api/diagnostics.py"
Cohesion: 0.10
Nodes (33): logging, scipy, compute_anomalies(), compute_correlation_matrix(), compute_data_health(), DataFrame, Autonomous Diagnostic Engine for Conversational Data Platform. Provides data…, Computes Pearson (linear) and Spearman (rank) correlation matrices for numeric… (+25 more)

### Community 22 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, clsx, lucide-react, @monaco-editor/react, plotly.js-dist-min, react, react-dom, react-plotly.js (+6 more)

### Community 23 - "types.ts"
Cohesion: 0.09
Nodes (26): DiagnosticsStudio(), DiagnosticsStudioProps, diagnosticsAnomaliesQueryOptions(), diagnosticsCorrelationsQueryOptions(), diagnosticsHealthQueryOptions(), AnomalyAttribution, AnomalyRecord, AnomalyReportResponse (+18 more)

### Community 24 - "DataFrameProfile"
Cohesion: 0.14
Nodes (10): Path, Execute an analytical SQL query against the warehouse, download the result as a…, DataFrameCheckpoint, DataFrameProfile, Deserialize stored JSON profiles., Serialize DataFrameProfile list to JSON string., Immutable copy-on-write snapshot of a DataFrame state., Deserialize stored profile. (+2 more)

### Community 25 - "SessionService"
Cohesion: 0.17
Nodes (9): Any, DataFrame, Calculate row/column deltas and column modifications between two versions., Fetch all checkpoints for a session with calculated schema diffs., Retrieve all registered DataFrameProfiles for the session., Orchestrates sessions, sandbox execution kernels, and dataset persistence., Retrieve dataset rows and column definitions for a session checkpoint., Load the active DataFrame into pandas for diagnostics and AutoML. (+1 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, baseUrl, esModuleInterop, isolatedModules, jsx, lib, module (+13 more)

### Community 27 - "typing"
Cohesion: 0.15
Nodes (13): pathlib, polars, BaseWarehouseConnector, ABC, Base interface and abstractions for external cloud data warehouse connectors.…, Abstract interface for external analytical data warehouse connections., Return True if required environment variables or credentials exist., List accessible datasets or databases. (+5 more)

### Community 28 - "api.ts"
Cohesion: 0.12
Nodes (29): authFetch(), checkpointsQueryOptions(), createSession(), diagnosticsApi, executeCode(), executeSqlQuery(), fetchCheckpoints(), fetchConnectorsStatus() (+21 more)

### Community 29 - "05_asset-st/DESIGN_SYSTEM.md"
Cohesion: 0.15
Nodes (12): Ambient Radiant Glows, Brand & Style, Core Tenets, Elevation & Depth, Geometric Application, Grid Models & Adaptive Behavior, Layout & Spacing, Shapes (+4 more)

### Community 30 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, type, version, autoprefixer, clsx, plotly.js-dist-min, postcss (+7 more)

### Community 31 - "router.tsx"
Cohesion: 0.10
Nodes (25): ActiveChatView(), ActiveChatViewProps, FloatingActionDock(), FloatingActionDockProps, Header(), HeaderProps, SqlPatchModal(), SqlPatchModalProps (+17 more)

### Community 32 - "useChatStream.ts"
Cohesion: 0.15
Nodes (13): Technical Stack:, Web Application Client (`apps/web`), useChatStream(), UseChatStreamOptions, apps_web_src_index, queryClient, DatasetEventPayload, ReflexionStep (+5 more)

### Community 34 - "design_system/DESIGN_SYSTEM.md"
Cohesion: 0.20
Nodes (8): Brand & Style, Core Tenets, Geometric Application, Shapes, Typographic Roles & Expressive Usage, Typography, Gemini Conversational Analytics Platform — Stitch Asset Catalog, Project Metadata

### Community 35 - "ExecutionResult"
Cohesion: 0.14
Nodes (7): BaseException, ExecutionResult, Any, Inspect the current namespace variables and DataFrame dimensions., Atomically persist active 'df' to a Parquet file., Encapsulates the output of a code execution turn., Run code in the IPython shell while redirecting stdout and stderr.

### Community 36 - "runner.py"
Cohesion: 0.13
Nodes (12): concurrent_futures, contextlib, ipython_core_interactiveshell, plotly_express, plotly_graph_objects, _df_fingerprint(), IPython-based stateful execution runner with output interception and Plotly…, Execute a Python code string sequentially within the persistent IPython shell. (+4 more)

### Community 37 - "ExportEngine"
Cohesion: 0.25
Nodes (5): ExportEngine, Generate a Markdown Executive Summary report synthesizing the dataset profile,…, Generates downloadable artifacts from active session state., Export the active DataFrame snapshot in CSV, Parquet, or Excel format. Returns:…, Generate a fully reproducible Jupyter Notebook (.ipynb) containing setup cells,…

### Community 38 - "SqlWorkspace.tsx"
Cohesion: 0.14
Nodes (18): SchemaMapper(), SchemaMapperProps, UserJoinLink, SqlWorkspace(), SqlWorkspaceProps, VirtualDataTable(), VirtualDataTableProps, executeSql (+10 more)

### Community 39 - "automl.py"
Cohesion: 0.10
Nodes (28): ast, numpy, detect_problem_type(), generate_python_code(), DataFrame, Autonomous AutoML Baseline Engine for Conversational Data Platform. Provides…, Synthesizes a clean, standalone, executable scikit-learn Python script., Detects whether target is binary, multiclass, or regression. (+20 more)

### Community 40 - "models.py"
Cohesion: 0.16
Nodes (21): execute_code(), execute_sql_query(), Execute arbitrary Python analytical code within the session's sandbox. Returns…, Non-destructively roll back the active DataFrame to a specified checkpoint…, Execute arbitrary analytical SQL on session datasets and checkpoints via…, revert_session_version(), ChatRequest, ChatTurnResponse (+13 more)

### Community 41 - "DuckDBEngine"
Cohesion: 0.16
Nodes (14): DuckDBPyConnection, SqlQueryColumn, DuckDBEngine, Any, DbSession, Execute an analytical SQL query against session tables and checkpoints. Returns…, Execute a SQL statement and materialize the result into a new Parquet…, Sanitize filename into a valid SQL identifier (lowercase, alphanumeric +… (+6 more)

### Community 46 - "workspaces.py"
Cohesion: 0.09
Nodes (39): delete, fastapi, fastapi_security, patch, Request, get_auth_context(), get_current_user(), get_current_user_optional() (+31 more)

### Community 47 - "FileUploadModal.tsx"
Cohesion: 0.60
Nodes (4): FileUploadModal(), FileUploadModalProps, uploadDataset(), FileUploadResponse

### Community 48 - "Session"
Cohesion: 0.16
Nodes (16): Conversational data analysis session., Session, Create a new session record in the database., sqlmodel_pool, asyncio, Path, test_incremental_checkpoint_on_dataframe_mutation(), test_initial_checkpoint_created_on_upload() (+8 more)

### Community 49 - "routers/auth.py"
Cohesion: 0.11
Nodes (38): bcrypt, hashlib, jwt, AuthTokenResponse, Secure database-backed refresh tokens supporting instant revocation., RefreshToken, RefreshTokenRequest, UserLoginRequest (+30 more)

### Community 51 - "os"
Cohesion: 0.18
Nodes (8): alembic, Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), logging_config, os, sqlalchemy

### Community 52 - "profile_dataframe"
Cohesion: 0.15
Nodes (12): Path, ColumnProfile, Metadata profile of a single column., profile_dataframe(), Any, Extract a comprehensive, privacy-compliant schema profile from a Polars…, Sanitize arbitrary Python/Pandas/Polars values for strict RFC 8259 JSON…, sanitize_value() (+4 more)

### Community 53 - "LocalSandboxClient"
Cohesion: 0.13
Nodes (10): argparse, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any, HTTP client communicating with the containerized sandbox runner., In-process sandbox client for rapid local testing without container… (+2 more)

### Community 54 - "ChatTurn"
Cohesion: 0.21
Nodes (8): BaseSandboxClient, ChatTurn, Individual analytical turn within a session., Extract active DataFrame from sandbox, persist Parquet checkpoint, profile…, Execute arbitrary Python analytical code inside the session's sandbox. Records…, Revert the session's active DataFrame to a previous checkpoint. Non-…, Get or initialize a sandbox client for the given session. Uses…, Execute smart data hygiene remediation in sandbox, materialize a new versioned…

### Community 55 - "database.py"
Cohesion: 0.06
Nodes (47): fastapi_testclient, io, listens_for, pytest, create_db_and_tables(), get_db_session(), patch_sqlite_columns(), Database configuration and session lifecycle management for services/api.… (+39 more)

### Community 56 - "AuthContext"
Cohesion: 0.15
Nodes (17): AuthContext, BaseModel, Execution context containing authenticated user, active workspace, and assigned…, chat_with_data(), import_warehouse_dataset(), post, Upload a tabular dataset (CSV, TSV, Parquet, Excel, JSON, SQLite).…, Reset the sandbox kernel state, prune incremental checkpoints, and re-hydrate… (+9 more)

### Community 57 - "setup_database"
Cohesion: 0.67
Nodes (3): fixture, Ensure database tables exist before each test., setup_database()

### Community 58 - "session_with_data"
Cohesion: 0.67
Nodes (3): fixture, Create a session and ingest sample transactional data., session_with_data()

### Community 59 - "setup_database"
Cohesion: 0.67
Nodes (3): fixture, Ensure clean schema and defaults for each test run., setup_database()

### Community 60 - "Imported Screens & Assets"
Cohesion: 0.20
Nodes (10): 1. Avatar Portrait of Fares (Tech Founder & Senior Data Analyst), 2. Gemini Insights & Automated Anomalies, 3. Gemini Ambient Spark Logo, 4. SQL & Deep Query Workspace, 5. Design System (Ambient Intelligence Workspace), 6. Conversational Analytics Canvas, 7. SQL Patch Remediation Modal, 8. Rollback Script & Snapshot Comparison (+2 more)

### Community 61 - "Sidebar.tsx"
Cohesion: 0.20
Nodes (18): AuthModal(), AuthModalProps, Sidebar(), SidebarProps, TeamDrawer(), TeamDrawerProps, authApi, clearStoredTokens() (+10 more)

### Community 62 - "main.py"
Cohesion: 0.08
Nodes (38): fastapi_middleware_cors, fastapi_responses, services_api_connectors, create_session(), export_session_data(), get_connectors_status(), get_dataset(), get_providers_status() (+30 more)

### Community 64 - "SnowflakeConnector"
Cohesion: 0.20
Nodes (4): Any, Path, Snowflake Data Cloud analytical connector., SnowflakeConnector

### Community 65 - "Components"
Cohesion: 0.29
Nodes (7): 1. Primary Prompt Input Bar, 2. Buttons, 3. Filter Chips & Model Switchers, 4. Conversational Cards & Response Bubbles, 5. Checkboxes & Radio Controls, 6. Responsive Collapsible Sidebar, Components

### Community 66 - "Components"
Cohesion: 0.29
Nodes (7): 1. Primary Prompt Input Bar, 2. Buttons, 3. Filter Chips & Model Switchers, 4. Conversational Cards & Response Bubbles, 5. Checkboxes & Radio Controls, 6. Responsive Collapsible Sidebar, Components

### Community 67 - "devDependencies"
Cohesion: 0.18
Nodes (11): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, @types/react-plotly.js (+3 more)

### Community 68 - "client.py"
Cohesion: 0.18
Nodes (5): httpx, Client SDK for interacting with the sandbox execution engine., fixture, Integration test verifying the running Docker sandbox container over HTTP., remote_client()

### Community 69 - "Colors"
Cohesion: 0.50
Nodes (4): Ambient AI Accents & Signals, Colors, Surface Tiers & Neutral Scales, Text Contrast Tiers

### Community 70 - "Colors"
Cohesion: 0.50
Nodes (4): Ambient AI Accents & Signals, Colors, Surface Tiers & Neutral Scales, Text Contrast Tiers

### Community 71 - "Elevation & Depth"
Cohesion: 0.67
Nodes (3): Ambient Radiant Glows, Elevation & Depth, The Depth Stack

### Community 72 - "Layout & Spacing"
Cohesion: 0.67
Nodes (3): Grid Models & Adaptive Behavior, Layout & Spacing, Spacing Density

### Community 74 - "routers/diagnostics.py"
Cohesion: 0.31
Nodes (10): ApplyHygieneRequest, ApplyHygieneResponse, AutoMLTrainRequest, CheckpointSummaryResponse, apply_hygiene_fix(), post, Diagnostics & AutoML Router for data_speaker. Exposes endpoints for dataset…, Validate that session exists and user has workspace-level permission to view it. (+2 more)

### Community 75 - "BigQueryConnector"
Cohesion: 0.24
Nodes (3): BigQueryConnector, Any, Google Cloud BigQuery warehouse connector.

### Community 76 - ".get_status"
Cohesion: 0.29
Nodes (4): Any, Return connector health and configuration metadata., Verify network connectivity and credentials with the cloud warehouse., Preview top rows from an external table.

### Community 77 - ".ingest_file"
Cohesion: 0.29
Nodes (4): Path, Convert a local filesystem path to the equivalent container mount path if…, Save uploaded file, profile all tables, record in database, hydrate sandbox,…, Reset session: clean up checkpoints except df_v0, reset sandbox, and rehydrate…

### Community 78 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 79 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_node_url, vite, @vitejs/plugin-react

### Community 80 - "get_me"
Cohesion: 0.50
Nodes (4): get_me(), Any, get, Return user profile and all workspace memberships with roles.

## Knowledge Gaps
- **232 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+227 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 577 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Session` connect `Session` to `session_service.py`, `ExportEngine`, `orchestrator.py`, `models.py`, `DuckDBEngine`, `routers/diagnostics.py`, `.ingest_file`, `workspaces.py`, `api/diagnostics.py`, `get_me`, `routers/auth.py`, `.get_session_relations`, `ChatTurn`, `database.py`, `AuthContext`, `SessionService`, `main.py`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `DataFrameProfile` connect `DataFrameProfile` to `SnowflakeConnector`, `session_service.py`, `orchestrator.py`, `models.py`, `BigQueryConnector`, `.ingest_file`, `.get_session_relations`, `profile_dataframe`, `ChatTurn`, `SessionService`, `typing`, `main.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `SandboxRunner` connect `SandboxRunner` to `ExecutionResult`, `client.py`, `server.py`, `runner.py`, `LocalSandboxClient`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `Session` (e.g. with `list_sessions()` and `verify_session_access()`) actually correct?**
  _`Session` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `SessionService` (e.g. with `ChatTurn` and `CheckpointSummaryResponse`) actually correct?**
  _`SessionService` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `DataFrameProfile` (e.g. with `build_system_prompt()` and `format_schema_context()`) actually correct?**
  _`DataFrameProfile` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `AuthContext` (e.g. with `User` and `Workspace`) actually correct?**
  _`AuthContext` has 23 INFERRED edges - model-reasoned connections that need verification._