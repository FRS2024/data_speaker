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


class DataFrameCheckpoint(SQLModel, table=True):
    """Immutable copy-on-write snapshot of a DataFrame state."""
    __tablename__ = "dataframe_checkpoints"

    id: str = Field(
        default_factory=lambda: f"chk_{uuid.uuid4().hex[:12]}",
        primary_key=True,
        index=True,
    )
    session_id: str = Field(index=True, foreign_key="sessions.id")
    version_tag: str = Field(description="e.g. df_v0, df_v1, df_v2", index=True)
    chat_turn_id: Optional[str] = Field(default=None)
    parquet_storage_path: str = Field(description="Local path or S3 URI of Parquet snapshot")
    row_count: int = Field(default=0)
    column_count: int = Field(default=0)
    memory_bytes: int = Field(default=0)
    operation_summary: str = Field(default="Initial dataset upload", description="Prompt or operation description")
    schema_profile_json: str = Field(
        default="{}",
        description="JSON string representing the DataFrameProfile at this version"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def get_profile(self) -> Optional[DataFrameProfile]:
        """Deserialize stored profile."""
        if not self.schema_profile_json or self.schema_profile_json == "{}":
            return None
        return DataFrameProfile.model_validate_json(self.schema_profile_json)

    def set_profile(self, profile: DataFrameProfile) -> None:
        """Serialize DataFrameProfile."""
        self.schema_profile_json = profile.model_dump_json()


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


class ChatRequest(BaseModel):
    prompt: str
    stream: bool = True
    max_attempts: int = 3
    provider: Optional[str] = None
    model: Optional[str] = None


class ChatTurnResponse(BaseModel):
    status: str
    turn_id: Optional[str] = None
    explanation: Optional[str] = None
    code: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    figures: List[Dict[str, Any]] = []
    reflexion_count: int = 0
    duration_ms: int = 0
    has_mutated_df: bool = False
    df_shape: Optional[Tuple[int, int]] = None
    active_version: str = "df_v0"
    error: Optional[str] = None
    detail: Optional[str] = None


class ColumnDiff(BaseModel):
    name: str
    diff_type: str  # "added" | "removed" | "modified"
    old_dtype: Optional[str] = None
    new_dtype: Optional[str] = None


class SchemaDiff(BaseModel):
    row_delta: int
    column_delta: int
    columns_added: List[str] = []
    columns_removed: List[str] = []
    columns_modified: List[ColumnDiff] = []


class CheckpointSummaryResponse(BaseModel):
    id: str
    session_id: str
    version_tag: str
    operation_summary: str
    row_count: int
    column_count: int
    memory_bytes: int
    created_at: datetime
    is_active: bool = False
    diff_from_previous: Optional[SchemaDiff] = None


class RevertVersionRequest(BaseModel):
    version_tag: str


class RevertVersionResponse(BaseModel):
    status: str
    session_id: str
    active_version: str
    profile: DataFrameProfile
    message: str


# ---------------------------------------------------------------------------
# DuckDB SQL Execution & Relational Mapper Models
# ---------------------------------------------------------------------------

class SqlQueryRequest(BaseModel):
    sql: str
    limit: int = 10000


class SqlQueryColumn(BaseModel):
    name: str
    type: str


class SqlQueryResponse(BaseModel):
    status: str = "success"
    session_id: str
    sql: str
    columns: List[SqlQueryColumn] = []
    rows: List[Dict[str, Any]] = []
    total_rows: int = 0
    execution_time_ms: float = 0.0
    error: Optional[str] = None


class SqlCheckpointRequest(BaseModel):
    sql: str
    version_tag: Optional[str] = None
    summary: Optional[str] = None


class ForeignKeyRelation(BaseModel):
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    confidence: float = 1.0
    suggested_join_type: str = "INNER JOIN"


class SessionRelationsResponse(BaseModel):
    session_id: str
    tables: List[str] = []
    relations: List[ForeignKeyRelation] = []

