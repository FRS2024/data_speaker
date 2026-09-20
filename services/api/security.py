"""
Security and authentication utilities for data-speaker.
Handles password hashing via bcrypt and HS256 JWT token generation / decoding.
"""

from __future__ import annotations

import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import bcrypt
import jwt

# Configuration
JWT_SECRET_KEY = os.environ.get(
    "JWT_SECRET_KEY",
    "data-speaker-enterprise-security-jwt-secret-key-2026"
)
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "30"))


# ---------------------------------------------------------------------------
# Password Hashing & Verification
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt with salt."""
    # Bcrypt has a 72-byte limit; pre-hash with SHA-256 for arbitrarily long passwords
    pwd_bytes = password.encode("utf-8")
    if len(pwd_bytes) > 72:
        pwd_bytes = hashlib.sha256(pwd_bytes).hexdigest().encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    try:
        pwd_bytes = plain_password.encode("utf-8")
        if len(pwd_bytes) > 72:
            pwd_bytes = hashlib.sha256(pwd_bytes).hexdigest().encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))
    except Exception:
        return False


# ---------------------------------------------------------------------------
# JWT Token Generation & Validation
# ---------------------------------------------------------------------------

def create_access_token(
    user_id: str,
    email: str,
    workspace_id: Optional[str] = None,
    role: str = "analyst",
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Generate a short-lived signed JWT access token.
    Defaults to 60 minutes as per requirements.
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: Dict[str, Any] = {
        "sub": user_id,
        "email": email,
        "role": role,
        "workspace_id": workspace_id,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(
    user_id: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Generate a signed JWT refresh token.
    Defaults to 30 days.
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    unique_entropy = hashlib.sha256(f"{user_id}:{now.isoformat()}:{os.urandom(16).hex()}".encode()).hexdigest()[:16]

    payload: Dict[str, Any] = {
        "sub": user_id,
        "type": "refresh",
        "jti": unique_entropy,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    Raises jwt.PyJWTError subclasses on failure.
    """
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])


def hash_token(token: str) -> str:
    """Compute deterministic SHA-256 hash of a token for secure database storage."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
