# Graph Report - Conversational_Data  (2026-09-23)

## Corpus Check
- 93 files · ~109,422 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 3, .example 1, .ini 1)

## Summary
- 1280 nodes · 2585 edges · 88 communities (71 shown, 17 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 174 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2b9387b3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SYSTEM ARCHITECTURE & DESIGN DOCUMENT
- TECHNICAL REQUIREMENTS DOCUMENT (TRD)
- Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)
- PRODUCT REQUIREMENTS DOCUMENT (PRD)
- session_service.py
- server.py
- BaseLLMProvider
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
- .compute_schema_diff
- compilerOptions
- typing
- api.ts
- 05_asset-st/DESIGN_SYSTEM.md
- package.json
- router.tsx
- useChatStream.ts
- design_system/DESIGN_SYSTEM.md
- deck_engine.py
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
- test_auth.py
- database.py
- infer_foreign_key_relations
- LocalSandboxClient
- SessionService
- test_duckdb_sql.py
- post
- test_api_ingestion.py
- orchestrator.py
- create_db_and_tables
- Imported Screens & Assets
- Sidebar.tsx
- main.py
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
- AuthContext
- BigQueryConnector
- pdf_engine.py
- DataFrameCheckpoint
- scripts
- vite.config.ts
- api/auth.py
- ReportsStudio.tsx
- tailwind.config.ts
- test_rbac.py
- .apply_hygiene_remediation
- test_dataframe_versioning.py
- io
- pytest

## God Nodes (most connected - your core abstractions)
1. `Session` - 97 edges
2. `AuthContext` - 36 edges
3. `SessionService` - 32 edges
4. `DataFrameProfile` - 31 edges
5. `DataFrameCheckpoint` - 24 edges
6. `SandboxClient` - 23 edges
7. `create_db_and_tables()` - 22 edges
8. `User` - 22 edges
9. `authFetch()` - 21 edges
10. `react` - 20 edges

## Surprising Connections (you probably didn't know these)
- `test_signup_creates_user_and_personal_workspace()` --uses--> `User`  [INFERRED]
  tests/test_auth.py → services/api/models.py
- `mock_session_with_data()` --uses--> `Session`  [INFERRED]
  tests/test_deck_engine.py → services/api/models.py
- `mock_session_with_data()` --uses--> `Session`  [INFERRED]
  tests/test_pdf_engine.py → services/api/models.py
- `mock_session_with_data()` --uses--> `DataFrameCheckpoint`  [INFERRED]
  tests/test_deck_engine.py → services/api/models.py
- `remote_client()` --uses--> `RemoteSandboxClient`  [INFERRED]
  tests/test_live_docker.py → services/sandbox/client.py

## Import Cycles
- None detected.

## Communities (88 total, 17 thin omitted)

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
Cohesion: 0.15
Nodes (15): chardet, csv, datetime, decimal, duckdb, math, pandas, Multi-format export engine for analytical datasets, reproducible notebooks, and… (+7 more)

### Community 5 - "server.py"
Cohesion: 0.18
Nodes (18): pydantic, CheckpointFileRequest, execute_code(), ExecuteRequest, ExecuteResponse, get_sandbox_state(), health_check(), HealthResponse (+10 more)

### Community 6 - "BaseLLMProvider"
Cohesion: 0.10
Nodes (16): AnthropicProvider, BaseLLMProvider, GeminiProvider, MockProvider, OpenAIProvider, ABC, Any, Google Gemini client powered by the official google-genai SDK. Supports native… (+8 more)

### Community 7 - "SandboxClient"
Cohesion: 0.12
Nodes (20): Base interface for sandbox interaction., SandboxClient, client(), fixture, Comprehensive test suite verifying the stateful execution sandbox engine., Verify that runaway or infinite loops are halted cleanly at the timeout…, Verify that reset clears custom variables while keeping baseline imports…, Verify that variable state survives sequential execution turns. (+12 more)

### Community 8 - "test_profiler.py"
Cohesion: 0.13
Nodes (23): detect_encoding_and_delimiter(), generate_loader_code(), DataFrame, Path, Ingest a file of any supported format and return a dictionary of named…, Synthesize the optimal Python code snippet to hydrate the dataset into the…, Detect character encoding via chardet and sniff tabular delimiter. Falls back…, read_file_to_dataframes() (+15 more)

### Community 9 - "SandboxRunner"
Cohesion: 0.10
Nodes (13): BaseException, Any, Hook into figure display calls to capture Plotly figures without a GUI., Reset the execution namespace, flushing variables while keeping baseline…, Inspect the current namespace variables and DataFrame dimensions., Atomically persist active 'df' to a Parquet file., Restore 'df' from a Parquet checkpoint file., Run code in the IPython shell while redirecting stdout and stderr. (+5 more)

### Community 10 - "test_agent_orchestrator.py"
Cohesion: 0.14
Nodes (14): fixture, Automated test suite for Phase 3: Autonomous AI Analyst & Reflexion Loop.…, Test real-time Server-Sent Events (SSE) streaming format and event multiplexing., Ensure database tables exist before each test., Create a session and upload a sample employee dataset., Test standard single-turn analytical query returning synchronous JSON., Test that chart requests produce interactive Plotly specifications., Test the Reflexion loop: 1. Attempt 1 triggers a KeyError… (+6 more)

### Community 14 - "api/diagnostics.py"
Cohesion: 0.11
Nodes (24): numpy, scipy, Compiles a complete PowerPoint (.pptx) file for the analytical session., compute_anomalies(), compute_correlation_matrix(), compute_data_health(), DataFrame, Autonomous Diagnostic Engine for Conversational Data Platform. Provides data… (+16 more)

### Community 22 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, clsx, lucide-react, @monaco-editor/react, plotly.js-dist-min, react, react-dom, react-plotly.js (+6 more)

### Community 23 - "types.ts"
Cohesion: 0.08
Nodes (30): DiagnosticsStudio(), DiagnosticsStudioProps, diagnosticsAnomaliesQueryOptions(), diagnosticsApi, diagnosticsCorrelationsQueryOptions(), diagnosticsHealthQueryOptions(), AnomalyAttribution, AnomalyRecord (+22 more)

### Community 24 - "DataFrameProfile"
Cohesion: 0.13
Nodes (12): Path, Execute an analytical SQL query against the warehouse, download the result as a…, Path, Path, DataFrameProfile, Deserialize stored JSON profiles., Serialize DataFrameProfile list to JSON string., Structural schema profile of a loaded dataset (privacy-safe, no raw bulk data). (+4 more)

### Community 25 - ".compute_schema_diff"
Cohesion: 0.40
Nodes (3): SchemaDiff, Calculate row/column deltas and column modifications between two versions., Fetch all checkpoints for a session with calculated schema diffs.

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, baseUrl, esModuleInterop, isolatedModules, jsx, lib, module (+13 more)

### Community 27 - "typing"
Cohesion: 0.10
Nodes (18): os, pathlib, polars, BaseWarehouseConnector, ABC, Any, Base interface and abstractions for external cloud data warehouse connectors.…, Abstract interface for external analytical data warehouse connections. (+10 more)

### Community 28 - "api.ts"
Cohesion: 0.13
Nodes (28): authFetch(), checkpointsQueryOptions(), createSession(), executeCode(), executeSqlQuery(), fetchCheckpoints(), fetchConnectorsStatus(), fetchDatasetData() (+20 more)

### Community 29 - "05_asset-st/DESIGN_SYSTEM.md"
Cohesion: 0.15
Nodes (12): Ambient Radiant Glows, Brand & Style, Core Tenets, Elevation & Depth, Geometric Application, Grid Models & Adaptive Behavior, Layout & Spacing, Shapes (+4 more)

### Community 30 - "package.json"
Cohesion: 0.12
Nodes (16): name, private, type, version, autoprefixer, clsx, plotly.js-dist-min, postcss (+8 more)

### Community 31 - "router.tsx"
Cohesion: 0.08
Nodes (31): ActiveChatView(), ActiveChatViewProps, FloatingActionDock(), FloatingActionDockProps, Header(), HeaderProps, SqlPatchModal(), SqlPatchModalProps (+23 more)

### Community 32 - "useChatStream.ts"
Cohesion: 0.29
Nodes (6): Technical Stack:, Web Application Client (`apps/web`), useChatStream(), UseChatStreamOptions, DatasetEventPayload, ReflexionStep

### Community 34 - "design_system/DESIGN_SYSTEM.md"
Cohesion: 0.20
Nodes (8): Brand & Style, Core Tenets, Geometric Application, Shapes, Typographic Roles & Expressive Usage, Typography, Gemini Conversational Analytics Platform — Stitch Asset Catalog, Project Metadata

### Community 35 - "deck_engine.py"
Cohesion: 0.06
Nodes (46): fastapi_responses, Inches, matplotlib, matplotlib_pyplot, pptx, pptx_chart_data, pptx_dml_color, pptx_enum_chart (+38 more)

### Community 36 - "runner.py"
Cohesion: 0.12
Nodes (12): concurrent_futures, contextlib, ipython_core_interactiveshell, plotly_express, plotly_graph_objects, _df_fingerprint(), ExecutionResult, IPython-based stateful execution runner with output interception and Plotly… (+4 more)

### Community 37 - "ExportEngine"
Cohesion: 0.15
Nodes (8): ExportEngine, Any, Generate a Markdown Executive Summary report synthesizing the dataset profile,…, Generates downloadable artifacts from active session state., Export the active DataFrame snapshot in CSV, Parquet, or Excel format. Returns:…, Generate a corporate PowerPoint (.pptx) presentation deck. Returns:…, Generate a polished executive PDF brief using ReportLab. Returns: (file_bytes,…, Generate a fully reproducible Jupyter Notebook (.ipynb) containing setup cells,…

### Community 38 - "SqlWorkspace.tsx"
Cohesion: 0.14
Nodes (18): SchemaMapper(), SchemaMapperProps, UserJoinLink, SqlWorkspace(), SqlWorkspaceProps, VirtualDataTable(), VirtualDataTableProps, executeSql (+10 more)

### Community 39 - "automl.py"
Cohesion: 0.10
Nodes (25): ast, logging, detect_problem_type(), generate_python_code(), DataFrame, Autonomous AutoML Baseline Engine for Conversational Data Platform. Provides…, Synthesizes a clean, standalone, executable scikit-learn Python script., Detects whether target is binary, multiclass, or regression. (+17 more)

### Community 40 - "models.py"
Cohesion: 0.11
Nodes (32): ChatRequest, ChatTurnResponse, CodeExecutionRequest, CodeExecutionResponse, ColumnDiff, ColumnHealth, ColumnProfile, ConfusionMatrixData (+24 more)

### Community 41 - "DuckDBEngine"
Cohesion: 0.16
Nodes (14): DuckDBPyConnection, SqlQueryColumn, DuckDBEngine, Any, DbSession, Execute an analytical SQL query against session tables and checkpoints. Returns…, Execute a SQL statement and materialize the result into a new Parquet…, Sanitize filename into a valid SQL identifier (lowercase, alphanumeric +… (+6 more)

### Community 46 - "workspaces.py"
Cohesion: 0.10
Nodes (33): delete, patch, Request, get_auth_context(), Resolves the active tenant context (User + Workspace + Role). If…, ensure_default_seed(), Ensure default workspace and guest user exist for zero-friction fallback., User account model for authentication and identity. (+25 more)

### Community 47 - "FileUploadModal.tsx"
Cohesion: 0.60
Nodes (4): FileUploadModal(), FileUploadModalProps, uploadDataset(), FileUploadResponse

### Community 48 - "Session"
Cohesion: 0.17
Nodes (12): Conversational data analysis session., Session, Retrieve distinct profiles for all uploaded files/tables in the session., Infer foreign key links and join opportunities between all tables in the…, Create a new session record in the database., asyncio, fixture, Tests for Phase 5: Multi-Format Export Engine. (+4 more)

### Community 49 - "routers/auth.py"
Cohesion: 0.18
Nodes (22): AuthTokenResponse, RefreshTokenRequest, UserResponse, login(), logout(), post, Authentication router: Signup, Login, Token Refresh, Logout, and User Profile., Log in with email and password to receive access and refresh tokens. (+14 more)

### Community 50 - "test_auth.py"
Cohesion: 0.10
Nodes (22): bcrypt, hashlib, jwt, get_current_user_optional(), Extract and validate JWT Bearer token if present. Returns None if…, Secure database-backed refresh tokens supporting instant revocation., RefreshToken, decode_token() (+14 more)

### Community 51 - "database.py"
Cohesion: 0.15
Nodes (11): alembic, Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), listens_for, logging_config, Database configuration and session lifecycle management for services/api.… (+3 more)

### Community 52 - "infer_foreign_key_relations"
Cohesion: 0.29
Nodes (7): infer_foreign_key_relations(), Any, Heuristically infer potential foreign key / join relationships between tables…, Sanitize arbitrary Python/Pandas/Polars values for strict RFC 8259 JSON…, sanitize_value(), Verify that NaNs, Infs, dates, and numpy scalars are sanitized for RFC 8259…, test_sanitize_value_rfc_8259()

### Community 53 - "LocalSandboxClient"
Cohesion: 0.11
Nodes (10): argparse, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any, HTTP client communicating with the containerized sandbox runner., In-process sandbox client for rapid local testing without container… (+2 more)

### Community 54 - "SessionService"
Cohesion: 0.13
Nodes (16): BaseSandboxClient, ChatTurn, Individual analytical turn within a session., DataFrame, Path, Convert a local filesystem path to the equivalent container mount path if…, Save uploaded file, profile all tables, record in database, hydrate sandbox,…, Extract active DataFrame from sandbox, persist Parquet checkpoint, profile… (+8 more)

### Community 55 - "test_duckdb_sql.py"
Cohesion: 0.18
Nodes (11): fixture, Unit tests for the embedded DuckDB SQL Execution Engine & Checkpoint…, Create a session and ingest sample transactional data., Test standard SELECT query with aggregations on uploaded orders dataset., Test querying the active dataset checkpoint via df_active or df., Test creating a new DataFrame checkpoint directly from a SQL filter query., session_with_data(), setup_db() (+3 more)

### Community 56 - "post"
Cohesion: 0.12
Nodes (16): chat_with_data(), create_session(), execute_code(), execute_sql_query(), import_warehouse_dataset(), post, Create a new data analysis session scoped to the active workspace., Upload a tabular dataset (CSV, TSV, Parquet, Excel, JSON, SQLite).… (+8 more)

### Community 57 - "test_api_ingestion.py"
Cohesion: 0.13
Nodes (14): fixture, End-to-end integration tests for the API Gateway and Ingestion Flow…, Test state persistence across turns and Plotly figure interception via API., Ensure database tables exist before each test., Verify API health check endpoint., Test creating a new session and querying its metadata., Test uploading a CSV dataset, extracting schema, and querying schema endpoint., Test that uploaded data is automatically hydrated and accessible as `df`. (+6 more)

### Community 58 - "orchestrator.py"
Cohesion: 0.10
Nodes (24): asyncio, json, re, AgentOrchestrator, format_sse(), Any, Autonomous AI Analyst & Reflexion Orchestration Engine. Coordinates schema…, Synchronous non-streaming execution wrapper. Consumes the SSE stream and… (+16 more)

### Community 59 - "create_db_and_tables"
Cohesion: 0.20
Nodes (10): create_db_and_tables(), patch_sqlite_columns(), Initialize all registered SQLModel tables in the database and seed defaults., Safely add new columns to existing SQLite tables if missing., lifespan(), FastAPI, Application lifespan: initialize database tables upon startup., fixture (+2 more)

### Community 60 - "Imported Screens & Assets"
Cohesion: 0.20
Nodes (10): 1. Avatar Portrait of Fares (Tech Founder & Senior Data Analyst), 2. Gemini Insights & Automated Anomalies, 3. Gemini Ambient Spark Logo, 4. SQL & Deep Query Workspace, 5. Design System (Ambient Intelligence Workspace), 6. Conversational Analytics Canvas, 7. SQL Patch Remediation Modal, 8. Rollback Script & Snapshot Comparison (+2 more)

### Community 61 - "Sidebar.tsx"
Cohesion: 0.20
Nodes (17): AuthModal(), AuthModalProps, Sidebar(), SidebarProps, TeamDrawer(), TeamDrawerProps, authApi, clearStoredTokens() (+9 more)

### Community 62 - "main.py"
Cohesion: 0.09
Nodes (34): dotenv, fastapi_middleware_cors, services_api_connectors, export_session_data(), get_connectors_status(), get_dataset(), get_providers_status(), get_session() (+26 more)

### Community 63 - "test_multi_tenancy.py"
Cohesion: 0.18
Nodes (10): fastapi_testclient, fixture, Integration tests for Workspace Multi-Tenancy: Workspace isolation, session…, Verify Admin can invite new members and modify their role., Verify user can create multiple workspaces and list memberships., Verify sessions created in Workspace A are strictly invisible to Workspace B., setup_database(), test_cross_tenant_session_isolation() (+2 more)

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

### Community 74 - "AuthContext"
Cohesion: 0.21
Nodes (19): AuthContext, BaseModel, Execution context containing authenticated user, active workspace, and assigned…, ApplyHygieneRequest, ApplyHygieneResponse, AutoMLTrainRequest, AutoMLTrainResponse, CheckpointSummaryResponse (+11 more)

### Community 75 - "BigQueryConnector"
Cohesion: 0.24
Nodes (3): BigQueryConnector, Any, Google Cloud BigQuery warehouse connector.

### Community 76 - "pdf_engine.py"
Cohesion: 0.14
Nodes (11): reportlab_lib, reportlab_lib_pagesizes, reportlab_lib_styles, reportlab_lib_units, reportlab_pdfgen, reportlab_platypus, NumberedCanvas, PdfEngine (+3 more)

### Community 77 - "DataFrameCheckpoint"
Cohesion: 0.14
Nodes (13): DataFrameCheckpoint, Immutable copy-on-write snapshot of a DataFrame state., Deserialize stored profile., Serialize DataFrameProfile., sqlmodel_pool, mock_session_with_data(), fixture, Path (+5 more)

### Community 78 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 79 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_node_url, vite, @vitejs/plugin-react

### Community 80 - "api/auth.py"
Cohesion: 0.18
Nodes (9): fastapi, fastapi_security, get_current_user(), Authentication & Authorization dependencies for services/api. Implements JWT…, Dependency factory that enforces the RBAC role hierarchy. Usage:…, Strict authentication guard requiring a valid logged-in user., require_role(), get_db_session() (+1 more)

### Community 81 - "ReportsStudio.tsx"
Cohesion: 0.33
Nodes (6): ReportsStudio(), ReportsStudioProps, reportsApi, reportsPreviewQueryOptions(), DeckSlidePreview, lucide-react

### Community 83 - "test_rbac.py"
Cohesion: 0.29
Nodes (6): fixture, Integration tests for Tiered Role-Based Access Control (RBAC): Verifies that…, Verify viewer role is strictly forbidden from write/execute actions., setup_database(), test_viewer_role_execution_restrictions(), uuid

### Community 84 - ".apply_hygiene_remediation"
Cohesion: 0.40
Nodes (3): Any, Retrieve dataset rows and column definitions for a session checkpoint., Execute smart data hygiene remediation in sandbox, materialize a new versioned…

### Community 91 - "test_dataframe_versioning.py"
Cohesion: 0.28
Nodes (8): asyncio, fixture, Path, Tests for Phase 5: DataFrame Versioning, Checkpointing & Time-Travel Rollback., test_db(), test_incremental_checkpoint_on_dataframe_mutation(), test_initial_checkpoint_created_on_upload(), test_time_travel_rollback()

### Community 94 - "io"
Cohesion: 0.29
Nodes (6): io, fixture, Unit tests for Multi-File Relational Joins & Foreign Key Inference., Test uploading two relational tables (customers and orders), verifying foreign…, setup_db(), test_multi_file_relational_inference_and_join()

### Community 95 - "pytest"
Cohesion: 0.22
Nodes (8): pytest, fixture, Unit tests for BigQuery and Snowflake Cloud Warehouse Connectors., Test inspecting BigQuery and Snowflake connector statuses., Test importing a cloud warehouse dataset query into a session as a Parquet…, setup_db(), test_warehouse_connectors_status(), test_warehouse_import_to_session()

## Knowledge Gaps
- **233 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+228 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 620 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Session` connect `Session` to `session_service.py`, `api/diagnostics.py`, `.compute_schema_diff`, `deck_engine.py`, `ExportEngine`, `models.py`, `DuckDBEngine`, `workspaces.py`, `routers/auth.py`, `test_auth.py`, `database.py`, `SessionService`, `post`, `orchestrator.py`, `main.py`, `AuthContext`, `pdf_engine.py`, `DataFrameCheckpoint`, `api/auth.py`, `.apply_hygiene_remediation`, `test_dataframe_versioning.py`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `SandboxRunner` connect `SandboxRunner` to `server.py`, `client.py`, `LocalSandboxClient`, `runner.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `LocalSandboxClient` connect `LocalSandboxClient` to `session_service.py`, `runner.py`, `client.py`, `SandboxClient`, `SandboxRunner`, `SessionService`, `test_dataframe_versioning.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Session` (e.g. with `list_sessions()` and `verify_session_access()`) actually correct?**
  _`Session` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `AuthContext` (e.g. with `User` and `Workspace`) actually correct?**
  _`AuthContext` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `SessionService` (e.g. with `ChatTurn` and `CheckpointSummaryResponse`) actually correct?**
  _`SessionService` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `DataFrameProfile` (e.g. with `build_system_prompt()` and `format_schema_context()`) actually correct?**
  _`DataFrameProfile` has 7 INFERRED edges - model-reasoned connections that need verification._