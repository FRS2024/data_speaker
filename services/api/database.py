"""
Database configuration and session lifecycle management for services/api.
Compatible with SQLite (local development) and PostgreSQL (production).
"""

import os
from pathlib import Path
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

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


def create_db_and_tables() -> None:
    """Initialize all registered SQLModel tables in the database."""
    SQLModel.metadata.create_all(engine)


def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency for database session injection."""
    with Session(engine) as session:
        yield session
