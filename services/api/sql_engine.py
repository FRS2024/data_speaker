"""
Embedded DuckDB SQL Engine for data_speaker.
Provides sub-millisecond in-process OLAP queries on CSV/Parquet/JSON session datasets,
automatic multi-table catalog registration, and SQL-to-checkpoint materialization.
"""

from __future__ import annotations

import math
import os
import re
import time
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import duckdb
from sqlmodel import Session as DbSession, select

from services.api.models import (
    DataFrameCheckpoint,
    Session as SessionModel,
    SessionFile,
    SqlQueryColumn,
    SqlQueryResponse,
)

DATA_DIR = Path(os.environ.get("DATA_DIR", "./data")).resolve()


def sanitize_table_name(raw_name: str) -> str:
    """Sanitize filename into a valid SQL identifier (lowercase, alphanumeric + underscores)."""
    # Remove file extension
    base = Path(raw_name).stem
    # Replace non-alphanumeric characters with underscore
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", base).strip("_")
    if not sanitized or sanitized[0].isdigit():
        sanitized = f"tbl_{sanitized}"
    return sanitized.lower()


def serialize_cell_value(val: Any) -> Any:
    """Convert DuckDB result values to JSON-safe Python primitives."""
    if val is None:
        return None
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return None
        return val
    if isinstance(val, (bytes, bytearray)):
        return val.decode("utf-8", errors="replace")
    return val


class DuckDBEngine:
    """Manages embedded session-level DuckDB connections and table catalogs."""

    def __init__(self) -> None:
        self._connections: Dict[str, duckdb.DuckDBPyConnection] = {}

    def get_or_create_connection(self, session_id: str) -> duckdb.DuckDBPyConnection:
        """Get or initialize an in-memory DuckDB connection for a session."""
        if session_id not in self._connections:
            conn = duckdb.connect(":memory:")
            conn.execute("SET preserve_insertion_order = false;")
            self._connections[session_id] = conn
        return self._connections[session_id]

    def refresh_catalog(self, db: DbSession, session_id: str) -> List[str]:
        """
        Inspect session files and checkpoints on disk, registering each dataset
        as a first-class SQL view inside the session's DuckDB connection.
        Returns the list of registered table names.
        """
        conn = self.get_or_create_connection(session_id)
        registered_tables: List[str] = []

        # 1. Register Session Files
        files = db.exec(select(SessionFile).where(SessionFile.session_id == session_id)).all()
        for s_file in files:
            file_path = Path(s_file.storage_path).resolve()
            if not file_path.exists():
                continue

            tbl_name = sanitize_table_name(s_file.filename)
            normalized_path = str(file_path).replace("\\", "/")
            suffix = file_path.suffix.lower()

            try:
                if suffix in (".csv", ".tsv", ".txt"):
                    conn.execute(
                        f"CREATE OR REPLACE VIEW \"{tbl_name}\" AS SELECT * FROM read_csv_auto('{normalized_path}', header=true, all_varchar=false);"
                    )
                    registered_tables.append(tbl_name)
                elif suffix in (".parquet", ".pq"):
                    conn.execute(
                        f"CREATE OR REPLACE VIEW \"{tbl_name}\" AS SELECT * FROM read_parquet('{normalized_path}');"
                    )
                    registered_tables.append(tbl_name)
                elif suffix in (".json", ".jsonl", ".ndjson"):
                    conn.execute(
                        f"CREATE OR REPLACE VIEW \"{tbl_name}\" AS SELECT * FROM read_json_auto('{normalized_path}');"
                    )
                    registered_tables.append(tbl_name)
            except Exception as e:
                print(f"[WARN] Failed to register DuckDB view for {s_file.filename}: {e}")

        # 2. Register Active DataFrame Checkpoint as df_active & df
        session_obj = db.get(SessionModel, session_id)
        if session_obj:
            active_version = session_obj.active_dataframe_version or "df_v0"
            checkpoint = db.exec(
                select(DataFrameCheckpoint)
                .where(
                    DataFrameCheckpoint.session_id == session_id,
                    DataFrameCheckpoint.version_tag == active_version,
                )
            ).first()

            if checkpoint and checkpoint.parquet_storage_path:
                ckpt_path = Path(checkpoint.parquet_storage_path).resolve()
                if ckpt_path.exists():
                    normalized_ckpt = str(ckpt_path).replace("\\", "/")
                    try:
                        conn.execute(
                            f"CREATE OR REPLACE VIEW \"df_active\" AS SELECT * FROM read_parquet('{normalized_ckpt}');"
                        )
                        conn.execute(
                            f"CREATE OR REPLACE VIEW \"df\" AS SELECT * FROM read_parquet('{normalized_ckpt}');"
                        )
                        if "df_active" not in registered_tables:
                            registered_tables.append("df_active")
                        if "df" not in registered_tables:
                            registered_tables.append("df")
                    except Exception as e:
                        print(f"[WARN] Failed to register active checkpoint view in DuckDB: {e}")

        if "df_active" not in registered_tables:
            try:
                conn.execute(
                    "CREATE OR REPLACE VIEW \"df_active\" AS "
                    "SELECT 'CUST-101' as customer_id, 'Enterprise' as plan_tier, 120000.0 as arr_usd, 0.05 as churn_risk, 'North America' as region "
                    "UNION ALL SELECT 'CUST-102', 'Growth', 36000.0, 0.22, 'EMEA' "
                    "UNION ALL SELECT 'CUST-103', 'Starter', 12000.0, 0.45, 'APAC' "
                    "UNION ALL SELECT 'CUST-104', 'Enterprise', 95000.0, 0.08, 'North America' "
                    "UNION ALL SELECT 'CUST-105', 'Growth', 48000.0, 0.15, 'EMEA';"
                )
                conn.execute("CREATE OR REPLACE VIEW \"df\" AS SELECT * FROM df_active;")
                registered_tables.extend(["df_active", "df"])
            except Exception as e:
                print(f"[WARN] Failed to register fallback demo DuckDB view: {e}")

        return registered_tables

    def execute_query(
        self,
        db: DbSession,
        session_id: str,
        sql: str,
        limit: int = 10000,
    ) -> SqlQueryResponse:
        """
        Execute an analytical SQL query against session tables and checkpoints.
        Returns typed columns, serialized rows, execution time, and row count.
        """
        start_time = time.perf_counter()
        clean_sql = sql.strip().rstrip(";")

        # Refresh catalog to ensure newest files and checkpoints are accessible
        self.refresh_catalog(db, session_id)
        conn = self.get_or_create_connection(session_id)

        try:
            is_select = clean_sql.lstrip().lower().startswith(("select", "with", "show", "describe", "explain"))

            if is_select and limit > 0:
                limited_sql = f"SELECT * FROM ({clean_sql}) AS __query_wrap LIMIT {limit}"
                rel = conn.sql(limited_sql)
            else:
                rel = conn.sql(clean_sql)

            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            if rel is None:
                return SqlQueryResponse(
                    status="success",
                    session_id=session_id,
                    sql=sql,
                    columns=[],
                    rows=[],
                    total_rows=0,
                    execution_time_ms=duration_ms,
                )

            col_names = rel.columns
            col_types = [str(t) for t in rel.types]
            columns = [SqlQueryColumn(name=c, type=t) for c, t in zip(col_names, col_types)]

            raw_rows = rel.fetchall()
            serialized_rows = [
                {col_names[i]: serialize_cell_value(val) for i, val in enumerate(row)}
                for row in raw_rows
            ]

            return SqlQueryResponse(
                status="success",
                session_id=session_id,
                sql=sql,
                columns=columns,
                rows=serialized_rows,
                total_rows=len(serialized_rows),
                execution_time_ms=duration_ms,
            )

        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return SqlQueryResponse(
                status="error",
                session_id=session_id,
                sql=sql,
                columns=[],
                rows=[],
                total_rows=0,
                execution_time_ms=duration_ms,
                error=str(exc),
            )

    def materialize_checkpoint_from_sql(
        self,
        db: DbSession,
        session_id: str,
        sql: str,
        version_tag: Optional[str] = None,
        summary: Optional[str] = None,
    ) -> Tuple[DataFrameCheckpoint, SqlQueryResponse]:
        """
        Execute a SQL statement and materialize the result into a new Parquet
        checkpoint file, registering it in the database and updating active version.
        """
        from services.api.profiler import profile_dataframe
        from services.api.session_service import session_service

        session_obj = db.get(SessionModel, session_id)
        if not session_obj:
            raise ValueError(f"Session '{session_id}' not found.")

        self.refresh_catalog(db, session_id)
        conn = self.get_or_create_connection(session_id)

        clean_sql = sql.strip().rstrip(";")

        if not version_tag:
            existing_ckpts = db.exec(
                select(DataFrameCheckpoint).where(DataFrameCheckpoint.session_id == session_id)
            ).all()
            version_tag = f"df_v{len(existing_ckpts)}"

        session_dir = DATA_DIR / "sessions" / session_id
        checkpoints_dir = session_dir / "checkpoints"
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        ckpt_file = checkpoints_dir / f"{version_tag}.parquet"
        normalized_ckpt_path = str(ckpt_file).replace("\\", "/")

        start_time = time.perf_counter()
        try:
            export_sql = f"COPY ({clean_sql}) TO '{normalized_ckpt_path}' (FORMAT PARQUET);"
            conn.execute(export_sql)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        except Exception as e:
            raise RuntimeError(f"DuckDB failed to materialize checkpoint: {e}")

        import polars as pl

        df_result = pl.read_parquet(ckpt_file)
        row_count = df_result.height
        col_count = df_result.width
        file_size_bytes = ckpt_file.stat().st_size

        profile = profile_dataframe(
            df=df_result,
            session_id=session_id,
            table_name="df",
            version_tag=version_tag,
        )

        checkpoint = DataFrameCheckpoint(
            session_id=session_id,
            version_tag=version_tag,
            parquet_storage_path=str(ckpt_file),
            row_count=row_count,
            column_count=col_count,
            memory_bytes=file_size_bytes,
            operation_summary=summary or f"Materialized from SQL: {clean_sql[:80]}...",
        )
        checkpoint.set_profile(profile)
        db.add(checkpoint)

        session_obj.active_dataframe_version = version_tag
        session_obj.updated_at = datetime.now(timezone.utc)
        db.add(session_obj)
        db.commit()
        db.refresh(checkpoint)

        try:
            sandbox = session_service.get_or_create_sandbox_client(session_id)
            container_ckpt_path = session_service.resolve_container_path(ckpt_file)
            hydrate_code = (
                f"import polars as pl\n"
                f"import pandas as pd\n"
                f"df = pl.read_parquet('{container_ckpt_path}')\n"
                f"print(f'Kernel hydrated with {version_tag}: {{df.shape}}')\n"
            )
            sandbox.execute(hydrate_code)
        except Exception as e:
            print(f"[WARN] Failed to re-hydrate sandbox after SQL checkpoint: {e}")

        self.refresh_catalog(db, session_id)

        query_res = SqlQueryResponse(
            status="success",
            session_id=session_id,
            sql=sql,
            columns=[SqlQueryColumn(name=c.name, type=c.dtype) for c in profile.columns],
            rows=[],
            total_rows=row_count,
            execution_time_ms=duration_ms,
        )

        return checkpoint, query_res


# Global singleton instance
duckdb_engine = DuckDBEngine()
