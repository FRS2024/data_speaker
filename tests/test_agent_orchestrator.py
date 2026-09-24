"""
Automated test suite for Phase 3: Autonomous AI Analyst & Reflexion Loop.
Verifies end-to-end question answering, code generation, error recovery via Reflexion,
SSE multiplexing, and synchronous response modes.
"""

import io
import json
import pytest
from fastapi.testclient import TestClient

from services.api.main import app
from services.api.database import create_db_and_tables

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure database tables exist before each test."""
    create_db_and_tables()


@pytest.fixture
def session_with_data() -> str:
    """Create a session and upload a sample employee dataset."""
    sess_res = client.post("/api/v1/sessions", json={"title": "HR Analytics"})
    session_id = sess_res.json()["session_id"]

    csv_data = (
        "emp_id,name,department,salary,performance_score\n"
        "1,Alice,Engineering,120000,4.8\n"
        "2,Bob,Engineering,110000,4.2\n"
        "3,Charlie,Marketing,85000,3.9\n"
        "4,Diana,Sales,95000,4.5\n"
        "5,Evan,Marketing,78000,3.6\n"
    ).encode("utf-8")

    files = {"file": ("employees.csv", io.BytesIO(csv_data), "text/csv")}
    upload_res = client.post(f"/api/v1/sessions/{session_id}/files/upload", files=files)
    assert upload_res.status_code == 202
    return session_id


def test_chat_sync_successful_analytical_query(session_with_data: str):
    """Test standard single-turn analytical query returning synchronous JSON."""
    chat_payload = {
        "prompt": "What are the summary statistics for employee salaries?",
        "stream": False,
        "provider": "mock",
    }
    res = client.post(f"/api/v1/sessions/{session_with_data}/chat", json=chat_payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert data["turn_id"].startswith("trn_")
    assert "df.describe()" in data["code"]
    assert "Summary Statistics:" in data["stdout"]
    assert len(data["explanation"]) > 0
    assert data["reflexion_count"] == 0
    assert data["duration_ms"] > 0


def test_chat_sync_chart_generation(session_with_data: str):
    """Test that chart requests produce interactive Plotly specifications."""
    chat_payload = {
        "prompt": "Please plot a histogram of employee salary distribution",
        "stream": False,
        "provider": "mock",
    }
    res = client.post(f"/api/v1/sessions/{session_with_data}/chat", json=chat_payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert len(data["figures"]) >= 1
    fig = data["figures"][0]
    assert "data" in fig
    assert "layout" in fig
    assert "title" in fig["layout"]


def test_chat_reflexion_self_correction(session_with_data: str):
    """
    Test the Reflexion loop:
    1. Attempt 1 triggers a KeyError ('non_existent_column').
    2. Orchestrator captures the traceback and emits a reflexion step.
    3. MockProvider receives error context and outputs corrected code.
    4. Execution succeeds on attempt 2!
    """
    chat_payload = {
        "prompt": "Please calculate values and trigger_error for testing",
        "stream": False,
        "max_attempts": 3,
        "provider": "mock",
    }
    res = client.post(f"/api/v1/sessions/{session_with_data}/chat", json=chat_payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert data["reflexion_count"] == 1
    assert "Reflexion Recovery: Column resolved." in data["stdout"]
    assert "Total Rows: 5" in data["stdout"]


def test_chat_stream_sse_events(session_with_data: str):
    """Test real-time Server-Sent Events (SSE) streaming format and event multiplexing."""
    chat_payload = {
        "prompt": "Analyze salary trends and chart the results",
        "stream": True,
        "provider": "mock",
    }

    events_received = []
    with client.stream("POST", f"/api/v1/sessions/{session_with_data}/chat", json=chat_payload) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

        current_event = None
        for line in response.iter_lines():
            if line.startswith("event: "):
                current_event = line.replace("event: ", "").strip()
            elif line.startswith("data: ") and current_event:
                data_str = line.replace("data: ", "").strip()
                try:
                    payload = json.loads(data_str)
                    events_received.append((current_event, payload))
                except Exception:
                    pass
                current_event = None

    # Verify event stream sequence
    event_names = [e[0] for e in events_received]

    assert "execution_status" in event_names
    assert "code_generated" in event_names
    assert "execution_stdout" in event_names
    assert "chart_generated" in event_names
    assert "token" in event_names
    assert "turn_complete" in event_names

    # Check turn_complete payload
    turn_complete_event = next(e[1] for e in events_received if e[0] == "turn_complete")
    assert turn_complete_event["turn_id"].startswith("trn_")
    assert turn_complete_event["duration_ms"] > 0
    assert turn_complete_event["reflexion_count"] == 0


def test_chat_sql_olap_query(session_with_data: str):
    """Test SQL query execution through chat interface with DuckDB scanning df_active."""
    chat_payload = {
        "prompt": "Execute SQL and optimize scan: ```sql -- Direct DuckDB & BigQuery OLAP Query SELECT * FROM df_active LIMIT 100; ```",
        "stream": False,
        "provider": "mock",
    }
    res = client.post(f"/api/v1/sessions/{session_with_data}/chat", json=chat_payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert "duckdb" in data["code"].lower()
    assert "Executing DuckDB OLAP Query" in data["stdout"]
    assert "Scan successful" in data["stdout"]
    assert data["reflexion_count"] == 0


@pytest.mark.asyncio
async def test_gemini_provider_503_fallback():
    """Verify GeminiProvider falls back to MockProvider when 503 UNAVAILABLE is raised."""
    from unittest.mock import AsyncMock, patch
    from services.api.agent.providers import GeminiProvider

    provider = GeminiProvider(api_key="test_fake_gemini_key")
    with patch.object(provider, "_get_client") as mock_client_factory:
        mock_client = AsyncMock()
        mock_client.aio.models.generate_content.side_effect = Exception(
            "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand.'}}"
        )
        mock_client_factory.return_value = mock_client

        messages = [{"role": "user", "content": "SELECT * FROM df_active LIMIT 10"}]
        system_prompt = "You are an autonomous AI analyst."

        result = await provider.generate_code_call(messages, system_prompt)
        assert result.name == "execute_python"
        # Must NOT contain raw unescaped print('Error: 503 ...') that causes SyntaxError
        assert "SyntaxError" not in result.code
        assert "print('Error: 503" not in result.code
        assert "duckdb" in result.code or "print(" in result.code


def test_fresh_session_no_upload_has_baseline_df():
    """Verify code execution in a fresh session with no uploaded file has df and df_active available."""
    sess_res = client.post("/api/v1/sessions", json={"title": "Fresh Empty Session"})
    session_id = sess_res.json()["session_id"]

    exec_res = client.post(
        f"/api/v1/sessions/{session_id}/execute",
        json={"code": "print('df len:', len(df)); print('df_active cols:', list(df_active.columns))"},
    )
    assert exec_res.status_code == 200
    data = exec_res.json()
    assert data["status"] == "success"
    assert "df len:" in data["stdout"]
    assert "customer_id" in data["stdout"]

