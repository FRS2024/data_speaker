"""
Database configuration and session lifecycle management for services/api.
Compatible with SQLite (local development) and PostgreSQL (production).
"""

import os
from pathlib import Path
from typing import Generator
from sqlalchemy import event
from sqlmodel import SQLModel, Session, create_engine, select

# Read DATABASE_URL or default to SQLite in ./data
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/platform.db")

# If using SQLite, ensure the target directory exists and configure threading
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # Parse path to create directory if relative or absolute file path
    db_path_str = DATABASE_URL.replace("sqlite:///", "").replace("sqlite://", "")
    if db_path_str and db_path_str != ":memory:":
        db_path = Path(db_path_str)
        db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args,
)

if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def ensure_default_seed(session: Session) -> None:
    """Ensure default workspace and guest user exist for zero-friction fallback."""
    from services.api.models import User, Workspace, WorkspaceMember

    default_ws = session.get(Workspace, "default_ws")
    if not default_ws:
        default_ws = Workspace(
            id="default_ws",
            name="Default Workspace",
            slug="default-workspace",
            plan_tier="free",
        )
        session.add(default_ws)

    guest_user = session.get(User, "guest_usr")
    if not guest_user:
        guest_user = User(
            id="guest_usr",
            email="guest@dataspkr.local",
            hashed_password="guest_disabled_password",
            full_name="Guest Analyst",
            is_active=True,
        )
        session.add(guest_user)

    membership = session.exec(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == "default_ws",
            WorkspaceMember.user_id == "guest_usr",
        )
    ).first()
    if not membership:
        membership = WorkspaceMember(
            id="wsm_default_guest",
            workspace_id="default_ws",
            user_id="guest_usr",
            role="owner",
        )
        session.add(membership)

    session.commit()


from sqlalchemy import event, inspect, text


def patch_sqlite_columns() -> None:
    """Safely add new columns to existing SQLite tables if missing."""
    try:
        insp = inspect(engine)
        if insp.has_table("sessions"):
            cols = [c["name"] for c in insp.get_columns("sessions")]
            with engine.begin() as conn:
                if "workspace_id" not in cols:
                    conn.execute(text("ALTER TABLE sessions ADD COLUMN workspace_id VARCHAR DEFAULT 'default_ws'"))
                if "created_by" not in cols:
                    conn.execute(text("ALTER TABLE sessions ADD COLUMN created_by VARCHAR DEFAULT NULL"))
    except Exception:
        pass


def create_db_and_tables() -> None:
    """Initialize all registered SQLModel tables in the database and seed defaults."""
    SQLModel.metadata.create_all(engine)
    patch_sqlite_columns()
    with Session(engine) as session:
        ensure_default_seed(session)


def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency for database session injection."""
    with Session(engine) as session:
        yield session
