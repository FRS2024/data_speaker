"""
FastAPI Application Gateway for data_speaker.
Exposes REST endpoints for session management, universal file ingestion & profiling,
schema retrieval, and analytical code execution dispatch.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from services.api.database import create_db_and_tables, get_db_session
from services.api.models import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    DataFrameProfile,
    FileUploadResponse,
    Session as DbSession,
    SessionCreateResponse,
    SessionDetailResponse,
    SessionFile,
)
from services.api.session_service import SANDBOX_URL, session_service


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
    """Reset the sandbox kernel state and re-hydrate loaded datasets."""
    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    sandbox = session_service.get_or_create_sandbox_client(session_id)
    await asyncio.to_thread(sandbox.reset)
    return {"status": "reset", "session_id": session_id}
