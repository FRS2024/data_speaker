"""
Warehouse connectors registry for data_speaker.
Supports PostgreSQL (Neon/Supabase/RDS), Google BigQuery, Snowflake, and Databricks Lakehouse.
"""

from services.api.connectors.base import BaseWarehouseConnector
from services.api.connectors.bigquery import BigQueryConnector
from services.api.connectors.databricks import DatabricksConnector
from services.api.connectors.postgres import PostgreSQLConnector
from services.api.connectors.snowflake import SnowflakeConnector

postgres_connector = PostgreSQLConnector()
bigquery_connector = BigQueryConnector()
snowflake_connector = SnowflakeConnector()
databricks_connector = DatabricksConnector()

CONNECTORS = {
    "postgres": postgres_connector,
    "bigquery": bigquery_connector,
    "snowflake": snowflake_connector,
    "databricks": databricks_connector,
}

__all__ = [
    "BaseWarehouseConnector",
    "PostgreSQLConnector",
    "BigQueryConnector",
    "SnowflakeConnector",
    "DatabricksConnector",
    "postgres_connector",
    "bigquery_connector",
    "snowflake_connector",
    "databricks_connector",
    "CONNECTORS",
]
