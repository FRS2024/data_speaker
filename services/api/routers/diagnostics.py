"""
Diagnostics & AutoML Router for data_speaker.
Exposes endpoints for dataset health scoring, 1-click smart data hygiene remediation,
correlation heatmaps, Isolation Forest anomaly exploration, and AutoML baseline training.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from services.api.auth import AuthContext, require_role
from services.api.automl import run_automl
from services.api.database import get_db_session
from services.api.diagnostics import (
    compute_anomalies,
    compute_correlation_matrix,
    compute_data_health,
)
from services.api.models import (
    AnomalyReportResponse,
    ApplyHygieneRequest,
    ApplyHygieneResponse,
    AutoMLTrainRequest,
    AutoMLTrainResponse,
    CheckpointSummaryResponse,
    CorrelationMatrixResponse,
    DataHealthResponse,
    Session as DbSession,
)
from services.api.session_service import session_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sessions/{session_id}", tags=["diagnostics"])


def verify_session_access(session_id: str, ctx: AuthContext, db: Session) -> DbSession:
    """Validate that session exists and user has workspace-level permission to view it."""
    session_obj = db.get(DbSession, session_id)
    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found",
        )

    # Multi-tenant isolation check
    if (
        session_obj.workspace_id
        and ctx.workspace
        and session_obj.workspace_id != ctx.workspace.id
        and not ctx.is_guest
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: session belongs to another workspace",
        )

    return session_obj


@router.get(
    "/diagnostics/health",
    response_model=DataHealthResponse,
    summary="Compute comprehensive dataset health score and actionable hygiene recommendations",
)
def get_session_health(
    session_id: str,
    ctx: AuthContext = Depends(require_role("viewer")),
    db: Session = Depends(get_db_session),
) -> DataHealthResponse:
    verify_session_access(session_id, ctx, db)
    df = session_service.get_active_dataframe(db, session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active dataset found for session '{session_id}'",
        )

    return compute_data_health(df, session_id)


@router.post(
    "/diagnostics/hygiene/apply",
    response_model=ApplyHygieneResponse,
    summary="1-Click apply smart hygiene fix, creating a versioned checkpoint and audit turn",
)
async def apply_hygiene_fix(
    session_id: str,
    req: ApplyHygieneRequest,
    ctx: AuthContext = Depends(require_role("analyst")),
    db: Session = Depends(get_db_session),
) -> ApplyHygieneResponse:
    verify_session_access(session_id, ctx, db)

    try:
        checkpoint, profile, python_code = await session_service.apply_hygiene_remediation(
            db=db,
            session_id=session_id,
            action=req.action,
            column=req.column,
            parameters=req.parameters,
        )
    except Exception as e:
        logger.error(f"Hygiene remediation error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to apply hygiene remediation: {str(e)}",
        )

    summary_resp = CheckpointSummaryResponse(
        id=checkpoint.id,
        session_id=checkpoint.session_id,
        version_tag=checkpoint.version_tag,
        operation_summary=checkpoint.operation_summary,
        row_count=checkpoint.row_count,
        column_count=checkpoint.column_count,
        memory_bytes=checkpoint.memory_bytes,
        created_at=checkpoint.created_at,
        is_active=True,
    )

    return ApplyHygieneResponse(
        status="success",
        session_id=session_id,
        checkpoint=summary_resp,
        profile=profile,
        applied_code=python_code,
        message=f"Successfully applied {req.action}. Created checkpoint {checkpoint.version_tag}.",
    )


@router.get(
    "/diagnostics/correlations",
    response_model=CorrelationMatrixResponse,
    summary="Calculate Pearson and Spearman correlation matrices for numeric features",
)
def get_session_correlations(
    session_id: str,
    ctx: AuthContext = Depends(require_role("viewer")),
    db: Session = Depends(get_db_session),
) -> CorrelationMatrixResponse:
    verify_session_access(session_id, ctx, db)
    df = session_service.get_active_dataframe(db, session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active dataset found for session '{session_id}'",
        )

    return compute_correlation_matrix(df, session_id)


@router.get(
    "/diagnostics/anomalies",
    response_model=AnomalyReportResponse,
    summary="Unsupervised multivariate Isolation Forest anomaly detection",
)
def get_session_anomalies(
    session_id: str,
    contamination: float = Query(0.05, ge=0.01, le=0.20),
    max_records: int = Query(50, ge=5, le=200),
    ctx: AuthContext = Depends(require_role("viewer")),
    db: Session = Depends(get_db_session),
) -> AnomalyReportResponse:
    verify_session_access(session_id, ctx, db)
    df = session_service.get_active_dataframe(db, session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active dataset found for session '{session_id}'",
        )

    return compute_anomalies(
        df,
        session_id=session_id,
        contamination=contamination,
        max_records=max_records,
    )


@router.post(
    "/automl/train",
    response_model=AutoMLTrainResponse,
    summary="Run fast-bounded AutoML baseline training, metric leaderboard, and code generation",
)
def train_automl_baseline(
    session_id: str,
    req: AutoMLTrainRequest,
    ctx: AuthContext = Depends(require_role("analyst")),
    db: Session = Depends(get_db_session),
) -> AutoMLTrainResponse:
    verify_session_access(session_id, ctx, db)
    df = session_service.get_active_dataframe(db, session_id)
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active dataset found for session '{session_id}'",
        )

    try:
        return run_automl(
            df=df,
            session_id=session_id,
            target_column=req.target_column,
            problem_type=req.problem_type,
            selected_features=req.selected_features,
            max_rows=req.max_rows,
        )
    except Exception as e:
        logger.error(f"AutoML baseline training error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"AutoML training failed: {str(e)}",
        )
