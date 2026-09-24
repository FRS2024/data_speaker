"""
Universal Ingestion and Schema Profiling Engine for data_speaker.
Supports CSV, TSV, Parquet, Excel, JSON, and SQLite with automatic encoding
detection, delimiter sniffing, privacy-safe RFC 8259 schema extraction,
and sandbox loader code synthesis.
"""

from __future__ import annotations

import csv
import math
import os
import re
import sqlite3
from datetime import date, datetime, time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import chardet
import pandas as pd
import polars as pl
from tabulate import tabulate

from services.api.models import ColumnProfile, DataFrameProfile


def clean_table_name(name: str) -> str:
    """Normalize a filename or table name into a valid Python identifier."""
    cleaned = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    cleaned = re.sub(r"^[^a-zA-Z_]+", "", cleaned)
    if not cleaned:
        cleaned = "data"
    return f"df_{cleaned.lower()}"


def detect_encoding_and_delimiter(file_path: Path) -> Tuple[str, str]:
    """
    Detect character encoding via chardet and sniff tabular delimiter.
    Falls back gracefully to ('utf-8', ',').
    """
    raw_sample = b""
    try:
        with open(file_path, "rb") as f:
            raw_sample = f.read(65536)  # 64 KB sample
    except Exception:
        return "utf-8", ","

    if not raw_sample:
        return "utf-8", ","

    # 1. Detect Encoding
    detected = chardet.detect(raw_sample)
    encoding = detected.get("encoding") or "utf-8"
    confidence = detected.get("confidence") or 0.0
    if confidence < 0.6:
        encoding = "utf-8"

    # Normalize common encoding aliases
    encoding_lower = encoding.lower().replace("-", "").replace("_", "")
    if "utf8" in encoding_lower:
        encoding = "utf-8"
    elif "ascii" in encoding_lower:
        encoding = "utf-8"
    elif "latin" in encoding_lower or "iso8859" in encoding_lower:
        encoding = "latin-1"
    elif "windows1252" in encoding_lower or "cp1252" in encoding_lower:
        encoding = "cp1252"

    # 2. Sniff Delimiter
    delimiter = ","
    try:
        text_sample = raw_sample.decode(encoding, errors="ignore")
        # Filter non-empty lines for sniffer
        lines = [line.strip() for line in text_sample.splitlines() if line.strip()][:20]
        if lines:
            sample_str = "\n".join(lines)
            dialect = csv.Sniffer().sniff(sample_str, delimiters=[",", "\t", ";", "|"])
            delimiter = dialect.delimiter
    except Exception:
        # Fallback heuristic: count common delimiters in first line
        try:
            first_line = text_sample.splitlines()[0]
            counts = {d: first_line.count(d) for d in [",", "\t", ";", "|"]}
            best = max(counts, key=counts.get)
            if counts[best] > 0:
                delimiter = best
        except Exception:
            delimiter = ","

    return encoding, delimiter


def sanitize_value(val: Any) -> Any:
    """Sanitize arbitrary Python/Pandas/Polars values for strict RFC 8259 JSON compliance."""
    if val is None or val is pl.Null:
        return None

    # Handle float NaNs and Infs
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return None
        return val

    if isinstance(val, (datetime, date, time)):
        return val.isoformat()

    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")

    # Handle numpy/polars scalar types
    if hasattr(val, "item"):
        try:
            native_val = val.item()
            if isinstance(native_val, float) and (math.isnan(native_val) or math.isinf(native_val)):
                return None
            return native_val
        except Exception:
            pass

    # Fallback to string if not basic JSON scalar
    if not isinstance(val, (int, str, bool)):
        try:
            if math.isnan(float(val)):
                return None
        except (ValueError, TypeError):
            return str(val)

    return val


def read_file_to_dataframes(file_path: Path) -> Dict[str, pl.DataFrame]:
    """
    Ingest a file of any supported format and return a dictionary of named DataFrames.
    For single-table files (CSV, Parquet), returns {table_name: pl.DataFrame}.
    For multi-table files (SQLite, multi-sheet Excel), returns {table_name: pl.DataFrame} per table.
    """
    suffix = file_path.suffix.lower()
    base_name = file_path.stem
    default_table = clean_table_name(base_name)
    dfs: Dict[str, pl.DataFrame] = {}

    # 1. Parquet
    if suffix in [".parquet", ".pq"]:
        df = pl.read_parquet(file_path)
        dfs[default_table] = df
        return dfs

    # 2. CSV / TSV / Delimited text
    if suffix in [".csv", ".tsv", ".txt", ".tab"]:
        encoding, delimiter = detect_encoding_and_delimiter(file_path)
        try:
            if encoding.lower() in ["utf-8", "ascii"]:
                df = pl.read_csv(
                    file_path,
                    separator=delimiter,
                    encoding="utf8",
                    infer_schema_length=10000,
                    ignore_errors=True,
                )
            else:
                # Use pandas fallback for non-UTF8 encodings (latin-1, cp1252, etc.)
                pdf = pd.read_csv(file_path, sep=delimiter, encoding=encoding, low_memory=False)
                df = pl.from_pandas(pdf)
        except Exception:
            # Universal fallback with pandas
            pdf = pd.read_csv(file_path, sep=delimiter, encoding=encoding, on_bad_lines="skip", low_memory=False)
            df = pl.from_pandas(pdf)

        dfs[default_table] = df
        return dfs

    # 3. Excel (.xlsx, .xls)
    if suffix in [".xlsx", ".xls"]:
        excel_dict = pd.read_excel(file_path, sheet_name=None)
        if not excel_dict:
            dfs[default_table] = pl.DataFrame()
            return dfs

        for sheet_name, sheet_df in excel_dict.items():
            t_name = clean_table_name(f"{base_name}_{sheet_name}") if len(excel_dict) > 1 else default_table
            dfs[t_name] = pl.from_pandas(sheet_df)
        return dfs

    # 4. JSON / NDJSON
    if suffix in [".json", ".jsonl", ".ndjson"]:
        try:
            df = pl.read_ndjson(file_path)
        except Exception:
            try:
                df = pl.read_json(file_path)
            except Exception:
                pdf = pd.read_json(file_path)
                df = pl.from_pandas(pdf)
        dfs[default_table] = df
        return dfs

    # 5. SQLite (.db, .sqlite, .sqlite3)
    if suffix in [".db", ".sqlite", ".sqlite3"]:
        conn = sqlite3.connect(str(file_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]
        if not tables:
            conn.close()
            dfs[default_table] = pl.DataFrame()
            return dfs

        for tbl in tables:
            t_name = clean_table_name(tbl)
            pdf = pd.read_sql_query(f'SELECT * FROM "{tbl}"', conn)
            dfs[t_name] = pl.from_pandas(pdf)
        conn.close()
        return dfs

    # Fallback attempt as CSV
    encoding, delimiter = detect_encoding_and_delimiter(file_path)
    pdf = pd.read_csv(file_path, sep=delimiter, encoding=encoding, on_bad_lines="skip", low_memory=False)
    dfs[default_table] = pl.from_pandas(pdf)
    return dfs


def profile_dataframe(
    df: pl.DataFrame,
    session_id: str,
    table_name: str = "df",
    version_tag: str = "df_v0",
) -> DataFrameProfile:
    """
    Extract a comprehensive, privacy-compliant schema profile from a Polars DataFrame.
    Strictly RFC 8259 JSON compliant: NaNs and Infs are converted to None.
    """
    row_count = df.height
    column_count = df.width
    memory_footprint_mb = round(df.estimated_size() / (1024 * 1024), 3)

    columns: List[ColumnProfile] = []
    for col_name in df.columns:
        s = df[col_name]
        null_count = s.null_count()
        if s.dtype.is_float():
            null_count += int(s.is_nan().sum())

        null_pct = round((null_count / row_count) * 100, 2) if row_count > 0 else 0.0
        cardinality = s.n_unique()

        # Extract up to 5 non-null, non-NaN sample values safely
        if s.dtype.is_float():
            filtered_s = s.filter(~s.is_null() & ~s.is_nan())
        else:
            filtered_s = s.drop_nulls()

        raw_samples = filtered_s.head(5).to_list()
        sanitized_samples = [sanitize_value(v) for v in raw_samples]

        columns.append(
            ColumnProfile(
                name=col_name,
                dtype=str(s.dtype),
                null_count=null_count,
                null_percentage=null_pct,
                cardinality=cardinality,
                sample_values=sanitized_samples,
            )
        )

    # 5-row preview as Markdown table
    preview_df = df.head(5).to_pandas()
    # Format NaNs as empty strings in preview table
    preview_md = tabulate(
        preview_df.fillna(""),
        headers="keys",
        tablefmt="pipe",
        showindex=False,
    )

    return DataFrameProfile(
        session_id=session_id,
        table_name=table_name,
        version_tag=version_tag,
        row_count=row_count,
        column_count=column_count,
        memory_footprint_mb=memory_footprint_mb,
        columns=columns,
        head_preview_markdown=preview_md,
    )


def generate_loader_code(
    file_path: Path,
    table_name: str,
    container_mount_path: Optional[str] = None,
) -> str:
    """
    Synthesize the optimal Python code snippet to hydrate the dataset into the sandbox.
    Uses container_mount_path if provided, else resolves the absolute local path.
    Also aliases the primary/first table to `df`.
    """
    target_path = container_mount_path or str(file_path.resolve()).replace("\\", "/")
    suffix = file_path.suffix.lower()

    if suffix in [".parquet", ".pq"]:
        return (
            f"import pandas as pd\n"
            f"{table_name} = pd.read_parquet(r'{target_path}')\n"
            f"df = {table_name}\n"
            f"df_active = df\n"
        )

    if suffix in [".csv", ".tsv", ".txt", ".tab"]:
        encoding, delimiter = detect_encoding_and_delimiter(file_path)
        return (
            f"import pandas as pd\n"
            f"{table_name} = pd.read_csv(r'{target_path}', sep={repr(delimiter)}, encoding={repr(encoding)})\n"
            f"df = {table_name}\n"
            f"df_active = df\n"
        )

    if suffix in [".xlsx", ".xls"]:
        return (
            f"import pandas as pd\n"
            f"{table_name} = pd.read_excel(r'{target_path}')\n"
            f"df = {table_name}\n"
            f"df_active = df\n"
        )

    if suffix in [".json", ".jsonl", ".ndjson"]:
        return (
            f"import pandas as pd\n"
            f"try:\n"
            f"    {table_name} = pd.read_json(r'{target_path}', lines=True)\n"
            f"except Exception:\n"
            f"    {table_name} = pd.read_json(r'{target_path}')\n"
            f"df = {table_name}\n"
            f"df_active = df\n"
        )

    if suffix in [".db", ".sqlite", ".sqlite3"]:
        return (
            f"import sqlite3\n"
            f"import pandas as pd\n"
            f"_conn = sqlite3.connect(r'{target_path}')\n"
            f"_tables = pd.read_sql_query(\"SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';\", _conn)['name'].tolist()\n"
            f"if _tables:\n"
            f"    {table_name} = pd.read_sql_query(f'SELECT * FROM \"{{_tables[0]}}\"', _conn)\n"
            f"    for _t in _tables:\n"
            f"        globals()[f'df_{{_t}}'] = pd.read_sql_query(f'SELECT * FROM \"{{_t}}\"', _conn)\n"
            f"    df = {table_name}\n"
            f"    df_active = df\n"
            f"_conn.close()\n"
        )

    # Universal CSV fallback
    return (
        f"import pandas as pd\n"
        f"{table_name} = pd.read_csv(r'{target_path}', on_bad_lines='skip')\n"
        f"df = {table_name}\n"
        f"df_active = df\n"
    )


def infer_foreign_key_relations(profiles: List[DataFrameProfile]) -> List[Any]:
    """
    Heuristically infer potential foreign key / join relationships between tables
    based on column names, suffixes, and data type compatibility.
    """
    from services.api.models import ForeignKeyRelation

    relations: List[ForeignKeyRelation] = []
    seen_pairs = set()

    for i, prof_a in enumerate(profiles):
        tbl_a = prof_a.table_name
        for prof_b in profiles[i + 1:]:
            tbl_b = prof_b.table_name

            for col_a in prof_a.columns:
                name_a = col_a.name.lower().strip()
                type_a = col_a.dtype.lower()

                for col_b in prof_b.columns:
                    name_b = col_b.name.lower().strip()
                    type_b = col_b.dtype.lower()

                    pair_key = tuple(sorted([(tbl_a, name_a), (tbl_b, name_b)]))
                    if pair_key in seen_pairs:
                        continue

                    # Case 1: Exact column name match
                    if name_a == name_b:
                        is_id = name_a.endswith("_id") or name_a == "id" or "code" in name_a or "key" in name_a
                        conf = 0.95 if is_id else 0.65
                        relations.append(
                            ForeignKeyRelation(
                                from_table=tbl_a,
                                from_column=col_a.name,
                                to_table=tbl_b,
                                to_column=col_b.name,
                                confidence=conf,
                                suggested_join_type="INNER JOIN" if is_id else "LEFT JOIN",
                            )
                        )
                        seen_pairs.add(pair_key)
                        continue

                    # Case 2: Table A has `{tbl_b_stem}_id` and Table B has `id`
                    stem_b = tbl_b.lower().replace("df_", "").rstrip("s")
                    stem_a = tbl_a.lower().replace("df_", "").rstrip("s")

                    if (name_a == f"{stem_b}_id" or name_a == f"{stem_b}id") and (name_b == "id" or name_b == f"{stem_b}_id"):
                        relations.append(
                            ForeignKeyRelation(
                                from_table=tbl_a,
                                from_column=col_a.name,
                                to_table=tbl_b,
                                to_column=col_b.name,
                                confidence=0.90,
                                suggested_join_type="INNER JOIN",
                            )
                        )
                        seen_pairs.add(pair_key)
                        continue

                    if (name_b == f"{stem_a}_id" or name_b == f"{stem_a}id") and (name_a == "id" or name_a == f"{stem_a}_id"):
                        relations.append(
                            ForeignKeyRelation(
                                from_table=tbl_b,
                                from_column=col_b.name,
                                to_table=tbl_a,
                                to_column=col_a.name,
                                confidence=0.90,
                                suggested_join_type="INNER JOIN",
                            )
                        )
                        seen_pairs.add(pair_key)
                        continue

    return relations
