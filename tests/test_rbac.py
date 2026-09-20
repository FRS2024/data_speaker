"""
Integration tests for Tiered Role-Based Access Control (RBAC):
Verifies that users with 'viewer' role have strictly read-only access
and cannot execute Python code, SQL, or upload datasets.
"""

from __future__ import annotations

import io
import uuid
import pytest
from fastapi.testclient import TestClient

from services.api.database import create_db_and_tables
from services.api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    create_db_and_tables()
    yield


def test_viewer_role_execution_restrictions():
    """Verify viewer role is strictly forbidden from write/execute actions."""
    uid = uuid.uuid4().hex[:6]
    boss_email = f"boss_{uid}@corp.com"
    viewer_email = f"auditor_{uid}@external.com"

    # 1. Owner sets up workspace and a session
    res_owner = client.post("/api/v1/auth/signup", json={"email": boss_email, "password": "BossPassword123"})
    assert res_owner.status_code == 201, res_owner.text
    token_owner = res_owner.json()["access_token"]
    ws_id = res_owner.json()["active_workspace"]["id"]
    headers_owner = {"Authorization": f"Bearer {token_owner}", "X-Workspace-Id": ws_id}

    # Create session as owner
    sess_res = client.post("/api/v1/sessions", json={"title": "Q3 Sales Review"}, headers=headers_owner)
    assert sess_res.status_code == 201
    sess_id = sess_res.json()["session_id"]

    # 2. Owner invites a viewer
    invite_res = client.post(
        f"/api/v1/workspaces/{ws_id}/members",
        json={"email": viewer_email, "role": "viewer"},
        headers=headers_owner,
    )
    assert invite_res.status_code == 201, invite_res.text

    # 3. Viewer user signs up with the same email to set their password
    client.post("/api/v1/auth/signup", json={"email": viewer_email, "password": "AuditorPassword123"})
    login_res = client.post("/api/v1/auth/login", json={"email": viewer_email, "password": "AuditorPassword123"})
    assert login_res.status_code == 200
    token_viewer = login_res.json()["access_token"]
    headers_viewer = {"Authorization": f"Bearer {token_viewer}", "X-Workspace-Id": ws_id}

    # 4. Viewer CAN list sessions
    list_res = client.get("/api/v1/sessions", headers=headers_viewer)
    assert list_res.status_code == 200

    # 5. Viewer CANNOT create a session (requires 'analyst')
    create_sess_res = client.post("/api/v1/sessions", json={"title": "Unauthorized Session"}, headers=headers_viewer)
    assert create_sess_res.status_code == 403
    assert "Permission denied" in create_sess_res.text

    # 6. Viewer CANNOT execute code
    exec_res = client.post(
        f"/api/v1/sessions/{sess_id}/execute",
        json={"code": "print('hacked')"},
        headers=headers_viewer,
    )
    assert exec_res.status_code == 403
    assert "Permission denied" in exec_res.text

    # 7. Viewer CANNOT execute DuckDB SQL
    sql_res = client.post(
        f"/api/v1/sessions/{sess_id}/sql",
        json={"sql": "SELECT 1"},
        headers=headers_viewer,
    )
    assert sql_res.status_code == 403
    assert "Permission denied" in sql_res.text

    # 8. Viewer CANNOT upload a dataset
    csv_file = io.BytesIO(b"id,val\n1,10\n2,20")
    upload_res = client.post(
        f"/api/v1/sessions/{sess_id}/files/upload",
        files={"file": ("test.csv", csv_file, "text/csv")},
        headers=headers_viewer,
    )
    assert upload_res.status_code == 403
    assert "Permission denied" in upload_res.text
