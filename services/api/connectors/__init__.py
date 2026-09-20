"""
Warehouse connectors registry for data_speaker.
"""

from services.api.connectors.base import BaseWarehouseConnector
from services.api.connectors.bigquery import BigQueryConnector
from services.api.connectors.snowflake import SnowflakeConnector

bigquery_connector = BigQueryConnector()
snowflake_connector = SnowflakeConnector()

CONNECTORS = {
    "bigquery": bigquery_connector,
    "snowflake": snowflake_connector,
}

__all__ = [
    "BaseWarehouseConnector",
    "BigQueryConnector",
    "SnowflakeConnector",
    "bigquery_connector",
    "snowflake_connector",
    "CONNECTORS",
]
