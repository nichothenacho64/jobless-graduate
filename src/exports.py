from __future__ import annotations

from collections.abc import Mapping
import json
from pathlib import Path

import pandas as pd

from src.sources import (
    PROCESSED_DIR,
    QILT_2024_GOS_L_SOURCE,
    QILT_2024_GOS_SOURCE,
    QILT_FOLDER_NAME,
    RAW_SOURCE_DIRS,
)
from src.types import ABSPreparedSheet, ChartMetadata, QILTPreparedSheet


CHART_METADATA_FILE_NAME = "chart_metadata.json"


def export_chart_table(table: pd.DataFrame, filename: str) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / filename
    table.to_csv(path, index=False)
    return path


def export_chart_tables(chart_tables: Mapping[str, pd.DataFrame]) -> dict[str, Path]:
    exported_paths: dict[str, Path] = {}

    for chart_id, table in chart_tables.items():
        exported_paths[chart_id] = export_chart_table(
            table,
            f"{chart_id}.csv",
        )

    return exported_paths


def export_chart_metadata(metadata: Mapping[str, object]) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / CHART_METADATA_FILE_NAME
    path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def build_chart_metadata(
    chart_tables: Mapping[str, pd.DataFrame],
    chart_sources: Mapping[str, object],
) -> ChartMetadata:
    metadata: ChartMetadata = {}

    for chart_id, chart_table in chart_tables.items():
        chart_specific_metadata = _chart_metadata(chart_table)
        sources = _build_sources(
            _collect_source_keys(chart_table),
            chart_sources,
            _chart_source_metadata(chart_specific_metadata),
        )
        chart_labels: dict[str, object] = {
            "sources": _build_source_labels(sources),
        }
        chart_entry: ChartMetadata = {
            "chart_id": chart_id,
            "data_file": f"{chart_id}.csv",
            "sources": sources,
            "labels": chart_labels,
        }

        labels = chart_specific_metadata.get("labels")
        if labels:
            if not isinstance(labels, Mapping):
                raise ValueError("Chart metadata 'labels' section must be a mapping.")
            chart_labels.update(labels)

        for section_name in ("details", "caveats"):
            section = chart_specific_metadata.get(section_name)
            if not section:
                continue
            if not isinstance(section, Mapping):
                raise ValueError(
                    f"Chart metadata {section_name!r} section must be a mapping."
                )
            chart_entry[section_name] = dict(section)

        metadata[chart_id] = chart_entry

    return metadata


def build_qilt_source_metadata(
    source_key: str, prepared_sheet: QILTPreparedSheet
) -> ChartMetadata:
    source_context = _derive_qilt_source_context(source_key)
    return {
        "source_system": "QILT",
        "dataset": source_context["dataset"],
        "source_file": source_context["source_file"],
        "sheet_name": prepared_sheet.sheet_name,
        "sheet_number": source_context["sheet_number"],
        "sheet_title": prepared_sheet.title,
    }


def build_sew_source_metadata(
    source_key: str, prepared_sheet: ABSPreparedSheet
) -> ChartMetadata:
    expected_source_key = f"sew_{prepared_sheet.table_number}"
    if source_key != expected_source_key:
        raise ValueError(
            f"SEW source key {source_key!r} does not match "
            f"table {prepared_sheet.table_number}."
        )

    source_metadata: ChartMetadata = {
        "source_system": "ABS",
        "dataset": "SEW",
        "source_file": prepared_sheet.source_file,
        "sheet_name": prepared_sheet.sheet_name,
        "table_number": prepared_sheet.table_number,
        "sheet_title": prepared_sheet.title,
    }

    return source_metadata


def _collect_source_keys(chart_table: pd.DataFrame) -> list[str]:
    source_keys: list[str] = []

    for column in chart_table.columns:
        column_name = str(column)
        if column_name != "source_key" and not column_name.endswith("_source_key"):
            continue

        for source_key in chart_table[column].dropna().tolist():
            source_key_text = str(source_key)
            if source_key_text not in source_keys:
                source_keys.append(source_key_text)

    return source_keys


def _build_sources(
    source_keys: list[str],
    chart_sources: Mapping[str, object],
    chart_source_metadata: Mapping[str, object],
) -> dict[str, object]:
    sources: dict[str, object] = {}

    for source_key in source_keys:
        if source_key in chart_source_metadata:
            source_metadata = chart_source_metadata[source_key]
            if not isinstance(source_metadata, Mapping):
                raise ValueError(
                    f"Chart source metadata for {source_key!r} must be a mapping."
                )
            sources[source_key] = dict(source_metadata)
            continue

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


def _build_source_labels(chart_sources: Mapping[str, object]) -> dict[str, str]:
    labels: dict[str, str] = {}

    for source_key, source in chart_sources.items():
        if not isinstance(source, Mapping):
            raise TypeError("Source label metadata requires mapping source objects.")

        labels[str(source_key)] = _derive_source_label(str(source_key), source)

    return labels


def _derive_source_label(source_key: str, source: Mapping[str, object]) -> str:
    label = source.get("label")
    if isinstance(label, str):
        return label

    dataset = source.get("dataset")

    if dataset in {"GOS", "GOS-L"}:
        sheet_number = source.get("sheet_number")
        if sheet_number is None:
            raise KeyError(f"QILT source {source_key!r} is missing a sheet_number.")

        return f"{dataset} #{sheet_number}"

    if dataset == "SEW":
        table_number = source.get("table_number")
        if table_number is None:
            raise KeyError(f"SEW source {source_key!r} is missing a table_number.")

        return f"SEW #{table_number}"

    raise KeyError(f"Cannot derive source label for {source_key!r}.")


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
        "source_file": source_file,
        "sheet_number": sheet_number,
    }


def _parse_source_key_number(source_key: str, prefix: str) -> int:
    source_number = source_key.removeprefix(prefix)
    if not source_number.isdecimal():
        raise KeyError(f"Cannot derive sheet number from source key {source_key!r}.")

    return int(source_number)


def _chart_metadata(chart_table: pd.DataFrame) -> ChartMetadata:
    chart_metadata = chart_table.attrs.get("chart_metadata", {})
    if not isinstance(chart_metadata, Mapping):
        raise ValueError("Chart table 'chart_metadata' attribute must be a mapping.")

    return dict(chart_metadata)


def _chart_source_metadata(chart_metadata: Mapping[str, object]) -> Mapping[str, object]:
    chart_sources = chart_metadata.get("sources", {})
    if not isinstance(chart_sources, Mapping):
        raise ValueError("Chart metadata 'sources' section must be a mapping.")

    return chart_sources
