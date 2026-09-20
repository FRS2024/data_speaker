"""
Unit tests for BigQuery and Snowflake Cloud Warehouse Connectors.
"""

import pytest
from fastapi.testclient import TestClient

from services.api.database import create_db_and_tables
from services.api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    create_db_and_tables()


def test_warehouse_connectors_status():
    """Test inspecting BigQuery and Snowflake connector statuses."""
    res = client.get("/api/v1/connectors/status")
    assert res.status_code == 200
    data = res.json()

    assert "bigquery" in data
    assert "snowflake" in data

    bq = data["bigquery"]
    assert bq["name"] == "Google BigQuery"
    assert "parquet_export" in bq["supported_features"]

    sf = data["snowflake"]
    assert sf["name"] == "Snowflake Data Cloud"
    assert "schema_discovery" in sf["supported_features"]


def test_warehouse_import_to_session():
    """Test importing a cloud warehouse dataset query into a session as a Parquet table."""
    sess_res = client.post("/api/v1/sessions", json={"title": "Warehouse Ingestion Session"})
    assert sess_res.status_code == 201
    session_id = sess_res.json()["session_id"]

    import_payload = {
        "query": "SELECT * FROM ecommerce_analytics.orders_v2 WHERE amount_usd > 50;",
        "table_name": "bq_orders",
    }

    res = client.post(
        f"/api/v1/sessions/{session_id}/connectors/bigquery/import",
        json=import_payload,
    )
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "ready"
    assert data["filename"] == "bq_orders.parquet"
    assert len(data["profiles"]) >= 1

    prof = data["profiles"][0]
    assert prof["table_name"] in ("bq_orders", "df_bq_orders")
    assert prof["row_count"] > 0

    # Verify newly imported table can be queried immediately via DuckDB
    sql_res = client.post(
        f"/api/v1/sessions/{session_id}/sql",
        json={"sql": "SELECT COUNT(*) AS total_imported FROM bq_orders;"},
    )
    assert sql_res.status_code == 200
    assert sql_res.json()["rows"][0]["total_imported"] == prof["row_count"]
