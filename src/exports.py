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
    CHART_1_GOS_L_MEDIUM_TERM_FTE_SERIES_KEY,
    CHART_1_GOS_L_SHORT_TERM_FTE_SERIES_KEY,
    CHART_1_GOS_SHORT_TERM_FTE_SERIES_KEY,
    CHART_1_ID,
    CHART_2_ID,
    CHART_3_ID,
    CHART_4_ID,
    CHART_5_ID,
    CHART_5_WORK_FIT_METRIC_KEY,
    CHART_6A_ID,
    CHART_6B_ID,
    CHART_7_GROUP_A_ROLE,
    CHART_7_GROUP_B_ROLE,
    CHART_7_ID,
    CHART_METADATA_FILE_NAME,
    CHART_SOURCE_KEY_COLUMNS,
    MEDIUM_TERM_TIME_WINDOW,
    SHORT_TERM_TIME_WINDOW,
)
from src.types import ABSPreparedSheet, ChartMetadata, MissingValues, QILTPreparedSheet

TIME_WINDOW_LABELS = {
    SHORT_TERM_TIME_WINDOW: "Short term",
    MEDIUM_TERM_TIME_WINDOW: "Medium term",
}

CHART_1_SERIES_LABELS = {
    CHART_1_GOS_L_SHORT_TERM_FTE_SERIES_KEY: "GOS-L short term",
    CHART_1_GOS_L_MEDIUM_TERM_FTE_SERIES_KEY: "GOS-L medium term",
    CHART_1_GOS_SHORT_TERM_FTE_SERIES_KEY: "GOS short term",
}

FIT_METRIC_LABELS = {
    CHART_5_WORK_FIT_METRIC_KEY: "Skills and education not fully utilised",
}

FIT_METRIC_DETAIL_KEYS = (
    "fit_metric_key",
    "employment_source_key",
    "fit_metric_source_key",
    "fit_metric_direction",
    "fit_change_formula",
    "fit_metric_source_columns",
)

INDEX_DERIVATION_DETAIL_KEYS = (
    "base_year",
    "base_value",
    "base_unit",
    "selected_measurement",
    "selected_population_group",
    "selected_row_label",
    "qualification_filter",
    "formula",
)

GROUP_ROLE_LABELS = {
    CHART_7_GROUP_A_ROLE: "Group A",
    CHART_7_GROUP_B_ROLE: "Group B",
}

METRIC_LABELS_BY_CHART_ID = {
    CHART_1_ID: {
        "value_pct": "Full-time employment",
    },
    CHART_2_ID: {
        "gap_pp": "Employment gap",
        "lower_group_pct": "Lower group full-time employment",
        "higher_group_pct": "Higher group full-time employment",
    },
    CHART_3_ID: {
        "signed_gap_pp": "Signed employment gap",
        "reference_group_pct": "Reference group full-time employment",
        "comparison_group_pct": "Comparison group full-time employment",
    },
    CHART_4_ID: {
        "short_term_fte_pct": "Short-term full-time employment",
        "medium_term_fte_pct": "Medium-term full-time employment",
    },
    CHART_5_ID: {
        "fte_gain_pp": "Full-time employment gain",
        "underutilisation_reduction_pp": "Underutilisation reduction",
    },
    CHART_6A_ID: {
        "share_pct": "Share",
    },
    CHART_6B_ID: {
        "bachelor_degree_or_above_count_index": (
            "Bachelor degree or above count index"
        ),
    },
    CHART_7_ID: {
        "full_time_employment_pct": "Full-time employment",
    },
}


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
        source_keys = _collect_source_keys(chart_table)
        source_metadata = _build_sources(source_keys, chart_sources)
        labels = build_chart_labels(chart_id, chart_table, source_metadata)

        chart_entry: ChartMetadata = {
            "chart_id": chart_id,
            "sources": source_metadata,
            "labels": labels,
        }
        chart_specific_metadata = _build_chart_specific_metadata(chart_table)
        details = build_chart_details(chart_specific_metadata)
        if details:
            chart_entry["details"] = details

        row_caveats = _build_missing_value_caveats(chart_table)
        caveats = build_chart_caveats(chart_specific_metadata, row_caveats)
        if caveats:
            chart_entry["caveats"] = caveats

        _raise_for_unhandled_chart_specific_metadata(chart_specific_metadata)

        metadata[chart_id] = chart_entry

    return metadata


def _build_chart_specific_metadata(chart_table: pd.DataFrame) -> ChartMetadata:
    chart_metadata = chart_table.attrs.get("chart_metadata", {})
    if not isinstance(chart_metadata, Mapping):
        raise TypeError(
            f"Chart table {'chart_metadata'!r} attribute must be a mapping."
        )

    return dict(chart_metadata)


def build_source_labels(chart_sources: Mapping[str, object]) -> dict[str, str]:
    labels: dict[str, str] = {}

    for source_key, source in chart_sources.items():
        if not isinstance(source, Mapping):
            raise TypeError("Source label metadata requires mapping source objects.")

        labels[str(source_key)] = _derive_source_label(str(source_key), source)

    return labels


def build_chart_labels(
    chart_id: str,
    chart_table: pd.DataFrame,
    chart_sources: Mapping[str, object],
) -> dict[str, object]:
    labels: dict[str, object] = {
        "sources": build_source_labels(chart_sources),
    }

    time_windows = _build_time_window_labels(chart_id, chart_table)
    if time_windows:
        labels["time_windows"] = time_windows

    series = _build_series_labels(chart_id, chart_table)
    if series:
        labels["series"] = series

    metrics = _build_metric_labels(chart_id, chart_table)
    if metrics:
        labels["metrics"] = metrics

    fit_metrics = _build_fit_metric_labels(chart_table)
    if fit_metrics:
        labels["fit_metrics"] = fit_metrics

    group_roles = _build_group_role_labels(chart_table)
    if group_roles:
        labels["group_roles"] = group_roles

    return labels


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

    for column in CHART_SOURCE_KEY_COLUMNS:
        if column not in chart_table.columns:
            continue

        for source_key in chart_table[column].dropna().tolist():
            source_key_text = str(source_key)
            if source_key_text not in source_keys:
                source_keys.append(source_key_text)

    return source_keys


def _build_sources(
    source_keys: list[str], chart_sources: Mapping[str, object]
) -> dict[str, object]:
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


def _derive_source_label(source_key: str, source: Mapping[str, object]) -> str:
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


def _build_missing_value_caveats(chart_table: pd.DataFrame) -> MissingValues:
    row_caveats: MissingValues = {}
    value_columns = [
        str(column)
        for column in chart_table.columns
        if _is_metric_value_column(str(column))
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


def build_chart_details(chart_metadata: Mapping[str, object]) -> dict[str, object]:
    details: dict[str, object] = {}

    year_semantics = chart_metadata.get("year_semantics")
    if year_semantics:
        details["year_semantics"] = year_semantics

    fit_metric = _select_existing_metadata(chart_metadata, FIT_METRIC_DETAIL_KEYS)
    if fit_metric:
        details["fit_metric"] = fit_metric

    index_derivation = _select_existing_metadata(
        chart_metadata,
        INDEX_DERIVATION_DETAIL_KEYS,
    )
    if index_derivation:
        details["index_derivation"] = index_derivation

    group_role_semantics = chart_metadata.get("group_role_semantics")
    if group_role_semantics:
        details["group_role_semantics"] = group_role_semantics

    signed_gap_direction = chart_metadata.get("signed_gap_direction")
    if signed_gap_direction:
        details["signed_gap_direction"] = signed_gap_direction

    reference_group_rule = chart_metadata.get("reference_group_rule")
    if reference_group_rule:
        details["reference_group_rule"] = reference_group_rule

    return _drop_empty_metadata(details)


def build_chart_caveats(
    chart_metadata: Mapping[str, object],
    row_caveats: MissingValues,
) -> dict[str, object]:
    caveats: dict[str, object] = {}

    excluded_rows = chart_metadata.get("excluded_rows")
    if excluded_rows:
        caveats["excluded_rows"] = excluded_rows

    if row_caveats:
        caveats["row_caveats"] = row_caveats

    return _drop_empty_metadata(caveats)


def _raise_for_unhandled_chart_specific_metadata(
    chart_metadata: Mapping[str, object],
) -> None:
    handled_keys = {
        "year_semantics",
        "group_role_semantics",
        "signed_gap_direction",
        "reference_group_rule",
        "excluded_rows",
        *FIT_METRIC_DETAIL_KEYS,
        *INDEX_DERIVATION_DETAIL_KEYS,
    }
    unhandled_keys = sorted(
        key
        for key, value in chart_metadata.items()
        if key not in handled_keys and not _is_empty_metadata_value(value)
    )

    if unhandled_keys:
        raise KeyError(
            "Unhandled chart-specific metadata keys: "
            + ", ".join(map(repr, unhandled_keys))
        )


def _select_existing_metadata(
    metadata: Mapping[str, object],
    keys: tuple[str, ...],
) -> dict[str, object]:
    return {
        key: metadata[key]
        for key in keys
        if key in metadata and not _is_empty_metadata_value(metadata[key])
    }


def _drop_empty_metadata(metadata: dict[str, object]) -> dict[str, object]:
    return {
        key: value
        for key, value in metadata.items()
        if not _is_empty_metadata_value(value)
    }


def _is_empty_metadata_value(value: object) -> bool:
    return isinstance(value, (dict, list)) and len(value) == 0


def _build_time_window_labels(
    chart_id: str,
    chart_table: pd.DataFrame,
) -> dict[str, str]:
    if "time_window" in chart_table.columns:
        return _build_observed_label_map(
            chart_table,
            "time_window",
            TIME_WINDOW_LABELS,
        )

    if chart_id != CHART_1_ID or "series_key" not in chart_table.columns:
        return {}

    time_windows: list[str] = []
    for series_key in _observed_column_keys(chart_table, "series_key"):
        if SHORT_TERM_TIME_WINDOW in series_key:
            _append_unique(time_windows, SHORT_TERM_TIME_WINDOW)
        if MEDIUM_TERM_TIME_WINDOW in series_key:
            _append_unique(time_windows, MEDIUM_TERM_TIME_WINDOW)

    return _select_labels(time_windows, TIME_WINDOW_LABELS, "time window")


def _build_series_labels(
    chart_id: str,
    chart_table: pd.DataFrame,
) -> dict[str, str]:
    if chart_id != CHART_1_ID or "series_key" not in chart_table.columns:
        return {}

    return _build_observed_label_map(
        chart_table,
        "series_key",
        CHART_1_SERIES_LABELS,
    )


def _build_metric_labels(
    chart_id: str,
    chart_table: pd.DataFrame,
) -> dict[str, dict[str, str]]:
    configured_labels = METRIC_LABELS_BY_CHART_ID.get(chart_id, {})
    labels: dict[str, dict[str, str]] = {}

    for metric_key, metric_label in configured_labels.items():
        if metric_key not in chart_table.columns:
            continue

        labels[metric_key] = {
            "label": metric_label,
            "unit": _metric_unit(metric_key),
        }

    return labels


def _build_fit_metric_labels(chart_table: pd.DataFrame) -> dict[str, str]:
    if "fit_metric_key" not in chart_table.columns:
        return {}

    return _build_observed_label_map(
        chart_table,
        "fit_metric_key",
        FIT_METRIC_LABELS,
    )


def _build_group_role_labels(chart_table: pd.DataFrame) -> dict[str, str]:
    if "group_role" not in chart_table.columns:
        return {}

    return _build_observed_label_map(
        chart_table,
        "group_role",
        GROUP_ROLE_LABELS,
    )


def _build_observed_label_map(
    chart_table: pd.DataFrame,
    column: str,
    labels_by_key: Mapping[str, str],
) -> dict[str, str]:
    observed_keys = _observed_column_keys(chart_table, column)
    return _select_labels(observed_keys, labels_by_key, column)


def _observed_column_keys(chart_table: pd.DataFrame, column: str) -> list[str]:
    observed_keys: list[str] = []

    for value in chart_table[column].dropna().tolist():
        _append_unique(observed_keys, str(value))

    return observed_keys


def _select_labels(
    observed_keys: list[str],
    labels_by_key: Mapping[str, str],
    label_kind: str,
) -> dict[str, str]:
    labels: dict[str, str] = {}

    for observed_key in observed_keys:
        if observed_key not in labels_by_key:
            raise KeyError(
                f"No frontend {label_kind} label configured for {observed_key!r}."
            )

        labels[observed_key] = labels_by_key[observed_key]

    return labels


def _append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def _metric_unit(metric_key: str) -> str:
    if metric_key.endswith("_pp"):
        return "percentage_point"

    if metric_key.endswith("_pct"):
        return "percent"

    if metric_key.startswith("index_") or metric_key.endswith("_index"):
        return "index"

    raise KeyError(f"No frontend metric unit configured for {metric_key!r}.")


def _is_metric_value_column(column: str) -> bool:
    return (
        column.endswith(("_pct", "_pp", "_index"))
        or column.startswith("index_")
    )


def _build_row_key(
    row: pd.Series,
    *,
    caveat_columns: set[str],
    value_columns: set[str],
) -> str:
    key_parts: list[str] = []

    for row_column in row.index:
        column = str(row_column)
        if not _is_row_key_column(
            column, caveat_columns=caveat_columns, value_columns=value_columns
        ):
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
