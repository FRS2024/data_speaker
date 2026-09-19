"""
Session lifecycle orchestration, sandbox coordination, and data ingestion service.
Manages session state, dataset persistence on disk, sandbox kernel hydration,
and code execution dispatch.
"""

from __future__ import annotations

import asyncio
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from sqlmodel import Session, select

from services.api.models import (
    ChatTurn,
    CodeExecutionResponse,
    DataFrameProfile,
    Session as DbSession,
    SessionFile,
)
from services.api.profiler import (
    generate_loader_code,
    profile_dataframe,
    read_file_to_dataframes,
)
from services.sandbox.client import BaseSandboxClient, LocalSandboxClient, RemoteSandboxClient

# Base data storage directory on host
DATA_DIR = Path(os.environ.get("DATA_DIR", "./data")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Container data mount prefix (used when sandbox is running in Docker)
CONTAINER_DATA_PREFIX = os.environ.get("CONTAINER_DATA_PREFIX", "/data")

# Sandbox URL: if set, use RemoteSandboxClient; if "local" or empty, use LocalSandboxClient
SANDBOX_URL = os.environ.get("SANDBOX_URL", "").strip()


class SessionService:
    """Orchestrates sessions, sandbox execution kernels, and dataset persistence."""

    def __init__(self) -> None:
        # Cache of active sandbox clients per session_id (especially for LocalSandboxClient)
        self._sandbox_clients: Dict[str, BaseSandboxClient] = {}

    def get_or_create_sandbox_client(self, session_id: str) -> BaseSandboxClient:
        """
        Get or initialize a sandbox client for the given session.
        Uses RemoteSandboxClient if SANDBOX_URL is set, otherwise LocalSandboxClient.
        """
        if session_id in self._sandbox_clients:
            return self._sandbox_clients[session_id]

        if SANDBOX_URL and SANDBOX_URL.lower() != "local":
            client = RemoteSandboxClient(base_url=SANDBOX_URL)
        else:
            client = LocalSandboxClient()

        self._sandbox_clients[session_id] = client
        return client

    def create_session(self, db: Session, title: str = "Untitled Analysis") -> DbSession:
        """Create a new session record in the database."""
        session_obj = DbSession(title=title)
        db.add(session_obj)
        db.commit()
        db.refresh(session_obj)

        # Create session data directory
        session_dir = DATA_DIR / "sessions" / session_obj.id
        session_dir.mkdir(parents=True, exist_ok=True)

        return session_obj

    def get_session(self, db: Session, session_id: str) -> Optional[DbSession]:
        """Fetch session by ID."""
        return db.get(DbSession, session_id)

    def resolve_container_path(self, local_path: Path) -> str:
        """
        Convert a local filesystem path to the equivalent container mount path
        if running against a remote/dockerized sandbox.
        """
        if SANDBOX_URL and SANDBOX_URL.lower() != "local":
            try:
                rel = local_path.relative_to(DATA_DIR)
                # Normalize forward slashes for Linux container path
                clean_rel = str(rel).replace("\\", "/")
                return f"{CONTAINER_DATA_PREFIX}/{clean_rel}"
            except ValueError:
                # If path is not inside DATA_DIR, return normalized path
                return str(local_path).replace("\\", "/")
        return str(local_path.resolve()).replace("\\", "/")

    async def ingest_file(
        self,
        db: Session,
        session_id: str,
        filename: str,
        content: bytes,
        mime_type: str = "application/octet-stream",
    ) -> Tuple[SessionFile, List[DataFrameProfile]]:
        """
        Save uploaded file, profile all tables, record in database, and hydrate sandbox.
        """
        session_obj = self.get_session(db, session_id)
        if not session_obj:
            raise ValueError(f"Session '{session_id}' not found.")

        # 1. Save file to disk in session workspace
        session_dir = DATA_DIR / "sessions" / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        file_path = session_dir / filename

        with open(file_path, "wb") as f:
            f.write(content)

        file_size_bytes = len(content)

        # 2. Extract DataFrames & Profile Schemas
        table_dfs = read_file_to_dataframes(file_path)
        profiles: List[DataFrameProfile] = []

        for table_name, df in table_dfs.items():
            profile = profile_dataframe(
                df=df,
                session_id=session_id,
                table_name=table_name,
                version_tag=session_obj.active_dataframe_version,
            )
            profiles.append(profile)

        # 3. Store SessionFile Record
        session_file = SessionFile(
            session_id=session_id,
            filename=filename,
            file_size_bytes=file_size_bytes,
            mime_type=mime_type,
            storage_path=str(file_path),
        )
        session_file.set_profiles(profiles)
        db.add(session_file)
        db.commit()
        db.refresh(session_file)

        # 4. Hydrate Sandbox Kernel
        sandbox = self.get_or_create_sandbox_client(session_id)
        container_path = self.resolve_container_path(file_path)
        primary_table = profiles[0].table_name if profiles else "df_data"

        loader_code = generate_loader_code(
            file_path=file_path,
            table_name=primary_table,
            container_mount_path=container_path,
        )

        exec_res = await asyncio.to_thread(sandbox.execute, loader_code)
        if exec_res.status != "success":
            # Log warning or error but do not fail upload; include stderr in logs
            print(f"[WARN] Sandbox dataset hydration warning for {filename}: {exec_res.stderr}")

        return session_file, profiles

    async def execute_code(
        self,
        db: Session,
        session_id: str,
        code: str,
        timeout: int = 60,
        user_prompt: str = "User execution request",
    ) -> CodeExecutionResponse:
        """
        Execute arbitrary Python analytical code inside the session's sandbox.
        Records the turn and execution performance metrics in the database.
        """
        session_obj = self.get_session(db, session_id)
        if not session_obj:
            raise ValueError(f"Session '{session_id}' not found.")

        sandbox = self.get_or_create_sandbox_client(session_id)
        exec_res = await asyncio.to_thread(sandbox.execute, code, timeout_seconds=timeout)

        # Record ChatTurn in DB
        chat_turn = ChatTurn(
            session_id=session_id,
            user_prompt=user_prompt,
            generated_code=code,
            stdout=exec_res.stdout,
            stderr=exec_res.stderr,
            status=exec_res.status,
            execution_time_ms=exec_res.duration_ms,
        )
        db.add(chat_turn)
        db.commit()

        return CodeExecutionResponse(
            status=exec_res.status,
            stdout=exec_res.stdout,
            stderr=exec_res.stderr,
            figures=exec_res.figures,
            duration_ms=exec_res.duration_ms,
            has_mutated_dataframe=exec_res.has_mutated_df,
            df_shape=exec_res.df_shape,
        )

    def get_session_profiles(self, db: Session, session_id: str) -> List[DataFrameProfile]:
        """Retrieve all registered DataFrameProfiles for the session."""
        statement = select(SessionFile).where(SessionFile.session_id == session_id)
        files = db.exec(statement).all()
        all_profiles: List[DataFrameProfile] = []
        for f in files:
            all_profiles.extend(f.get_profiles())
        return all_profiles


# Global service instance
session_service = SessionService()
