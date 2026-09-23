"""
Automated test suite for Track D: Multi-Agent Critic & Statistician Debate Swarm.
Validates multi-agent collaborative execution, SSE event streaming, debate loops,
and statistical peer review persistence.
"""

import io
import json
import pytest
from fastapi.testclient import TestClient

from services.api.main import app
from services.api.database import create_db_and_tables, get_db_session
from services.api.models import ChatTurn
from sqlmodel import select

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure database tables exist before each test."""
    create_db_and_tables()


@pytest.fixture
def session_with_data() -> str:
    """Create a session and upload a sample employee dataset."""
    sess_res = client.post("/api/v1/sessions", json={"title": "HR Swarm Analytics"})
    session_id = sess_res.json()["session_id"]

    csv_data = (
        "emp_id,name,department,salary,performance_score\n"
        "1,Alice,Engineering,120000,4.8\n"
        "2,Bob,Engineering,110000,4.2\n"
        "3,Charlie,Marketing,85000,3.9\n"
        "4,Diana,Sales,95000,4.5\n"
        "5,Evan,Marketing,78000,3.6\n"
        "6,Frank,Engineering,130000,4.9\n"
        "7,Grace,Sales,91000,4.1\n"
    ).encode("utf-8")

    files = {"file": ("employees.csv", io.BytesIO(csv_data), "text/csv")}
    upload_res = client.post(f"/api/v1/sessions/{session_id}/files/upload", files=files)
    assert upload_res.status_code == 202
    return session_id


def test_swarm_mode_sync_execution(session_with_data: str):
    """Test running synchronous analytical turn with swarm_mode=True."""
    payload = {
        "prompt": "What is the average salary across departments?",
        "stream": False,
        "provider": "mock",
        "swarm_mode": True,
    }
    res = client.post(f"/api/v1/sessions/{session_with_data}/chat", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert "code" in data
    assert "critic_review" in data
    assert data["critic_review"] is not None
    assert "verdict" in data["critic_review"]
    assert "confidence_score" in data["critic_review"]

    # Verify database persistence of peer review
    with next(get_db_session()) as db:
        turn = db.exec(
            select(ChatTurn)
            .where(ChatTurn.session_id == session_with_data)
            .order_by(ChatTurn.created_at.desc())
        ).first()

        assert turn is not None
        assert turn.critic_review_json is not None
        review_data = json.loads(turn.critic_review_json)
        assert "verdict" in review_data
        assert "confidence_score" in review_data


def test_swarm_mode_sse_streaming(session_with_data: str):
    """Test SSE event stream with swarm_phase, critic_review, and execution events."""
    payload = {
        "prompt": "Calculate department salary distribution",
        "stream": True,
        "provider": "mock",
        "swarm_mode": True,
    }
    res = client.post(f"/api/v1/sessions/{session_with_data}/chat", json=payload)
    assert res.status_code == 200
    assert "text/event-stream" in res.headers["content-type"]

    events = []
    for line in res.iter_lines():
        if line.startswith("event: "):
            events.append(line.replace("event: ", "").strip())

    assert "swarm_phase" in events
    assert "code_generated" in events
    assert "critic_review" in events
    assert "execution_stdout" in events
    assert "turn_complete" in events
