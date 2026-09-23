"""
Integration & Unit tests for Track F: Enterprise Warehouse & Lakehouse Connectors Studio.
Covers PostgreSQL, BigQuery, Snowflake, and Databricks Lakehouse:
- Listing connectors & capability summaries
- Testing ping/connection endpoints (live & demo sandbox fallback)
- Dynamic workspace credential vault (create, mask on read, list, delete)
- Schema discovery tree & table listings
- Live table preview with data types and sample rows
- One-click table sync and push-down SQL query execution into versioned Parquet datasets
"""

import pytest
from fastapi.testclient import TestClient

from services.api.database import create_db_and_tables
from services.api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    create_db_and_tables()


def test_list_all_warehouse_connectors():
    """Verify all 4 connectors in quadrant are returned with metadata."""
    res = client.get("/api/v1/connectors")
    assert res.status_code == 200
    connectors = res.json()
    assert len(connectors) == 4

    types = [c["connector_type"] for c in connectors]
    assert "postgres" in types
    assert "bigquery" in types
    assert "snowflake" in types
    assert "databricks" in types

    for c in connectors:
        assert c["name"]
        assert c["description"]
        assert len(c["supported_features"]) > 0
        assert c["mode"] in ("connected", "demo_sandbox")


def test_warehouse_test_connection_ping():
    """Verify connection ping tests for all connector types."""
    for c_type in ["postgres", "bigquery", "snowflake", "databricks"]:
        res = client.post(
            "/api/v1/connectors/test",
            json={"connector_type": c_type, "config": {}},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] in ("mock_mode", "connected")
        assert data["latency_ms"] > 0
        assert data["message"]


def test_invalid_connector_test():
    """Verify testing unsupported connector returns 404."""
    res = client.post(
        "/api/v1/connectors/test",
        json={"connector_type": "oracle_legacy", "config": {}},
    )
    assert res.status_code == 404


def test_credentials_vault_lifecycle():
    """Verify saving, masking, reading, and deleting credentials in workspace vault."""
    # 1. Save secret config
    save_payload = {
        "connector_type": "postgres",
        "name": "Production Neon Database",
        "config": {
            "host": "ep-prod-01.neon.tech",
            "port": "5432",
            "database": "production_analytics",
            "user": "alex_analyst",
            "password": "super_secret_password_123",
            "sslmode": "require",
        },
    }
    res = client.post("/api/v1/connectors/config", json=save_payload)
    assert res.status_code == 200
    config_data = res.json()
    assert config_data["connector_type"] == "postgres"
    assert config_data["name"] == "Production Neon Database"
    assert config_data["masked_config"]["password"] == "••••••••"
    assert config_data["masked_config"]["host"] == "ep-prod-01.neon.tech"
    config_id = config_data["id"]

    # 2. Get saved configs for connector
    get_res = client.get("/api/v1/connectors/config/postgres")
    assert get_res.status_code == 200
    configs = get_res.json()
    assert any(c["id"] == config_id for c in configs)

    # 3. Delete config
    del_res = client.delete(f"/api/v1/connectors/config/{config_id}")
    assert del_res.status_code == 204

    # 4. Verify gone
    get_after = client.get("/api/v1/connectors/config/postgres")
    assert not any(c["id"] == config_id for c in get_after.json())


def test_schema_tree_and_tables():
    """Verify listing schemas and tables across connectors."""
    # PostgreSQL
    res_pg_schemas = client.get("/api/v1/connectors/postgres/schemas")
    assert res_pg_schemas.status_code == 200
    pg_schemas = res_pg_schemas.json()["schemas"]
    assert "public" in pg_schemas or "billing" in pg_schemas

    res_pg_tables = client.get("/api/v1/connectors/postgres/schemas/billing/tables")
    assert res_pg_tables.status_code == 200
    assert "stripe_charges" in res_pg_tables.json()["tables"]

    # Databricks
    res_db_schemas = client.get("/api/v1/connectors/databricks/schemas")
    assert res_db_schemas.status_code == 200
    db_schemas = res_db_schemas.json()["schemas"]
    assert "lakehouse_gold" in db_schemas

    res_db_tables = client.get("/api/v1/connectors/databricks/schemas/lakehouse_gold/tables")
    assert res_db_tables.status_code == 200
    assert "gold_daily_active_users" in res_db_tables.json()["tables"]


def test_table_preview_metadata():
    """Verify live table preview with column dtypes and rows."""
    res = client.get("/api/v1/connectors/postgres/schemas/billing/tables/stripe_charges/preview?limit=10")
    assert res.status_code == 200
    data = res.json()

    assert data["connector_type"] == "postgres"
    assert data["schema_name"] == "billing"
    assert data["table_name"] == "stripe_charges"
    assert len(data["columns"]) >= 4
    assert len(data["rows"]) >= 1
    assert data["total_rows_estimate"] > 0


def test_sync_table_to_session_parquet():
    """Verify one-click table sync streaming into a session Parquet dataset."""
    sess_res = client.post("/api/v1/sessions", json={"title": "Postgres Billing Sync Session"})
    assert sess_res.status_code == 201
    session_id = sess_res.json()["session_id"]

    sync_payload = {
        "schema_name": "billing",
        "table_name": "stripe_charges",
        "limit": 500,
    }

    sync_res = client.post(
        f"/api/v1/connectors/postgres/sync/{session_id}",
        json=sync_payload,
    )
    assert sync_res.status_code == 200
    data = sync_res.json()

    assert data["status"] == "success"
    assert data["session_id"] == session_id
    assert data["connector_type"] == "postgres"
    assert data["table_name"] in ("stripe_charges", "df_stripe_charges")
    assert data["rows_synced"] == 500
    assert data["profile"] is not None
    assert data["profile"]["row_count"] == 500


def test_sync_pushdown_sql_query():
    """Verify pushdown SQL query execution into a session dataset."""
    sess_res = client.post("/api/v1/sessions", json={"title": "Databricks DAU Session"})
    assert sess_res.status_code == 201
    session_id = sess_res.json()["session_id"]

    query_payload = {
        "sql_query": "SELECT metric_date, dau, wau, mau, stickiness_ratio FROM lakehouse_gold.gold_daily_active_users",
        "table_name": "dau_growth_metrics",
        "limit": 300,
    }

    res = client.post(
        f"/api/v1/connectors/databricks/sync/{session_id}",
        json=query_payload,
    )
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert data["table_name"] in ("dau_growth_metrics", "df_dau_growth_metrics")
    assert data["rows_synced"] == 300
    assert data["profile"]["row_count"] == 300
