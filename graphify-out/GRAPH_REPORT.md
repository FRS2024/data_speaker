# Graph Report - Conversational_Data  (2026-09-24)

## Corpus Check
- 110 files · ~126,078 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 3, .example 1, .ini 1)

## Summary
- 1526 nodes · 3173 edges · 95 communities (77 shown, 18 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 226 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d0159eae`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SYSTEM ARCHITECTURE & DESIGN DOCUMENT
- TECHNICAL REQUIREMENTS DOCUMENT (TRD)
- Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)
- PRODUCT REQUIREMENTS DOCUMENT (PRD)
- pdf_engine.py
- server.py
- typing
- SandboxClient
- profiler.py
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
- test_duckdb_sql.py
- Session
- compilerOptions
- postgres.py
- api.ts
- 05_asset-st/DESIGN_SYSTEM.md
- package.json
- router.tsx
- react
- design_system/DESIGN_SYSTEM.md
- deck_engine.py
- runner.py
- env.py
- SqlWorkspace.tsx
- automl.py
- workspaces.py
- DuckDBEngine
- apps_web_src_app_globals
- apps_web_src_lib_api_resetsession
- subprocess
- urllib_request
- database.py
- FileUploadModal.tsx
- AuthContext
- routers/auth.py
- MockProvider
- test_warehouse_studio.py
- post
- LocalSandboxClient
- SessionService
- create_db_and_tables
- .get_or_create_sandbox_client
- test_api_ingestion.py
- StatisticianCritic
- test_audio_service.py
- Imported Screens & Assets
- Sidebar.tsx
- main.py
- models.py
- DataFrameProfile
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
- NumberedCanvas
- DataFrameCheckpoint
- scripts
- vite.config.ts
- ExecutionResult
- AudioService
- tailwind.config.ts
- DiagnosticsStudio.tsx
- PostgreSQLConnector
- DatabricksConnector
- test_diagnostics.py
- .get_session
- .get_config
- .ingest_file
- test_export_engine.py
- compute_correlation_matrix
- session_service.py
- BaseWarehouseConnector
- get_me

## God Nodes (most connected - your core abstractions)
1. `Session` - 109 edges
2. `AuthContext` - 49 edges
3. `DataFrameProfile` - 37 edges
4. `SessionService` - 33 edges
5. `create_db_and_tables()` - 28 edges
6. `react` - 27 edges
7. `DataFrameCheckpoint` - 24 edges
8. `profile_dataframe()` - 24 edges
9. `SandboxClient` - 23 edges
10. `User` - 22 edges

## Surprising Connections (you probably didn't know these)
- `test_signup_creates_user_and_personal_workspace()` --uses--> `User`  [INFERRED]
  tests/test_auth.py → services/api/models.py
- `mock_session_with_data()` --uses--> `Session`  [INFERRED]
  tests/test_deck_engine.py → services/api/models.py
- `mock_session_with_data()` --uses--> `Session`  [INFERRED]
  tests/test_pdf_engine.py → services/api/models.py
- `test_swarm_mode_sync_execution()` --uses--> `ChatTurn`  [INFERRED]
  tests/test_swarm_orchestrator.py → services/api/models.py
- `mock_session_with_data()` --uses--> `DataFrameCheckpoint`  [INFERRED]
  tests/test_deck_engine.py → services/api/models.py

## Import Cycles
- None detected.

## Communities (95 total, 18 thin omitted)

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

### Community 4 - "pdf_engine.py"
Cohesion: 0.18
Nodes (9): reportlab_lib, reportlab_lib_pagesizes, reportlab_lib_styles, reportlab_lib_units, reportlab_pdfgen, reportlab_platypus, PdfEngine, Executive PDF Brief Compiler for Track C Executive Report & Presentation… (+1 more)

### Community 5 - "server.py"
Cohesion: 0.18
Nodes (18): pydantic, CheckpointFileRequest, execute_code(), ExecuteRequest, ExecuteResponse, get_sandbox_state(), health_check(), HealthResponse (+10 more)

### Community 6 - "typing"
Cohesion: 0.09
Nodes (35): json, re, Statistician & Critic Agent for Track D Multi-Agent Swarm. Performs two-stage…, AgentOrchestrator, format_sse(), Any, Autonomous AI Analyst & Reflexion Orchestration Engine. Coordinates schema…, Synchronous non-streaming execution wrapper. Consumes the SSE stream and… (+27 more)

### Community 7 - "SandboxClient"
Cohesion: 0.10
Nodes (20): Base interface for sandbox interaction., SandboxClient, client(), fixture, Comprehensive test suite verifying the stateful execution sandbox engine., Verify that runaway or infinite loops are halted cleanly at the timeout…, Verify that reset clears custom variables while keeping baseline imports…, Verify that variable state survives sequential execution turns. (+12 more)

### Community 8 - "profiler.py"
Cohesion: 0.08
Nodes (38): chardet, csv, detect_encoding_and_delimiter(), generate_loader_code(), infer_foreign_key_relations(), profile_dataframe(), Any, DataFrame (+30 more)

### Community 9 - "SandboxRunner"
Cohesion: 0.16
Nodes (8): BaseException, Hook into figure display calls to capture Plotly figures without a GUI., Reset the execution namespace, flushing variables while keeping baseline…, Run code in the IPython shell while redirecting stdout and stderr., Maintains a persistent, stateful IPython session for executing data science…, Instantiate and configure the persistent IPython InteractiveShell., Pre-populate the namespace with standard analytical packages and baseline…, SandboxRunner

### Community 10 - "test_agent_orchestrator.py"
Cohesion: 0.11
Nodes (18): fixture, Automated test suite for Phase 3: Autonomous AI Analyst & Reflexion Loop.…, Test real-time Server-Sent Events (SSE) streaming format and event multiplexing., Test SQL query execution through chat interface with DuckDB scanning df_active., Verify code execution in a fresh session with no uploaded file has df and…, Ensure database tables exist before each test., Create a session and upload a sample employee dataset., Test standard single-turn analytical query returning synchronous JSON. (+10 more)

### Community 14 - "api/diagnostics.py"
Cohesion: 0.31
Nodes (9): scipy, compute_data_health(), Autonomous Diagnostic Engine for Conversational Data Platform. Provides data…, Computes a multi-dimensional health score (0-100) and actionable hygiene…, ColumnHealth, DataHealthResponse, HealthScoreBreakdown, HygieneRecommendation (+1 more)

### Community 22 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, clsx, lucide-react, @monaco-editor/react, plotly.js-dist-min, react, react-dom, react-plotly.js (+6 more)

### Community 23 - "types.ts"
Cohesion: 0.08
Nodes (23): AnomalyAttribution, AnomalyRecord, ColumnDiff, ColumnHealth, ColumnProfile, ConfusionMatrixData, ConnectorsStatusResponse, CorrelationPair (+15 more)

### Community 24 - "test_duckdb_sql.py"
Cohesion: 0.18
Nodes (11): fixture, Unit tests for the embedded DuckDB SQL Execution Engine & Checkpoint…, Create a session and ingest sample transactional data., Test standard SELECT query with aggregations on uploaded orders dataset., Test querying the active dataset checkpoint via df_active or df., Test creating a new DataFrame checkpoint directly from a SQL filter query., session_with_data(), setup_db() (+3 more)

### Community 25 - "Session"
Cohesion: 0.10
Nodes (27): fastapi_responses, logging, Dependency factory that enforces the RBAC role hierarchy. Usage:…, require_role(), Conversational data analysis session., Session, export_pdf(), export_pptx() (+19 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, baseUrl, esModuleInterop, isolatedModules, jsx, lib, module (+13 more)

### Community 27 - "postgres.py"
Cohesion: 0.16
Nodes (13): numpy, os, polars, Voice & Audio Interaction Service for Track E. Handles speech-to-text audio…, ABC, Base interface and abstractions for external cloud data warehouse connectors.…, Google Cloud BigQuery Connector for data_speaker. Supports schema discovery,…, Databricks Lakehouse Connector for data_speaker. Supports Unity Catalog, Delta… (+5 more)

### Community 28 - "api.ts"
Cohesion: 0.08
Nodes (43): WarehouseStudio(), WarehouseStudioProps, authFetch(), checkpointsQueryOptions(), createSession(), executeCode(), executeSqlQuery(), fetchCheckpoints() (+35 more)

### Community 29 - "05_asset-st/DESIGN_SYSTEM.md"
Cohesion: 0.15
Nodes (12): Ambient Radiant Glows, Brand & Style, Core Tenets, Elevation & Depth, Geometric Application, Grid Models & Adaptive Behavior, Layout & Spacing, Shapes (+4 more)

### Community 30 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, type, version, autoprefixer, clsx, plotly.js-dist-min, postcss (+7 more)

### Community 31 - "router.tsx"
Cohesion: 0.07
Nodes (29): Technical Stack:, Web Application Client (`apps/web`), Header(), HeaderProps, SqlPatchModal(), SqlPatchModalProps, VersionHistoryView(), VersionHistoryViewProps (+21 more)

### Community 32 - "react"
Cohesion: 0.10
Nodes (28): ActiveChatView(), ActiveChatViewProps, AudioWaveVisualizer(), AudioWaveVisualizerProps, FloatingActionDock(), FloatingActionDockProps, StatisticalPeerReviewCard(), StatisticalPeerReviewCardProps (+20 more)

### Community 34 - "design_system/DESIGN_SYSTEM.md"
Cohesion: 0.20
Nodes (8): Brand & Style, Core Tenets, Geometric Application, Shapes, Typographic Roles & Expressive Usage, Typography, Gemini Conversational Analytics Platform — Stitch Asset Catalog, Project Metadata

### Community 35 - "deck_engine.py"
Cohesion: 0.07
Nodes (33): Inches, matplotlib, matplotlib_pyplot, pptx, pptx_chart_data, pptx_dml_color, pptx_enum_chart, pptx_enum_shapes (+25 more)

### Community 36 - "runner.py"
Cohesion: 0.13
Nodes (12): ast, concurrent_futures, contextlib, ipython_core_interactiveshell, plotly_express, plotly_graph_objects, _df_fingerprint(), IPython-based stateful execution runner with output interception and Plotly… (+4 more)

### Community 37 - "env.py"
Cohesion: 0.20
Nodes (7): alembic, Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), logging_config, sqlalchemy

### Community 38 - "SqlWorkspace.tsx"
Cohesion: 0.10
Nodes (24): ReportsStudio(), ReportsStudioProps, SchemaMapper(), SchemaMapperProps, UserJoinLink, SqlWorkspace(), SqlWorkspaceProps, VirtualDataTable() (+16 more)

### Community 39 - "automl.py"
Cohesion: 0.10
Nodes (27): detect_problem_type(), generate_python_code(), DataFrame, Autonomous AutoML Baseline Engine for Conversational Data Platform. Provides…, Synthesizes a clean, standalone, executable scikit-learn Python script., Detects whether target is binary, multiclass, or regression., Executes fast-bounded multi-model training, scoring, feature importance, and…, run_automl() (+19 more)

### Community 40 - "workspaces.py"
Cohesion: 0.10
Nodes (32): fastapi, fastapi_security, patch, Request, get_auth_context(), get_current_user(), get_current_user_optional(), Authentication & Authorization dependencies for services/api. Implements JWT… (+24 more)

### Community 41 - "DuckDBEngine"
Cohesion: 0.16
Nodes (14): DuckDBPyConnection, SqlQueryColumn, DuckDBEngine, Any, DbSession, Execute an analytical SQL query against session tables and checkpoints. Returns…, Execute a SQL statement and materialize the result into a new Parquet…, Sanitize filename into a valid SQL identifier (lowercase, alphanumeric +… (+6 more)

### Community 46 - "database.py"
Cohesion: 0.08
Nodes (31): listens_for, ensure_default_seed(), get_db_session(), Database configuration and session lifecycle management for services/api.…, FastAPI dependency for database session injection., Ensure default workspace and guest user exist for zero-friction fallback., set_sqlite_pragma(), Secure database-backed refresh tokens supporting instant revocation. (+23 more)

### Community 47 - "FileUploadModal.tsx"
Cohesion: 0.60
Nodes (4): FileUploadModal(), FileUploadModalProps, uploadDataset(), FileUploadResponse

### Community 48 - "AuthContext"
Cohesion: 0.10
Nodes (35): AuthContext, BaseModel, Execution context containing authenticated user, active workspace, and assigned…, Secure workspace-scoped warehouse connection configuration., WarehouseConfigResponse, WarehouseConnectionConfig, WarehouseSyncRequest, WarehouseTablePreviewResponse (+27 more)

### Community 49 - "routers/auth.py"
Cohesion: 0.12
Nodes (32): bcrypt, hashlib, jwt, AuthTokenResponse, RefreshTokenRequest, UserResponse, WorkspaceResponse, login() (+24 more)

### Community 50 - "MockProvider"
Cohesion: 0.09
Nodes (16): AnthropicProvider, GeminiProvider, MockProvider, OpenAIProvider, Any, Google Gemini client powered by the official google-genai SDK. Supports native…, Represents a structured tool call emitted by an LLM., OpenAI API client supporting native function calling and token streaming. (+8 more)

### Community 51 - "test_warehouse_studio.py"
Cohesion: 0.10
Nodes (19): fixture, Integration & Unit tests for Track F: Enterprise Warehouse & Lakehouse…, Verify listing schemas and tables across connectors., Verify live table preview with column dtypes and rows., Verify one-click table sync streaming into a session Parquet dataset., Verify pushdown SQL query execution into a session dataset., Verify all 4 connectors in quadrant are returned with metadata., Verify connection ping tests for all connector types. (+11 more)

### Community 52 - "post"
Cohesion: 0.09
Nodes (23): Response, chat_with_data(), create_session(), execute_code(), execute_sql_query(), generate_executive_recap_endpoint(), import_warehouse_dataset(), post (+15 more)

### Community 53 - "LocalSandboxClient"
Cohesion: 0.14
Nodes (10): argparse, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any, HTTP client communicating with the containerized sandbox runner., In-process sandbox client for rapid local testing without container… (+2 more)

### Community 54 - "SessionService"
Cohesion: 0.17
Nodes (9): ColumnDiff, SchemaDiff, Calculate row/column deltas and column modifications between two versions., Fetch all checkpoints for a session with calculated schema diffs., Orchestrates sessions, sandbox execution kernels, and dataset persistence., Retrieve distinct profiles for all uploaded files/tables in the session., Infer foreign key links and join opportunities between all tables in the…, Create a new session record in the database. (+1 more)

### Community 55 - "create_db_and_tables"
Cohesion: 0.06
Nodes (37): fastapi_testclient, io, pytest, create_db_and_tables(), patch_sqlite_columns(), Initialize all registered SQLModel tables in the database and seed defaults., Safely add new columns to existing SQLite tables if missing., fixture (+29 more)

### Community 56 - ".get_or_create_sandbox_client"
Cohesion: 0.24
Nodes (6): BaseSandboxClient, Extract active DataFrame from sandbox, persist Parquet checkpoint, profile…, Verify that the sandbox kernel has an active dataset loaded in memory. If…, Execute arbitrary Python analytical code inside the session's sandbox. Records…, Get or initialize a sandbox client for the given session. Uses…, Execute smart data hygiene remediation in sandbox, materialize a new versioned…

### Community 57 - "test_api_ingestion.py"
Cohesion: 0.13
Nodes (14): fixture, End-to-end integration tests for the API Gateway and Ingestion Flow…, Test state persistence across turns and Plotly figure interception via API., Ensure database tables exist before each test., Verify API health check endpoint., Test creating a new session and querying its metadata., Test uploading a CSV dataset, extracting schema, and querying schema endpoint., Test that uploaded data is automatically hydrated and accessible as `df`. (+6 more)

### Community 58 - "StatisticianCritic"
Cohesion: 0.10
Nodes (26): Any, DataFrame, Deep post-execution audit inspecting numeric values, sample sizes, and output…, Rigorous statistical reviewer that audits code and outputs before user delivery., Static AST and heuristic scan of Python code prior to sandbox execution.…, StatisticianCritic, CriticReview, critic() (+18 more)

### Community 59 - "test_audio_service.py"
Cohesion: 0.09
Nodes (22): asyncio, fixture, Automated test suite for Track E: Voice & Audio Interaction Engine. Validates…, POST /api/v1/audio/recap returns natural 20-second executive audio script., POST /api/v1/audio/synthesize returns streaming audio/wav bytes., Ensure database tables exist before each test., Generate mock 1-second 16kHz mono WAV audio bytes for testing., Empty audio payload returns 0 duration and empty text. (+14 more)

### Community 60 - "Imported Screens & Assets"
Cohesion: 0.20
Nodes (10): 1. Avatar Portrait of Fares (Tech Founder & Senior Data Analyst), 2. Gemini Insights & Automated Anomalies, 3. Gemini Ambient Spark Logo, 4. SQL & Deep Query Workspace, 5. Design System (Ambient Intelligence Workspace), 6. Conversational Analytics Canvas, 7. SQL Patch Remediation Modal, 8. Rollback Script & Snapshot Comparison (+2 more)

### Community 61 - "Sidebar.tsx"
Cohesion: 0.20
Nodes (17): AuthModal(), AuthModalProps, Sidebar(), SidebarProps, TeamDrawer(), TeamDrawerProps, authApi, clearStoredTokens() (+9 more)

### Community 62 - "main.py"
Cohesion: 0.09
Nodes (35): dotenv, fastapi_middleware_cors, services_api_connectors, export_session_data(), get_connectors_status(), get_dataset(), get_providers_status(), get_session() (+27 more)

### Community 63 - "models.py"
Cohesion: 0.09
Nodes (40): AIPolishRequest, AIPolishResponse, AnomalyAttribution, AnomalyRecord, AudioTranscribeResponse, ChatRequest, ChatTurnResponse, CheckpointSummaryResponse (+32 more)

### Community 64 - "DataFrameProfile"
Cohesion: 0.15
Nodes (8): Any, Path, Snowflake Data Cloud analytical connector., SnowflakeConnector, DataFrameProfile, Deserialize stored JSON profiles., Serialize DataFrameProfile list to JSON string., Structural schema profile of a loaded dataset (privacy-safe, no raw bulk data).

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
Cohesion: 0.25
Nodes (13): compute_anomalies(), Performs unsupervised multivariate anomaly detection with Isolation Forest plus…, AnomalyReportResponse, ApplyHygieneRequest, ApplyHygieneResponse, AutoMLTrainRequest, apply_hygiene_fix(), get_session_anomalies() (+5 more)

### Community 75 - "BigQueryConnector"
Cohesion: 0.24
Nodes (4): BigQueryConnector, Any, Path, Google Cloud BigQuery warehouse connector.

### Community 77 - "DataFrameCheckpoint"
Cohesion: 0.14
Nodes (13): DataFrameCheckpoint, Immutable copy-on-write snapshot of a DataFrame state., Deserialize stored profile., Serialize DataFrameProfile., sqlmodel_pool, mock_session_with_data(), fixture, Path (+5 more)

### Community 78 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 79 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_node_url, vite, @vitejs/plugin-react

### Community 80 - "ExecutionResult"
Cohesion: 0.15
Nodes (6): ExecutionResult, Any, Inspect the current namespace variables and DataFrame dimensions., Atomically persist active 'df' to a Parquet file., Restore 'df' from a Parquet checkpoint file., Encapsulates the output of a code execution turn.

### Community 81 - "AudioService"
Cohesion: 0.22
Nodes (6): AudioService, Any, Distill raw analytical output and tables into a conversational, high-impact…, Synthesize audio speech for given text into standard WAV format. Generates a…, Core audio processing and voice synthesis service., Transcribe audio recording to text. Supports WebM, WAV, MP3, and OGG formats…

### Community 83 - "DiagnosticsStudio.tsx"
Cohesion: 0.21
Nodes (12): DiagnosticsStudio(), DiagnosticsStudioProps, diagnosticsAnomaliesQueryOptions(), diagnosticsApi, diagnosticsCorrelationsQueryOptions(), diagnosticsHealthQueryOptions(), schemaQueryOptions(), AnomalyReportResponse (+4 more)

### Community 84 - "PostgreSQLConnector"
Cohesion: 0.31
Nodes (4): PostgreSQLConnector, Any, Path, PostgreSQL analytical & transactional connector.

### Community 85 - "DatabricksConnector"
Cohesion: 0.24
Nodes (4): DatabricksConnector, Any, Path, Databricks Lakehouse and Unity Catalog connector.

### Community 86 - "test_diagnostics.py"
Cohesion: 0.20
Nodes (9): Unit and integration tests for Autonomous Diagnostic Engine (Track B). Tests…, A pristine dataset should receive a near-100% health score and 0 critical…, A dataset with missing values, duplicate rows, and constant columns triggers…, Verifies Pearson and Spearman correlation matrices and top ranked pairs., Verifies unsupervised anomaly detection flags injected extreme outliers with…, test_clean_dataframe_health(), test_correlation_matrix_computation(), test_dirty_dataframe_health_and_recommendations() (+1 more)

### Community 87 - ".get_session"
Cohesion: 0.22
Nodes (5): Any, DataFrame, Retrieve all registered DataFrameProfiles for the session., Retrieve dataset rows and column definitions for a session checkpoint., Load the active DataFrame into pandas for diagnostics and AutoML.

### Community 88 - ".get_config"
Cohesion: 0.50
Nodes (3): Any, Deserialize config_json to dictionary., Return config with sensitive keys (passwords, tokens, keys) masked.

### Community 89 - ".ingest_file"
Cohesion: 0.22
Nodes (5): Path, Convert a local filesystem path to the equivalent container mount path if…, Save uploaded file, profile all tables, record in database, hydrate sandbox,…, Revert the session's active DataFrame to a previous checkpoint. Non-…, Reset session: clean up checkpoints except df_v0, reset sandbox, and rehydrate…

### Community 90 - "test_export_engine.py"
Cohesion: 0.32
Nodes (7): asyncio, fixture, Tests for Phase 5: Multi-Format Export Engine., test_dataset_exports(), test_db(), test_executive_report_export(), test_jupyter_notebook_export()

### Community 91 - "compute_correlation_matrix"
Cohesion: 0.40
Nodes (6): compute_correlation_matrix(), DataFrame, Computes Pearson (linear) and Spearman (rank) correlation matrices for numeric…, CorrelationMatrixResponse, get_session_correlations(), get

### Community 92 - "session_service.py"
Cohesion: 0.10
Nodes (21): asyncio, datetime, decimal, duckdb, math, pandas, pathlib, ExportEngine (+13 more)

### Community 93 - "BaseWarehouseConnector"
Cohesion: 0.13
Nodes (11): BaseWarehouseConnector, Any, Path, Abstract interface for external analytical data warehouse connections., Return True if required environment variables or credentials exist., Return connector health and configuration metadata., Verify network connectivity and credentials with the cloud warehouse., List accessible datasets or databases. (+3 more)

### Community 94 - "get_me"
Cohesion: 0.50
Nodes (4): get_me(), Any, get, Return user profile and all workspace memberships with roles.

## Knowledge Gaps
- **242 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+237 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 707 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Session` connect `Session` to `pdf_engine.py`, `typing`, `api/diagnostics.py`, `deck_engine.py`, `workspaces.py`, `DuckDBEngine`, `database.py`, `AuthContext`, `routers/auth.py`, `post`, `SessionService`, `.get_or_create_sandbox_client`, `main.py`, `models.py`, `routers/diagnostics.py`, `DataFrameCheckpoint`, `.get_session`, `.ingest_file`, `test_export_engine.py`, `compute_correlation_matrix`, `session_service.py`, `get_me`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `DataFrameProfile` connect `DataFrameProfile` to `typing`, `profiler.py`, `BigQueryConnector`, `DataFrameCheckpoint`, `PostgreSQLConnector`, `DatabricksConnector`, `SessionService`, `.get_session`, `.get_or_create_sandbox_client`, `.ingest_file`, `postgres.py`, `session_service.py`, `BaseWarehouseConnector`, `main.py`, `models.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `DatabricksConnector` connect `DatabricksConnector` to `DataFrameProfile`, `postgres.py`, `BaseWarehouseConnector`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Session` (e.g. with `list_sessions()` and `verify_session_access()`) actually correct?**
  _`Session` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 40 inferred relationships involving `AuthContext` (e.g. with `User` and `Workspace`) actually correct?**
  _`AuthContext` has 40 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DataFrameProfile` (e.g. with `build_system_prompt()` and `format_schema_context()`) actually correct?**
  _`DataFrameProfile` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `version`, `private` to the rest of the system?**
  _242 weakly-connected nodes found - possible documentation gaps or missing edges._