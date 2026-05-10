from __future__ import annotations

from collections.abc import Mapping
import json
from pathlib import Path

import pandas as pd

from src.preparation.series import is_missing_scalar, format_row_key_value
from src.sources import (
    PROCESSED_DIR,
    QILT_2024_GOS_L_SOURCE,
    QILT_2024_GOS_SOURCE,
    QILT_FOLDER_NAME,
    RAW_SOURCE_DIRS,
)
from src.transform.constants import (
    CHART_METADATA_FILE_NAME,
    CHART_OUTPUT_FILENAMES,
    CHART_SOURCE_KEY_COLUMNS,
)
from src.types import ABSPreparedSheet, ChartMetadata, MissingValues, QILTPreparedSheet


def export_chart_table(table: pd.DataFrame, filename: str) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / filename
    table.to_csv(path, index=False)
    return path


def export_chart_tables(chart_tables: Mapping[str, pd.DataFrame]) -> dict[str, Path]:
    exported_paths: dict[str, Path] = {}

    for chart_id, table in chart_tables.items():
        if chart_id not in CHART_OUTPUT_FILENAMES:
            raise KeyError(f"No chart output filename is defined for {chart_id!r}.")

        exported_paths[chart_id] = export_chart_table(
            table,
            CHART_OUTPUT_FILENAMES[chart_id],
        )

    return exported_paths


def export_chart_metadata(metadata: Mapping[str, object]) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / CHART_METADATA_FILE_NAME
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return path


def build_chart_metadata(
    chart_tables: Mapping[str, pd.DataFrame],
    chart_sources: Mapping[str, object],
) -> ChartMetadata:
    metadata: ChartMetadata = {}

    for chart_id, chart_table in chart_tables.items():
        if chart_id not in CHART_OUTPUT_FILENAMES:
            raise KeyError(f"No chart output filename is defined for {chart_id!r}.")

        source_keys = _collect_source_keys(chart_table)
        source_metadata = _build_sources(source_keys, chart_sources)

        chart_entry: ChartMetadata = {
            "chart_id": chart_id,
            "data_file": CHART_OUTPUT_FILENAMES[chart_id],
            "source_keys": source_keys,
            "sources": source_metadata,
        }

        row_caveats = _build_missing_value_caveats(chart_table)
        if row_caveats:
            chart_entry["row_caveats"] = row_caveats

        metadata[chart_id] = chart_entry

    return metadata


def build_qilt_source_metadata(source_key: str, prepared_sheet: QILTPreparedSheet) -> ChartMetadata:
    source_context = _derive_qilt_source_context(source_key)
    return {
        "source_key": source_key,
        "source_system": "QILT",
        "dataset": source_context["dataset"],
        "plain_label": source_context["plain_label"],
        "source_file": source_context["source_file"],
        "sheet_name": prepared_sheet.sheet_name,
        "sheet_number": source_context["sheet_number"],
        "sheet_title": prepared_sheet.title,
        "classification": prepared_sheet.classification,
        "source_metadata": prepared_sheet.metadata,
    }


def build_sew_source_metadata(source_key: str, prepared_sheet: ABSPreparedSheet) -> ChartMetadata:
    expected_source_key = f"sew_{prepared_sheet.table_number}"
    if source_key != expected_source_key:
        raise ValueError(
            f"SEW source key {source_key!r} does not match "
            f"table {prepared_sheet.table_number}."
        )

    source_metadata: ChartMetadata = {
        "source_key": source_key,
        "source_system": "ABS",
        "dataset": "SEW",
        "plain_label": f"SEW #{prepared_sheet.table_number}",
        "source_file": prepared_sheet.source_file,
        "sheet_name": prepared_sheet.sheet_name,
        "table_number": prepared_sheet.table_number,
        "sheet_title": prepared_sheet.title,
        "source_metadata": prepared_sheet.metadata,
    }

    reliability_summary = _build_abs_reliability_summary(prepared_sheet.table)
    if reliability_summary:
        source_metadata["reliability_summary"] = reliability_summary

    return source_metadata


def _collect_source_keys(chart_table: pd.DataFrame) -> list[str]:
    source_keys: list[str] = []

    for column in CHART_SOURCE_KEY_COLUMNS:
        if column not in chart_table.columns:
            continue

        for source_key in chart_table[column].dropna().tolist():
            source_key_text = str(source_key)
            if source_key_text not in source_keys:
                source_keys.append(source_key_text)

    return source_keys


def _build_sources(source_keys: list[str], chart_sources: Mapping[str, object]) -> dict[str, object]:
    sources: dict[str, object] = {}

    for source_key in source_keys:
        if source_key not in chart_sources:
            raise KeyError(
                f"Missing prepared source for chart source key {source_key!r}."
            )

        prepared_sheet = chart_sources[source_key]
        if isinstance(prepared_sheet, QILTPreparedSheet):
            sources[source_key] = build_qilt_source_metadata(source_key, prepared_sheet)
            continue

        if isinstance(prepared_sheet, ABSPreparedSheet):
            sources[source_key] = build_sew_source_metadata(source_key, prepared_sheet)
            continue

        raise TypeError(
            "Chart source metadata requires QILTPreparedSheet or ABSPreparedSheet."
        )

    return sources


def _derive_qilt_source_context(source_key: str) -> dict[str, object]:
    if source_key.startswith("gos_l_"):
        dataset = "GOS-L"
        sheet_number = _parse_source_key_number(source_key, "gos_l_")
        source_file = RAW_SOURCE_DIRS[QILT_FOLDER_NAME][QILT_2024_GOS_L_SOURCE]
    elif source_key.startswith("gos_"):
        dataset = "GOS"
        sheet_number = _parse_source_key_number(source_key, "gos_")
        source_file = RAW_SOURCE_DIRS[QILT_FOLDER_NAME][QILT_2024_GOS_SOURCE]
    else:
        raise KeyError(f"Cannot derive QILT source metadata for {source_key!r}.")

    return {
        "dataset": dataset,
        "plain_label": f"{dataset} #{sheet_number}",
        "source_file": source_file,
        "sheet_number": sheet_number,
    }


def _parse_source_key_number(source_key: str, prefix: str) -> int:
    source_number = source_key.removeprefix(prefix)
    if not source_number.isdecimal():
        raise KeyError(f"Cannot derive sheet number from source key {source_key!r}.")

    return int(source_number)


def _build_abs_reliability_summary(table: pd.DataFrame) -> dict[str, int]:
    if "is_reliable" not in table.columns:
        return {}

    reliable = table["is_reliable"].fillna(False).astype(bool)
    summary = {
        "prepared_rows": int(len(table)),
        "reliable_rows": int(reliable.sum()),
        "unreliable_rows": int((~reliable).sum()),
    }

    for column in ("is_suppressed", "is_not_available"):
        if column in table.columns:
            summary[column.replace("is_", "") + "_rows"] = int(
                table[column].fillna(False).astype(bool).sum()
            )

    return summary


def _build_missing_value_caveats(chart_table: pd.DataFrame) -> MissingValues:
    row_caveats: MissingValues = {}
    value_columns = [
        str(column)
        for column in chart_table.columns
        if str(column).endswith(("_pct", "_pp")) or str(column).startswith("index_")
    ]
    value_column_set = set(value_columns)

    for _, row in chart_table.iterrows():
        missing_columns = [
            column for column in value_columns if is_missing_scalar(row[column])
        ]
        if not missing_columns:
            continue

        row_key = _build_row_key(
            row,
            caveat_columns=set(missing_columns),
            value_columns=value_column_set,
        )
        row_caveats.setdefault(row_key, []).append(
            {
                "type": "missing_value",
                "columns": missing_columns,
            }
        )

    return row_caveats


def _build_row_key(
    row: pd.Series,
    *,
    caveat_columns: set[str],
    value_columns: set[str],
) -> str:
    key_parts: list[str] = []

    for row_column in row.index:
        column = str(row_column)
        if not _is_row_key_column(column, caveat_columns=caveat_columns, value_columns=value_columns):
            continue

        if is_missing_scalar(row[column]):
            continue

        key_parts.append(f"{column}={format_row_key_value(row[column])}")

    if key_parts:
        return "|".join(key_parts)

    return f"row={format_row_key_value(row.name)}"


def _is_row_key_column(
    column: str,
    *,
    caveat_columns: set[str],
    value_columns: set[str],
) -> bool:
    if column in caveat_columns or column in CHART_SOURCE_KEY_COLUMNS:
        return False

    if column == "sort_order" or column.endswith("_order"):
        return False

    return column not in value_columns
