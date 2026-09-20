"""
FastAPI Application Gateway for data_speaker.
Exposes REST endpoints for session management, universal file ingestion & profiling,
schema retrieval, and analytical code execution dispatch.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, FastAPI, File, HTTPException, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from services.api.agent.orchestrator import agent_orchestrator
from services.api.database import create_db_and_tables, get_db_session
from services.api.exporter import export_engine
from services.api.models import (
    ChatRequest,
    ChatTurnResponse,
    CheckpointSummaryResponse,
    CodeExecutionRequest,
    CodeExecutionResponse,
    DataFrameProfile,
    FileUploadResponse,
    RevertVersionRequest,
    RevertVersionResponse,
    Session as DbSession,
    SessionCreateResponse,
    SessionDetailResponse,
    SessionFile,
    SessionRelationsResponse,
    SqlCheckpointRequest,
    SqlQueryRequest,
    SqlQueryResponse,
)
from services.api.connectors import CONNECTORS
from services.api.profiler import clean_table_name
from services.api.session_service import DATA_DIR, SANDBOX_URL, session_service
from services.api.sql_engine import duckdb_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize database tables upon startup."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="data_speaker API Gateway",
    description="Conversational Data Analysis Platform — Gateway, Ingestion & Orchestration",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS for local web development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
def health_check() -> Dict[str, Any]:
    """Health status and configuration."""
    return {
        "status": "healthy",
        "service": "data-speaker-api",
        "sandbox_mode": "remote" if (SANDBOX_URL and SANDBOX_URL.lower() != "local") else "in-process",
        "sandbox_url": SANDBOX_URL or "in-process",
    }


@app.get("/api/v1/system/providers", tags=["System"])
def get_providers_status() -> Dict[str, Any]:
    """Inspect configured LLM providers and active credentials."""
    load_dotenv()
    gemini_key = bool(os.environ.get("GEMINI_API_KEY"))
    openai_key = bool(os.environ.get("OPENAI_API_KEY"))
    anthropic_key = bool(os.environ.get("ANTHROPIC_API_KEY"))

    active_provider = os.environ.get("LLM_PROVIDER")
    if not active_provider:
        if gemini_key:
            active_provider = "gemini"
        elif openai_key:
            active_provider = "openai"
        elif anthropic_key:
            active_provider = "anthropic"
        else:
            active_provider = "mock"

    return {
        "active_provider": active_provider,
        "providers": {
            "gemini": {
                "name": "Google Gemini",
                "configured": gemini_key,
                "default_model": os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
                "recommended_models": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
            },
            "openai": {
                "name": "OpenAI",
                "configured": openai_key,
                "default_model": os.environ.get("OPENAI_MODEL", "gpt-4o"),
                "recommended_models": ["gpt-4o", "gpt-4o-mini"],
            },
            "anthropic": {
                "name": "Anthropic Claude",
                "configured": anthropic_key,
                "default_model": os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
                "recommended_models": ["claude-3-5-sonnet-20241022"],
            },
            "mock": {
                "name": "Local Sandbox Mock",
                "configured": True,
                "default_model": "mock-deterministic",
                "recommended_models": ["mock-deterministic"],
            },
        },
    }


@app.post("/api/v1/sessions", response_model=SessionCreateResponse, status_code=status.HTTP_201_CREATED, tags=["Sessions"])
def create_session(
    payload: Optional[Dict[str, str]] = None,
    db: Session = Depends(get_db_session),
) -> SessionCreateResponse:
    """Create a new data analysis session."""
    title = (payload or {}).get("title", "Untitled Analysis")
    session_obj = session_service.create_session(db, title=title)
    return SessionCreateResponse(
        session_id=session_obj.id,
        title=session_obj.title,
        created_at=session_obj.created_at,
        status="active",
    )


@app.get("/api/v1/sessions", tags=["Sessions"])
def list_sessions(
    limit: int = 20,
    db: Session = Depends(get_db_session),
) -> List[Dict[str, Any]]:
    """List recent sessions ordered by updated_at descending."""
    sessions = db.exec(select(DbSession).order_by(DbSession.updated_at.desc()).limit(limit)).all()
    return [
        {
            "session_id": s.id,
            "title": s.title,
            "active_dataframe_version": s.active_dataframe_version,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "updated_at": s.updated_at.isoformat() if s.updated_at else None,
        }
        for s in sessions
    ]


@app.get("/api/v1/sessions/{session_id}", response_model=SessionDetailResponse, tags=["Sessions"])
def get_session(
    session_id: str,
    db: Session = Depends(get_db_session),
) -> SessionDetailResponse:
    """Retrieve session details and associated files."""
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    files = db.exec(select(SessionFile).where(SessionFile.session_id == session_id)).all()
    file_list = [
        {
            "id": f.id,
            "filename": f.filename,
            "size_bytes": f.file_size_bytes,
            "mime_type": f.mime_type,
            "created_at": f.created_at.isoformat(),
        }
        for f in files
    ]

    return SessionDetailResponse(
        session_id=session_obj.id,
        title=session_obj.title,
        active_dataframe_version=session_obj.active_dataframe_version,
        created_at=session_obj.created_at,
        updated_at=session_obj.updated_at,
        files=file_list,
    )


@app.post(
    "/api/v1/sessions/{session_id}/files/upload",
    response_model=FileUploadResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Ingestion"],
)
async def upload_file(
    session_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
) -> FileUploadResponse:
    """
    Upload a tabular dataset (CSV, TSV, Parquet, Excel, JSON, SQLite).
    Automatically sniffs delimiter/encoding, extracts privacy-safe schema profile,
    and hydrates the sandbox execution kernel.
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        session_file, profiles = await session_service.ingest_file(
            db=db,
            session_id=session_id,
            filename=file.filename or "uploaded_data.csv",
            content=content,
            mime_type=file.content_type or "application/octet-stream",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to ingest and profile file: {str(exc)}")

    return FileUploadResponse(
        file_id=session_file.id,
        filename=session_file.filename,
        size_bytes=session_file.file_size_bytes,
        mime_type=session_file.mime_type,
        storage_path=session_file.storage_path,
        profiles=profiles,
        status="ready",
    )


@app.get("/api/v1/sessions/{session_id}/schema", tags=["Schema"])
def get_session_schema(
    session_id: str,
    db: Session = Depends(get_db_session),
) -> Dict[str, Any]:
    """
    Fetch privacy-safe schema profiles for all datasets loaded in the session.
    Used by orchestrators to ground prompts without leaking raw data rows.
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    profiles = session_service.get_session_profiles(db, session_id)
    return {
        "session_id": session_id,
        "active_version": session_obj.active_dataframe_version,
        "table_count": len(profiles),
        "profiles": [p.model_dump() for p in profiles],
    }


@app.get("/api/v1/sessions/{session_id}/dataset", tags=["Data"])
def get_session_dataset(
    session_id: str,
    version_tag: Optional[str] = None,
    limit: int = 50000,
    db: Session = Depends(get_db_session),
) -> Dict[str, Any]:
    """Retrieve full tabular records and schema for virtualized data grids."""
    data = session_service.get_dataset_data(db, session_id, version_tag=version_tag, limit=limit)
    if not data:
        raise HTTPException(status_code=404, detail="No dataset found for this session/version")
    return data


@app.post("/api/v1/sessions/{session_id}/execute", response_model=CodeExecutionResponse, tags=["Execution"])
async def execute_code(
    session_id: str,
    request: CodeExecutionRequest,
    db: Session = Depends(get_db_session),
) -> CodeExecutionResponse:
    """
    Execute arbitrary Python analytical code within the session's sandbox.
    Returns stdout, stderr, execution duration, and serialized Plotly figures.
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    try:
        response = await session_service.execute_code(
            db=db,
            session_id=session_id,
            code=request.code,
            timeout=request.timeout,
        )
        return response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Execution dispatch failed: {str(exc)}")


@app.post("/api/v1/sessions/{session_id}/reset", tags=["Execution"])
async def reset_session_sandbox(
    session_id: str,
    db: Session = Depends(get_db_session),
) -> Dict[str, Any]:
    """Reset the sandbox kernel state, prune incremental checkpoints, and re-hydrate df_v0."""
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    await session_service.reset_session(db, session_id)
    return {"status": "reset", "session_id": session_id, "active_version": "df_v0"}


@app.get(
    "/api/v1/sessions/{session_id}/checkpoints",
    response_model=List[CheckpointSummaryResponse],
    tags=["Versioning"],
)
def list_session_checkpoints(
    session_id: str,
    db: Session = Depends(get_db_session),
) -> List[CheckpointSummaryResponse]:
    """List all recorded DataFrame checkpoints for a session with calculated schema diffs."""
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    return session_service.list_checkpoints(db, session_id)


@app.post(
    "/api/v1/sessions/{session_id}/revert",
    response_model=RevertVersionResponse,
    tags=["Versioning"],
)
async def revert_session_version(
    session_id: str,
    payload: RevertVersionRequest,
    db: Session = Depends(get_db_session),
) -> RevertVersionResponse:
    """Non-destructively roll back the active DataFrame to a specified checkpoint version."""
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    try:
        updated_session, profile = await session_service.revert_to_version(
            db=db,
            session_id=session_id,
            version_tag=payload.version_tag,
        )
        return RevertVersionResponse(
            status="success",
            session_id=session_id,
            active_version=updated_session.active_dataframe_version,
            profile=profile,
            message=f"Successfully restored DataFrame state to {payload.version_tag} ({profile.row_count} rows, {profile.column_count} columns).",
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Rollback failed: {str(exc)}")


@app.get("/api/v1/sessions/{session_id}/export/{export_format}", tags=["Export"])
def export_session_data(
    session_id: str,
    export_format: str,
    db: Session = Depends(get_db_session),
):
    """
    Download session data or reports.
    Supported formats:
    - 'csv': Active DataFrame as CSV
    - 'parquet': Active DataFrame as Parquet
    - 'xlsx': Active DataFrame as Excel workbook
    - 'ipynb': Fully reproducible Jupyter Notebook (.ipynb)
    - 'report': Executive Markdown analysis summary
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    fmt = export_format.lower().strip()
    try:
        if fmt in ("csv", "parquet", "xlsx", "excel"):
            content, mime_type, filename = export_engine.export_dataset(db, session_id, fmt)
        elif fmt in ("ipynb", "notebook"):
            content, mime_type, filename = export_engine.export_jupyter_notebook(db, session_id)
        elif fmt in ("report", "markdown", "md"):
            content, mime_type, filename = export_engine.export_executive_report(db, session_id)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown export format: '{export_format}'. Supported: csv, parquet, xlsx, ipynb, report.",
            )

        return Response(
            content=content,
            media_type=mime_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Export generation failed: {str(exc)}")



@app.get("/api/v1/sessions/{session_id}/dataset", tags=["Data"])
def get_dataset(
    session_id: str,
    version_tag: Optional[str] = None,
    limit: int = 50000,
    db: Session = Depends(get_db_session),
) -> Dict[str, Any]:
    """
    Retrieve high-performance tabular dataset rows and typed schema
    for headless TanStack Table and TanStack Virtual rendering.
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    data = session_service.get_dataset_data(db, session_id, version_tag=version_tag, limit=limit)
    if not data:
        return {
            "session_id": session_id,
            "total_rows": 0,
            "columns": [],
            "rows": [],
            "truncated": False,
        }
    return data


@app.post("/api/v1/sessions/{session_id}/chat", tags=["Agent"])
async def chat_with_data(
    session_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db_session),
):
    """
    Autonomous AI Analyst turn.
    - If stream=True (default): Real-time Server-Sent Events (tokens, code, execution status, stdout, charts, reflexion).
    - If stream=False: Synchronous unified JSON response.
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    if request.stream:
        return StreamingResponse(
            agent_orchestrator.run_chat_stream(
                db=db,
                session_id=session_id,
                user_prompt=request.prompt,
                max_attempts=request.max_attempts,
                provider_name=request.provider,
                model_name=request.model,
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    response_data = await agent_orchestrator.run_chat_sync(
        db=db,
        session_id=session_id,
        user_prompt=request.prompt,
        max_attempts=request.max_attempts,
        provider_name=request.provider,
        model_name=request.model,
    )
    return response_data


# ---------------------------------------------------------------------------
# DuckDB SQL Execution & Checkpoint Materialization
# ---------------------------------------------------------------------------

@app.post("/api/v1/sessions/{session_id}/sql", response_model=SqlQueryResponse, tags=["SQL"])
def execute_sql_query(
    session_id: str,
    request: SqlQueryRequest,
    db: Session = Depends(get_db_session),
) -> SqlQueryResponse:
    """
    Execute arbitrary analytical SQL on session datasets and checkpoints via DuckDB.
    Returns typed column definitions, JSON-safe rows, execution latency (ms), and row counts.
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    return duckdb_engine.execute_query(db, session_id, request.sql, limit=request.limit)


@app.post("/api/v1/sessions/{session_id}/sql/save-checkpoint", tags=["SQL"])
def save_sql_as_checkpoint(
    session_id: str,
    request: SqlCheckpointRequest,
    db: Session = Depends(get_db_session),
) -> Dict[str, Any]:
    """
    Execute a SQL query and materialize the result into a new Parquet checkpoint (df_vX).
    Updates session active version and hydrates the sandbox execution kernel.
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    try:
        ckpt, res = duckdb_engine.materialize_checkpoint_from_sql(
            db=db,
            session_id=session_id,
            sql=request.sql,
            version_tag=request.version_tag,
            summary=request.summary,
        )
        return {
            "status": "success",
            "session_id": session_id,
            "version_tag": ckpt.version_tag,
            "row_count": ckpt.row_count,
            "column_count": ckpt.column_count,
            "execution_time_ms": res.execution_time_ms,
            "message": f"Successfully created checkpoint {ckpt.version_tag} from SQL query.",
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to materialize checkpoint from SQL: {str(exc)}")


# ---------------------------------------------------------------------------
# Multi-Table Relational Schema Mapper
# ---------------------------------------------------------------------------

@app.get("/api/v1/sessions/{session_id}/relations", response_model=SessionRelationsResponse, tags=["Relations"])
def get_session_table_relations(
    session_id: str,
    db: Session = Depends(get_db_session),
) -> SessionRelationsResponse:
    """
    Infer foreign key links and join opportunities between all tables in the session.
    Used by the visual Schema Mapper canvas to render interactive connector paths.
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    return session_service.get_session_relations(db, session_id)


# ---------------------------------------------------------------------------
# Cloud Warehouse Connectors (BigQuery & Snowflake)
# ---------------------------------------------------------------------------

@app.get("/api/v1/connectors/status", tags=["Connectors"])
def get_connectors_status() -> Dict[str, Any]:
    """Inspect configured external analytical data warehouse connectors."""
    return {
        c_type: connector.get_status()
        for c_type, connector in CONNECTORS.items()
    }


@app.post("/api/v1/sessions/{session_id}/connectors/{connector_type}/import", tags=["Connectors"])
async def import_warehouse_dataset(
    session_id: str,
    connector_type: str,
    payload: Dict[str, str],
    db: Session = Depends(get_db_session),
) -> FileUploadResponse:
    """
    Execute an analytical query against a cloud warehouse (BigQuery, Snowflake),
    download the result as a Parquet table, and hydrate it into the session.
    """
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    connector = CONNECTORS.get(connector_type.lower())
    if not connector:
        raise HTTPException(status_code=400, detail=f"Unsupported warehouse connector: '{connector_type}'")

    query = payload.get("query", "SELECT * FROM sample_table LIMIT 100")
    raw_tbl_name = payload.get("table_name", f"{connector_type}_dataset")
    destination_table = clean_table_name(raw_tbl_name).replace("df_", "")

    session_dir = DATA_DIR / "sessions" / session_id
    parquet_path, profile = connector.execute_and_import(
        session_id=session_id,
        sql_query=query,
        destination_table_name=destination_table,
        target_dir=session_dir,
    )

    with open(parquet_path, "rb") as f:
        content = f.read()

    session_file, profiles = await session_service.ingest_file(
        db=db,
        session_id=session_id,
        filename=f"{destination_table}.parquet",
        content=content,
        mime_type="application/vnd.apache.parquet",
    )

    return FileUploadResponse(
        file_id=session_file.id,
        filename=session_file.filename,
        size_bytes=session_file.file_size_bytes,
        mime_type=session_file.mime_type,
        storage_path=session_file.storage_path,
        profiles=profiles,
        status="ready",
    )

