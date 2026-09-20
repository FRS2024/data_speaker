"""
Workspaces router: Workspace creation, membership, role-based member management, and team invites.
"""

from __future__ import annotations

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from services.api.auth import AuthContext, get_auth_context, get_current_user, require_role
from services.api.database import get_db_session
from services.api.models import (
    InviteMemberRequest,
    UpdateMemberRoleRequest,
    User,
    Workspace,
    WorkspaceCreateRequest,
    WorkspaceMember,
    WorkspaceMemberResponse,
    WorkspaceResponse,
)

router = APIRouter(prefix="/api/v1/workspaces", tags=["workspaces"])


@router.get(
    "",
    response_model=List[WorkspaceResponse],
    summary="List all workspaces accessible by the current user",
)
def list_workspaces(
    ctx: AuthContext = Depends(get_auth_context),
    session: Session = Depends(get_db_session),
) -> List[WorkspaceResponse]:
    """Retrieve all workspaces where the user has an active membership."""
    memberships = session.exec(
        select(WorkspaceMember).where(WorkspaceMember.user_id == ctx.user.id)
    ).all()

    workspaces = []
    for m in memberships:
        ws = session.get(Workspace, m.workspace_id)
        if ws:
            workspaces.append(
                WorkspaceResponse(
                    id=ws.id,
                    name=ws.name,
                    slug=ws.slug,
                    plan_tier=ws.plan_tier,
                    role=m.role,
                    created_at=ws.created_at,
                )
            )

    # Fallback to current context workspace if list is empty
    if not workspaces and ctx.workspace:
        workspaces.append(
            WorkspaceResponse(
                id=ctx.workspace.id,
                name=ctx.workspace.name,
                slug=ctx.workspace.slug,
                plan_tier=ctx.workspace.plan_tier,
                role=ctx.role,
                created_at=ctx.workspace.created_at,
            )
        )

    return workspaces


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new workspace",
)
def create_workspace(
    payload: WorkspaceCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> WorkspaceResponse:
    """Create a new workspace and assign the calling user as the Owner."""
    name = payload.name.strip()
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace name cannot be empty",
        )

    slug = name.lower().replace(" ", "-")
    workspace = Workspace(
        name=name,
        slug=slug,
        plan_tier="free",
        created_by=current_user.id,
    )
    session.add(workspace)
    session.commit()
    session.refresh(workspace)

    member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=current_user.id,
        role="owner",
    )
    session.add(member)
    session.commit()

    return WorkspaceResponse(
        id=workspace.id,
        name=workspace.name,
        slug=workspace.slug,
        plan_tier=workspace.plan_tier,
        role="owner",
        created_at=workspace.created_at,
    )


@router.get(
    "/{workspace_id}/members",
    response_model=List[WorkspaceMemberResponse],
    summary="List members and assigned roles in a workspace",
)
def list_workspace_members(
    workspace_id: str,
    ctx: AuthContext = Depends(get_auth_context),
    session: Session = Depends(get_db_session),
) -> List[WorkspaceMemberResponse]:
    """Retrieve all team members and their roles in the workspace."""
    # Check calling user has access to this workspace
    user_member = session.exec(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == ctx.user.id,
        )
    ).first()

    if not user_member and not ctx.is_guest:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: you are not a member of this workspace",
        )

    members = session.exec(
        select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id)
    ).all()

    results = []
    for m in members:
        u = session.get(User, m.user_id)
        if u:
            results.append(
                WorkspaceMemberResponse(
                    id=m.id,
                    workspace_id=m.workspace_id,
                    user_id=m.user_id,
                    email=u.email,
                    full_name=u.full_name or u.email.split("@")[0],
                    role=m.role,
                    created_at=m.created_at,
                )
            )

    return results


@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Invite or add a user to the workspace with a role",
)
def invite_workspace_member(
    workspace_id: str,
    payload: InviteMemberRequest,
    ctx: AuthContext = Depends(require_role("admin")),
    session: Session = Depends(get_db_session),
) -> WorkspaceMemberResponse:
    """Invite an existing user or add them to the workspace by email (requires Admin+ role)."""
    target_email = payload.email.strip().lower()
    valid_roles = {"admin", "analyst", "viewer"}
    if payload.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role '{payload.role}'. Must be one of: {', '.join(valid_roles)}",
        )

    # Ensure workspace exists
    workspace = session.get(Workspace, workspace_id)
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace '{workspace_id}' not found",
        )

    # Find or auto-provision invited user
    target_user = session.exec(
        select(User).where(User.email == target_email)
    ).first()

    if not target_user:
        # Create a pending/invited user account
        target_user = User(
            email=target_email,
            hashed_password="invited_user_placeholder",
            full_name=target_email.split("@")[0],
            is_active=True,
        )
        session.add(target_user)
        session.commit()
        session.refresh(target_user)

    # Check if already a member
    existing = session.exec(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == target_user.id,
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this workspace",
        )

    member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=target_user.id,
        role=payload.role,
    )
    session.add(member)
    session.commit()
    session.refresh(member)

    return WorkspaceMemberResponse(
        id=member.id,
        workspace_id=member.workspace_id,
        user_id=member.user_id,
        email=target_user.email,
        full_name=target_user.full_name,
        role=member.role,
        created_at=member.created_at,
    )


@router.patch(
    "/{workspace_id}/members/{user_id}",
    response_model=WorkspaceMemberResponse,
    summary="Update member role in workspace",
)
def update_member_role(
    workspace_id: str,
    user_id: str,
    payload: UpdateMemberRoleRequest,
    ctx: AuthContext = Depends(require_role("admin")),
    session: Session = Depends(get_db_session),
) -> WorkspaceMemberResponse:
    """Modify a member's role within the workspace (requires Admin+ role)."""
    valid_roles = {"admin", "analyst", "viewer"}
    if payload.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role '{payload.role}'. Must be one of: {', '.join(valid_roles)}",
        )

    member = session.exec(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace membership not found",
        )

    if member.role == "owner" and ctx.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the Owner can modify Owner permissions",
        )

    member.role = payload.role
    session.commit()
    session.refresh(member)

    target_user = session.get(User, user_id)

    return WorkspaceMemberResponse(
        id=member.id,
        workspace_id=member.workspace_id,
        user_id=member.user_id,
        email=target_user.email if target_user else "unknown",
        full_name=target_user.full_name if target_user else "",
        role=member.role,
        created_at=member.created_at,
    )


@router.delete(
    "/{workspace_id}/members/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove a member from the workspace",
)
def remove_workspace_member(
    workspace_id: str,
    user_id: str,
    ctx: AuthContext = Depends(require_role("admin")),
    session: Session = Depends(get_db_session),
) -> Dict[str, str]:
    """Remove a user from the workspace."""
    member = session.exec(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found in this workspace",
        )

    if member.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot remove the workspace Owner",
        )

    session.delete(member)
    session.commit()

    return {"status": "removed", "message": f"User '{user_id}' removed from workspace"}
