"""
Unit tests for Multi-File Relational Joins & Foreign Key Inference.
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


def test_multi_file_relational_inference_and_join():
    """
    Test uploading two relational tables (customers and orders),
    verifying foreign key inference, and executing a cross-table SQL join.
    """
    # 1. Create session
    res = client.post("/api/v1/sessions", json={"title": "Relational Join Session"})
    assert res.status_code == 201
    session_id = res.json()["session_id"]

    # 2. Upload customers dataset
    customers_csv = (
        "customer_id,name,city\n"
        "c_1,Alice,Paris\n"
        "c_2,Bob,London\n"
        "c_3,Charlie,Berlin\n"
    )
    up1 = client.post(
        f"/api/v1/sessions/{session_id}/files/upload",
        files={"file": ("customers.csv", io.BytesIO(customers_csv.encode("utf-8")), "text/csv")},
    )
    assert up1.status_code == 202

    # 3. Upload orders dataset (matching customer_id)
    orders_csv = (
        "order_id,customer_id,total_amount\n"
        "o_101,c_1,250.00\n"
        "o_102,c_2,80.00\n"
        "o_103,c_1,120.00\n"
    )
    up2 = client.post(
        f"/api/v1/sessions/{session_id}/files/upload",
        files={"file": ("orders.csv", io.BytesIO(orders_csv.encode("utf-8")), "text/csv")},
    )
    assert up2.status_code == 202

    # 4. Check relations endpoint
    rel_res = client.get(f"/api/v1/sessions/{session_id}/relations")
    assert rel_res.status_code == 200
    rel_data = rel_res.json()

    assert any("customer" in t.lower() for t in rel_data["tables"])
    assert any("order" in t.lower() for t in rel_data["tables"])

    relations = rel_data["relations"]
    assert len(relations) >= 1

    # Check that customer_id was correctly linked
    found_fk = any(
        (r["from_column"].lower() == "customer_id" and r["to_column"].lower() == "customer_id")
        for r in relations
    )
    assert found_fk is True

    # 5. Execute cross-table DuckDB join
    join_sql = """
    SELECT
      customers.name,
      customers.city,
      COUNT(orders.order_id) AS order_count,
      SUM(orders.total_amount) AS customer_spend
    FROM customers
    JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.name, customers.city
    ORDER BY customer_spend DESC;
    """

    sql_res = client.post(f"/api/v1/sessions/{session_id}/sql", json={"sql": join_sql})
    assert sql_res.status_code == 200
    sql_data = sql_res.json()

    assert sql_data["status"] == "success"
    assert sql_data["total_rows"] == 2

    top_customer = sql_data["rows"][0]
    assert top_customer["name"] == "Alice"
    assert top_customer["order_count"] == 2
    assert top_customer["customer_spend"] == 370.0
