"""
Core domain models and schemas for services/api.
Includes SQLModel tables (PostgreSQL/SQLite compatible) and Pydantic schemas.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Pydantic Schemas for Schema Profiling & Analytics Context
# ---------------------------------------------------------------------------

class ColumnProfile(BaseModel):
    """Metadata profile of a single column."""
    name: str
    dtype: str
    null_count: int
    null_percentage: float
    cardinality: int
    sample_values: List[Any]

    model_config = ConfigDict(from_attributes=True)


class DataFrameProfile(BaseModel):
    """Structural schema profile of a loaded dataset (privacy-safe, no raw bulk data)."""
    session_id: str
    table_name: str = "df"
    version_tag: str = "df_v0"
    row_count: int
    column_count: int
    memory_footprint_mb: float
    columns: List[ColumnProfile]
    head_preview_markdown: str

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# SQLModel Relational Database Tables
# ---------------------------------------------------------------------------

class Session(SQLModel, table=True):
    """Conversational data analysis session."""
    __tablename__ = "sessions"

    id: str = Field(
        default_factory=lambda: f"sess_{uuid.uuid4().hex[:12]}",
        primary_key=True,
        index=True,
    )
    title: str = Field(default="Untitled Analysis")
    active_dataframe_version: str = Field(default="df_v0")
    is_archived: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class SessionFile(SQLModel, table=True):
    """File uploaded and ingested into a session."""
    __tablename__ = "session_files"

    id: str = Field(
        default_factory=lambda: f"file_{uuid.uuid4().hex[:12]}",
        primary_key=True,
        index=True,
    )
    session_id: str = Field(index=True, foreign_key="sessions.id")
    filename: str = Field(description="Original filename uploaded by the user")
    file_size_bytes: int = Field(description="File size in bytes")
    mime_type: str = Field(default="application/octet-stream")
    storage_path: str = Field(description="Local file path or S3 URI")
    schema_profile_json: str = Field(
        default="{}",
        description="JSON string representing the DataFrameProfile(s)"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def get_profiles(self) -> List[DataFrameProfile]:
        """Deserialize stored JSON profiles."""
        raw = json.loads(self.schema_profile_json)
        if isinstance(raw, list):
            return [DataFrameProfile.model_validate(p) for p in raw]
        elif isinstance(raw, dict) and raw:
            return [DataFrameProfile.model_validate(raw)]
        return []

    def set_profiles(self, profiles: List[DataFrameProfile]) -> None:
        """Serialize DataFrameProfile list to JSON string."""
        self.schema_profile_json = json.dumps([p.model_dump() for p in profiles])


class ChatTurn(SQLModel, table=True):
    """Individual analytical turn within a session."""
    __tablename__ = "chat_turns"

    id: str = Field(
        default_factory=lambda: f"trn_{uuid.uuid4().hex[:12]}",
        primary_key=True,
        index=True,
    )
    session_id: str = Field(index=True, foreign_key="sessions.id")
    user_prompt: str = Field(description="User prompt or analytical query")
    generated_code: Optional[str] = Field(default=None)
    stdout: Optional[str] = Field(default=None)
    stderr: Optional[str] = Field(default=None)
    status: str = Field(default="success")  # "success" | "error" | "timeout"
    execution_time_ms: Optional[int] = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# API Request & Response DTOs
# ---------------------------------------------------------------------------

class SessionCreateResponse(BaseModel):
    session_id: str
    title: str
    created_at: datetime
    status: str = "active"


class SessionDetailResponse(BaseModel):
    session_id: str
    title: str
    active_dataframe_version: str
    created_at: datetime
    updated_at: datetime
    files: List[Dict[str, Any]] = []


class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    size_bytes: int
    mime_type: str
    storage_path: str
    profiles: List[DataFrameProfile]
    status: str = "ready"


class CodeExecutionRequest(BaseModel):
    code: str
    timeout: int = 60


class CodeExecutionResponse(BaseModel):
    status: str  # "success" | "error" | "timeout"
    stdout: str
    stderr: str
    figures: List[Dict[str, Any]] = []
    duration_ms: int
    has_mutated_dataframe: bool = False
    df_shape: Optional[Tuple[int, int]] = None
