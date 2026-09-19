# TECHNICAL REQUIREMENTS DOCUMENT (TRD)

**Project Title:** Conversational Data Analysis Platform (Code-Interpreting Autonomous Analyst)  
**Document Version:** 1.0.0  
**Target Release:** Production Phase 1 (MVP)  
**Author:** Senior Software Developer / Tech Lead  
**Status:** Approved for Implementation  

---

## 1. Technical Overview

### 1.1 High-Level Technical Goals
The platform architecture provides a secure, sub-second, multi-tenant execution runtime capable of running untrusted, user-generated Python code while maintaining conversational state across multiple turns.
* **Determinism:** All analytical claims must be computed via Python runtime execution; mathematical hallucinations are treated as system faults.
* **Sub-Second Responsiveness:** Time-to-First-Token (TTFT) for conversational responses must remain under 800ms; warm sandbox assignment must complete in ≤ 150ms.
* **Strict Defense-in-Depth:** Zero untrusted code may touch the host filesystem, access the internal network, or make outbound public internet calls.

### 1.2 Key Technical Constraints & Non-Negotiables
1. **Schema-Only Context Boundary:** Raw user data rows must NEVER be transmitted to external LLM provider APIs (Anthropic, OpenAI, Google). Only structural metadata, data types, null distributions, and synthetic summaries are permitted in prompt payloads.
2. **Zero-Network Sandboxes:** Sandbox execution environments must have all networking hardware and loopback access detached (`network: none`) to physically prevent data exfiltration.
3. **Deterministic State Continuity:** Computational state must not be reset across turns. If a user mutates a DataFrame in Turn 1, that mutation must be present in memory during Turn 2 without re-reading the source file from disk.
4. **Hard Limits:** Hard timeout ceiling of 60 seconds per execution snippet, 2 vCPUs, and 4GB RAM per container sandbox.

### 1.3 Technology Philosophy & Engineering Principles
* **Code is the Canonical Truth:** Data transformations must be expressed as pure, reproducible Python code snippets rather than proprietary internal state graphs.
* **Fail-Fast & Auto-Heal:** Intercept execution errors at the runtime layer and invoke automated self-correction before alerting the user.
* **Observable by Default:** Every microsecond of latency across the API gateway, agent orchestrator, and execution sandbox is instrumented via OpenTelemetry.

---

## 2. Functional Technical Requirements

### 2.1 API Contracts & Interaction Protocols

#### 2.1.1 REST Endpoints Specification
```http
POST /api/v1/sessions
Headers: Authorization: Bearer <JWT>
Response (201 Created):
{
  "session_id": "sess_01HZX89ABCKXYZ789",
  "created_at": "2026-09-19T14:30:00Z",
  "status": "active",
  "sandbox_status": "assigned"
}

POST /api/v1/sessions/{session_id}/files/upload
Headers: Content-Type: multipart/form-data
Body: file: binary (< 500MB)
Response (202 Accepted):
{
  "file_id": "file_01HZX89DEF",
  "filename": "customer_churn.csv",
  "size_bytes": 104857600,
  "mime_type": "text/csv",
  "storage_uri": "s3://prod-analytics-storage/tenants/t_123/sess_01HZX89ABCKXYZ789/raw/customer_churn.csv",
  "status": "profiling_queued"
}

GET /api/v1/sessions/{session_id}/schema
Response (200 OK):
{
  "session_id": "sess_01HZX89ABCKXYZ789",
  "dataframe_version": "df_v0",
  "dimensions": { "rows": 500000, "columns": 8 },
  "memory_footprint_mb": 142.8,
  "columns": [
    {
      "name": "customer_id",
      "dtype": "int64",
      "null_count": 0,
      "null_percentage": 0.0,
      "cardinality": 500000,
      "sample_values": [1001, 1002, 1003, 1004, 1005]
    },
    {
      "name": "monthly_charges",
      "dtype": "float64",
      "null_count": 142,
      "null_percentage": 0.028,
      "cardinality": 1820,
      "sample_values": [29.85, 56.95, 53.85, 42.30, 70.70]
    }
  ],
  "head_preview_markdown": "| customer_id | monthly_charges |\n| --- | --- |\n| 1001 | 29.85 |\n| 1002 | 56.95 |"
}

POST /api/v1/sessions/{session_id}/revert
Body: { "target_version": "df_v1" }
Response (200 OK):
{
  "status": "reverted",
  "active_version": "df_v1",
  "restored_at": "2026-09-19T14:35:12Z"
}

POST /api/v1/sessions/{session_id}/export
Body: { "format": "notebook" } -- "notebook" | "script" | "parquet" | "csv"
Response (200 OK):
{
  "download_url": "https://prod-analytics-storage.s3.amazonaws.com/exports/analysis_sess_01.ipynb?AWSAccessKeyId=...",
  "expires_at": "2026-09-19T15:35:12Z"
}
```

#### 2.1.2 Real-Time Event Stream (Server-Sent Events)
Clients subscribe via `GET /api/v1/sessions/{session_id}/events`. The stream multiplexes conversational tokens, intermediate execution milestones, raw stdout/stderr logs, and Plotly visualization specifications:

```json
event: token
data: {"token": "Calculating", "turn_id": "trn_01"}

event: code_generated
data: {"code": "df = df[df['monthly_charges'] > 50.0]\nprint(df.shape)", "language": "python"}

event: execution_status
data: {"status": "running_sandbox", "assigned_worker": "worker-pool-08"}

event: execution_stdout
data: {"stdout": "(342150, 8)\n"}

event: chart_generated
data: {
  "figure_type": "plotly",
  "spec": {
    "data": [{"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar"}],
    "layout": {"title": "Monthly Revenue Distribution"}
  }
}

event: reflexion_step
data: {"attempt": 1, "error": "KeyError: 'churn_date'", "status": "retrying"}

event: turn_complete
data: {"turn_id": "trn_01", "active_version": "df_v1", "duration_ms": 2340}
```

### 2.2 Domain Data Models & Database Schemas

#### PostgreSQL 16 Relational DDL
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE workspaces (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    plan_tier VARCHAR(32) NOT NULL DEFAULT 'free',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id VARCHAR(36) REFERENCES workspaces(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'member',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id VARCHAR(36) REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by VARCHAR(36) REFERENCES users(id),
    title VARCHAR(255) NOT NULL DEFAULT 'Untitled Analysis',
    active_dataframe_version VARCHAR(32) NOT NULL DEFAULT 'df_v0',
    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE session_files (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(36) REFERENCES sessions(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    mime_type VARCHAR(128) NOT NULL,
    storage_s3_uri VARCHAR(1024) NOT NULL,
    schema_profile_json JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_turns (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(36) REFERENCES sessions(id) ON DELETE CASCADE,
    user_prompt TEXT NOT NULL,
    generated_code TEXT,
    stdout TEXT,
    stderr TEXT,
    reflexion_count INT NOT NULL DEFAULT 0,
    status VARCHAR(32) NOT NULL, -- 'success', 'failed', 'reverted'
    execution_time_ms INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dataframe_checkpoints (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(36) REFERENCES sessions(id) ON DELETE CASCADE,
    version_tag VARCHAR(32) NOT NULL, -- 'df_v0', 'df_v1'
    chat_turn_id VARCHAR(36) REFERENCES chat_turns(id),
    parquet_storage_uri VARCHAR(1024) NOT NULL,
    row_count BIGINT NOT NULL,
    column_count INT NOT NULL,
    memory_bytes BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_workspace ON sessions(workspace_id);
CREATE INDEX idx_chat_turns_session ON chat_turns(session_id);
CREATE INDEX idx_checkpoints_session ON dataframe_checkpoints(session_id, version_tag);
```

#### Pydantic v2 Core Domain Schemas
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class ColumnProfile(BaseModel):
    name: str
    dtype: str
    null_count: int
    null_percentage: float
    cardinality: int
    sample_values: List[Any]

class DataFrameProfile(BaseModel):
    session_id: str
    version_tag: str
    row_count: int
    column_count: int
    memory_footprint_mb: float
    columns: List[ColumnProfile]
    head_preview_markdown: str

class CodeExecutionPayload(BaseModel):
    session_id: str
    turn_id: str
    code: str
    timeout_seconds: int = 60

class CodeExecutionResult(BaseModel):
    status: str  # "success" | "error" | "timeout" | "oom"
    stdout: str
    stderr: str
    execution_time_ms: int
    figures: List[Dict[str, Any]] = Field(default_factory=list)
    has_mutated_dataframe: bool = False
    new_version_tag: Optional[str] = None
```

### 2.3 Business Logic & Edge Cases
1. **Delimiter & Encoding Detection:** Automated character encoding detection via `chardet` (UTF-8, UTF-16, ISO-8859-1, Windows-1252). Fallback sniffing for `,`, `\t`, `;`, `|` delimiters using `csv.Sniffer`.
2. **DataFrame Memory Guardrails:** For raw datasets > 100MB, default ingestion engine leverages Polars for fast lazy-scanning and conversion to memory-compact Arrow/Pandas structures.
3. **Safe Serialization:** Infinite (`inf`) and `NaN` numerical values produced during zero-division or imputation are sanitized into `null` literals to conform strictly with RFC 8259 JSON standards.
4. **Out-of-Memory (OOM) Interception:** Sandboxes register Linux cgroup OOM notifications. When triggered, the process sends a structured JSON error to the orchestrator rather than hanging or silently dying.

---

## 3. Non-Functional Technical Requirements

### 3.1 Latency Budgets & Throughput Targets
```
┌────────────────────────────────────────────────────────────────────────┐
│                   END-TO-END EXECUTION LATENCY BUDGET                  │
├───────────────────────────────────────────────────────┬────────────────┤
│ OPERATION PHASE                                       │ TIME BUDGET    │
├───────────────────────────────────────────────────────┼────────────────┤
│ 1. Ingress API Gateway & JWT Validation               │ 15 ms          │
│ 2. Session & Checkpoint Metadata Fetch (Redis Cache)  │ 10 ms          │
│ 3. Schema Context Construction                        │ 5 ms           │
│ 4. LLM Time to First Token (TTFT - Claude 3.5 Sonnet) │ 750 ms         │
│ 5. Code Stream Completion & Extraction                │ 800 ms         │
│ 6. Warm Sandbox Allocation (Pool Arbiter)             │ 45 ms          │
│ 7. Kernel Execution (1M Rows Pandas Aggregation)      │ 1,200 ms       │
│ 8. Plotly Serialization & Stdout Interception         │ 50 ms          │
│ 9. S3 Parquet Checkpoint (Async Background Worker)    │ (Non-blocking) │
├───────────────────────────────────────────────────────┼────────────────┤
│ TOTAL END-TO-END TURN TIME                            │ 2,875 ms       │
└───────────────────────────────────────────────────────┴────────────────┘
```

### 3.2 Scalability Targets
* **Stateless API Gateway:** Scale horizontally up to 50 pods on Kubernetes (EKS) targeting ≤ 60% CPU utilization.
* **Execution Sandbox Worker Pool:** Scale warm nodes dynamically to sustain 5,000 concurrent active sessions with pool availability headroom of ≥ 15% at all times.
* **Database IOPS:** Provisioned PostgreSQL RDS scaling to 15,000 IOPS with read-replica offloading for analytical session history.

### 3.3 Security & Threat Modeling (STRIDE Analysis)

| STRIDE Category | Threat Vector | Technical Mitigation Architecture |
| :--- | :--- | :--- |
| **Spoofing** | Unauthorized token usage / identity theft | Short-lived asymmetric RS256 JWTs (15 min expiry) + HttpOnly secure refresh cookies. |
| **Tampering** | Modifying executed code or Parquet snapshots | S3 Object Lock (WORM) on historical checkpoints; SHA-256 integrity hashes recorded in PostgreSQL. |
| **Repudiation** | Denying sensitive data execution | Immutable append-only audit trail logging every user prompt, generated code, and kernel exit code. |
| **Information Disclosure** | Data exfiltration via malicious Python code | Sandboxes run with `network: none`; strict kernel syscall whitelisting via seccomp filters. |
| **Denial of Service** | Infinite loops (`while True:`) or memory bombs | Strict Linux cgroups limits: 2 vCPUs (100% quota), 4GB RAM ceiling, hard `SIGKILL` timeout at 60s. |
| **Elevation of Privilege** | Container escape to host kernel | Sandboxes executed inside **gVisor (`runsc`)** application kernels or **Firecracker MicroVMs**; non-root user (`uid 1000`). |

### 3.4 Observability & Telemetry Standards
* **Distributed Tracing:** OpenTelemetry instrumentation injected across all microservices (Next.js BFF → FastAPI Gateway → Agent Orchestrator → Sandbox Daemon). Traces exported to Jaeger / Datadog.
* **Metrics:** Prometheus endpoint scraping:
  * `sandbox_pool_idle_count` (Gauge)
  * `sandbox_acquisition_latency_ms` (Histogram)
  * `code_execution_duration_ms` (Histogram)
  * `reflexion_retries_total` (Counter, partitioned by error type)
* **Structured Logging:** JSON logs via `structlog` emitting `trace_id`, `span_id`, `session_id`, `user_id`, and `turn_id`.

---

## 4. Data Requirements & Retention Architecture

### 4.1 Data Volume Forecast
* **Active Datasets:** Average compressed dataset size = 45MB. 100,000 users × 3 active files = 13.5TB raw storage.
* **Checkpoint Multiplier:** Average analysis session generates 6 mutating operations. 13.5TB × 6 = 81TB Parquet checkpoint volume per month.
* **Retention Policy:**
  * Free Tier: 7-day TTL on raw files and checkpoints.
  * Pro Tier: 90-day TTL on checkpoints; raw files persisted until user deletion.
  * Enterprise: Configurable (immediate purge upon session disconnect supported).

### 4.2 Backup & Disaster Recovery RPO / RTO
* **Recovery Point Objective (RPO):** < 5 minutes for metadata (PostgreSQL Continuous WAL archiving to S3); 0 minutes for file storage (S3 Cross-Region Versioned Replication).
* **Recovery Time Objective (RTO):** < 45 minutes for full regional failover.

---

## 5. Infrastructure & Operational Requirements

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ENVIRONMENTS STRATEGY                           │
├─────────────┬──────────────────────────┬───────────────────────────────┤
│ ENVIRONMENT │ PURPOSE                  │ INFRASTRUCTURE                │
├─────────────┼──────────────────────────┼───────────────────────────────┤
│ Local Dev   │ Development & debugging  │ Docker Compose + Local gVisor │
│ Preview PR  │ Ephemeral PR validation  │ EKS dynamic namespace via Argo│
│ Staging     │ Pre-production soak test │ Multi-AZ mirrored EKS cluster │
│ Production  │ Live customer traffic    │ Multi-AZ Bare-Metal EKS Nodes │
└─────────────┴──────────────────────────┴───────────────────────────────┘
```

* **Deployment Frequency:** Continuous delivery (CD) to production multiple times daily via ArgoCD GitOps.
* **Rollback Strategy:** Automated canary rollback via Argo Rollouts / Flagger if P99 HTTP 5xx error rate exceeds 0.2% over a 3-minute window.

---

## 6. Technical Risks & Mitigations

* **Risk 1: Fork Bombs and Kernel Resource Depletion.**  
  * *Mitigation:* Apply strict Linux PID limits (`pids.max = 128`) and drop all capabilities (`cap-drop=ALL`).
* **Risk 2: Multi-LLM API Rate Limiting & Outages.**  
  * *Mitigation:* Implement client-side exponential backoff with jitter and an automated circuit-breaker fallback matrix: Primary (Claude 3.5 Sonnet) → Fallback 1 (GPT-4o) → Fallback 2 (Gemini 1.5 Pro).
* **Risk 3: Memory Thrashing on Large File Merging.**  
  * *Mitigation:* Pre-flight code analysis detects high-cardinality Cartesian joins (`merge` / `join` without index) and alerts the user before kernel OOM crashes.

---

## 7. Open Technical Decisions

1. **Inter-Process Communication (IPC) Protocol:** Evaluating ZeroMQ over Unix Domain Sockets vs. lightweight gRPC over loopback for kernel execution commands.  
   * *Status:* Benchmarking in progress; ZeroMQ yields 12ms lower execution initiation latency in preliminary spikes.
2. **Dynamic Pip Package Injection:** Whether to permit isolated, un-networked wheels to be loaded from a pre-synchronized local cache.  
   * *Status:* Slated for Architecture Spike in Sprint 3.
