"""
Authentication & Authorization dependencies for services/api.
Implements JWT token extraction, user resolution, workspace context isolation,
and Role-Based Access Control (RBAC) guards.
"""

from __future__ import annotations

from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlmodel import Session, select

from services.api.database import get_db_session
from services.api.models import User, Workspace, WorkspaceMember
from services.api.security import decode_token

# Role hierarchy: viewer < analyst < admin < owner
ROLE_HIERARCHY = {
    "viewer": 10,
    "analyst": 20,
    "admin": 30,
    "owner": 40,
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)


from pydantic import BaseModel, ConfigDict


class AuthContext(BaseModel):
    """Execution context containing authenticated user, active workspace, and assigned role."""
    user: User
    workspace: Workspace
    role: str
    is_guest: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)


def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    session: Session = Depends(get_db_session),
) -> Optional[User]:
    """
    Extract and validate JWT Bearer token if present.
    Returns None if unauthenticated, or User instance if valid.
    """
    if not token:
        return None

    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type: expected access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Malformed token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(exc)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account inactive or not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_user(
    user: Optional[User] = Depends(get_current_user_optional),
) -> User:
    """Strict authentication guard requiring a valid logged-in user."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_auth_context(
    request: Request,
    user: Optional[User] = Depends(get_current_user_optional),
    session: Session = Depends(get_db_session),
) -> AuthContext:
    """
    Resolves the active tenant context (User + Workspace + Role).
    If unauthenticated, seamlessly falls back to the Default Workspace and Guest User
    to preserve 100% backward compatibility for existing tests and guest exploration.
    """
    # 1. Unauthenticated / Guest fallback
    if not user:
        default_ws = session.get(Workspace, "default_ws")
        if not default_ws:
            default_ws = Workspace(
                id="default_ws",
                name="Default Workspace",
                slug="default-workspace",
                plan_tier="free",
            )
            session.add(default_ws)
            session.commit()
            session.refresh(default_ws)

        guest_usr = session.get(User, "guest_usr")
        if not guest_usr:
            guest_usr = User(
                id="guest_usr",
                email="guest@dataspkr.local",
                hashed_password="guest_disabled_password",
                full_name="Guest Analyst",
                is_active=True,
            )
            session.add(guest_usr)
            session.commit()
            session.refresh(guest_usr)

        return AuthContext(
            user=guest_usr,
            workspace=default_ws,
            role="owner",
            is_guest=True,
        )

    # 2. Authenticated user: resolve requested or default workspace
    requested_ws_id = request.headers.get("x-workspace-id")
    membership: Optional[WorkspaceMember] = None

    if requested_ws_id:
        membership = session.exec(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == requested_ws_id,
                WorkspaceMember.user_id == user.id,
            )
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: you are not a member of workspace '{requested_ws_id}'",
            )
        active_workspace = session.get(Workspace, requested_ws_id)
    else:
        # Resolve user's primary/first workspace
        membership = session.exec(
            select(WorkspaceMember).where(WorkspaceMember.user_id == user.id)
        ).first()

        if not membership:
            # Auto-create personal workspace
            clean_name = user.full_name or user.email.split("@")[0]
            personal_ws = Workspace(
                name=f"{clean_name}'s Workspace",
                slug=f"{clean_name.lower().replace(' ', '-')}-workspace",
                plan_tier="free",
                created_by=user.id,
            )
            session.add(personal_ws)
            session.commit()
            session.refresh(personal_ws)

            membership = WorkspaceMember(
                workspace_id=personal_ws.id,
                user_id=user.id,
                role="owner",
            )
            session.add(membership)
            session.commit()
            active_workspace = personal_ws
        else:
            active_workspace = session.get(Workspace, membership.workspace_id)

    if not active_workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active workspace not found",
        )

    return AuthContext(
        user=user,
        workspace=active_workspace,
        role=membership.role,
        is_guest=False,
    )


def require_role(min_role: str):
    """
    Dependency factory that enforces the RBAC role hierarchy.
    Usage: Depends(require_role("analyst"))
    """
    def rbac_dependency(
        ctx: AuthContext = Depends(get_auth_context),
    ) -> AuthContext:
        user_level = ROLE_HIERARCHY.get(ctx.role, 0)
        required_level = ROLE_HIERARCHY.get(min_role, 0)

        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: action requires '{min_role}' role (current: '{ctx.role}')",
            )
        return ctx

    return rbac_dependency
