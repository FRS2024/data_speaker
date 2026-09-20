"""
Unit and integration tests for Authentication:
Signup, login, password hashing, 60m access token issuance,
30d refresh token rotation, revocation, and me endpoint.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from services.api.database import create_db_and_tables, engine, get_db_session
from services.api.main import app
from services.api.models import RefreshToken, User, Workspace, WorkspaceMember
from services.api.security import decode_token, verify_password

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure clean schema and defaults for each test run."""
    create_db_and_tables()
    yield


import uuid


def test_signup_creates_user_and_personal_workspace():
    """Verify signup creates user with hashed password and initial owner workspace."""
    uid = uuid.uuid4().hex[:6]
    email = f"alice_{uid}@example.com"
    password = "SuperSecretPassword123"

    response = client.post(
        "/api/v1/auth/signup",
        json={"email": email, "password": password, "full_name": "Alice Wonderland"},
    )
    assert response.status_code == 201, response.text
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 3600
    assert data["user"]["email"] == email
    assert data["user"]["full_name"] == "Alice Wonderland"
    assert data["active_workspace"]["role"] == "owner"

    # Verify password was hashed in database
    with Session(engine) as db:
        user = db.exec(select(User).where(User.email == email)).first()
        assert user is not None
        assert user.hashed_password != password
        assert verify_password(password, user.hashed_password)

        # Verify refresh token was stored in DB
        db_ref = db.exec(select(RefreshToken).where(RefreshToken.user_id == user.id)).first()
        assert db_ref is not None
        assert not db_ref.is_revoked


def test_login_and_token_lifecycles():
    """Verify login authenticates correctly, returning valid 60m access token."""
    uid = uuid.uuid4().hex[:6]
    email = f"bob_{uid}@example.com"
    password = "BobSecurePassword456"

    # Signup first
    client.post("/api/v1/auth/signup", json={"email": email, "password": password, "full_name": "Bob Builder"})

    # Login
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    data = response.json()

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    # Decode and check access token payload
    decoded_access = decode_token(access_token)
    assert decoded_access["sub"] == data["user"]["id"]
    assert decoded_access["email"] == email
    assert decoded_access["type"] == "access"
    # Verify ~60 minute expiry (3600 seconds +/- 10s tolerance)
    duration = decoded_access["exp"] - decoded_access["iat"]
    assert 3590 <= duration <= 3610

    # Check refresh token payload
    decoded_refresh = decode_token(refresh_token)
    assert decoded_refresh["type"] == "refresh"


def test_refresh_token_rotation_and_revocation():
    """Verify refresh token rotation and immediate revocation on logout."""
    uid = uuid.uuid4().hex[:6]
    email = f"charlie_{uid}@example.com"
    password = "CharliePassword789"

    signup_res = client.post("/api/v1/auth/signup", json={"email": email, "password": password})
    tokens = signup_res.json()
    first_refresh = tokens["refresh_token"]

    # Rotate refresh token
    rotate_res = client.post("/api/v1/auth/refresh", json={"refresh_token": first_refresh})
    assert rotate_res.status_code == 200, rotate_res.text
    new_tokens = rotate_res.json()
    second_refresh = new_tokens["refresh_token"]
    assert second_refresh != first_refresh

    # Trying to reuse the old rotated refresh token MUST fail (401)
    reuse_res = client.post("/api/v1/auth/refresh", json={"refresh_token": first_refresh})
    assert reuse_res.status_code == 401

    # Logout with active refresh token
    logout_res = client.post("/api/v1/auth/logout", json={"refresh_token": second_refresh})
    assert logout_res.status_code == 200

    # Using revoked token MUST fail (401)
    post_logout_res = client.post("/api/v1/auth/refresh", json={"refresh_token": second_refresh})
    assert post_logout_res.status_code == 401


def test_get_me_profile_and_workspaces():
    """Verify /me returns profile and user workspace memberships."""
    uid = uuid.uuid4().hex[:6]
    email = f"diana_{uid}@example.com"
    password = "DianaPassword321"

    signup_res = client.post("/api/v1/auth/signup", json={"email": email, "password": password, "full_name": "Diana Prince"})
    token = signup_res.json()["access_token"]

    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()

    assert me_data["user"]["email"] == email
    assert me_data["user"]["full_name"] == "Diana Prince"
    assert len(me_data["workspaces"]) >= 1
    assert me_data["workspaces"][0]["role"] == "owner"
