# Graph Report - Conversational_Data  (2026-09-23)

## Corpus Check
- 110 files · ~125,122 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 3, .example 1, .ini 1)

## Summary
- 1517 nodes · 3156 edges · 93 communities (74 shown, 19 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 225 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8754dd99`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SYSTEM ARCHITECTURE & DESIGN DOCUMENT
- TECHNICAL REQUIREMENTS DOCUMENT (TRD)
- Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)
- PRODUCT REQUIREMENTS DOCUMENT (PRD)
- pdf_engine.py
- server.py
- swarm.py
- test_sandbox_runner.py
- profile_dataframe
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
- .set_profile
- AuthContext
- compilerOptions
- session_service.py
- api.ts
- 05_asset-st/DESIGN_SYSTEM.md
- package.json
- router.tsx
- react
- design_system/DESIGN_SYSTEM.md
- DeckEngine
- runner.py
- api/auth.py
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
- models.py
- routers/auth.py
- MockProvider
- test_warehouse_studio.py
- post
- SandboxClient
- SessionService
- create_db_and_tables
- main.py
- test_api_ingestion.py
- StatisticianCritic
- test_audio_service.py
- Imported Screens & Assets
- Sidebar.tsx
- get
- BaseModel
- SnowflakeConnector
- Components
- Components
- devDependencies
- test_live_docker.py
- Colors
- Colors
- Elevation & Depth
- Layout & Spacing
- routers/__init__.py
- routers/diagnostics.py
- BigQueryConnector
- NumberedCanvas
- test_dataframe_versioning.py
- scripts
- vite.config.ts
- ExecutionResult
- AudioService
- tailwind.config.ts
- DiagnosticsStudio.tsx
- PostgreSQLConnector
- DatabricksConnector
- sql_engine.py
- deck_engine.py
- .get_config
- SessionRelationsResponse
- test_deck_engine.py
- Session
- Any

## God Nodes (most connected - your core abstractions)
1. `Session` - 108 edges
2. `AuthContext` - 49 edges
3. `DataFrameProfile` - 37 edges
4. `SessionService` - 32 edges
5. `create_db_and_tables()` - 28 edges
6. `react` - 27 edges
7. `DataFrameCheckpoint` - 24 edges
8. `profile_dataframe()` - 24 edges
9. `SandboxClient` - 23 edges
10. `User` - 22 edges

## Surprising Connections (you probably didn't know these)
- `test_signup_creates_user_and_personal_workspace()` --uses--> `RefreshToken`  [INFERRED]
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

## Communities (93 total, 19 thin omitted)

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
Cohesion: 0.12
Nodes (15): reportlab_lib, reportlab_lib_pagesizes, reportlab_lib_styles, reportlab_lib_units, reportlab_pdfgen, reportlab_platypus, compute_correlation_matrix(), DataFrame (+7 more)

### Community 5 - "server.py"
Cohesion: 0.20
Nodes (17): CheckpointFileRequest, execute_code(), ExecuteRequest, ExecuteResponse, get_sandbox_state(), health_check(), HealthResponse, lifespan() (+9 more)

### Community 6 - "swarm.py"
Cohesion: 0.09
Nodes (32): asyncio, AgentOrchestrator, format_sse(), Any, Autonomous AI Analyst & Reflexion Orchestration Engine. Coordinates schema…, Synchronous non-streaming execution wrapper. Consumes the SSE stream and…, Format structured payload into a Server-Sent Event (SSE) frame., Orchestrates multi-turn analytical reasoning, code generation, and Reflexion. (+24 more)

### Community 7 - "test_sandbox_runner.py"
Cohesion: 0.11
Nodes (18): client(), fixture, Comprehensive test suite verifying the stateful execution sandbox engine., Verify that runaway or infinite loops are halted cleanly at the timeout…, Verify that reset clears custom variables while keeping baseline imports…, Verify that variable state survives sequential execution turns., Verify that DataFrames persist and shape mutations are tracked accurately., Verify that Plotly figures created and shown via fig.show() are intercepted. (+10 more)

### Community 8 - "profile_dataframe"
Cohesion: 0.10
Nodes (31): detect_encoding_and_delimiter(), generate_loader_code(), profile_dataframe(), Any, DataFrame, Path, Ingest a file of any supported format and return a dictionary of named…, Extract a comprehensive, privacy-compliant schema profile from a Polars… (+23 more)

### Community 9 - "SandboxRunner"
Cohesion: 0.17
Nodes (7): Hook into figure display calls to capture Plotly figures without a GUI., Reset the execution namespace, flushing variables while keeping baseline…, Atomically persist active 'df' to a Parquet file., Maintains a persistent, stateful IPython session for executing data science…, Instantiate and configure the persistent IPython InteractiveShell., Pre-populate the namespace with standard analytical packages., SandboxRunner

### Community 10 - "test_agent_orchestrator.py"
Cohesion: 0.14
Nodes (14): fixture, Automated test suite for Phase 3: Autonomous AI Analyst & Reflexion Loop.…, Test real-time Server-Sent Events (SSE) streaming format and event multiplexing., Ensure database tables exist before each test., Create a session and upload a sample employee dataset., Test standard single-turn analytical query returning synchronous JSON., Test that chart requests produce interactive Plotly specifications., Test the Reflexion loop: 1. Attempt 1 triggers a KeyError… (+6 more)

### Community 14 - "api/diagnostics.py"
Cohesion: 0.15
Nodes (19): scipy, compute_anomalies(), compute_data_health(), Autonomous Diagnostic Engine for Conversational Data Platform. Provides data…, Computes a multi-dimensional health score (0-100) and actionable hygiene…, Performs unsupervised multivariate anomaly detection with Isolation Forest plus…, AnomalyAttribution, AnomalyRecord (+11 more)

### Community 22 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, clsx, lucide-react, @monaco-editor/react, plotly.js-dist-min, react, react-dom, react-plotly.js (+6 more)

### Community 23 - "types.ts"
Cohesion: 0.08
Nodes (23): AnomalyAttribution, AnomalyRecord, ColumnDiff, ColumnHealth, ColumnProfile, ConfusionMatrixData, ConnectorsStatusResponse, CorrelationPair (+15 more)

### Community 25 - "AuthContext"
Cohesion: 0.17
Nodes (19): AuthContext, BaseModel, Execution context containing authenticated user, active workspace, and assigned…, AIPolishRequest, AIPolishResponse, DeckPreviewResponse, export_pdf(), export_pptx() (+11 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, baseUrl, esModuleInterop, isolatedModules, jsx, lib, module (+13 more)

### Community 27 - "session_service.py"
Cohesion: 0.10
Nodes (32): chardet, csv, numpy, os, pandas, pathlib, polars, BaseWarehouseConnector (+24 more)

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

### Community 35 - "DeckEngine"
Cohesion: 0.20
Nodes (9): Inches, RGBColor, DeckEngine, Compiles a complete PowerPoint (.pptx) file for the analytical session., Generates structured slide preview metadata for the web UI studio., Orchestrates PowerPoint presentation construction and preview generation., Fill slide background with a full-bleed colored rectangle., Renders correlation matrix as a high-res PNG image using matplotlib. (+1 more)

### Community 36 - "runner.py"
Cohesion: 0.13
Nodes (12): concurrent_futures, contextlib, ipython_core_interactiveshell, plotly_express, plotly_graph_objects, _df_fingerprint(), IPython-based stateful execution runner with output interception and Plotly…, Execute a Python code string sequentially within the persistent IPython shell. (+4 more)

### Community 37 - "api/auth.py"
Cohesion: 0.11
Nodes (17): fastapi, fastapi_security, pydantic, Request, get_auth_context(), get_current_user(), get_current_user_optional(), Authentication & Authorization dependencies for services/api. Implements JWT… (+9 more)

### Community 38 - "SqlWorkspace.tsx"
Cohesion: 0.10
Nodes (24): ReportsStudio(), ReportsStudioProps, SchemaMapper(), SchemaMapperProps, UserJoinLink, SqlWorkspace(), SqlWorkspaceProps, VirtualDataTable() (+16 more)

### Community 39 - "automl.py"
Cohesion: 0.09
Nodes (31): ast, logging, detect_problem_type(), generate_python_code(), DataFrame, Autonomous AutoML Baseline Engine for Conversational Data Platform. Provides…, Synthesizes a clean, standalone, executable scikit-learn Python script., Detects whether target is binary, multiclass, or regression. (+23 more)

### Community 40 - "workspaces.py"
Cohesion: 0.13
Nodes (22): patch, InviteMemberRequest, UpdateMemberRoleRequest, WorkspaceCreateRequest, WorkspaceMemberResponse, WorkspaceResponse, create_workspace(), invite_workspace_member() (+14 more)

### Community 41 - "DuckDBEngine"
Cohesion: 0.16
Nodes (14): DuckDBPyConnection, SqlQueryColumn, DuckDBEngine, Any, DbSession, Execute an analytical SQL query against session tables and checkpoints. Returns…, Execute a SQL statement and materialize the result into a new Parquet…, Sanitize filename into a valid SQL identifier (lowercase, alphanumeric +… (+6 more)

### Community 46 - "database.py"
Cohesion: 0.08
Nodes (26): alembic, Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), listens_for, logging_config, ensure_default_seed() (+18 more)

### Community 47 - "FileUploadModal.tsx"
Cohesion: 0.60
Nodes (4): FileUploadModal(), FileUploadModalProps, uploadDataset(), FileUploadResponse

### Community 48 - "models.py"
Cohesion: 0.09
Nodes (40): services_api_connectors, ColumnProfile, Core domain models and schemas for services/api. Includes SQLModel tables…, Metadata profile of a single column., Secure workspace-scoped warehouse connection configuration., WarehouseConfigRequest, WarehouseConfigResponse, WarehouseConnectionConfig (+32 more)

### Community 49 - "routers/auth.py"
Cohesion: 0.10
Nodes (41): bcrypt, hashlib, jwt, AuthTokenResponse, Secure database-backed refresh tokens supporting instant revocation., Multi-tenant workspace container for sessions and datasets., RefreshToken, RefreshTokenRequest (+33 more)

### Community 50 - "MockProvider"
Cohesion: 0.10
Nodes (13): AnthropicProvider, GeminiProvider, MockProvider, OpenAIProvider, Any, Google Gemini client powered by the official google-genai SDK. Supports native…, Represents a structured tool call emitted by an LLM., OpenAI API client supporting native function calling and token streaming. (+5 more)

### Community 51 - "test_warehouse_studio.py"
Cohesion: 0.10
Nodes (19): fixture, Integration & Unit tests for Track F: Enterprise Warehouse & Lakehouse…, Verify listing schemas and tables across connectors., Verify live table preview with column dtypes and rows., Verify one-click table sync streaming into a session Parquet dataset., Verify pushdown SQL query execution into a session dataset., Verify all 4 connectors in quadrant are returned with metadata., Verify connection ping tests for all connector types. (+11 more)

### Community 52 - "post"
Cohesion: 0.13
Nodes (17): Response, import_warehouse_dataset(), post, Upload a tabular dataset (CSV, TSV, Parquet, Excel, JSON, SQLite).…, Reset the sandbox kernel state, prune incremental checkpoints, and re-hydrate…, Execute an analytical query against a cloud warehouse (BigQuery, Snowflake),…, Transcribe audio recording from microphone into prompt text. Acts as zero-…, Synthesize natural speech audio bytes from text as fallback for client-side… (+9 more)

### Community 53 - "SandboxClient"
Cohesion: 0.11
Nodes (13): argparse, httpx, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any, Client SDK for interacting with the sandbox execution engine. (+5 more)

### Community 54 - "SessionService"
Cohesion: 0.08
Nodes (27): BaseSandboxClient, ChatTurn, ColumnDiff, DataFrameCheckpoint, File uploaded and ingested into a session., Individual analytical turn within a session., Immutable copy-on-write snapshot of a DataFrame state., SchemaDiff (+19 more)

### Community 55 - "create_db_and_tables"
Cohesion: 0.04
Nodes (56): fastapi_testclient, io, pytest, create_db_and_tables(), patch_sqlite_columns(), Initialize all registered SQLModel tables in the database and seed defaults., Safely add new columns to existing SQLite tables if missing., fixture (+48 more)

### Community 56 - "main.py"
Cohesion: 0.11
Nodes (22): dotenv, fastapi_middleware_cors, fastapi_responses, chat_with_data(), create_session(), get_session(), lifespan(), list_session_checkpoints() (+14 more)

### Community 57 - "test_api_ingestion.py"
Cohesion: 0.13
Nodes (14): fixture, End-to-end integration tests for the API Gateway and Ingestion Flow…, Test state persistence across turns and Plotly figure interception via API., Ensure database tables exist before each test., Verify API health check endpoint., Test creating a new session and querying its metadata., Test uploading a CSV dataset, extracting schema, and querying schema endpoint., Test that uploaded data is automatically hydrated and accessible as `df`. (+6 more)

### Community 58 - "StatisticianCritic"
Cohesion: 0.10
Nodes (25): Any, DataFrame, Deep post-execution audit inspecting numeric values, sample sizes, and output…, Rigorous statistical reviewer that audits code and outputs before user delivery., Static AST and heuristic scan of Python code prior to sandbox execution.…, StatisticianCritic, critic(), fixture (+17 more)

### Community 59 - "test_audio_service.py"
Cohesion: 0.09
Nodes (22): asyncio, fixture, Automated test suite for Track E: Voice & Audio Interaction Engine. Validates…, POST /api/v1/audio/recap returns natural 20-second executive audio script., POST /api/v1/audio/synthesize returns streaming audio/wav bytes., Ensure database tables exist before each test., Generate mock 1-second 16kHz mono WAV audio bytes for testing., Empty audio payload returns 0 duration and empty text. (+14 more)

### Community 60 - "Imported Screens & Assets"
Cohesion: 0.20
Nodes (10): 1. Avatar Portrait of Fares (Tech Founder & Senior Data Analyst), 2. Gemini Insights & Automated Anomalies, 3. Gemini Ambient Spark Logo, 4. SQL & Deep Query Workspace, 5. Design System (Ambient Intelligence Workspace), 6. Conversational Analytics Canvas, 7. SQL Patch Remediation Modal, 8. Rollback Script & Snapshot Comparison (+2 more)

### Community 61 - "Sidebar.tsx"
Cohesion: 0.20
Nodes (17): AuthModal(), AuthModalProps, Sidebar(), SidebarProps, TeamDrawer(), TeamDrawerProps, authApi, clearStoredTokens() (+9 more)

### Community 62 - "get"
Cohesion: 0.15
Nodes (18): export_session_data(), get_connectors_status(), get_dataset(), get_providers_status(), get_session_dataset(), get_session_schema(), health_check(), list_sessions() (+10 more)

### Community 63 - "BaseModel"
Cohesion: 0.16
Nodes (15): execute_code(), execute_sql_query(), Execute arbitrary Python analytical code within the session's sandbox. Returns…, Non-destructively roll back the active DataFrame to a specified checkpoint…, Execute arbitrary analytical SQL on session datasets and checkpoints via…, revert_session_version(), ChatTurnResponse, CodeExecutionRequest (+7 more)

### Community 64 - "SnowflakeConnector"
Cohesion: 0.24
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

### Community 68 - "test_live_docker.py"
Cohesion: 0.25
Nodes (3): fixture, Integration test verifying the running Docker sandbox container over HTTP., remote_client()

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
Nodes (13): ApplyHygieneRequest, ApplyHygieneResponse, AutoMLTrainRequest, CorrelationMatrixResponse, DataHealthResponse, apply_hygiene_fix(), get_session_anomalies(), get_session_correlations() (+5 more)

### Community 75 - "BigQueryConnector"
Cohesion: 0.24
Nodes (4): BigQueryConnector, Any, Path, Google Cloud BigQuery warehouse connector.

### Community 77 - "test_dataframe_versioning.py"
Cohesion: 0.12
Nodes (17): sqlmodel_pool, asyncio, fixture, Path, Tests for Phase 5: DataFrame Versioning, Checkpointing & Time-Travel Rollback., test_db(), test_incremental_checkpoint_on_dataframe_mutation(), test_initial_checkpoint_created_on_upload() (+9 more)

### Community 78 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 79 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_node_url, vite, @vitejs/plugin-react

### Community 80 - "ExecutionResult"
Cohesion: 0.15
Nodes (7): BaseException, ExecutionResult, Any, Inspect the current namespace variables and DataFrame dimensions., Restore 'df' from a Parquet checkpoint file., Encapsulates the output of a code execution turn., Run code in the IPython shell while redirecting stdout and stderr.

### Community 81 - "AudioService"
Cohesion: 0.16
Nodes (11): AudioService, Any, Distill raw analytical output and tables into a conversational, high-impact…, Synthesize audio speech for given text into standard WAV format. Generates a…, Core audio processing and voice synthesis service., Transcribe audio recording to text. Supports WebM, WAV, MP3, and OGG formats…, generate_executive_recap_endpoint(), Formulate a natural, spoken 20-second executive audio recap from turn insights.… (+3 more)

### Community 83 - "DiagnosticsStudio.tsx"
Cohesion: 0.21
Nodes (12): DiagnosticsStudio(), DiagnosticsStudioProps, diagnosticsAnomaliesQueryOptions(), diagnosticsApi, diagnosticsCorrelationsQueryOptions(), diagnosticsHealthQueryOptions(), schemaQueryOptions(), AnomalyReportResponse (+4 more)

### Community 84 - "PostgreSQLConnector"
Cohesion: 0.31
Nodes (4): PostgreSQLConnector, Any, Path, PostgreSQL analytical & transactional connector.

### Community 85 - "DatabricksConnector"
Cohesion: 0.24
Nodes (4): DatabricksConnector, Any, Path, Databricks Lakehouse and Unity Catalog connector.

### Community 86 - "sql_engine.py"
Cohesion: 0.17
Nodes (10): datetime, decimal, duckdb, math, re, Statistician & Critic Agent for Track D Multi-Agent Swarm. Performs two-stage…, Voice & Audio Interaction Service for Track E. Handles speech-to-text audio…, CriticReview (+2 more)

### Community 87 - "deck_engine.py"
Cohesion: 0.18
Nodes (10): matplotlib, matplotlib_pyplot, pptx, pptx_chart_data, pptx_dml_color, pptx_enum_chart, pptx_enum_shapes, pptx_enum_text (+2 more)

### Community 88 - ".get_config"
Cohesion: 0.50
Nodes (3): Any, Deserialize config_json to dictionary., Return config with sensitive keys (passwords, tokens, keys) masked.

### Community 89 - "SessionRelationsResponse"
Cohesion: 0.67
Nodes (3): get_session_table_relations(), Infer foreign key links and join opportunities between all tables in the…, SessionRelationsResponse

### Community 90 - "test_deck_engine.py"
Cohesion: 0.21
Nodes (11): DeckConfigRequest, mock_session_with_data(), fixture, Path, Tests for Track C PowerPoint Deck Engine (services.api.deck_engine)., Creates a test session with a versioned Parquet checkpoint., Test generating structured slide outlines for web studio preview., Test compiling valid .pptx binary with native charts and shapes. (+3 more)

### Community 92 - "Session"
Cohesion: 0.09
Nodes (22): json, ExportEngine, Any, Multi-format export engine for analytical datasets, reproducible notebooks, and…, Generate a Markdown Executive Summary report synthesizing the dataset profile,…, Generates downloadable artifacts from active session state., Export the active DataFrame snapshot in CSV, Parquet, or Excel format. Returns:…, Generate a corporate PowerPoint (.pptx) presentation deck. Returns:… (+14 more)

### Community 93 - "Any"
Cohesion: 0.14
Nodes (8): Any, Path, Return connector health and configuration metadata., Verify network connectivity and credentials with the cloud warehouse., List accessible datasets or databases., List tables within a specified dataset., Preview top rows from an external table., Execute an analytical SQL query against the warehouse, download the result as a…

## Knowledge Gaps
- **242 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+237 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 703 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Session` connect `Session` to `pdf_engine.py`, `swarm.py`, `AuthContext`, `session_service.py`, `DeckEngine`, `api/auth.py`, `automl.py`, `workspaces.py`, `DuckDBEngine`, `database.py`, `models.py`, `routers/auth.py`, `post`, `SessionService`, `main.py`, `get`, `BaseModel`, `routers/diagnostics.py`, `test_dataframe_versioning.py`, `sql_engine.py`, `deck_engine.py`, `SessionRelationsResponse`, `test_deck_engine.py`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `DataFrameProfile` connect `session_service.py` to `SnowflakeConnector`, `swarm.py`, `profile_dataframe`, `BigQueryConnector`, `models.py`, `PostgreSQLConnector`, `DatabricksConnector`, `SessionService`, `main.py`, `.set_profile`, `Session`, `Any`, `BaseModel`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `LocalSandboxClient` connect `SandboxClient` to `test_sandbox_runner.py`, `SandboxRunner`, `test_dataframe_versioning.py`, `ExecutionResult`, `SessionService`, `session_service.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Session` (e.g. with `list_sessions()` and `verify_session_access()`) actually correct?**
  _`Session` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 40 inferred relationships involving `AuthContext` (e.g. with `User` and `Workspace`) actually correct?**
  _`AuthContext` has 40 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DataFrameProfile` (e.g. with `build_system_prompt()` and `format_schema_context()`) actually correct?**
  _`DataFrameProfile` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `version`, `private` to the rest of the system?**
  _242 weakly-connected nodes found - possible documentation gaps or missing edges._