"""
End-to-end integration tests for the API Gateway and Ingestion Flow (services/api).
Tests session lifecycle, file upload, schema profiling, and sandbox code execution.
"""

import io
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from services.api.main import app
from services.api.database import create_db_and_tables

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure database tables exist before each test."""
    create_db_and_tables()


def test_health():
    """Verify API health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "data-speaker-api"


def test_create_and_get_session():
    """Test creating a new session and querying its metadata."""
    create_res = client.post("/api/v1/sessions", json={"title": "Q3 Revenue Analysis"})
    assert create_res.status_code == 201
    session_data = create_res.json()
    session_id = session_data["session_id"]
    assert session_id.startswith("sess_")
    assert session_data["title"] == "Q3 Revenue Analysis"

    get_res = client.get(f"/api/v1/sessions/{session_id}")
    assert get_res.status_code == 200
    detail = get_res.json()
    assert detail["session_id"] == session_id
    assert detail["title"] == "Q3 Revenue Analysis"
    assert detail["active_dataframe_version"] == "df_v0"
    assert detail["files"] == []


def test_upload_and_profile_dataset():
    """Test uploading a CSV dataset, extracting schema, and querying schema endpoint."""
    # 1. Create session
    sess_res = client.post("/api/v1/sessions", json={"title": "Customer Segmentation"})
    session_id = sess_res.json()["session_id"]

    # 2. Upload CSV
    csv_content = (
        "customer_id,tier,monthly_charges,tenure_months\n"
        "101,Gold,89.50,24\n"
        "102,Silver,45.00,12\n"
        "103,Gold,99.90,36\n"
        "104,Bronze,19.99,6\n"
        "105,Silver,49.99,18\n"
    ).encode("utf-8")

    files = {"file": ("customers.csv", io.BytesIO(csv_content), "text/csv")}
    upload_res = client.post(f"/api/v1/sessions/{session_id}/files/upload", files=files)
    assert upload_res.status_code == 202
    upload_data = upload_res.json()

    assert upload_data["status"] == "ready"
    assert upload_data["filename"] == "customers.csv"
    assert len(upload_data["profiles"]) == 1

    profile = upload_data["profiles"][0]
    assert profile["row_count"] == 5
    assert profile["column_count"] == 4
    col_names = [c["name"] for c in profile["columns"]]
    assert "customer_id" in col_names
    assert "monthly_charges" in col_names

    # 3. Query schema endpoint
    schema_res = client.get(f"/api/v1/sessions/{session_id}/schema")
    assert schema_res.status_code == 200
    schema_data = schema_res.json()
    assert schema_data["session_id"] == session_id
    assert schema_data["table_count"] == 1
    assert len(schema_data["profiles"]) == 1


def test_execute_code_against_hydrated_dataframe():
    """Test that uploaded data is automatically hydrated and accessible as `df`."""
    # 1. Create session and upload data
    sess_res = client.post("/api/v1/sessions", json={"title": "Analytics Run"})
    session_id = sess_res.json()["session_id"]

    csv_content = (
        "item,price,quantity\n"
        "Widget A,10.0,5\n"
        "Widget B,20.0,3\n"
        "Widget C,15.0,4\n"
    ).encode("utf-8")

    files = {"file": ("inventory.csv", io.BytesIO(csv_content), "text/csv")}
    upload_res = client.post(f"/api/v1/sessions/{session_id}/files/upload", files=files)
    assert upload_res.status_code == 202

    # 2. Execute calculation referencing `df`
    calc_code = (
        "total_value = (df['price'] * df['quantity']).sum()\n"
        "print(f'Total Inventory Value: {total_value}')\n"
    )
    exec_res = client.post(
        f"/api/v1/sessions/{session_id}/execute",
        json={"code": calc_code, "timeout": 30},
    )
    assert exec_res.status_code == 200, f"Error body: {exec_res.text}"
    res_data = exec_res.json()
    assert res_data["status"] == "success"
    # Total: (10*5) + (20*3) + (15*4) = 50 + 60 + 60 = 170.0
    assert "Total Inventory Value: 170.0" in res_data["stdout"]


def test_multi_turn_state_and_plotly_generation():
    """Test state persistence across turns and Plotly figure interception via API."""
    sess_res = client.post("/api/v1/sessions", json={"title": "Multi-Turn Plotly"})
    session_id = sess_res.json()["session_id"]

    csv_content = (
        "region,sales\n"
        "North,500\n"
        "South,300\n"
        "East,450\n"
        "West,600\n"
    ).encode("utf-8")

    files = {"file": ("sales.csv", io.BytesIO(csv_content), "text/csv")}
    client.post(f"/api/v1/sessions/{session_id}/files/upload", files=files)

    # Turn 1: Mutate DataFrame
    turn1_code = "df['tax'] = df['sales'] * 0.1\nprint('Max sales:', df['sales'].max())"
    res1 = client.post(
        f"/api/v1/sessions/{session_id}/execute",
        json={"code": turn1_code},
    )
    assert res1.status_code == 200
    assert "Max sales: 600" in res1.json()["stdout"]

    # Turn 2: Plot mutated DataFrame
    turn2_code = (
        "import plotly.express as px\n"
        "fig = px.bar(df, x='region', y='sales', title='Regional Performance')\n"
    )
    res2 = client.post(
        f"/api/v1/sessions/{session_id}/execute",
        json={"code": turn2_code},
    )
    assert res2.status_code == 200
    turn2_data = res2.json()
    assert turn2_data["status"] == "success"
    assert len(turn2_data["figures"]) == 1
    figure = turn2_data["figures"][0]
    assert "data" in figure
    assert figure["layout"]["title"]["text"] == "Regional Performance"
