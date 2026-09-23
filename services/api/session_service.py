"""
Session lifecycle orchestration, sandbox coordination, and data ingestion service.
Manages session state, dataset persistence on disk, sandbox kernel hydration,
and code execution dispatch.
"""

from __future__ import annotations

import asyncio
import os
import shutil
from datetime import date, datetime, time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import polars as pl
from sqlmodel import Session, select

from services.api.models import (
    ChatTurn,
    CheckpointSummaryResponse,
    CodeExecutionResponse,
    ColumnDiff,
    DataFrameCheckpoint,
    DataFrameProfile,
    SchemaDiff,
    Session as DbSession,
    SessionFile,
    SessionRelationsResponse,
)
from services.api.profiler import (
    clean_table_name,
    generate_loader_code,
    infer_foreign_key_relations,
    profile_dataframe,
    read_file_to_dataframes,
)
from services.api.sql_engine import duckdb_engine
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

    def create_session(
        self,
        db: Session,
        title: str = "Untitled Analysis",
        workspace_id: str = "default_ws",
        created_by: Optional[str] = None,
    ) -> DbSession:
        """Create a new session record in the database."""
        session_obj = DbSession(
            title=title,
            workspace_id=workspace_id,
            created_by=created_by,
        )
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
        Save uploaded file, profile all tables, record in database, hydrate sandbox,
        and establish initial df_v0 checkpoint.
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
            print(f"[WARN] Sandbox dataset hydration warning for {filename}: {exec_res.stderr}")

        # 5. Create Initial df_v0 Checkpoint
        if profiles:
            checkpoints_dir = session_dir / "checkpoints"
            checkpoints_dir.mkdir(parents=True, exist_ok=True)
            v0_path = checkpoints_dir / "df_v0.parquet"
            target_df = table_dfs[primary_table] if primary_table in table_dfs else list(table_dfs.values())[0]
            if hasattr(target_df, "write_parquet"):
                target_df.write_parquet(v0_path)
            elif hasattr(target_df, "to_parquet"):
                target_df.to_parquet(v0_path, index=False)

            primary_prof = profiles[0]
            existing_v0 = db.exec(
                select(DataFrameCheckpoint).where(
                    DataFrameCheckpoint.session_id == session_id,
                    DataFrameCheckpoint.version_tag == "df_v0",
                )
            ).first()

            if not existing_v0:
                v0_checkpoint = DataFrameCheckpoint(
                    session_id=session_id,
                    version_tag="df_v0",
                    parquet_storage_path=str(v0_path),
                    row_count=primary_prof.row_count,
                    column_count=primary_prof.column_count,
                    memory_bytes=int(primary_prof.memory_footprint_mb * 1024 * 1024),
                    operation_summary=f"Initial ingestion of {filename}",
                )
                v0_checkpoint.set_profile(primary_prof)
                db.add(v0_checkpoint)
                db.commit()

        # 6. Synchronize DuckDB In-Memory OLAP Catalog
        try:
            duckdb_engine.refresh_catalog(db, session_id)
        except Exception as e:
            print(f"[WARN] Failed to refresh DuckDB catalog: {e}")

        return session_file, profiles

    async def create_incremental_checkpoint(
        self,
        db: Session,
        session_id: str,
        chat_turn_id: Optional[str] = None,
        operation_summary: str = "DataFrame transformation",
    ) -> Optional[DataFrameCheckpoint]:
        """
        Extract active DataFrame from sandbox, persist Parquet checkpoint,
        profile updated schema, and update active session version.
        """
        session_obj = self.get_session(db, session_id)
        if not session_obj:
            return None

        # Determine next version tag (df_v1, df_v2, ...)
        existing_checkpoints = db.exec(
            select(DataFrameCheckpoint)
            .where(DataFrameCheckpoint.session_id == session_id)
            .order_by(DataFrameCheckpoint.created_at.asc())
        ).all()
        version_num = len(existing_checkpoints)
        new_version_tag = f"df_v{version_num}"

        session_dir = DATA_DIR / "sessions" / session_id
        checkpoints_dir = session_dir / "checkpoints"
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        checkpoint_path = checkpoints_dir / f"{new_version_tag}.parquet"

        # Ask sandbox to persist active 'df' to checkpoint_path
        sandbox = self.get_or_create_sandbox_client(session_id)
        container_path = self.resolve_container_path(checkpoint_path)

        try:
            await asyncio.to_thread(sandbox.save_checkpoint, container_path)
        except Exception:
            # Fallback direct code execution
            save_code = f"df.to_parquet('{container_path}', index=False)"
            fallback_res = await asyncio.to_thread(sandbox.execute, save_code)
            if fallback_res.status != "success":
                print(f"[ERROR] Failed to save checkpoint {new_version_tag}: {fallback_res.stderr}")
                return None

        if not checkpoint_path.exists():
            return None

        import polars as pl
        pl_df = pl.read_parquet(checkpoint_path)
        new_profile = profile_dataframe(
            df=pl_df,
            session_id=session_id,
            table_name="df",
            version_tag=new_version_tag,
        )

        checkpoint_record = DataFrameCheckpoint(
            session_id=session_id,
            version_tag=new_version_tag,
            chat_turn_id=chat_turn_id,
            parquet_storage_path=str(checkpoint_path),
            row_count=new_profile.row_count,
            column_count=new_profile.column_count,
            memory_bytes=int(new_profile.memory_footprint_mb * 1024 * 1024),
            operation_summary=operation_summary,
        )
        checkpoint_record.set_profile(new_profile)
        db.add(checkpoint_record)

        session_obj.active_dataframe_version = new_version_tag
        db.add(session_obj)
        db.commit()
        db.refresh(checkpoint_record)
        return checkpoint_record

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
        Records the turn, execution performance metrics, and triggers checkpointing if mutated.
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

        # Handle mutation checkpointing
        if exec_res.has_mutated_df:
            await self.create_incremental_checkpoint(
                db=db,
                session_id=session_id,
                chat_turn_id=chat_turn.id,
                operation_summary=user_prompt[:120],
            )

        return CodeExecutionResponse(
            status=exec_res.status,
            stdout=exec_res.stdout,
            stderr=exec_res.stderr,
            figures=exec_res.figures,
            duration_ms=exec_res.duration_ms,
            has_mutated_dataframe=exec_res.has_mutated_df,
            df_shape=exec_res.df_shape,
        )

    async def revert_to_version(
        self,
        db: Session,
        session_id: str,
        version_tag: str,
    ) -> Tuple[DbSession, DataFrameProfile]:
        """
        Revert the session's active DataFrame to a previous checkpoint.
        Non-destructive: reloads parquet in sandbox, updates active version,
        logs an audit turn, and returns restored profile.
        """
        session_obj = self.get_session(db, session_id)
        if not session_obj:
            raise ValueError(f"Session '{session_id}' not found.")

        checkpoint = db.exec(
            select(DataFrameCheckpoint)
            .where(
                DataFrameCheckpoint.session_id == session_id,
                DataFrameCheckpoint.version_tag == version_tag,
            )
        ).first()
        if not checkpoint:
            raise ValueError(f"Checkpoint '{version_tag}' not found for session '{session_id}'.")

        checkpoint_path = Path(checkpoint.parquet_storage_path)
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint file does not exist on disk: {checkpoint_path}")

        sandbox = self.get_or_create_sandbox_client(session_id)
        container_path = self.resolve_container_path(checkpoint_path)

        try:
            await asyncio.to_thread(sandbox.restore_checkpoint, container_path)
        except Exception:
            restore_code = f"import pandas as pd\ndf = pd.read_parquet('{container_path}')"
            res = await asyncio.to_thread(sandbox.execute, restore_code)
            if res.status != "success":
                raise RuntimeError(f"Failed to restore checkpoint in sandbox: {res.stderr}")

        session_obj.active_dataframe_version = version_tag
        db.add(session_obj)

        profile = checkpoint.get_profile()
        if not profile:
            import polars as pl
            pl_df = pl.read_parquet(checkpoint_path)
            profile = profile_dataframe(
                df=pl_df,
                session_id=session_id,
                table_name="df",
                version_tag=version_tag,
            )

        # Record audit ChatTurn
        audit_turn = ChatTurn(
            session_id=session_id,
            user_prompt=f"[Time-Travel] Reverted active DataFrame to {version_tag}",
            stdout=f"Restored dataset state: {profile.row_count} rows, {profile.column_count} columns.",
            status="success",
        )
        db.add(audit_turn)
        db.commit()
        db.refresh(session_obj)

        return session_obj, profile

    @staticmethod
    def compute_schema_diff(
        prev_profile: Optional[DataFrameProfile],
        curr_profile: DataFrameProfile,
    ) -> SchemaDiff:
        """Calculate row/column deltas and column modifications between two versions."""
        if not prev_profile:
            return SchemaDiff(
                row_delta=curr_profile.row_count,
                column_delta=curr_profile.column_count,
                columns_added=[c.name for c in curr_profile.columns],
                columns_removed=[],
                columns_modified=[],
            )

        row_delta = curr_profile.row_count - prev_profile.row_count
        column_delta = curr_profile.column_count - prev_profile.column_count

        prev_col_map = {c.name: c.dtype for c in prev_profile.columns}
        curr_col_map = {c.name: c.dtype for c in curr_profile.columns}

        added = [col for col in curr_col_map if col not in prev_col_map]
        removed = [col for col in prev_col_map if col not in curr_col_map]

        modified: List[ColumnDiff] = []
        for col in curr_col_map:
            if col in prev_col_map and curr_col_map[col] != prev_col_map[col]:
                modified.append(
                    ColumnDiff(
                        name=col,
                        diff_type="modified",
                        old_dtype=prev_col_map[col],
                        new_dtype=curr_col_map[col],
                    )
                )

        return SchemaDiff(
            row_delta=row_delta,
            column_delta=column_delta,
            columns_added=added,
            columns_removed=removed,
            columns_modified=modified,
        )

    def list_checkpoints(self, db: Session, session_id: str) -> List[CheckpointSummaryResponse]:
        """Fetch all checkpoints for a session with calculated schema diffs."""
        session_obj = self.get_session(db, session_id)
        if not session_obj:
            return []

        checkpoints = db.exec(
            select(DataFrameCheckpoint)
            .where(DataFrameCheckpoint.session_id == session_id)
            .order_by(DataFrameCheckpoint.created_at.asc())
        ).all()

        results: List[CheckpointSummaryResponse] = []
        prev_profile: Optional[DataFrameProfile] = None

        for chk in checkpoints:
            profile = chk.get_profile()
            diff = None
            if profile:
                diff = self.compute_schema_diff(prev_profile, profile)
                prev_profile = profile

            results.append(
                CheckpointSummaryResponse(
                    id=chk.id,
                    session_id=chk.session_id,
                    version_tag=chk.version_tag,
                    operation_summary=chk.operation_summary,
                    row_count=chk.row_count,
                    column_count=chk.column_count,
                    memory_bytes=chk.memory_bytes,
                    created_at=chk.created_at,
                    is_active=(chk.version_tag == session_obj.active_dataframe_version),
                    diff_from_previous=diff,
                )
            )

        return results

    def get_session_profiles(self, db: Session, session_id: str) -> List[DataFrameProfile]:
        """Retrieve all registered DataFrameProfiles for the session."""
        session_obj = self.get_session(db, session_id)
        active_version = session_obj.active_dataframe_version if session_obj else "df_v0"

        # Check if active version has a checkpoint profile
        active_chk = db.exec(
            select(DataFrameCheckpoint)
            .where(
                DataFrameCheckpoint.session_id == session_id,
                DataFrameCheckpoint.version_tag == active_version,
            )
        ).first()
        if active_chk:
            prof = active_chk.get_profile()
            if prof:
                return [prof]

        statement = select(SessionFile).where(SessionFile.session_id == session_id)
        files = db.exec(statement).all()
        all_profiles: List[DataFrameProfile] = []
        for f in files:
            all_profiles.extend(f.get_profiles())
        return all_profiles

    def get_all_table_profiles(self, db: Session, session_id: str) -> List[DataFrameProfile]:
        """Retrieve distinct profiles for all uploaded files/tables in the session."""
        statement = select(SessionFile).where(SessionFile.session_id == session_id)
        files = db.exec(statement).all()
        profiles: List[DataFrameProfile] = []
        for f in files:
            profiles.extend(f.get_profiles())
        return profiles

    def get_session_relations(self, db: Session, session_id: str) -> SessionRelationsResponse:
        """Infer foreign key links and join opportunities between all tables in the session."""
        profiles = self.get_all_table_profiles(db, session_id)
        tables = [p.table_name for p in profiles]
        relations = infer_foreign_key_relations(profiles)
        return SessionRelationsResponse(
            session_id=session_id,
            tables=tables,
            relations=relations,
        )

    async def reset_session(self, db: Session, session_id: str) -> None:
        """Reset session: clean up checkpoints except df_v0, reset sandbox, and rehydrate initial state."""
        session_dir = DATA_DIR / "sessions" / session_id
        checkpoints_dir = session_dir / "checkpoints"
        if checkpoints_dir.exists():
            for p in checkpoints_dir.glob("*.parquet"):
                if p.name != "df_v0.parquet":
                    try:
                        p.unlink()
                    except Exception:
                        pass

        # Reset DB checkpoints except df_v0
        non_v0_chks = db.exec(
            select(DataFrameCheckpoint)
            .where(
                DataFrameCheckpoint.session_id == session_id,
                DataFrameCheckpoint.version_tag != "df_v0",
            )
        ).all()
        for chk in non_v0_chks:
            db.delete(chk)

        session_obj = self.get_session(db, session_id)
        if session_obj:
            session_obj.active_dataframe_version = "df_v0"
            db.add(session_obj)
        db.commit()

        sandbox = self.get_or_create_sandbox_client(session_id)
        await asyncio.to_thread(sandbox.reset)

        v0_path = checkpoints_dir / "df_v0.parquet"
        if v0_path.exists():
            container_path = self.resolve_container_path(v0_path)
            await asyncio.to_thread(
                sandbox.execute,
                f"import pandas as pd\ndf = pd.read_parquet('{container_path}')",
            )

    def get_dataset_data(
        self,
        db: Session,
        session_id: str,
        version_tag: Optional[str] = None,
        limit: int = 50000,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve dataset rows and column definitions for a session checkpoint."""
        session_obj = self.get_session(db, session_id)
        if not session_obj:
            return None

        target_version = version_tag or session_obj.active_dataframe_version or "df_v0"
        session_dir = DATA_DIR / "sessions" / session_id
        checkpoints_dir = session_dir / "checkpoints"
        parquet_path = checkpoints_dir / f"{target_version}.parquet"

        pdf: Optional[pd.DataFrame] = None
        if parquet_path.exists():
            try:
                df_pl = pl.read_parquet(parquet_path)
                pdf = df_pl.to_pandas()
            except Exception:
                try:
                    pdf = pd.read_parquet(parquet_path)
                except Exception:
                    pass

        if pdf is None:
            files = db.exec(select(SessionFile).where(SessionFile.session_id == session_id)).all()
            if not files:
                return None
            target_path = Path(files[0].storage_path)
            if not target_path.exists():
                return None
            try:
                table_dfs = read_file_to_dataframes(target_path, files[0].mime_type)
                first_df = list(table_dfs.values())[0]
                if hasattr(first_df, "to_pandas"):
                    pdf = first_df.to_pandas()
                else:
                    pdf = first_df
            except Exception:
                return None

        if pdf is None:
            return None

        total_rows = len(pdf)
        sliced_df = pdf.head(limit)

        columns = [
            {"name": str(col), "dtype": str(dtype)}
            for col, dtype in zip(sliced_df.columns, sliced_df.dtypes)
        ]

        records = []
        for row in sliced_df.to_dict(orient="records"):
            clean_row = {}
            for k, v in row.items():
                if pd.isna(v):
                    clean_row[k] = None
                elif isinstance(v, (datetime, date, time)):
                    clean_row[k] = v.isoformat()
                elif isinstance(v, (int, float, str, bool)):
                    clean_row[k] = v
                else:
                    clean_row[k] = str(v)
            records.append(clean_row)

        return {
            "dataset_id": f"{session_id}_{target_version}",
            "session_id": session_id,
            "version_tag": target_version,
            "total_rows": total_rows,
            "limit": limit,
            "columns": columns,
            "rows": records,
        }

    def get_active_dataframe(
        self,
        db: Session,
        session_id: str,
        version_tag: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Load the active DataFrame into pandas for diagnostics and AutoML."""
        session_obj = self.get_session(db, session_id)
        if not session_obj:
            return None

        target_version = version_tag or session_obj.active_dataframe_version or "df_v0"
        session_dir = DATA_DIR / "sessions" / session_id
        checkpoints_dir = session_dir / "checkpoints"
        parquet_path = checkpoints_dir / f"{target_version}.parquet"

        if parquet_path.exists():
            try:
                import polars as pl
                return pl.read_parquet(parquet_path).to_pandas()
            except Exception:
                try:
                    return pd.read_parquet(parquet_path)
                except Exception:
                    pass

        files = db.exec(select(SessionFile).where(SessionFile.session_id == session_id)).all()
        if not files:
            return None
        target_path = Path(files[0].storage_path)
        if not target_path.exists():
            return None

        try:
            table_dfs = read_file_to_dataframes(target_path, files[0].mime_type)
            first_df = list(table_dfs.values())[0]
            if hasattr(first_df, "to_pandas"):
                return first_df.to_pandas()
            return first_df
        except Exception:
            return None

    async def apply_hygiene_remediation(
        self,
        db: Session,
        session_id: str,
        action: str,
        column: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[DataFrameCheckpoint, DataFrameProfile, str]:
        """
        Execute smart data hygiene remediation in sandbox, materialize a new versioned
        checkpoint (df_vX), record audit ChatTurn, and refresh DuckDB catalog.
        """
        params = parameters or {}
        code_lines = []

        if action == "impute_median" and column:
            code_lines.append(f"df['{column}'] = df['{column}'].fillna(df['{column}'].median())")
        elif action == "impute_mean" and column:
            code_lines.append(f"df['{column}'] = df['{column}'].fillna(df['{column}'].mean())")
        elif action == "impute_mode" and column:
            code_lines.append(
                f"df['{column}'] = df['{column}'].fillna(df['{column}'].mode()[0] if not df['{column}'].mode().empty else 'Unknown')"
            )
        elif action == "drop_missing" and column:
            code_lines.append(f"df = df.dropna(subset=['{column}']).reset_index(drop=True)")
        elif action == "drop_column" and column:
            code_lines.append(f"df = df.drop(columns=['{column}'])")
        elif action == "drop_duplicates":
            code_lines.append("df = df.drop_duplicates().reset_index(drop=True)")
        elif action == "clip_outliers" and column:
            lower = params.get("lower", 0)
            upper = params.get("upper", 100)
            code_lines.append(f"df['{column}'] = df['{column}'].clip(lower={lower}, upper={upper})")
        elif action == "log_transform" and column:
            code_lines.append("import numpy as np")
            code_lines.append(f"df['{column}_log'] = np.log1p(df['{column}'])")
        else:
            raise ValueError(f"Unsupported hygiene action '{action}' on column '{column}'")

        python_code = "\n".join(code_lines)

        sandbox = self.get_or_create_sandbox_client(session_id)
        exec_res = await asyncio.to_thread(sandbox.execute, python_code)
        if exec_res.status != "success":
            raise RuntimeError(f"Hygiene execution failed: {exec_res.stderr}")

        summary = f"Smart Hygiene: {action} on {column or 'dataset'}"
        checkpoint = await self.create_incremental_checkpoint(
            db=db,
            session_id=session_id,
            operation_summary=summary,
        )

        if not checkpoint:
            raise RuntimeError("Failed to create checkpoint after applying hygiene remediation.")

        profile = checkpoint.get_profile()

        # Record audit ChatTurn
        audit_turn = ChatTurn(
            session_id=session_id,
            user_prompt=f"[Smart Hygiene] Applied {action} on {column or 'dataset'}",
            generated_code=python_code,
            stdout=f"Hygiene remediation applied successfully. Materialized version {checkpoint.version_tag}.",
            status="success",
        )
        db.add(audit_turn)
        db.commit()

        # Refresh DuckDB catalog
        try:
            duckdb_engine.refresh_catalog(db, session_id)
        except Exception:
            pass

        return checkpoint, profile, python_code


# Global service instance
session_service = SessionService()

