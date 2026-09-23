"""
Base interface and abstractions for external cloud data warehouse connectors.
Supports BigQuery, Snowflake, and future OLAP databases.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from services.api.models import DataFrameProfile


class BaseWarehouseConnector(ABC):
    """Abstract interface for external analytical data warehouse connections."""

    def __init__(self, name: str, connector_type: str) -> None:
        self.name = name
        self.connector_type = connector_type

    @property
    @abstractmethod
    def is_configured(self) -> bool:
        """Return True if required environment variables or credentials exist."""
        pass

    @abstractmethod
    def get_status(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return connector health and configuration metadata."""
        pass

    @abstractmethod
    def test_connection(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Verify network connectivity and credentials with the cloud warehouse."""
        pass

    @abstractmethod
    def list_datasets(self, config: Optional[Dict[str, Any]] = None) -> List[str]:
        """List accessible datasets or databases."""
        pass

    @abstractmethod
    def list_tables(self, dataset_id: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
        """List tables within a specified dataset."""
        pass

    @abstractmethod
    def preview_table(
        self,
        dataset_id: str,
        table_id: str,
        limit: int = 50,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Preview top rows from an external table."""
        pass

    @abstractmethod
    def execute_and_import(
        self,
        session_id: str,
        sql_query: str,
        destination_table_name: str,
        target_dir: Path,
        config: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> Tuple[Path, DataFrameProfile]:
        """
        Execute an analytical SQL query against the warehouse, download the result
        as a compressed Parquet file into session storage, and return its profile.
        """
        pass
