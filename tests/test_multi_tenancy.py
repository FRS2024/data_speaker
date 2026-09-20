"""
Integration tests for Workspace Multi-Tenancy:
Workspace isolation, session scoping, cross-tenant isolation,
and member invites / role updates.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from services.api.database import create_db_and_tables
from services.api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    create_db_and_tables()
    yield


import uuid


def test_workspace_creation_and_listing():
    """Verify user can create multiple workspaces and list memberships."""
    uid = uuid.uuid4().hex[:6]
    email = f"tenant_admin_{uid}@corp.com"

    # Register user
    res = client.post(
        "/api/v1/auth/signup",
        json={"email": email, "password": "AdminPassword123", "full_name": "Tenant Admin"},
    )
    assert res.status_code == 201, res.text
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create new team workspace
    create_res = client.post(
        "/api/v1/workspaces",
        json={"name": "Analytics Dept"},
        headers=headers,
    )
    assert create_res.status_code == 201, create_res.text
    ws_data = create_res.json()
    assert ws_data["name"] == "Analytics Dept"
    assert ws_data["role"] == "owner"

    # List workspaces
    list_res = client.get("/api/v1/workspaces", headers=headers)
    assert list_res.status_code == 200
    workspaces = list_res.json()
    assert len(workspaces) >= 2
    ws_names = [w["name"] for w in workspaces]
    assert "Analytics Dept" in ws_names


def test_cross_tenant_session_isolation():
    """Verify sessions created in Workspace A are strictly invisible to Workspace B."""
    uid_a = uuid.uuid4().hex[:6]
    uid_b = uuid.uuid4().hex[:6]

    # User A in Workspace A
    res_a = client.post("/api/v1/auth/signup", json={"email": f"user_a_{uid_a}@alpha.com", "password": "PasswordA123"})
    assert res_a.status_code == 201, res_a.text
    token_a = res_a.json()["access_token"]
    ws_a_id = res_a.json()["active_workspace"]["id"]
    headers_a = {"Authorization": f"Bearer {token_a}", "X-Workspace-Id": ws_a_id}

    # User B in Workspace B
    res_b = client.post("/api/v1/auth/signup", json={"email": f"user_b_{uid_b}@beta.com", "password": "PasswordB123"})
    assert res_b.status_code == 201, res_b.text
    token_b = res_b.json()["access_token"]
    ws_b_id = res_b.json()["active_workspace"]["id"]
    headers_b = {"Authorization": f"Bearer {token_b}", "X-Workspace-Id": ws_b_id}

    # User A creates a confidential session in Workspace A
    sess_a_res = client.post(
        "/api/v1/sessions",
        json={"title": "Alpha Confidential Q4 Strategy"},
        headers=headers_a,
    )
    assert sess_a_res.status_code == 201
    sess_a_id = sess_a_res.json()["session_id"]

    # User B creates a session in Workspace B
    sess_b_res = client.post(
        "/api/v1/sessions",
        json={"title": "Beta Public Growth Metrics"},
        headers=headers_b,
    )
    assert sess_b_res.status_code == 201
    sess_b_id = sess_b_res.json()["session_id"]

    # User A lists sessions -> sees ONLY sess_a
    list_a = client.get("/api/v1/sessions", headers=headers_a).json()
    session_ids_a = [s["session_id"] for s in list_a]
    assert sess_a_id in session_ids_a
    assert sess_b_id not in session_ids_a

    # User B lists sessions -> sees ONLY sess_b
    list_b = client.get("/api/v1/sessions", headers=headers_b).json()
    session_ids_b = [s["session_id"] for s in list_b]
    assert sess_b_id in session_ids_b
    assert sess_a_id not in session_ids_b


def test_invite_member_and_role_management():
    """Verify Admin can invite new members and modify their role."""
    uid = uuid.uuid4().hex[:6]
    owner_email = f"owner_{uid}@team.com"
    colleague_email = f"colleague_{uid}@team.com"

    # Owner signup
    res_owner = client.post("/api/v1/auth/signup", json={"email": owner_email, "password": "OwnerPassword123"})
    assert res_owner.status_code == 201, res_owner.text
    token_owner = res_owner.json()["access_token"]
    ws_id = res_owner.json()["active_workspace"]["id"]
    headers = {"Authorization": f"Bearer {token_owner}", "X-Workspace-Id": ws_id}

    # Invite analyst
    invite_res = client.post(
        f"/api/v1/workspaces/{ws_id}/members",
        json={"email": colleague_email, "role": "analyst"},
        headers=headers,
    )
    assert invite_res.status_code == 201, invite_res.text
    invited_member = invite_res.json()
    assert invited_member["email"] == colleague_email
    assert invited_member["role"] == "analyst"
    colleague_id = invited_member["user_id"]

    # Change role to admin
    patch_res = client.patch(
        f"/api/v1/workspaces/{ws_id}/members/{colleague_id}",
        json={"role": "admin"},
        headers=headers,
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["role"] == "admin"

    # Remove member
    del_res = client.delete(
        f"/api/v1/workspaces/{ws_id}/members/{colleague_id}",
        headers=headers,
    )
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "removed"
