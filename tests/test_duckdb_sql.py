"""
Unit tests for the embedded DuckDB SQL Execution Engine & Checkpoint Materialization.
"""

import io
import pytest
from fastapi.testclient import TestClient

from services.api.database import create_db_and_tables
from services.api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    create_db_and_tables()


@pytest.fixture
def session_with_data() -> str:
    """Create a session and ingest sample transactional data."""
    res = client.post("/api/v1/sessions", json={"title": "DuckDB SQL Test Session"})
    assert res.status_code == 201
    session_id = res.json()["session_id"]

    csv_data = (
        "order_id,user_id,amount,category\n"
        "ord_1,usr_101,150.50,electronics\n"
        "ord_2,usr_102,49.99,books\n"
        "ord_3,usr_101,200.00,electronics\n"
        "ord_4,usr_103,12.50,grocery\n"
        "ord_5,usr_102,85.25,books\n"
    )

    upload_res = client.post(
        f"/api/v1/sessions/{session_id}/files/upload",
        files={"file": ("orders.csv", io.BytesIO(csv_data.encode("utf-8")), "text/csv")},
    )
    assert upload_res.status_code == 202
    return session_id


def test_duckdb_select_query(session_with_data: str):
    """Test standard SELECT query with aggregations on uploaded orders dataset."""
    sql = """
    SELECT
      category,
      COUNT(*) AS total_orders,
      ROUND(SUM(amount), 2) AS total_revenue,
      ROUND(AVG(amount), 2) AS avg_revenue
    FROM orders
    GROUP BY category
    ORDER BY total_revenue DESC;
    """

    res = client.post(f"/api/v1/sessions/{session_with_data}/sql", json={"sql": sql})
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert data["total_rows"] == 3
    assert data["execution_time_ms"] >= 0

    col_names = [c["name"] for c in data["columns"]]
    assert "category" in col_names
    assert "total_orders" in col_names
    assert "total_revenue" in col_names

    rows = data["rows"]
    top_cat = rows[0]
    assert top_cat["category"] == "electronics"
    assert top_cat["total_orders"] == 2
    assert top_cat["total_revenue"] == 350.5


def test_duckdb_query_on_df_active_alias(session_with_data: str):
    """Test querying the active dataset checkpoint via df_active or df."""
    sql = "SELECT COUNT(*) AS cnt FROM df_active;"
    res = client.post(f"/api/v1/sessions/{session_with_data}/sql", json={"sql": sql})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["rows"][0]["cnt"] == 5


def test_duckdb_materialize_checkpoint_from_sql(session_with_data: str):
    """Test creating a new DataFrame checkpoint directly from a SQL filter query."""
    filter_sql = "SELECT * FROM orders WHERE amount >= 100.0;"
    payload = {
        "sql": filter_sql,
        "version_tag": "df_v1",
        "summary": "High value transactions (>= $100)",
    }

    res = client.post(f"/api/v1/sessions/{session_with_data}/sql/save-checkpoint", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert data["version_tag"] == "df_v1"
    assert data["row_count"] == 2
    assert data["column_count"] == 4

    # Verify session active version was updated
    sess_res = client.get(f"/api/v1/sessions/{session_with_data}")
    assert sess_res.status_code == 200
    assert sess_res.json()["active_dataframe_version"] == "df_v1"
