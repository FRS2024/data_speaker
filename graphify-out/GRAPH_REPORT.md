# Graph Report - Conversational_Data  (2026-09-23)

## Corpus Check
- 105 files · ~116,826 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 3, .example 1, .ini 1)

## Summary
- 1407 nodes · 2860 edges · 96 communities (77 shown, 19 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 197 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c94163c0`
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
- DataFrameCheckpoint
- Session
- compilerOptions
- DataFrameProfile
- api.ts
- 05_asset-st/DESIGN_SYSTEM.md
- package.json
- router.tsx
- react
- design_system/DESIGN_SYSTEM.md
- DeckConfigRequest
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
- MockProvider
- env.py
- profiler.py
- LocalSandboxClient
- SessionService
- create_db_and_tables
- main.py
- test_api_ingestion.py
- test_critic_guardrails.py
- test_audio_service.py
- Imported Screens & Assets
- Sidebar.tsx
- get
- swarm.py
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
- AuthContext
- BigQueryConnector
- NumberedCanvas
- test_pdf_engine.py
- scripts
- vite.config.ts
- get_me
- audio_service.py
- tailwind.config.ts
- test_duckdb_sql.py
- numpy
- StatisticianCritic
- sql_engine.py
- deck_engine.py
- providers.py
- test_dataframe_versioning.py
- test_deck_engine.py
- profile_dataframe
- test_export_engine.py
- .get_status
- GeminiProvider
- detect_problem_type

## God Nodes (most connected - your core abstractions)
1. `Session` - 99 edges
2. `AuthContext` - 39 edges
3. `SessionService` - 32 edges
4. `DataFrameProfile` - 31 edges
5. `react` - 26 edges
6. `create_db_and_tables()` - 26 edges
7. `DataFrameCheckpoint` - 24 edges
8. `SandboxClient` - 23 edges
9. `User` - 22 edges
10. `authFetch()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `test_post_execute_audit_catches_correlation_guardrail()` --uses--> `StatisticianCritic`  [INFERRED]
  tests/test_critic_guardrails.py → services/api/agent/critic.py
- `test_post_execute_audit_catches_severe_data_loss()` --uses--> `StatisticianCritic`  [INFERRED]
  tests/test_critic_guardrails.py → services/api/agent/critic.py
- `test_post_execute_audit_catches_skewness()` --uses--> `StatisticianCritic`  [INFERRED]
  tests/test_critic_guardrails.py → services/api/agent/critic.py
- `test_post_execute_audit_catches_small_sample_size()` --uses--> `StatisticianCritic`  [INFERRED]
  tests/test_critic_guardrails.py → services/api/agent/critic.py
- `test_pre_execute_audit_catches_arbitrary_head()` --uses--> `StatisticianCritic`  [INFERRED]
  tests/test_critic_guardrails.py → services/api/agent/critic.py

## Import Cycles
- None detected.

## Communities (96 total, 19 thin omitted)

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
Nodes (16): datetime, httpx, pandas, pathlib, reportlab_lib, reportlab_lib_pagesizes, reportlab_lib_styles, reportlab_lib_units (+8 more)

### Community 5 - "server.py"
Cohesion: 0.18
Nodes (18): pydantic, CheckpointFileRequest, execute_code(), ExecuteRequest, ExecuteResponse, get_sandbox_state(), health_check(), HealthResponse (+10 more)

### Community 6 - "orchestrator.py"
Cohesion: 0.13
Nodes (18): json, AgentOrchestrator, format_sse(), Any, Autonomous AI Analyst & Reflexion Orchestration Engine. Coordinates schema…, Synchronous non-streaming execution wrapper. Consumes the SSE stream and…, Format structured payload into a Server-Sent Event (SSE) frame., Orchestrates multi-turn analytical reasoning, code generation, and Reflexion. (+10 more)

### Community 7 - "SandboxClient"
Cohesion: 0.10
Nodes (20): Base interface for sandbox interaction., SandboxClient, client(), fixture, Comprehensive test suite verifying the stateful execution sandbox engine., Verify that runaway or infinite loops are halted cleanly at the timeout…, Verify that reset clears custom variables while keeping baseline imports…, Verify that variable state survives sequential execution turns. (+12 more)

### Community 8 - "test_profiler.py"
Cohesion: 0.11
Nodes (26): clean_table_name(), detect_encoding_and_delimiter(), generate_loader_code(), DataFrame, Path, Ingest a file of any supported format and return a dictionary of named…, Normalize a filename or table name into a valid Python identifier., Synthesize the optimal Python code snippet to hydrate the dataset into the… (+18 more)

### Community 9 - "SandboxRunner"
Cohesion: 0.10
Nodes (13): BaseException, Any, Hook into figure display calls to capture Plotly figures without a GUI., Reset the execution namespace, flushing variables while keeping baseline…, Inspect the current namespace variables and DataFrame dimensions., Atomically persist active 'df' to a Parquet file., Restore 'df' from a Parquet checkpoint file., Run code in the IPython shell while redirecting stdout and stderr. (+5 more)

### Community 10 - "test_agent_orchestrator.py"
Cohesion: 0.14
Nodes (14): fixture, Automated test suite for Phase 3: Autonomous AI Analyst & Reflexion Loop.…, Test real-time Server-Sent Events (SSE) streaming format and event multiplexing., Ensure database tables exist before each test., Create a session and upload a sample employee dataset., Test standard single-turn analytical query returning synchronous JSON., Test that chart requests produce interactive Plotly specifications., Test the Reflexion loop: 1. Attempt 1 triggers a KeyError… (+6 more)

### Community 14 - "api/diagnostics.py"
Cohesion: 0.11
Nodes (26): logging, scipy, compute_anomalies(), compute_correlation_matrix(), compute_data_health(), DataFrame, Autonomous Diagnostic Engine for Conversational Data Platform. Provides data…, Computes Pearson (linear) and Spearman (rank) correlation matrices for numeric… (+18 more)

### Community 22 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, clsx, lucide-react, @monaco-editor/react, plotly.js-dist-min, react, react-dom, react-plotly.js (+6 more)

### Community 23 - "types.ts"
Cohesion: 0.08
Nodes (28): StatisticalPeerReviewCard(), StatisticalPeerReviewCardProps, VersionHistoryView(), VersionHistoryViewProps, UseChatStreamOptions, AnomalyAttribution, AnomalyRecord, CheckpointSummary (+20 more)

### Community 24 - "DataFrameCheckpoint"
Cohesion: 0.25
Nodes (6): DataFrameCheckpoint, Immutable copy-on-write snapshot of a DataFrame state., Deserialize stored profile., Serialize DataFrameProfile., PdfEngine, Compiles multi-page executive PDF reports.

### Community 25 - "Session"
Cohesion: 0.10
Nodes (25): ExportEngine, Any, Generate a Markdown Executive Summary report synthesizing the dataset profile,…, Generates downloadable artifacts from active session state., Export the active DataFrame snapshot in CSV, Parquet, or Excel format. Returns:…, Generate a corporate PowerPoint (.pptx) presentation deck. Returns:…, Generate a polished executive PDF brief using ReportLab. Returns: (file_bytes,…, Generate a fully reproducible Jupyter Notebook (.ipynb) containing setup cells,… (+17 more)

### Community 26 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, baseUrl, esModuleInterop, isolatedModules, jsx, lib, module (+13 more)

### Community 27 - "DataFrameProfile"
Cohesion: 0.10
Nodes (18): os, polars, BaseWarehouseConnector, ABC, Path, Base interface and abstractions for external cloud data warehouse connectors.…, Abstract interface for external analytical data warehouse connections., Return True if required environment variables or credentials exist. (+10 more)

### Community 28 - "api.ts"
Cohesion: 0.09
Nodes (42): DiagnosticsStudio(), DiagnosticsStudioProps, authFetch(), checkpointsQueryOptions(), createSession(), diagnosticsAnomaliesQueryOptions(), diagnosticsApi, diagnosticsCorrelationsQueryOptions() (+34 more)

### Community 29 - "05_asset-st/DESIGN_SYSTEM.md"
Cohesion: 0.15
Nodes (12): Ambient Radiant Glows, Brand & Style, Core Tenets, Elevation & Depth, Geometric Application, Grid Models & Adaptive Behavior, Layout & Spacing, Shapes (+4 more)

### Community 30 - "package.json"
Cohesion: 0.12
Nodes (15): name, private, type, version, autoprefixer, clsx, plotly.js-dist-min, postcss (+7 more)

### Community 31 - "router.tsx"
Cohesion: 0.09
Nodes (26): Header(), HeaderProps, ReportsStudio(), ReportsStudioProps, SqlPatchModal(), SqlPatchModalProps, VisualizationStudio(), VisualizationStudioProps (+18 more)

### Community 32 - "react"
Cohesion: 0.11
Nodes (24): ActiveChatView(), ActiveChatViewProps, AudioWaveVisualizer(), AudioWaveVisualizerProps, FloatingActionDock(), FloatingActionDockProps, StepConfig, STEPS (+16 more)

### Community 34 - "design_system/DESIGN_SYSTEM.md"
Cohesion: 0.20
Nodes (8): Brand & Style, Core Tenets, Geometric Application, Shapes, Typographic Roles & Expressive Usage, Typography, Gemini Conversational Analytics Platform — Stitch Asset Catalog, Project Metadata

### Community 35 - "DeckConfigRequest"
Cohesion: 0.14
Nodes (15): Inches, RGBColor, DeckEngine, Compiles a complete PowerPoint (.pptx) file for the analytical session., Generates structured slide preview metadata for the web UI studio., Orchestrates PowerPoint presentation construction and preview generation., Fill slide background with a full-bleed colored rectangle., Renders correlation matrix as a high-res PNG image using matplotlib. (+7 more)

### Community 36 - "runner.py"
Cohesion: 0.12
Nodes (12): concurrent_futures, contextlib, ipython_core_interactiveshell, plotly_express, plotly_graph_objects, _df_fingerprint(), ExecutionResult, IPython-based stateful execution runner with output interception and Plotly… (+4 more)

### Community 37 - "test_swarm_orchestrator.py"
Cohesion: 0.20
Nodes (10): fixture, Automated test suite for Track D: Multi-Agent Critic & Statistician Debate…, Ensure database tables exist before each test., Create a session and upload a sample employee dataset., Test running synchronous analytical turn with swarm_mode=True., Test SSE event stream with swarm_phase, critic_review, and execution events., session_with_data(), setup_database() (+2 more)

### Community 38 - "SqlWorkspace.tsx"
Cohesion: 0.14
Nodes (18): SchemaMapper(), SchemaMapperProps, UserJoinLink, SqlWorkspace(), SqlWorkspaceProps, VirtualDataTable(), VirtualDataTableProps, executeSql (+10 more)

### Community 39 - "automl.py"
Cohesion: 0.17
Nodes (11): generate_python_code(), Autonomous AutoML Baseline Engine for Conversational Data Platform. Provides…, Synthesizes a clean, standalone, executable scikit-learn Python script., sklearn_compose, sklearn_ensemble, sklearn_impute, sklearn_linear_model, sklearn_metrics (+3 more)

### Community 40 - "models.py"
Cohesion: 0.10
Nodes (30): patch, Executes fast-bounded multi-model training, scoring, feature importance, and…, run_automl(), execute_code(), Execute arbitrary Python analytical code within the session's sandbox. Returns…, CheckpointSummaryResponse, CodeExecutionRequest, CodeExecutionResponse (+22 more)

### Community 41 - "DuckDBEngine"
Cohesion: 0.24
Nodes (10): DuckDBPyConnection, SqlQueryColumn, SqlQueryResponse, DuckDBEngine, DbSession, Execute an analytical SQL query against session tables and checkpoints. Returns…, Execute a SQL statement and materialize the result into a new Parquet…, Manages embedded session-level DuckDB connections and table catalogs. (+2 more)

### Community 46 - "database.py"
Cohesion: 0.08
Nodes (45): delete, fastapi, fastapi_security, listens_for, Request, get_auth_context(), get_current_user(), get_current_user_optional() (+37 more)

### Community 47 - "FileUploadModal.tsx"
Cohesion: 0.60
Nodes (4): FileUploadModal(), FileUploadModalProps, uploadDataset(), FileUploadResponse

### Community 48 - "useChatStream"
Cohesion: 0.50
Nodes (3): Technical Stack:, Web Application Client (`apps/web`), useChatStream()

### Community 49 - "routers/auth.py"
Cohesion: 0.10
Nodes (38): bcrypt, hashlib, jwt, AuthTokenResponse, Secure database-backed refresh tokens supporting instant revocation., RefreshToken, RefreshTokenRequest, UserResponse (+30 more)

### Community 50 - "MockProvider"
Cohesion: 0.13
Nodes (10): AnthropicProvider, MockProvider, OpenAIProvider, Any, Represents a structured tool call emitted by an LLM., OpenAI API client supporting native function calling and token streaming., Anthropic Claude API client supporting native tool use., Call the LLM with tool definitions to produce an `execute_python` call. (+2 more)

### Community 51 - "env.py"
Cohesion: 0.20
Nodes (7): alembic, Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online(), logging_config, sqlalchemy

### Community 52 - "profiler.py"
Cohesion: 0.18
Nodes (12): chardet, csv, ForeignKeyRelation, infer_foreign_key_relations(), Any, Universal Ingestion and Schema Profiling Engine for data_speaker. Supports CSV,…, Heuristically infer potential foreign key / join relationships between tables…, Sanitize arbitrary Python/Pandas/Polars values for strict RFC 8259 JSON… (+4 more)

### Community 53 - "LocalSandboxClient"
Cohesion: 0.14
Nodes (10): argparse, main(), Interactive Terminal REPL for developer testing of the stateful sandbox engine., run_repl(), LocalSandboxClient, Any, HTTP client communicating with the containerized sandbox runner., In-process sandbox client for rapid local testing without container… (+2 more)

### Community 54 - "SessionService"
Cohesion: 0.09
Nodes (19): BaseSandboxClient, Any, DataFrame, Path, Convert a local filesystem path to the equivalent container mount path if…, Extract active DataFrame from sandbox, persist Parquet checkpoint, profile…, Execute arbitrary Python analytical code inside the session's sandbox. Records…, Revert the session's active DataFrame to a previous checkpoint. Non-… (+11 more)

### Community 55 - "create_db_and_tables"
Cohesion: 0.06
Nodes (37): fastapi_testclient, io, pytest, create_db_and_tables(), patch_sqlite_columns(), Initialize all registered SQLModel tables in the database and seed defaults., Safely add new columns to existing SQLite tables if missing., fixture (+29 more)

### Community 56 - "main.py"
Cohesion: 0.06
Nodes (47): fastapi_middleware_cors, fastapi_responses, Response, services_api_connectors, chat_with_data(), create_session(), execute_sql_query(), generate_executive_recap_endpoint() (+39 more)

### Community 57 - "test_api_ingestion.py"
Cohesion: 0.13
Nodes (14): fixture, End-to-end integration tests for the API Gateway and Ingestion Flow…, Test state persistence across turns and Plotly figure interception via API., Ensure database tables exist before each test., Verify API health check endpoint., Test creating a new session and querying its metadata., Test uploading a CSV dataset, extracting schema, and querying schema endpoint., Test that uploaded data is automatically hydrated and accessible as `df`. (+6 more)

### Community 58 - "test_critic_guardrails.py"
Cohesion: 0.11
Nodes (17): Unit test suite for Track D: Statistician Critic Guardrails & AST Audits.…, Clean idiomatic pandas code should be approved with high confidence., Calling dropna() without logging shape/counts should trigger an AST warning., Slicing head() without sort_values() should trigger a selection bias warning., Averaging averages should trigger a revision requirement., Stdout reporting sample sizes N < 30 should be flagged with small sample…, Severe divergence between Mean and Median should flag outlier/skewness…, Losing >20% of rows after operation flags survivorship bias risk. (+9 more)

### Community 59 - "test_audio_service.py"
Cohesion: 0.10
Nodes (21): asyncio, fixture, Automated test suite for Track E: Voice & Audio Interaction Engine. Validates…, POST /api/v1/audio/recap returns natural 20-second executive audio script., POST /api/v1/audio/synthesize returns streaming audio/wav bytes., Ensure database tables exist before each test., Generate mock 1-second 16kHz mono WAV audio bytes for testing., Empty audio payload returns 0 duration and empty text. (+13 more)

### Community 60 - "Imported Screens & Assets"
Cohesion: 0.20
Nodes (10): 1. Avatar Portrait of Fares (Tech Founder & Senior Data Analyst), 2. Gemini Insights & Automated Anomalies, 3. Gemini Ambient Spark Logo, 4. SQL & Deep Query Workspace, 5. Design System (Ambient Intelligence Workspace), 6. Conversational Analytics Canvas, 7. SQL Patch Remediation Modal, 8. Rollback Script & Snapshot Comparison (+2 more)

### Community 61 - "Sidebar.tsx"
Cohesion: 0.20
Nodes (17): AuthModal(), AuthModalProps, Sidebar(), SidebarProps, TeamDrawer(), TeamDrawerProps, authApi, clearStoredTokens() (+9 more)

### Community 62 - "get"
Cohesion: 0.11
Nodes (23): export_session_data(), get_connectors_status(), get_dataset(), get_providers_status(), get_session_dataset(), get_session_schema(), get_session_table_relations(), health_check() (+15 more)

### Community 63 - "swarm.py"
Cohesion: 0.20
Nodes (12): get_llm_provider(), Instantiate the configured LLM provider based on request parameter or…, format_sse(), Any, Multi-Agent Swarm Coordinator for Track D. Coordinates the collaborative loop…, Format structured payload into a Server-Sent Event (SSE) frame., Coordinates collaborative multi-agent execution with peer review and debate., Executes a peer-reviewed multi-agent analytical turn. Streams swarm phases,… (+4 more)

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

### Community 74 - "AuthContext"
Cohesion: 0.21
Nodes (19): AuthContext, BaseModel, Execution context containing authenticated user, active workspace, and assigned…, ApplyHygieneRequest, ApplyHygieneResponse, AutoMLTrainRequest, AutoMLTrainResponse, CorrelationMatrixResponse (+11 more)

### Community 75 - "BigQueryConnector"
Cohesion: 0.24
Nodes (3): BigQueryConnector, Any, Google Cloud BigQuery warehouse connector.

### Community 77 - "test_pdf_engine.py"
Cohesion: 0.22
Nodes (9): sqlmodel_pool, mock_session_with_data(), fixture, Path, Tests for Track C Executive PDF Brief Engine (services.api.pdf_engine)., Creates a test session with a versioned Parquet checkpoint., Test compiling executive PDF brief using ReportLab., test_db() (+1 more)

### Community 78 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 79 - "vite.config.ts"
Cohesion: 0.50
Nodes (3): ref_node_url, vite, @vitejs/plugin-react

### Community 80 - "get_me"
Cohesion: 0.50
Nodes (4): get_me(), Any, get, Return user profile and all workspace memberships with roles.

### Community 81 - "audio_service.py"
Cohesion: 0.14
Nodes (10): math, AudioService, Any, Voice & Audio Interaction Service for Track E. Handles speech-to-text audio…, Distill raw analytical output and tables into a conversational, high-impact…, Synthesize audio speech for given text into standard WAV format. Generates a…, Core audio processing and voice synthesis service., Transcribe audio recording to text. Supports WebM, WAV, MP3, and OGG formats… (+2 more)

### Community 83 - "test_duckdb_sql.py"
Cohesion: 0.18
Nodes (11): fixture, Unit tests for the embedded DuckDB SQL Execution Engine & Checkpoint…, Create a session and ingest sample transactional data., Test standard SELECT query with aggregations on uploaded orders dataset., Test querying the active dataset checkpoint via df_active or df., Test creating a new DataFrame checkpoint directly from a SQL filter query., session_with_data(), setup_db() (+3 more)

### Community 84 - "numpy"
Cohesion: 0.20
Nodes (9): ast, numpy, re, Statistician & Critic Agent for Track D Multi-Agent Swarm. Performs two-stage…, Unit and integration tests for Autonomous AutoML Baseline Engine (Track B).…, Verifies end-to-end classification benchmarking and feature importances., Verifies end-to-end regression benchmarking, R² scoring, and feature…, test_automl_classification_training() (+1 more)

### Community 85 - "StatisticianCritic"
Cohesion: 0.24
Nodes (9): Any, DataFrame, Deep post-execution audit inspecting numeric values, sample sizes, and output…, Rigorous statistical reviewer that audits code and outputs before user delivery., Static AST and heuristic scan of Python code prior to sandbox execution.…, StatisticianCritic, CriticReview, critic() (+1 more)

### Community 86 - "sql_engine.py"
Cohesion: 0.20
Nodes (9): decimal, duckdb, Any, Embedded DuckDB SQL Engine for data_speaker. Provides sub-millisecond in-…, Sanitize filename into a valid SQL identifier (lowercase, alphanumeric +…, Convert DuckDB result values to JSON-safe Python primitives., sanitize_table_name(), serialize_cell_value() (+1 more)

### Community 87 - "deck_engine.py"
Cohesion: 0.20
Nodes (9): matplotlib, matplotlib_pyplot, pptx_chart_data, pptx_dml_color, pptx_enum_chart, pptx_enum_shapes, pptx_enum_text, pptx_util (+1 more)

### Community 88 - "providers.py"
Cohesion: 0.25
Nodes (7): asyncio, dotenv, BaseLLMProvider, ABC, Multi-Provider LLM abstraction layer for the Autonomous AI Analyst. Supports…, Abstract interface for LLM providers., Stream conversational natural language insights and business interpretation.

### Community 89 - "test_dataframe_versioning.py"
Cohesion: 0.28
Nodes (8): asyncio, fixture, Path, Tests for Phase 5: DataFrame Versioning, Checkpointing & Time-Travel Rollback., test_db(), test_incremental_checkpoint_on_dataframe_mutation(), test_initial_checkpoint_created_on_upload(), test_time_travel_rollback()

### Community 90 - "test_deck_engine.py"
Cohesion: 0.29
Nodes (7): pptx, mock_session_with_data(), fixture, Path, Tests for Track C PowerPoint Deck Engine (services.api.deck_engine)., Creates a test session with a versioned Parquet checkpoint., test_db()

### Community 91 - "profile_dataframe"
Cohesion: 0.25
Nodes (6): Path, Path, profile_dataframe(), Extract a comprehensive, privacy-compliant schema profile from a Polars…, Test schema metrics computation (null percentage, cardinality, preview)., test_profile_dataframe_metrics()

### Community 92 - "test_export_engine.py"
Cohesion: 0.32
Nodes (7): asyncio, fixture, Tests for Phase 5: Multi-Format Export Engine., test_dataset_exports(), test_db(), test_executive_report_export(), test_jupyter_notebook_export()

### Community 93 - ".get_status"
Cohesion: 0.29
Nodes (4): Any, Return connector health and configuration metadata., Verify network connectivity and credentials with the cloud warehouse., Preview top rows from an external table.

### Community 95 - "detect_problem_type"
Cohesion: 0.40
Nodes (5): detect_problem_type(), DataFrame, Detects whether target is binary, multiclass, or regression., Verifies heuristic problem type detection across varied column types., test_problem_type_detection()

## Knowledge Gaps
- **241 isolated node(s):** `name`, `version`, `private`, `type`, `dev` (+236 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 674 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Session` connect `Session` to `session_service.py`, `orchestrator.py`, `test_profiler.py`, `api/diagnostics.py`, `DeckConfigRequest`, `models.py`, `DuckDBEngine`, `database.py`, `routers/auth.py`, `SessionService`, `main.py`, `get`, `swarm.py`, `AuthContext`, `test_pdf_engine.py`, `get_me`, `sql_engine.py`, `deck_engine.py`, `test_dataframe_versioning.py`, `test_deck_engine.py`, `test_export_engine.py`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `DataFrameProfile` connect `DataFrameProfile` to `SnowflakeConnector`, `session_service.py`, `orchestrator.py`, `models.py`, `test_profiler.py`, `BigQueryConnector`, `profiler.py`, `SessionService`, `main.py`, `DataFrameCheckpoint`, `profile_dataframe`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `SandboxRunner` connect `SandboxRunner` to `server.py`, `session_service.py`, `LocalSandboxClient`, `runner.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Session` (e.g. with `list_sessions()` and `verify_session_access()`) actually correct?**
  _`Session` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 31 inferred relationships involving `AuthContext` (e.g. with `User` and `Workspace`) actually correct?**
  _`AuthContext` has 31 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `SessionService` (e.g. with `ChatTurn` and `CheckpointSummaryResponse`) actually correct?**
  _`SessionService` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `DataFrameProfile` (e.g. with `build_system_prompt()` and `format_schema_context()`) actually correct?**
  _`DataFrameProfile` has 7 INFERRED edges - model-reasoned connections that need verification._