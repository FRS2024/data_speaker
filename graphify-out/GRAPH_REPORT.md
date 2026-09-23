# Graph Report - Conversational_Data  (2026-09-23)

## Corpus Check
- 99 files · ~113,267 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 3, .example 1, .ini 1)

## Summary
- 1345 nodes · 2737 edges · 83 communities (65 shown, 18 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 188 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `508d4e36`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SYSTEM ARCHITECTURE & DESIGN DOCUMENT
- TECHNICAL REQUIREMENTS DOCUMENT (TRD)
- Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)
- PRODUCT REQUIREMENTS DOCUMENT (PRD)
- session_service.py
- server.py
- swarm.py
- SandboxClient
- test_profiler.py
- SandboxRunner
- test_agent_orchestrator.py
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
- ExecutionResult
- compilerOptions
- BaseWarehouseConnector
- api.ts
- 05_asset-st/DESIGN_SYSTEM.md
- package.json
- router.tsx
- react
- design_system/DESIGN_SYSTEM.md
- deck_engine.py
- runner.py
- test_swarm_orchestrator.py
- SqlWorkspace.tsx
- automl.py
- models.py
- DuckDBEngine
- apps_web_src_app_globals
- apps_web_src_lib_api_resetsession
- subprocess
- urllib_request
- database.py
- FileUploadModal.tsx
- useChatStream
- routers/auth.py
- test_auth.py
- env.py
- infer_foreign_key_relations
- LocalSandboxClient
- SessionService
- create_db_and_tables
- main.py
- test_api_ingestion.py
- StatisticianCritic
- VersionHistoryView.tsx
- Imported Screens & Assets
- Sidebar.tsx
- get
- test_multi_tenancy.py
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
- Session
- BigQueryConnector
- NumberedCanvas
- test_dataframe_versioning.py
- scripts
- vite.config.ts
- get_me
- ReportsStudio.tsx
- tailwind.config.ts

## God Nodes (most connected - your core abstractions)
1. `Session` - 99 edges
2. `AuthContext` - 36 edges
3. `SessionService` - 32 edges
4. `DataFrameProfile` - 31 edges
5. `create_db_and_tables()` - 24 edges
6. `DataFrameCheckpoint` - 24 edges
7. `SandboxClient` - 23 edges
8. `react` - 22 edges
9. `User` - 22 edges
10. `authFetch()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `test_signup_creates_user_and_personal_workspace()` --uses--> `User`  [INFERRED]
  tests/test_auth.py → services/api/models.py
- `test_signup_creates_user_and_personal_workspace()` --uses--> `RefreshToken`  [INFERRED]
  tests/test_auth.py → services/api/models.py
- `mock_session_with_data()` --uses--> `Session`  [INFERRED]
  tests/test_deck_engine.py → services/api/models.py
- `mock_session_with_data()` --uses--> `Session`  [INFERRED]
  tests/test_pdf_engine.py → services/api/models.py
- `test_swarm_mode_sync_execution()` --uses--> `ChatTurn`  [INFERRED]
  tests/test_swarm_orchestrator.py → services/api/models.py

## Import Cycles
- None detected.

## Communities (83 total, 18 thin omitted)

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
Cohesion: 0.12
Nodes (25): chardet, csv, datetime, decimal, duckdb, math, os, pandas (+17 more)

### Community 5 - "server.py"
Cohesion: 0.18
Nodes (18): pydantic, CheckpointFileRequest, execute_code(), ExecuteRequest, ExecuteResponse, get_sandbox_state(), health_check(), HealthResponse (+10 more)

### Community 6 - "swarm.py"
Cohesion: 0.05
Nodes (49): asyncio, dotenv, json, AgentOrchestrator, format_sse(), Any, Autonomous AI Analyst & Reflexion Orchestration Engine. Coordinates schema…, Synchronous non-streaming execution wrapper. Consumes the SSE stream and… (+41 more)

### Community 7 - "SandboxClient"
Cohesion: 0.10
Nodes (20): Base interface for sandbox interaction., SandboxClient, client(), fixture, Comprehensive test suite verifying the stateful execution sandbox engine., Verify that runaway or infinite loops are halted cleanly at the timeout…, Verify that reset clears custom variables while keeping baseline imports…, Verify that variable state survives sequential execution turns. (+12 more)

### Community 8 - "test_profiler.py"
Cohesion: 0.10
Nodes (29): Path, detect_encoding_and_delimiter(), generate_loader_code(), profile_dataframe(), DataFrame, Path, Ingest a file of any supported format and return a dictionary of named…, Extract a comprehensive, privacy-compliant schema profile from a Polars… (+21 more)

### Community 9 - "SandboxRunner"
Cohesion: 0.19
Nodes (7): Hook into figure display calls to capture Plotly figures without a GUI., Reset the execution namespace, flushing variables while keeping baseline…, Restore 'df' from a Parquet checkpoint file., Maintains a persistent, stateful IPython session for executing data science…, Instantiate and configure the persistent IPython InteractiveShell., Pre-populate the namespace with standard analytical packages., SandboxRunner

### Community 10 - "test_agent_orchestrator.py"
Cohesion: 0.14
Nodes (14): fixture, Automated test suite for Phase 3: Autonomous AI Analyst & Reflexion Loop.…, Test real-time Server-Sent Events (SSE) streaming format and event multiplexing., Ensure database tables exist before each test., Create a session and upload a sample employee dataset., Test standard single-turn analytical query returning synchronous JSON., Test that chart requests produce interactive Plotly specifications., Test the Reflexion loop: 1. Attempt 1 triggers a KeyError… (+6 more)

### Community 14 - "api/diagnostics.py"
Cohesion: 0.08
Nodes (37): numpy, reportlab_lib, reportlab_lib_pagesizes, reportlab_lib_styles, reportlab_lib_units, reportlab_pdfgen, reportlab_platypus, scipy (+29 more)

### Community 22 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, clsx, lucide-react, @monaco-editor/react, plotly.js-dist-min, react, react-dom, react-plotly.js (+6 more)

### Community 23 - "types.ts"
Cohesion: 0.08
Nodes (29): DiagnosticsStudio(), DiagnosticsStudioProps, diagnosticsAnomaliesQueryOptions(), diagnosticsApi, diagnosticsCorrelationsQueryOptions(), diagnosticsHealthQueryOptions(), AnomalyAttribution, AnomalyRecord (+21 more)

### Community 24 - "DataFrameProfile"
Cohesion: 0.20
Nodes (6): DataFrameProfile, Deserialize stored JSON profiles., Serialize DataFrameProfile list to JSON string., Deserialize stored profile., Serialize DataFrameProfile., Structural schema profile of a loaded dataset (privacy-safe, no raw bulk data).

### Community 25 - "ExecutionResult"
Cohesion: 0.14
Nodes (7): BaseException, ExecutionResult, Any, Inspect the current namespace variables and DataFrame dimensions., Atomically persist active 'df' to a Parquet file., Encapsulates the output of a code execution turn., Run code in the IPython shell while redirecting stdout and stderr.

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, baseUrl, esModuleInterop, isolatedModules, jsx, lib, module (+13 more)

### Community 27 - "BaseWarehouseConnector"
Cohesion: 0.11
Nodes (12): BaseWarehouseConnector, ABC, Any, Path, Abstract interface for external analytical data warehouse connections., Return True if required environment variables or credentials exist., Return connector health and configuration metadata., Verify network connectivity and credentials with the cloud warehouse. (+4 more)

### Community 28 - "api.ts"
Cohesion: 0.12
Nodes (29): authFetch(), checkpointsQueryOptions(), createSession(), executeCode(), executeSqlQuery(), fetchCheckpoints(), fetchConnectorsStatus(), fetchDatasetData() (+21 more)

### Community 29 - "05_asset-st/DESIGN_SYSTEM.md"
Cohesion: 0.15
Nodes (12): Ambient Radiant Glows, Brand & Style, Core Tenets, Elevation & Depth, Geometric Application, Grid Models & Adaptive Behavior, Layout & Spacing, Shapes (+4 more)

### Community 30 - "package.json"
Cohesion: 0.11
Nodes (18): name, private, type, version, autoprefixer, clsx, @monaco-editor/react, plotly.js-dist-min (+10 more)

### Community 31 - "router.tsx"
Cohesion: 0.10
Nodes (21): Header(), HeaderProps, SqlPatchModal(), SqlPatchModalProps, VisualizationStudio(), VisualizationStudioProps, apps_web_src_index, queryClient (+13 more)

### Community 32 - "react"
Cohesion: 0.13
Nodes (21): ActiveChatView(), ActiveChatViewProps, FloatingActionDock(), FloatingActionDockProps, StatisticalPeerReviewCard(), StatisticalPeerReviewCardProps, StepConfig, STEPS (+13 more)

### Community 34 - "design_system/DESIGN_SYSTEM.md"
Cohesion: 0.20
Nodes (8): Brand & Style, Core Tenets, Geometric Application, Shapes, Typographic Roles & Expressive Usage, Typography, Gemini Conversational Analytics Platform — Stitch Asset Catalog, Project Metadata

### Community 35 - "deck_engine.py"
Cohesion: 0.05
Nodes (39): Inches, matplotlib, matplotlib_pyplot, pptx, pptx_chart_data, pptx_dml_color, pptx_enum_chart, pptx_enum_shapes (+31 more)

### Community 36 - "runner.py"
Cohesion: 0.13
Nodes (12): concurrent_futures, contextlib, ipython_core_interactiveshell, plotly_express, plotly_graph_objects, _df_fingerprint(), IPython-based stateful execution runner with output interception and Plotly…, Execute a Python code string sequentially within the persistent IPython shell. (+4 more)

### Community 37 - "test_swarm_orchestrator.py"
Cohesion: 0.20
Nodes (10): fixture, Automated test suite for Track D: Multi-Agent Critic & Statistician Debate…, Ensure database tables exist before each test., Create a session and upload a sample employee dataset., Test running synchronous analytical turn with swarm_mode=True., Test SSE event stream with swarm_phase, critic_review, and execution events., session_with_data(), setup_database() (+2 more)

### Community 38 - "SqlWorkspace.tsx"
Cohesion: 0.18
Nodes (15): SchemaMapper(), SchemaMapperProps, UserJoinLink, SqlWorkspace(), SqlWorkspaceProps, VirtualDataTable(), VirtualDataTableProps, executeSql (+7 more)

### Community 39 - "automl.py"
Cohesion: 0.09
Nodes (29): ast, logging, detect_problem_type(), generate_python_code(), DataFrame, Autonomous AutoML Baseline Engine for Conversational Data Platform. Provides…, Synthesizes a clean, standalone, executable scikit-learn Python script., Detects whether target is binary, multiclass, or regression. (+21 more)

### Community 40 - "models.py"
Cohesion: 0.15
Nodes (22): execute_code(), Execute arbitrary Python analytical code within the session's sandbox. Returns…, Non-destructively roll back the active DataFrame to a specified checkpoint…, revert_session_version(), AIPolishRequest, ChatRequest, ChatTurnResponse, CodeExecutionRequest (+14 more)

### Community 41 - "DuckDBEngine"
Cohesion: 0.16
Nodes (15): DuckDBPyConnection, SqlQueryColumn, SqlQueryResponse, DuckDBEngine, Any, DbSession, Execute an analytical SQL query against session tables and checkpoints. Returns…, Execute a SQL statement and materialize the result into a new Parquet… (+7 more)

### Community 46 - "database.py"
Cohesion: 0.09
Nodes (42): delete, fastapi, fastapi_security, listens_for, patch, Request, get_auth_context(), get_current_user() (+34 more)

### Community 47 - "FileUploadModal.tsx"
Cohesion: 0.60
Nodes (4): FileUploadModal(), FileUploadModalProps, uploadDataset(), FileUploadResponse

### Community 48 - "useChatStream"
Cohesion: 0.50
Nodes (3): Technical Stack:, Web Application Client (`apps/web`), useChatStream()

### Community 49 - "routers/auth.py"
Cohesion: 0.13
Nodes (32): bcrypt, hashlib, jwt, AuthTokenResponse, Secure database-backed refresh tokens supporting instant revocation., RefreshToken, RefreshTokenRequest, UserResponse (+24 more)

### Community 50 - "test_auth.py"
Cohesion: 0.18
Nodes (11): Verify a plaintext password against a stored bcrypt hash., verify_password(), Unit and integration tests for Authentication: Signup, login, password hashing,…, Verify /me returns profile and user workspace memberships., Verify signup creates user with hashed password and initial owner workspace., Verify login authenticates correctly, returning valid 60m access token., Verify refresh token rotation and immediate revocation on logout., test_get_me_profile_and_workspaces() (+3 more)

### Community 51 - "env.py"
Cohesion: 0.20
Nodes (7): alembic, Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), logging_config, sqlalchemy

### Community 52 - "infer_foreign_key_relations"
Cohesion: 0.18
Nodes (9): infer_foreign_key_relations(), Any, Heuristically infer potential foreign key / join relationships between tables…, Sanitize arbitrary Python/Pandas/Polars values for strict RFC 8259 JSON…, sanitize_value(), Retrieve distinct profiles for all uploaded files/tables in the session., Infer foreign key links and join opportunities between all tables in the…, Verify that NaNs, Infs, dates, and numpy scalars are sanitized for RFC 8259… (+1 more)

### Community 53 - "LocalSandboxClient"
Cohesion: 0.13
Nodes (10): argparse, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any, HTTP client communicating with the containerized sandbox runner., In-process sandbox client for rapid local testing without container… (+2 more)

### Community 54 - "SessionService"
Cohesion: 0.09
Nodes (21): BaseSandboxClient, ColumnDiff, SchemaDiff, Any, DataFrame, Path, Convert a local filesystem path to the equivalent container mount path if…, Extract active DataFrame from sandbox, persist Parquet checkpoint, profile… (+13 more)

### Community 55 - "create_db_and_tables"
Cohesion: 0.06
Nodes (39): fastapi_testclient, io, pytest, create_db_and_tables(), patch_sqlite_columns(), Initialize all registered SQLModel tables in the database and seed defaults., Safely add new columns to existing SQLite tables if missing., fixture (+31 more)

### Community 56 - "main.py"
Cohesion: 0.07
Nodes (38): fastapi_middleware_cors, fastapi_responses, Dependency factory that enforces the RBAC role hierarchy. Usage:…, require_role(), services_api_connectors, chat_with_data(), create_session(), execute_sql_query() (+30 more)

### Community 57 - "test_api_ingestion.py"
Cohesion: 0.13
Nodes (14): fixture, End-to-end integration tests for the API Gateway and Ingestion Flow…, Test state persistence across turns and Plotly figure interception via API., Ensure database tables exist before each test., Verify API health check endpoint., Test creating a new session and querying its metadata., Test uploading a CSV dataset, extracting schema, and querying schema endpoint., Test that uploaded data is automatically hydrated and accessible as `df`. (+6 more)

### Community 58 - "StatisticianCritic"
Cohesion: 0.09
Nodes (28): re, Any, DataFrame, Statistician & Critic Agent for Track D Multi-Agent Swarm. Performs two-stage…, Deep post-execution audit inspecting numeric values, sample sizes, and output…, Rigorous statistical reviewer that audits code and outputs before user delivery., Static AST and heuristic scan of Python code prior to sandbox execution.…, StatisticianCritic (+20 more)

### Community 59 - "VersionHistoryView.tsx"
Cohesion: 0.67
Nodes (3): VersionHistoryView(), VersionHistoryViewProps, CheckpointSummary

### Community 60 - "Imported Screens & Assets"
Cohesion: 0.20
Nodes (10): 1. Avatar Portrait of Fares (Tech Founder & Senior Data Analyst), 2. Gemini Insights & Automated Anomalies, 3. Gemini Ambient Spark Logo, 4. SQL & Deep Query Workspace, 5. Design System (Ambient Intelligence Workspace), 6. Conversational Analytics Canvas, 7. SQL Patch Remediation Modal, 8. Rollback Script & Snapshot Comparison (+2 more)

### Community 61 - "Sidebar.tsx"
Cohesion: 0.20
Nodes (17): AuthModal(), AuthModalProps, Sidebar(), SidebarProps, TeamDrawer(), TeamDrawerProps, authApi, clearStoredTokens() (+9 more)

### Community 62 - "get"
Cohesion: 0.15
Nodes (18): export_session_data(), get_connectors_status(), get_dataset(), get_providers_status(), get_session_dataset(), get_session_schema(), health_check(), list_sessions() (+10 more)

### Community 63 - "test_multi_tenancy.py"
Cohesion: 0.20
Nodes (9): fixture, Integration tests for Workspace Multi-Tenancy: Workspace isolation, session…, Verify Admin can invite new members and modify their role., Verify user can create multiple workspaces and list memberships., Verify sessions created in Workspace A are strictly invisible to Workspace B., setup_database(), test_cross_tenant_session_isolation(), test_invite_member_and_role_management() (+1 more)

### Community 64 - "SnowflakeConnector"
Cohesion: 0.24
Nodes (3): Any, Snowflake Data Cloud analytical connector., SnowflakeConnector

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

### Community 74 - "Session"
Cohesion: 0.12
Nodes (34): AuthContext, BaseModel, Execution context containing authenticated user, active workspace, and assigned…, list_session_checkpoints(), List all recorded DataFrame checkpoints for a session with calculated schema…, AIPolishResponse, ApplyHygieneRequest, ApplyHygieneResponse (+26 more)

### Community 75 - "BigQueryConnector"
Cohesion: 0.20
Nodes (4): BigQueryConnector, Any, Path, Google Cloud BigQuery warehouse connector.

### Community 77 - "test_dataframe_versioning.py"
Cohesion: 0.09
Nodes (24): sqlmodel_pool, asyncio, fixture, Path, Tests for Phase 5: DataFrame Versioning, Checkpointing & Time-Travel Rollback., test_db(), test_incremental_checkpoint_on_dataframe_mutation(), test_initial_checkpoint_created_on_upload() (+16 more)

### Community 78 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 79 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_node_url, vite, @vitejs/plugin-react

### Community 80 - "get_me"
Cohesion: 0.50
Nodes (4): get_me(), Any, get, Return user profile and all workspace memberships with roles.

### Community 81 - "ReportsStudio.tsx"
Cohesion: 0.40
Nodes (5): ReportsStudio(), ReportsStudioProps, reportsApi, reportsPreviewQueryOptions(), DeckSlidePreview

## Knowledge Gaps
- **235 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+230 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 647 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Session` connect `Session` to `deck_engine.py`, `session_service.py`, `swarm.py`, `models.py`, `test_profiler.py`, `DuckDBEngine`, `test_dataframe_versioning.py`, `database.py`, `api/diagnostics.py`, `get_me`, `routers/auth.py`, `test_auth.py`, `infer_foreign_key_relations`, `SessionService`, `main.py`, `get`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `DataFrameProfile` connect `DataFrameProfile` to `SnowflakeConnector`, `session_service.py`, `swarm.py`, `test_profiler.py`, `models.py`, `BigQueryConnector`, `infer_foreign_key_relations`, `SessionService`, `main.py`, `BaseWarehouseConnector`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `SandboxClient` connect `SandboxClient` to `ExecutionResult`, `client.py`, `LocalSandboxClient`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Session` (e.g. with `list_sessions()` and `verify_session_access()`) actually correct?**
  _`Session` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `AuthContext` (e.g. with `User` and `Workspace`) actually correct?**
  _`AuthContext` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `SessionService` (e.g. with `ChatTurn` and `CheckpointSummaryResponse`) actually correct?**
  _`SessionService` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `DataFrameProfile` (e.g. with `build_system_prompt()` and `format_schema_context()`) actually correct?**
  _`DataFrameProfile` has 7 INFERRED edges - model-reasoned connections that need verification._