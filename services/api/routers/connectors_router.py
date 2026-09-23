"""
Connectors Router: Enterprise Warehouse & Lakehouse Connectors Studio.
Manages connections, schema discovery, table previews, and Parquet data sync
for PostgreSQL, Google BigQuery, Snowflake, and Databricks Lakehouse.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from services.api.auth import AuthContext, get_auth_context, require_role
from services.api.connectors import CONNECTORS
from services.api.database import get_db_session
from services.api.models import (
    ColumnProfile,
    WarehouseConfigRequest,
    WarehouseConfigResponse,
    WarehouseConnectionConfig,
    WarehouseConnectorSummary,
    WarehouseSchemaTreeResponse,
    WarehouseSyncRequest,
    WarehouseTableListResponse,
    WarehouseTablePreviewResponse,
    WarehouseTestRequest,
    WarehouseTestResponse,
)
from services.api.profiler import clean_table_name
from services.api.session_service import DATA_DIR, session_service

router = APIRouter(prefix="/api/v1/connectors", tags=["connectors"])


CONNECTOR_METADATA = {
    "postgres": {
        "name": "PostgreSQL (Neon / Supabase / RDS)",
        "description": "Connect to operational or analytical PostgreSQL databases, Cloud SQL, Neon, or Supabase.",
        "supported_features": ["schema_discovery", "cross_schema_joins", "pushdown_sql", "parquet_export", "ssl_encryption"],
    },
    "bigquery": {
        "name": "Google BigQuery",
        "description": "Serverless multi-cloud data warehouse with ultra-fast petabyte SQL execution.",
        "supported_features": ["schema_discovery", "partition_scanning", "pushdown_sql", "parquet_export"],
    },
    "snowflake": {
        "name": "Snowflake Data Cloud",
        "description": "Elastic data warehouse for high-concurrency analytical and reporting workloads.",
        "supported_features": ["schema_discovery", "virtual_warehouse_querying", "pushdown_sql", "parquet_export"],
    },
    "databricks": {
        "name": "Databricks Lakehouse (Unity Catalog)",
        "description": "Open lakehouse architecture combining data lakes and warehouses via Delta Lake.",
        "supported_features": ["unity_catalog", "delta_lake_time_travel", "serverless_sql", "parquet_export", "photon_acceleration"],
    },
}


def _get_active_vault_config(db: Session, workspace_id: str, connector_type: str) -> Optional[Dict[str, Any]]:
    """Retrieve decrypted/raw connection config dictionary from workspace vault."""
    record = db.exec(
        select(WarehouseConnectionConfig).where(
            WarehouseConnectionConfig.workspace_id == workspace_id,
            WarehouseConnectionConfig.connector_type == connector_type,
        ).order_by(WarehouseConnectionConfig.updated_at.desc())
    ).first()
    return record.get_config() if record else None


@router.get("", response_model=List[WarehouseConnectorSummary])
def list_connectors(
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db_session),
) -> List[WarehouseConnectorSummary]:
    """List all available warehouse connectors, their configuration status, and saved credentials."""
    summaries: List[WarehouseConnectorSummary] = []

    for c_type in ["postgres", "bigquery", "snowflake", "databricks"]:
        connector = CONNECTORS.get(c_type)
        meta = CONNECTOR_METADATA.get(c_type, {})
        
        # Look up saved configs in current workspace
        saved_records = db.exec(
            select(WarehouseConnectionConfig).where(
                WarehouseConnectionConfig.workspace_id == ctx.workspace.id,
                WarehouseConnectionConfig.connector_type == c_type,
            ).order_by(WarehouseConnectionConfig.created_at.desc())
        ).all()

        saved_configs = [
            WarehouseConfigResponse(
                id=rec.id,
                connector_type=rec.connector_type,
                name=rec.name,
                masked_config=rec.get_masked_config(),
                created_at=rec.created_at,
                updated_at=rec.updated_at,
            )
            for rec in saved_records
        ]

        active_cfg = saved_records[0].get_config() if saved_records else None
        status_info = connector.get_status(active_cfg) if connector else {}
        is_cfg = bool(saved_records or (connector and connector.is_configured))

        mode = "connected" if is_cfg else "demo_sandbox"

        summaries.append(
            WarehouseConnectorSummary(
                connector_type=c_type,
                name=meta.get("name", c_type.capitalize()),
                configured=is_cfg,
                mode=mode,
                description=meta.get("description", ""),
                supported_features=meta.get("supported_features", []),
                saved_configs=saved_configs,
            )
        )

    return summaries


@router.post("/test", response_model=WarehouseTestResponse)
def test_connector_connection(
    req: WarehouseTestRequest,
    ctx: AuthContext = Depends(get_auth_context),
) -> WarehouseTestResponse:
    """Validate connection credentials against the specified cloud warehouse."""
    connector = CONNECTORS.get(req.connector_type)
    if not connector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Connector '{req.connector_type}' is not supported.",
        )

    result = connector.test_connection(req.config)
    return WarehouseTestResponse(
        status=result.get("status", "mock_mode"),
        message=result.get("message", "Test completed"),
        latency_ms=result.get("latency_ms", 10.0),
        details=result.get("details"),
    )


@router.post("/config", response_model=WarehouseConfigResponse)
def save_connector_config(
    req: WarehouseConfigRequest,
    ctx: AuthContext = Depends(require_role("analyst")),
    db: Session = Depends(get_db_session),
) -> WarehouseConfigResponse:
    """Save or update warehouse credentials in the workspace vault."""
    if req.connector_type not in CONNECTORS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid connector type: {req.connector_type}",
        )

    # Check for existing config with same name or connector_type
    existing = db.exec(
        select(WarehouseConnectionConfig).where(
            WarehouseConnectionConfig.workspace_id == ctx.workspace.id,
            WarehouseConnectionConfig.connector_type == req.connector_type,
            WarehouseConnectionConfig.name == req.name,
        )
    ).first()

    now = datetime.now(timezone.utc)
    if existing:
        existing.config_json = json.dumps(req.config)
        existing.updated_at = now
        db.add(existing)
        db.commit()
        db.refresh(existing)
        record = existing
    else:
        record = WarehouseConnectionConfig(
            workspace_id=ctx.workspace.id,
            connector_type=req.connector_type,
            name=req.name,
            config_json=json.dumps(req.config),
            created_at=now,
            updated_at=now,
        )
        db.add(record)
        db.commit()
        db.refresh(record)

    return WarehouseConfigResponse(
        id=record.id,
        connector_type=record.connector_type,
        name=record.name,
        masked_config=record.get_masked_config(),
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


@router.get("/config/{connector_type}", response_model=List[WarehouseConfigResponse])
def get_connector_configs(
    connector_type: str,
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db_session),
) -> List[WarehouseConfigResponse]:
    """Retrieve saved connection profiles for a connector within the current workspace."""
    records = db.exec(
        select(WarehouseConnectionConfig).where(
            WarehouseConnectionConfig.workspace_id == ctx.workspace.id,
            WarehouseConnectionConfig.connector_type == connector_type,
        ).order_by(WarehouseConnectionConfig.created_at.desc())
    ).all()

    return [
        WarehouseConfigResponse(
            id=r.id,
            connector_type=r.connector_type,
            name=r.name,
            masked_config=r.get_masked_config(),
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in records
    ]


@router.delete("/config/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connector_config(
    config_id: str,
    ctx: AuthContext = Depends(require_role("analyst")),
    db: Session = Depends(get_db_session),
) -> None:
    """Remove a connection profile from the workspace vault."""
    record = db.get(WarehouseConnectionConfig, config_id)
    if not record or record.workspace_id != ctx.workspace.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection profile not found in current workspace.",
        )
    db.delete(record)
    db.commit()


@router.get("/{connector_type}/schemas", response_model=WarehouseSchemaTreeResponse)
def list_connector_schemas(
    connector_type: str,
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db_session),
) -> WarehouseSchemaTreeResponse:
    """List accessible schemas, datasets, or databases for the connector."""
    connector = CONNECTORS.get(connector_type)
    if not connector:
        raise HTTPException(status_code=404, detail=f"Connector '{connector_type}' not found.")

    vault_cfg = _get_active_vault_config(db, ctx.workspace.id, connector_type)
    schemas = connector.list_datasets(vault_cfg)
    return WarehouseSchemaTreeResponse(
        connector_type=connector_type,
        schemas=schemas,
    )


@router.get("/{connector_type}/schemas/{schema_name}/tables", response_model=WarehouseTableListResponse)
def list_connector_tables(
    connector_type: str,
    schema_name: str,
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db_session),
) -> WarehouseTableListResponse:
    """List tables within the specified schema or dataset."""
    connector = CONNECTORS.get(connector_type)
    if not connector:
        raise HTTPException(status_code=404, detail=f"Connector '{connector_type}' not found.")

    vault_cfg = _get_active_vault_config(db, ctx.workspace.id, connector_type)
    tables = connector.list_tables(schema_name, vault_cfg)
    return WarehouseTableListResponse(
        connector_type=connector_type,
        schema_name=schema_name,
        tables=tables,
    )


@router.get("/{connector_type}/schemas/{schema_name}/tables/{table_name}/preview", response_model=WarehouseTablePreviewResponse)
def preview_connector_table(
    connector_type: str,
    schema_name: str,
    table_name: str,
    limit: int = Query(default=50, ge=1, le=100),
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db_session),
) -> WarehouseTablePreviewResponse:
    """Preview schema columns and sample rows from an external warehouse table."""
    connector = CONNECTORS.get(connector_type)
    if not connector:
        raise HTTPException(status_code=404, detail=f"Connector '{connector_type}' not found.")

    vault_cfg = _get_active_vault_config(db, ctx.workspace.id, connector_type)
    preview = connector.preview_table(schema_name, table_name, limit=limit, config=vault_cfg)

    # Convert column strings/dicts to ColumnProfile objects
    columns: List[ColumnProfile] = []
    raw_cols = preview.get("columns", [])
    raw_rows = preview.get("sample_rows", [])

    for c in raw_cols:
        col_name = c if isinstance(c, str) else c.get("name", "col")
        sample_vals = [row.get(col_name) for row in raw_rows if col_name in row][:5]
        # Infer basic type from sample value
        dtype = "str"
        if sample_vals:
            first_val = sample_vals[0]
            if isinstance(first_val, bool):
                dtype = "bool"
            elif isinstance(first_val, int):
                dtype = "int64"
            elif isinstance(first_val, float):
                dtype = "float64"
            elif "date" in col_name.lower() or "time" in col_name.lower():
                dtype = "datetime"

        columns.append(
            ColumnProfile(
                name=col_name,
                dtype=dtype,
                null_count=0,
                null_percentage=0.0,
                cardinality=len(sample_vals),
                sample_values=sample_vals,
            )
        )

    return WarehouseTablePreviewResponse(
        connector_type=connector_type,
        schema_name=schema_name,
        table_name=table_name,
        columns=columns,
        rows=raw_rows,
        total_rows_estimate=preview.get("total_rows_estimate", 1000),
    )


@router.post("/{connector_type}/sync/{session_id}")
async def sync_warehouse_data(
    connector_type: str,
    session_id: str,
    req: WarehouseSyncRequest,
    ctx: AuthContext = Depends(require_role("analyst")),
    db: Session = Depends(get_db_session),
) -> Dict[str, Any]:
    """
    Sync an external warehouse table or push-down query into a versioned Parquet dataset.
    Automatically profiles data and registers it for immediate querying.
    """
    connector = CONNECTORS.get(connector_type)
    if not connector:
        raise HTTPException(status_code=404, detail=f"Connector '{connector_type}' not found.")

    session_obj = session_service.get_session(db, session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    vault_cfg = _get_active_vault_config(db, ctx.workspace.id, connector_type)

    # Determine SQL query and destination table name
    if req.sql_query and req.sql_query.strip():
        sql_query = req.sql_query.strip()
        table_name = req.table_name or f"{connector_type}_query"
    else:
        if not req.schema_name or not req.table_name:
            raise HTTPException(
                status_code=400,
                detail="Must provide both schema_name and table_name, or custom sql_query.",
            )
        sql_query = f'SELECT * FROM "{req.schema_name}"."{req.table_name}" LIMIT {req.limit};'
        table_name = req.table_name

    dest_name = clean_table_name(table_name)
    temp_dir = DATA_DIR / "temp" / session_id
    temp_dir.mkdir(parents=True, exist_ok=True)

    parquet_path, _ = connector.execute_and_import(
        session_id=session_id,
        sql_query=sql_query,
        destination_table_name=dest_name,
        target_dir=temp_dir,
        config=vault_cfg,
        limit=req.limit,
    )

    with open(parquet_path, "rb") as f:
        parquet_bytes = f.read()

    # Ingest into session workspace via session_service
    filename = f"{dest_name}.parquet"
    session_file, profiles = await session_service.ingest_file(
        db=db,
        session_id=session_id,
        filename=filename,
        content=parquet_bytes,
        mime_type="application/octet-stream",
    )

    # Clean up temp parquet
    try:
        parquet_path.unlink(missing_ok=True)
    except Exception:
        pass

    matched_profile = next((p for p in profiles if p.table_name == dest_name), profiles[0] if profiles else None)

    return {
        "status": "success",
        "session_id": session_id,
        "connector_type": connector_type,
        "table_name": dest_name,
        "rows_synced": matched_profile.row_count if matched_profile else req.limit,
        "active_version": session_obj.active_dataframe_version,
        "profile": matched_profile,
    }
