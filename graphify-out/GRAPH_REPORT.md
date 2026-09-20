# Graph Report - Conversational_Data  (2026-09-20)

## Corpus Check
- 78 files · ~92,977 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 3, .example 1, .ini 1)

## Summary
- 1063 nodes · 1939 edges · 74 communities (57 shown, 17 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 137 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f9f6cee8`
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
- design_system/DESIGN_SYSTEM.md
- Any
- runner.py
- Session
- SqlWorkspace.tsx
- .execute
- models.py
- DuckDBEngine
- apps_web_src_app_globals
- apps_web_src_lib_api_resetsession
- subprocess
- urllib_request
- workspaces.py
- FileUploadModal.tsx
- test_dataframe_versioning.py
- routers/auth.py
- test_auth.py
- database.py
- infer_foreign_key_relations
- get
- api/auth.py
- pytest
- AuthContext
- test_api_ingestion.py
- session_with_data
- create_db_and_tables
- Imported Screens & Assets
- Sidebar.tsx
- main.py
- test_multi_tenancy.py
- DataFrameCheckpoint
- Components
- Components
- test_rbac.py
- import_warehouse_dataset
- Colors
- Colors
- Elevation & Depth
- Layout & Spacing
- routers/__init__.py

## God Nodes (most connected - your core abstractions)
1. `Session` - 68 edges
2. `DataFrameProfile` - 30 edges
3. `SessionService` - 30 edges
4. `AuthContext` - 23 edges
5. `SandboxClient` - 23 edges
6. `create_db_and_tables()` - 22 edges
7. `User` - 22 edges
8. `WorkspaceMember` - 20 edges
9. `profile_dataframe()` - 20 edges
10. `LocalSandboxClient` - 20 edges

## Surprising Connections (you probably didn't know these)
- `test_signup_creates_user_and_personal_workspace()` --uses--> `User`  [INFERRED]
  tests/test_auth.py → services/api/models.py
- `test_signup_creates_user_and_personal_workspace()` --uses--> `RefreshToken`  [INFERRED]
  tests/test_auth.py → services/api/models.py
- `Technical Stack:` --references--> `useChatStream()`  [INFERRED]
  apps/web/README.md → apps/web/src/hooks/useChatStream.ts
- `setup_database()` --calls--> `create_db_and_tables()`  [EXTRACTED]
  tests/test_agent_orchestrator.py → services/api/database.py
- `setup_database()` --calls--> `create_db_and_tables()`  [EXTRACTED]
  tests/test_api_ingestion.py → services/api/database.py

## Import Cycles
- None detected.

## Communities (74 total, 17 thin omitted)

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
Cohesion: 0.14
Nodes (22): chardet, csv, datetime, decimal, duckdb, math, os, pandas (+14 more)

### Community 5 - "server.py"
Cohesion: 0.18
Nodes (18): pydantic, CheckpointFileRequest, execute_code(), ExecuteRequest, ExecuteResponse, get_sandbox_state(), health_check(), HealthResponse (+10 more)

### Community 6 - "orchestrator.py"
Cohesion: 0.06
Nodes (39): asyncio, dotenv, json, AgentOrchestrator, format_sse(), Any, Autonomous AI Analyst & Reflexion Orchestration Engine. Coordinates schema…, Synchronous non-streaming execution wrapper. Consumes the SSE stream and… (+31 more)

### Community 7 - "SandboxClient"
Cohesion: 0.05
Nodes (37): argparse, httpx, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any, Client SDK for interacting with the sandbox execution engine. (+29 more)

### Community 8 - "test_profiler.py"
Cohesion: 0.13
Nodes (24): DataFrame, numpy, detect_encoding_and_delimiter(), generate_loader_code(), Path, Ingest a file of any supported format and return a dictionary of named…, Synthesize the optimal Python code snippet to hydrate the dataset into the…, Detect character encoding via chardet and sniff tabular delimiter. Falls back… (+16 more)

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
Cohesion: 0.08
Nodes (25): dependencies, clsx, lucide-react, @monaco-editor/react, plotly.js-dist-min, react, react-dom, react-plotly.js (+17 more)

### Community 24 - "DataFrameProfile"
Cohesion: 0.15
Nodes (12): Path, Path, DataFrameProfile, File uploaded and ingested into a session., Deserialize stored JSON profiles., Serialize DataFrameProfile list to JSON string., Structural schema profile of a loaded dataset (privacy-safe, no raw bulk data)., SessionFile (+4 more)

### Community 25 - "SessionService"
Cohesion: 0.10
Nodes (20): BaseSandboxClient, ChatTurn, ColumnDiff, Individual analytical turn within a session., SchemaDiff, Any, Path, Convert a local filesystem path to the equivalent container mount path if… (+12 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, baseUrl, esModuleInterop, isolatedModules, jsx, lib, module (+13 more)

### Community 27 - "BaseWarehouseConnector"
Cohesion: 0.06
Nodes (18): BaseWarehouseConnector, ABC, Any, Path, Abstract interface for external analytical data warehouse connections., Return True if required environment variables or credentials exist., Return connector health and configuration metadata., Verify network connectivity and credentials with the cloud warehouse. (+10 more)

### Community 28 - "router.tsx"
Cohesion: 0.09
Nodes (21): Sidebar(), SqlPatchModal(), SqlPatchModalProps, VersionHistoryView(), VersionHistoryViewProps, apps_web_src_lib_api_createsession, apps_web_src_lib_api_fetchcheckpoints, apps_web_src_lib_api_fetchdatasetdata (+13 more)

### Community 29 - "05_asset-st/DESIGN_SYSTEM.md"
Cohesion: 0.15
Nodes (12): Ambient Radiant Glows, Brand & Style, Core Tenets, Elevation & Depth, Geometric Application, Grid Models & Adaptive Behavior, Layout & Spacing, Shapes (+4 more)

### Community 30 - "package.json"
Cohesion: 0.07
Nodes (25): name, private, scripts, build, dev, lint, preview, type (+17 more)

### Community 31 - "react"
Cohesion: 0.14
Nodes (13): ActiveChatView(), ActiveChatViewProps, FloatingActionDock(), FloatingActionDockProps, Header(), HeaderProps, VisualizationStudio(), VisualizationStudioProps (+5 more)

### Community 32 - "useChatStream.ts"
Cohesion: 0.17
Nodes (11): UseChatStreamOptions, apps_web_src_index, apps_web_src_lib_queryclient, apps_web_src_lib_queryclient_queryclient, apps_web_src_lib_types_dataseteventpayload, apps_web_src_lib_types_reflexionstep, rootElement, router (+3 more)

### Community 34 - "design_system/DESIGN_SYSTEM.md"
Cohesion: 0.20
Nodes (8): Brand & Style, Core Tenets, Geometric Application, Shapes, Typographic Roles & Expressive Usage, Typography, Gemini Conversational Analytics Platform — Stitch Asset Catalog, Project Metadata

### Community 35 - "Any"
Cohesion: 0.17
Nodes (6): BaseException, Any, Inspect the current namespace variables and DataFrame dimensions., Atomically persist active 'df' to a Parquet file., Restore 'df' from a Parquet checkpoint file., Run code in the IPython shell while redirecting stdout and stderr.

### Community 36 - "runner.py"
Cohesion: 0.20
Nodes (9): ast, concurrent_futures, contextlib, ipython_core_interactiveshell, plotly_express, plotly_graph_objects, IPython-based stateful execution runner with output interception and Plotly…, time (+1 more)

### Community 37 - "Session"
Cohesion: 0.15
Nodes (9): delete, Generate a Markdown Executive Summary report synthesizing the dataset profile,…, Export the active DataFrame snapshot in CSV, Parquet, or Excel format. Returns:…, Generate a fully reproducible Jupyter Notebook (.ipynb) containing setup cells,…, Conversational data analysis session., Session, Remove a user from the workspace., remove_workspace_member() (+1 more)

### Community 38 - "SqlWorkspace.tsx"
Cohesion: 0.10
Nodes (18): SchemaMapper(), SchemaMapperProps, UserJoinLink, SqlWorkspace(), SqlWorkspaceProps, VirtualDataTable(), VirtualDataTableProps, apps_web_src_lib_api_executesql (+10 more)

### Community 39 - ".execute"
Cohesion: 0.33
Nodes (4): _df_fingerprint(), Execute a Python code string sequentially within the persistent IPython shell., Collect and serialize all Plotly figures generated in this execution turn., Generate a lightweight structural and content fingerprint of a DataFrame.

### Community 40 - "models.py"
Cohesion: 0.14
Nodes (24): execute_code(), execute_sql_query(), Execute arbitrary Python analytical code within the session's sandbox. Returns…, Non-destructively roll back the active DataFrame to a specified checkpoint…, Execute arbitrary analytical SQL on session datasets and checkpoints via…, revert_session_version(), ChatRequest, ChatTurnResponse (+16 more)

### Community 41 - "DuckDBEngine"
Cohesion: 0.16
Nodes (14): DuckDBPyConnection, SqlQueryColumn, DuckDBEngine, Any, DbSession, Execute an analytical SQL query against session tables and checkpoints. Returns…, Execute a SQL statement and materialize the result into a new Parquet…, Sanitize filename into a valid SQL identifier (lowercase, alphanumeric +… (+6 more)

### Community 46 - "workspaces.py"
Cohesion: 0.12
Nodes (30): patch, Request, get_auth_context(), Resolves the active tenant context (User + Workspace + Role). If…, ensure_default_seed(), Ensure default workspace and guest user exist for zero-friction fallback., User account model for authentication and identity., Multi-tenant workspace container for sessions and datasets. (+22 more)

### Community 47 - "FileUploadModal.tsx"
Cohesion: 0.40
Nodes (4): FileUploadModal(), FileUploadModalProps, apps_web_src_lib_api_uploaddataset, apps_web_src_lib_types_fileuploadresponse

### Community 48 - "test_dataframe_versioning.py"
Cohesion: 0.14
Nodes (16): sqlmodel_pool, asyncio, fixture, Path, Tests for Phase 5: DataFrame Versioning, Checkpointing & Time-Travel Rollback., test_db(), test_incremental_checkpoint_on_dataframe_mutation(), test_initial_checkpoint_created_on_upload() (+8 more)

### Community 49 - "routers/auth.py"
Cohesion: 0.17
Nodes (25): AuthTokenResponse, Secure database-backed refresh tokens supporting instant revocation., RefreshToken, RefreshTokenRequest, UserResponse, WorkspaceResponse, login(), logout() (+17 more)

### Community 50 - "test_auth.py"
Cohesion: 0.12
Nodes (18): bcrypt, hashlib, jwt, decode_token(), Any, Security and authentication utilities for data-speaker. Handles password…, Decode and validate a JWT token. Raises jwt.PyJWTError subclasses on failure., Verify a plaintext password against a stored bcrypt hash. (+10 more)

### Community 51 - "database.py"
Cohesion: 0.15
Nodes (11): alembic, Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), listens_for, logging_config, Database configuration and session lifecycle management for services/api.… (+3 more)

### Community 52 - "infer_foreign_key_relations"
Cohesion: 0.18
Nodes (9): infer_foreign_key_relations(), Any, Heuristically infer potential foreign key / join relationships between tables…, Sanitize arbitrary Python/Pandas/Polars values for strict RFC 8259 JSON…, sanitize_value(), Retrieve distinct profiles for all uploaded files/tables in the session., Infer foreign key links and join opportunities between all tables in the…, Verify that NaNs, Infs, dates, and numpy scalars are sanitized for RFC 8259… (+1 more)

### Community 53 - "get"
Cohesion: 0.15
Nodes (18): export_session_data(), get_connectors_status(), get_dataset(), get_providers_status(), get_session_dataset(), get_session_schema(), health_check(), list_sessions() (+10 more)

### Community 54 - "api/auth.py"
Cohesion: 0.15
Nodes (11): fastapi, fastapi_security, get_current_user(), get_current_user_optional(), Authentication & Authorization dependencies for services/api. Implements JWT…, Dependency factory that enforces the RBAC role hierarchy. Usage:…, Extract and validate JWT Bearer token if present. Returns None if…, Strict authentication guard requiring a valid logged-in user. (+3 more)

### Community 55 - "pytest"
Cohesion: 0.11
Nodes (18): fastapi_testclient, io, pytest, Unit tests for the embedded DuckDB SQL Execution Engine & Checkpoint…, Test standard SELECT query with aggregations on uploaded orders dataset., Test querying the active dataset checkpoint via df_active or df., Test creating a new DataFrame checkpoint directly from a SQL filter query., test_duckdb_materialize_checkpoint_from_sql() (+10 more)

### Community 56 - "AuthContext"
Cohesion: 0.15
Nodes (17): AuthContext, BaseModel, Execution context containing authenticated user, active workspace, and assigned…, chat_with_data(), create_session(), post, Create a new data analysis session scoped to the active workspace., Upload a tabular dataset (CSV, TSV, Parquet, Excel, JSON, SQLite).… (+9 more)

### Community 57 - "test_api_ingestion.py"
Cohesion: 0.13
Nodes (14): fixture, End-to-end integration tests for the API Gateway and Ingestion Flow…, Test state persistence across turns and Plotly figure interception via API., Ensure database tables exist before each test., Verify API health check endpoint., Test creating a new session and querying its metadata., Test uploading a CSV dataset, extracting schema, and querying schema endpoint., Test that uploaded data is automatically hydrated and accessible as `df`. (+6 more)

### Community 58 - "session_with_data"
Cohesion: 0.50
Nodes (4): fixture, Create a session and ingest sample transactional data., session_with_data(), setup_db()

### Community 59 - "create_db_and_tables"
Cohesion: 0.18
Nodes (11): create_db_and_tables(), patch_sqlite_columns(), Initialize all registered SQLModel tables in the database and seed defaults., Safely add new columns to existing SQLite tables if missing., fixture, Ensure clean schema and defaults for each test run., setup_database(), fixture (+3 more)

### Community 60 - "Imported Screens & Assets"
Cohesion: 0.20
Nodes (10): 1. Avatar Portrait of Fares (Tech Founder & Senior Data Analyst), 2. Gemini Insights & Automated Anomalies, 3. Gemini Ambient Spark Logo, 4. SQL & Deep Query Workspace, 5. Design System (Ambient Intelligence Workspace), 6. Conversational Analytics Canvas, 7. SQL Patch Remediation Modal, 8. Rollback Script & Snapshot Comparison (+2 more)

### Community 61 - "Sidebar.tsx"
Cohesion: 0.16
Nodes (19): AuthModal(), AuthModalProps, SidebarProps, TeamDrawer(), TeamDrawerProps, apps_web_src_lib_api, apps_web_src_lib_api_authapi, apps_web_src_lib_api_clearstoredtokens (+11 more)

### Community 62 - "main.py"
Cohesion: 0.15
Nodes (16): fastapi_middleware_cors, fastapi_responses, services_api_connectors, get_session(), get_session_table_relations(), lifespan(), list_session_checkpoints(), FastAPI (+8 more)

### Community 63 - "test_multi_tenancy.py"
Cohesion: 0.20
Nodes (9): fixture, Integration tests for Workspace Multi-Tenancy: Workspace isolation, session…, Verify Admin can invite new members and modify their role., Verify user can create multiple workspaces and list memberships., Verify sessions created in Workspace A are strictly invisible to Workspace B., setup_database(), test_cross_tenant_session_isolation(), test_invite_member_and_role_management() (+1 more)

### Community 64 - "DataFrameCheckpoint"
Cohesion: 0.25
Nodes (6): ExportEngine, Generates downloadable artifacts from active session state., DataFrameCheckpoint, Immutable copy-on-write snapshot of a DataFrame state., Deserialize stored profile., Serialize DataFrameProfile.

### Community 65 - "Components"
Cohesion: 0.29
Nodes (7): 1. Primary Prompt Input Bar, 2. Buttons, 3. Filter Chips & Model Switchers, 4. Conversational Cards & Response Bubbles, 5. Checkboxes & Radio Controls, 6. Responsive Collapsible Sidebar, Components

### Community 66 - "Components"
Cohesion: 0.29
Nodes (7): 1. Primary Prompt Input Bar, 2. Buttons, 3. Filter Chips & Model Switchers, 4. Conversational Cards & Response Bubbles, 5. Checkboxes & Radio Controls, 6. Responsive Collapsible Sidebar, Components

### Community 67 - "test_rbac.py"
Cohesion: 0.29
Nodes (6): fixture, Integration tests for Tiered Role-Based Access Control (RBAC): Verifies that…, Verify viewer role is strictly forbidden from write/execute actions., setup_database(), test_viewer_role_execution_restrictions(), uuid

### Community 68 - "import_warehouse_dataset"
Cohesion: 0.40
Nodes (5): import_warehouse_dataset(), Execute an analytical query against a cloud warehouse (BigQuery, Snowflake),…, FileUploadResponse, clean_table_name(), Normalize a filename or table name into a valid Python identifier.

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

## Knowledge Gaps
- **222 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+217 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 567 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Session` connect `Session` to `session_service.py`, `import_warehouse_dataset`, `orchestrator.py`, `models.py`, `DuckDBEngine`, `workspaces.py`, `test_dataframe_versioning.py`, `routers/auth.py`, `test_auth.py`, `database.py`, `infer_foreign_key_relations`, `get`, `api/auth.py`, `AuthContext`, `SessionService`, `main.py`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `LocalSandboxClient` connect `SandboxClient` to `test_dataframe_versioning.py`, `SessionService`, `session_service.py`, `SandboxRunner`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `DataFrameProfile` connect `DataFrameProfile` to `DataFrameCheckpoint`, `session_service.py`, `orchestrator.py`, `models.py`, `infer_foreign_key_relations`, `SessionService`, `BaseWarehouseConnector`, `main.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Session` (e.g. with `list_sessions()` and `SessionService`) actually correct?**
  _`Session` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `DataFrameProfile` (e.g. with `build_system_prompt()` and `format_schema_context()`) actually correct?**
  _`DataFrameProfile` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `SessionService` (e.g. with `ChatTurn` and `CheckpointSummaryResponse`) actually correct?**
  _`SessionService` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `AuthContext` (e.g. with `User` and `Workspace`) actually correct?**
  _`AuthContext` has 17 INFERRED edges - model-reasoned connections that need verification._