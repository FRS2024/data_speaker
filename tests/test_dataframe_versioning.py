"""
Tests for Phase 5: DataFrame Versioning, Checkpointing & Time-Travel Rollback.
"""

import pytest
import pandas as pd
from pathlib import Path
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from services.api.database import get_db_session
from services.api.models import DataFrameCheckpoint, Session as DbSession
from services.api.session_service import session_service
from services.sandbox.client import LocalSandboxClient


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
async def test_initial_checkpoint_created_on_upload(test_db: Session, tmp_path: Path):
    # Setup sample CSV
    csv_content = b"id,name,salary,department\n1,Alice,90000,Engineering\n2,Bob,75000,Sales\n3,Charlie,110000,Engineering\n"
    session_obj = session_service.create_session(test_db, title="Versioning Test Session")
    
    # Ingest
    session_file, profiles = await session_service.ingest_file(
        db=test_db,
        session_id=session_obj.id,
        filename="staff.csv",
        content=csv_content,
    )

    assert session_file is not None
    assert len(profiles) == 1
    assert profiles[0].row_count == 3
    assert profiles[0].column_count == 4

    # Verify initial df_v0 checkpoint in DB
    checkpoints = session_service.list_checkpoints(test_db, session_obj.id)
    assert len(checkpoints) == 1
    assert checkpoints[0].version_tag == "df_v0"
    assert checkpoints[0].row_count == 3
    assert checkpoints[0].column_count == 4
    assert checkpoints[0].is_active is True


@pytest.mark.asyncio
async def test_incremental_checkpoint_on_dataframe_mutation(test_db: Session):
    csv_content = b"id,name,salary\n1,Alice,90000\n2,Bob,75000\n3,Charlie,110000\n"
    session_obj = session_service.create_session(test_db, title="Mutation Checkpoint Test")
    
    await session_service.ingest_file(
        db=test_db,
        session_id=session_obj.id,
        filename="staff.csv",
        content=csv_content,
    )

    # 1. Non-mutating code: simple print / aggregate
    res1 = await session_service.execute_code(
        db=test_db,
        session_id=session_obj.id,
        code="print(df['salary'].mean())",
        user_prompt="Compute mean salary",
    )
    assert res1.status == "success"
    assert res1.has_mutated_dataframe is False
    
    # Checkpoint count should still be 1 (df_v0)
    chks1 = session_service.list_checkpoints(test_db, session_obj.id)
    assert len(chks1) == 1

    # 2. Mutating code: add a new column 'bonus'
    res2 = await session_service.execute_code(
        db=test_db,
        session_id=session_obj.id,
        code="df['bonus'] = df['salary'] * 0.15\nprint('Added bonus column')",
        user_prompt="Calculate 15% bonus",
    )
    assert res2.status == "success"
    assert res2.has_mutated_dataframe is True

    # Checkpoint count should now be 2 (df_v0, df_v1)
    chks2 = session_service.list_checkpoints(test_db, session_obj.id)
    assert len(chks2) == 2
    assert chks2[1].version_tag == "df_v1"
    assert chks2[1].column_count == 4
    assert chks2[1].row_count == 3
    assert chks2[1].is_active is True

    # Verify schema diff
    diff = chks2[1].diff_from_previous
    assert diff is not None
    assert diff.column_delta == 1
    assert diff.row_delta == 0
    assert "bonus" in diff.columns_added

    # 3. Another mutating code: filter rows
    res3 = await session_service.execute_code(
        db=test_db,
        session_id=session_obj.id,
        code="df = df[df['salary'] >= 90000]\nprint('Filtered high earners')",
        user_prompt="Keep salaries >= 90000",
    )
    assert res3.status == "success"
    assert res3.has_mutated_dataframe is True

    chks3 = session_service.list_checkpoints(test_db, session_obj.id)
    assert len(chks3) == 3
    assert chks3[2].version_tag == "df_v2"
    assert chks3[2].row_count == 2
    assert chks3[2].diff_from_previous.row_delta == -1


@pytest.mark.asyncio
async def test_time_travel_rollback(test_db: Session):
    csv_content = b"id,val\n1,10\n2,20\n3,30\n"
    session_obj = session_service.create_session(test_db, title="Time Travel Test")
    
    await session_service.ingest_file(
        db=test_db,
        session_id=session_obj.id,
        filename="vals.csv",
        content=csv_content,
    )

    # Mutate 1: add col
    await session_service.execute_code(
        db=test_db,
        session_id=session_obj.id,
        code="df['multiplier'] = 2",
        user_prompt="Add multiplier",
    )
    # Mutate 2: filter rows
    await session_service.execute_code(
        db=test_db,
        session_id=session_obj.id,
        code="df = df.head(1)",
        user_prompt="Keep top 1",
    )

    # Verify we are at df_v2 with 1 row, 3 cols
    test_db.refresh(session_obj)
    assert session_obj.active_dataframe_version == "df_v2"

    # Roll back to df_v0!
    updated_session, profile = await session_service.revert_to_version(
        db=test_db,
        session_id=session_obj.id,
        version_tag="df_v0",
    )

    assert updated_session.active_dataframe_version == "df_v0"
    assert profile.row_count == 3
    assert profile.column_count == 2

    # Verify sandbox kernel 'df' is restored in memory
    sandbox = session_service.get_or_create_sandbox_client(session_obj.id)
    state = sandbox.get_state()
    df_meta = state["dataframes"]["df"]
    assert df_meta["shape"] == [3, 2]
