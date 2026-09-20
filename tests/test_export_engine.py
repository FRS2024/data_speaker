"""
Tests for Phase 5: Multi-Format Export Engine.
"""

import io
import json
import pytest
import pandas as pd
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from services.api.exporter import export_engine
from services.api.models import ChatTurn, DataFrameCheckpoint, Session as DbSession
from services.api.session_service import session_service


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


@pytest.mark.asyncio
async def test_dataset_exports(test_db: Session):
    csv_content = b"dept,budget,headcount\nSales,500000,12\nEngineering,1200000,25\nMarketing,300000,8\n"
    session_obj = session_service.create_session(test_db, title="Q3 Budget Analysis")
    
    await session_service.ingest_file(
        db=test_db,
        session_id=session_obj.id,
        filename="budget.csv",
        content=csv_content,
    )

    # 1. Export as CSV
    csv_bytes, mime_csv, fn_csv = export_engine.export_dataset(test_db, session_obj.id, "csv")
    assert mime_csv == "text/csv"
    assert fn_csv.endswith(".csv")
    df_read_csv = pd.read_csv(io.BytesIO(csv_bytes))
    assert len(df_read_csv) == 3
    assert list(df_read_csv.columns) == ["dept", "budget", "headcount"]

    # 2. Export as Parquet
    pq_bytes, mime_pq, fn_pq = export_engine.export_dataset(test_db, session_obj.id, "parquet")
    assert mime_pq == "application/octet-stream"
    assert fn_pq.endswith(".parquet")
    df_read_pq = pd.read_parquet(io.BytesIO(pq_bytes))
    assert len(df_read_pq) == 3

    # 3. Export as Excel
    xlsx_bytes, mime_xlsx, fn_xlsx = export_engine.export_dataset(test_db, session_obj.id, "xlsx")
    assert "spreadsheetml" in mime_xlsx
    assert fn_xlsx.endswith(".xlsx")
    df_read_xlsx = pd.read_excel(io.BytesIO(xlsx_bytes))
    assert len(df_read_xlsx) == 3
    assert "Engineering" in df_read_xlsx["dept"].values


@pytest.mark.asyncio
async def test_jupyter_notebook_export(test_db: Session):
    csv_content = b"x,y\n1,10\n2,20\n3,30\n"
    session_obj = session_service.create_session(test_db, title="Scatter Exploration")
    
    await session_service.ingest_file(
        db=test_db,
        session_id=session_obj.id,
        filename="points.csv",
        content=csv_content,
    )

    # Add a mock chat turn
    await session_service.execute_code(
        db=test_db,
        session_id=session_obj.id,
        code="df['z'] = df['x'] + df['y']\nprint('Computed z col')",
        user_prompt="Compute sum of x and y into z",
    )

    nb_bytes, mime_nb, fn_nb = export_engine.export_jupyter_notebook(test_db, session_obj.id)
    assert mime_nb == "application/x-ipynb+json"
    assert fn_nb.endswith(".ipynb")

    nb_data = json.loads(nb_bytes.decode("utf-8"))
    assert nb_data["nbformat"] == 4
    assert len(nb_data["cells"]) >= 4  # Header, setup, ingest, step
    
    # Check that the code was preserved
    code_cells = [c for c in nb_data["cells"] if c["cell_type"] == "code"]
    assert any("df['z'] = df['x'] + df['y']" in "".join(c["source"]) for c in code_cells)


@pytest.mark.asyncio
async def test_executive_report_export(test_db: Session):
    csv_content = b"metric,value\nRevenue,1500000\nCost,800000\nProfit,700000\n"
    session_obj = session_service.create_session(test_db, title="Financial Summary")
    
    await session_service.ingest_file(
        db=test_db,
        session_id=session_obj.id,
        filename="finance.csv",
        content=csv_content,
    )

    await session_service.execute_code(
        db=test_db,
        session_id=session_obj.id,
        code="margin = (700000 / 1500000) * 100\nprint(f'Profit margin: {margin:.1f}%')",
        user_prompt="Calculate profit margin percentage",
    )

    rep_bytes, mime_rep, fn_rep = export_engine.export_executive_report(test_db, session_obj.id)
    assert mime_rep == "text/markdown"
    assert fn_rep.endswith(".md")

    report_text = rep_bytes.decode("utf-8")
    assert "# Executive Data Analysis Report: Financial Summary" in report_text
    assert "Schema Architecture" in report_text
    assert "Calculate profit margin percentage" in report_text
    assert "Profit margin: 46.7%" in report_text
    assert "Version History & Checkpoint Log" in report_text
