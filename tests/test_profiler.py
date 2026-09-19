"""
Unit tests for the Universal Ingestion & Schema Profiling Engine (services/api/profiler.py).
Tests encoding/delimiter sniffing, schema profiling, JSON sanitization, and multiple tabular formats.
"""

import json
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import polars as pl
import pytest

from services.api.profiler import (
    detect_encoding_and_delimiter,
    generate_loader_code,
    profile_dataframe,
    read_file_to_dataframes,
    sanitize_value,
)


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


def test_detect_delimiter_and_encoding_csv(temp_dir: Path):
    """Test sniffing standard comma-separated and semicolon-separated CSVs."""
    csv_file = temp_dir / "sample.csv"
    csv_file.write_text("name,age,salary\nAlice,30,75000\nBob,25,50000\n", encoding="utf-8")

    encoding, delimiter = detect_encoding_and_delimiter(csv_file)
    assert encoding == "utf-8"
    assert delimiter == ","

    # Semicolon delimited
    semi_file = temp_dir / "semi.csv"
    semi_file.write_text("id;product;price\n1;Laptop;999.99\n2;Mouse;29.50\n", encoding="utf-8")
    _, delimiter_semi = detect_encoding_and_delimiter(semi_file)
    assert delimiter_semi == ";"

    # Tab delimited
    tsv_file = temp_dir / "sample.tsv"
    tsv_file.write_text("col_a\tcol_b\n10\t20\n30\t40\n", encoding="utf-8")
    _, delimiter_tsv = detect_encoding_and_delimiter(tsv_file)
    assert delimiter_tsv == "\t"


def test_sanitize_value_rfc_8259():
    """Verify that NaNs, Infs, dates, and numpy scalars are sanitized for RFC 8259 JSON."""
    assert sanitize_value(float("nan")) is None
    assert sanitize_value(float("inf")) is None
    assert sanitize_value(float("-inf")) is None
    assert sanitize_value(np.nan) is None
    assert sanitize_value(None) is None
    assert sanitize_value(42) == 42
    assert sanitize_value("hello") == "hello"
    assert sanitize_value(True) is True
    assert sanitize_value(np.int64(100)) == 100
    assert sanitize_value(np.float64(3.14)) == pytest.approx(3.14)


def test_profile_dataframe_metrics():
    """Test schema metrics computation (null percentage, cardinality, preview)."""
    df = pl.DataFrame({
        "user_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "category": ["A", "B", "A", "B", "C", "A", None, "B", "C", "A"],
        "metric": [1.1, np.nan, 3.3, 4.4, np.nan, 6.6, 7.7, 8.8, 9.9, 10.0],
    })

    profile = profile_dataframe(df=df, session_id="test_sess", table_name="df_test")

    assert profile.session_id == "test_sess"
    assert profile.table_name == "df_test"
    assert profile.row_count == 10
    assert profile.column_count == 3
    assert profile.memory_footprint_mb >= 0.0

    col_map = {c.name: c for c in profile.columns}
    assert "user_id" in col_map
    assert col_map["user_id"].null_count == 0
    assert col_map["user_id"].cardinality == 10

    assert "category" in col_map
    assert col_map["category"].null_count == 1
    assert col_map["category"].null_percentage == 10.0

    assert "metric" in col_map
    assert col_map["metric"].null_count == 2
    assert col_map["metric"].null_percentage == 20.0

    # Ensure sample values do not contain NaNs
    for s in col_map["metric"].sample_values:
        assert s is not None

    # Verify preview markdown exists and contains column names
    assert "user_id" in profile.head_preview_markdown
    assert "category" in profile.head_preview_markdown

    # Verify strict JSON serializability
    json_str = json.dumps(profile.model_dump())
    assert "NaN" not in json_str
    assert "Infinity" not in json_str


def test_parquet_ingestion(temp_dir: Path):
    """Test reading and profiling a Parquet file."""
    pq_path = temp_dir / "dataset.parquet"
    df = pl.DataFrame({"idx": range(100), "val": [f"item_{i}" for i in range(100)]})
    df.write_parquet(pq_path)

    dfs = read_file_to_dataframes(pq_path)
    assert len(dfs) == 1
    table_name = list(dfs.keys())[0]
    assert table_name == "df_dataset"
    assert dfs[table_name].height == 100

    profile = profile_dataframe(dfs[table_name], session_id="pq_sess", table_name=table_name)
    assert profile.row_count == 100
    assert profile.column_count == 2


def test_excel_ingestion(temp_dir: Path):
    """Test reading and profiling an Excel file."""
    xlsx_path = temp_dir / "sample.xlsx"
    pdf = pd.DataFrame({"quarter": ["Q1", "Q2", "Q3", "Q4"], "revenue": [100, 150, 200, 250]})
    pdf.to_excel(xlsx_path, index=False)

    dfs = read_file_to_dataframes(xlsx_path)
    assert len(dfs) == 1
    table_name = list(dfs.keys())[0]
    assert dfs[table_name].height == 4

    profile = profile_dataframe(dfs[table_name], session_id="xl_sess", table_name=table_name)
    assert profile.row_count == 4
    assert profile.column_count == 2


def test_sqlite_multi_table_ingestion(temp_dir: Path):
    """Test reading and profiling a multi-table SQLite database."""
    db_path = temp_dir / "test_store.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE customers (id INT PRIMARY KEY, name TEXT);")
    cursor.execute("INSERT INTO customers VALUES (1, 'Alice'), (2, 'Bob');")
    cursor.execute("CREATE TABLE orders (order_id INT, customer_id INT, total REAL);")
    cursor.execute("INSERT INTO orders VALUES (101, 1, 59.99), (102, 1, 12.50), (103, 2, 99.00);")
    conn.commit()
    conn.close()

    dfs = read_file_to_dataframes(db_path)
    assert "df_customers" in dfs
    assert "df_orders" in dfs
    assert dfs["df_customers"].height == 2
    assert dfs["df_orders"].height == 3


def test_generate_loader_code(temp_dir: Path):
    """Test synthesis of Python dataset loading code."""
    csv_path = temp_dir / "orders.csv"
    code = generate_loader_code(csv_path, table_name="df_orders", container_mount_path="/data/orders.csv")
    assert "pd.read_csv(r'/data/orders.csv'" in code
    assert "df = df_orders" in code
