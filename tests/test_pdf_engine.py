"""
Tests for Track C Executive PDF Brief Engine (services.api.pdf_engine).
"""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from services.api.models import (
    DataFrameCheckpoint,
    Session as DbSession,
)
from services.api.pdf_engine import pdf_engine


@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def mock_session_with_data(test_db: Session, tmp_path: Path):
    """Creates a test session with a versioned Parquet checkpoint."""
    session = DbSession(
        id="test-pdf-session-456",
        title="Revenue & Margin Diagnostics Brief",
        active_dataframe_version="df_v0",
        workspace_id="default_ws",
    )
    test_db.add(session)
    test_db.commit()

    # Create dummy DataFrame
    np.random.seed(42)
    df = pd.DataFrame({
        "mrr": np.random.uniform(500, 5000, 60),
        "arpu": np.random.uniform(20, 80, 60),
        "cac": np.random.uniform(100, 300, 60),
        "region": np.random.choice(["EMEA", "APAC", "AMER"], 60),
    })

    parquet_path = tmp_path / "df_v0.parquet"
    df.to_parquet(parquet_path, index=False)

    chk = DataFrameCheckpoint(
        checkpoint_id="chk_pdf_001",
        session_id="test-pdf-session-456",
        version_tag="df_v0",
        parquet_storage_path=str(parquet_path),
        row_count=len(df),
        column_count=len(df.columns),
        operation_summary="Initial ingestion",
        is_active=True,
    )
    test_db.add(chk)
    test_db.commit()

    return session


def test_pdf_report_compilation(test_db: Session, mock_session_with_data):
    """Test compiling executive PDF brief using ReportLab."""
    pdf_bytes = pdf_engine.build_pdf_report(
        test_db,
        "test-pdf-session-456",
        title="Executive Margin Review",
        author="Lead Data Strategist",
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000

    # Verify standard PDF magic number header
    assert pdf_bytes.startswith(b"%PDF-")

    # Verify non-trivial size
    assert len(pdf_bytes) >= 3000
