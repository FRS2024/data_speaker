"""
Authentication router: Signup, Login, Token Refresh, Logout, and User Profile.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from services.api.auth import get_current_user
from services.api.database import get_db_session
from services.api.models import (
    AuthTokenResponse,
    RefreshToken,
    RefreshTokenRequest,
    User,
    UserLoginRequest,
    UserResponse,
    UserSignUpRequest,
    Workspace,
    WorkspaceMember,
    WorkspaceResponse,
)
from services.api.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user and generate personal workspace",
)
def signup(
    payload: UserSignUpRequest,
    session: Session = Depends(get_db_session),
) -> AuthTokenResponse:
    """Register a new user account with secure password hashing and initial workspace."""
    normalized_email = payload.email.strip().lower()
    if not normalized_email or "@" not in normalized_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address",
        )

    if len(payload.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long",
        )

    # Check for existing email
    existing = session.exec(
        select(User).where(User.email == normalized_email)
    ).first()
    if existing:
        if existing.hashed_password == "invited_user_placeholder":
            # Invited user claiming account
            existing.hashed_password = hash_password(payload.password)
            if payload.full_name:
                existing.full_name = payload.full_name
            session.commit()
            session.refresh(existing)
            user = existing
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email address already exists",
            )
    else:
        # Create user
        user = User(
            email=normalized_email,
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name or "",
            is_active=True,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    # Check if user was already invited into a workspace
    existing_member = session.exec(
        select(WorkspaceMember).where(WorkspaceMember.user_id == user.id)
    ).first()

    if existing_member:
        workspace = session.get(Workspace, existing_member.workspace_id)
        role = existing_member.role
    else:
        # Auto-create personal workspace
        workspace_name = f"{user.full_name or user.email.split('@')[0]}'s Workspace"
        workspace = Workspace(
            name=workspace_name,
            slug=f"{user.email.split('@')[0]}-workspace".lower(),
            plan_tier="free",
            created_by=user.id,
        )
        session.add(workspace)
        session.commit()
        session.refresh(workspace)

        # Assign owner membership
        membership = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=user.id,
            role="owner",
        )
        session.add(membership)
        session.commit()
        role = "owner"

    # Generate 60m access token and 30d refresh token
    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        workspace_id=workspace.id,
        role=role,
    )
    refresh_token = create_refresh_token(user_id=user.id)

    # Save refresh token hash in DB
    ref_payload = decode_token(refresh_token)
    db_refresh = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.fromtimestamp(ref_payload["exp"], tz=timezone.utc),
        is_revoked=False,
    )
    session.add(db_refresh)
    session.commit()

    return AuthTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600,
        user=UserResponse.model_validate(user),
        active_workspace=WorkspaceResponse(
            id=workspace.id,
            name=workspace.name,
            slug=workspace.slug,
            plan_tier=workspace.plan_tier,
            role="owner",
            created_at=workspace.created_at,
        ),
    )


@router.post(
    "/login",
    response_model=AuthTokenResponse,
    summary="Authenticate with email and password",
)
def login(
    payload: UserLoginRequest,
    session: Session = Depends(get_db_session),
) -> AuthTokenResponse:
    """Log in with email and password to receive access and refresh tokens."""
    normalized_email = payload.email.strip().lower()
    user = session.exec(
        select(User).where(User.email == normalized_email)
    ).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    # Resolve primary workspace
    membership = session.exec(
        select(WorkspaceMember).where(WorkspaceMember.user_id == user.id)
    ).first()

    if not membership:
        workspace = Workspace(
            name=f"{user.email.split('@')[0]}'s Workspace",
            slug=f"{user.email.split('@')[0]}-workspace".lower(),
            plan_tier="free",
            created_by=user.id,
        )
        session.add(workspace)
        session.commit()
        session.refresh(workspace)

        membership = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=user.id,
            role="owner",
        )
        session.add(membership)
        session.commit()
    else:
        workspace = session.get(Workspace, membership.workspace_id)

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        workspace_id=workspace.id,
        role=membership.role,
    )
    refresh_token = create_refresh_token(user_id=user.id)

    ref_payload = decode_token(refresh_token)
    db_refresh = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.fromtimestamp(ref_payload["exp"], tz=timezone.utc),
        is_revoked=False,
    )
    session.add(db_refresh)
    session.commit()

    return AuthTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600,
        user=UserResponse.model_validate(user),
        active_workspace=WorkspaceResponse(
            id=workspace.id,
            name=workspace.name,
            slug=workspace.slug,
            plan_tier=workspace.plan_tier,
            role=membership.role,
            created_at=workspace.created_at,
        ),
    )


@router.post(
    "/refresh",
    response_model=AuthTokenResponse,
    summary="Rotate refresh token and issue fresh 60-minute access token",
)
def refresh_token(
    payload: RefreshTokenRequest,
    session: Session = Depends(get_db_session),
) -> AuthTokenResponse:
    """Validate refresh token against database, rotate it, and issue fresh access token."""
    raw_token = payload.refresh_token
    try:
        decoded = decode_token(raw_token)
        if decoded.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expected refresh token",
            )
        user_id = decoded.get("sub")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(exc)}",
        )

    # Verify token exists and is not revoked in database
    t_hash = hash_token(raw_token)
    db_token = session.exec(
        select(RefreshToken).where(
            RefreshToken.token_hash == t_hash,
            RefreshToken.user_id == user_id,
        )
    ).first()

    if not db_token or db_token.is_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired or revoked",
        )

    # Check expiration
    now = datetime.now(timezone.utc)
    # Ensure expires_at is timezone-aware for comparison
    exp = db_token.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if exp < now:
        db_token.is_revoked = True
        session.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )

    # Revoke old refresh token (rotation)
    db_token.is_revoked = True

    # Look up user
    user = session.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Primary workspace
    membership = session.exec(
        select(WorkspaceMember).where(WorkspaceMember.user_id == user.id)
    ).first()
    workspace = session.get(Workspace, membership.workspace_id) if membership else None
    if not workspace:
        workspace = session.get(Workspace, "default_ws")
        role = "owner"
    else:
        role = membership.role

    # Generate new token pair
    new_access = create_access_token(
        user_id=user.id,
        email=user.email,
        workspace_id=workspace.id,
        role=role,
    )
    new_refresh = create_refresh_token(user_id=user.id)
    new_ref_payload = decode_token(new_refresh)

    new_db_ref = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(new_refresh),
        expires_at=datetime.fromtimestamp(new_ref_payload["exp"], tz=timezone.utc),
        is_revoked=False,
    )
    session.add(new_db_ref)
    session.commit()

    return AuthTokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        token_type="bearer",
        expires_in=3600,
        user=UserResponse.model_validate(user),
        active_workspace=WorkspaceResponse(
            id=workspace.id,
            name=workspace.name,
            slug=workspace.slug,
            plan_tier=workspace.plan_tier,
            role=role,
            created_at=workspace.created_at,
        ),
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Revoke active refresh token",
)
def logout(
    payload: RefreshTokenRequest,
    session: Session = Depends(get_db_session),
) -> Dict[str, str]:
    """Revoke refresh token to terminate session."""
    t_hash = hash_token(payload.refresh_token)
    db_token = session.exec(
        select(RefreshToken).where(RefreshToken.token_hash == t_hash)
    ).first()
    if db_token:
        db_token.is_revoked = True
        session.commit()
    return {"status": "logged_out", "message": "Session successfully terminated"}


@router.get(
    "/me",
    summary="Get current user profile and workspaces",
)
def get_me(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> Dict[str, Any]:
    """Return user profile and all workspace memberships with roles."""
    memberships = session.exec(
        select(WorkspaceMember).where(WorkspaceMember.user_id == current_user.id)
    ).all()

    workspaces_list = []
    for m in memberships:
        ws = session.get(Workspace, m.workspace_id)
        if ws:
            workspaces_list.append({
                "id": ws.id,
                "name": ws.name,
                "slug": ws.slug,
                "plan_tier": ws.plan_tier,
                "role": m.role,
                "created_at": ws.created_at.isoformat(),
            })

    return {
        "user": UserResponse.model_validate(current_user).model_dump(),
        "workspaces": workspaces_list,
    }
