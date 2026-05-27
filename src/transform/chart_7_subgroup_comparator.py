from __future__ import annotations

import pandas as pd

from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_7_METADATA,
    CHART_7_TABLE_COLUMNS,
    GOS_8_SOURCE_KEY,
    GOS_L_160_SOURCE_KEY,
    MEDIUM_TERM_TIME_WINDOW,
    SHORT_TERM_TIME_WINDOW,
)
from src.transform.qilt import (
    QILT_MEDIUM_TERM_VALUE_COLUMN,
    QILT_SHORT_TERM_VALUE_COLUMN,
    build_qilt_full_time_employment_comparison_table,
    build_qilt_subgroup_gap_sort_order,
    build_qilt_subgroup_id,
    format_qilt_subgroup_label,
    select_qilt_subgroup_pair_rows,
)
from src.types import PreparedRows, QILTPreparedSheet


def build_chart_7_table(
    gos_sheet: QILTPreparedSheet,
    gos_l_sheet: QILTPreparedSheet,
) -> pd.DataFrame:
    comparison_table = build_qilt_full_time_employment_comparison_table(
        gos_sheet.table,
        gos_l_sheet.table,
        validate="one_to_one",
    )
    comparison_table["sort_order"] = build_qilt_subgroup_gap_sort_order(
        comparison_table,
        value_column=QILT_SHORT_TERM_VALUE_COLUMN,
    )
    summary_rows = [
        _build_comparator_rows(group_table)
        for _, group_table in comparison_table.groupby("subgroup_dimension", sort=False)
    ]
    chart_table = pd.DataFrame(row for group_rows in summary_rows for row in group_rows)
    chart_table = chart_table.sort_values(
        ["sort_order", "time_window_order"],
        kind="mergesort",
    )
    chart_table = select_chart_table_schema(chart_table, CHART_7_TABLE_COLUMNS)
    chart_table.attrs["chart_metadata"] = CHART_7_METADATA
    return chart_table


def _build_comparator_rows(group_table: pd.DataFrame) -> PreparedRows:
    subgroup_dimension = str(group_table["subgroup_dimension"].iloc[0])
    selector_id = build_qilt_subgroup_id(subgroup_dimension)
    sort_order = group_table["sort_order"].iloc[0]
    selected_pair = select_qilt_subgroup_pair_rows(
        group_table,
        value_column=QILT_SHORT_TERM_VALUE_COLUMN,
    )

    if selected_pair is None:
        return []

    low_row, high_row = selected_pair
    return [
        _build_comparator_row(
            low_row,
            high_row,
            selector_id=selector_id,
            subgroup_dimension=subgroup_dimension,
            value_column=QILT_SHORT_TERM_VALUE_COLUMN,
            time_window=SHORT_TERM_TIME_WINDOW,
            time_window_order=0,
            source_key=GOS_8_SOURCE_KEY,
            sort_order=sort_order,
        ),
        _build_comparator_row(
            low_row,
            high_row,
            selector_id=selector_id,
            subgroup_dimension=subgroup_dimension,
            value_column=QILT_MEDIUM_TERM_VALUE_COLUMN,
            time_window=MEDIUM_TERM_TIME_WINDOW,
            time_window_order=1,
            source_key=GOS_L_160_SOURCE_KEY,
            sort_order=sort_order,
        ),
    ]


def _build_comparator_row(
    reference_row: pd.Series,
    comparison_row: pd.Series,
    *,
    selector_id: str,
    subgroup_dimension: str,
    value_column: str,
    time_window: str,
    time_window_order: int,
    source_key: str,
    sort_order: object,
) -> dict[str, object]:
    reference_value = reference_row[value_column]
    comparison_value = comparison_row[value_column]

    return {
        "selector_id": selector_id,
        "subgroup_dimension": subgroup_dimension,
        "time_window": time_window,
        "time_window_order": time_window_order,
        "reference_group": format_qilt_subgroup_label(reference_row["row_label"]),
        "reference_group_pct": reference_value,
        "comparison_group": format_qilt_subgroup_label(comparison_row["row_label"]),
        "comparison_group_pct": comparison_value,
        "signed_gap_pp": round(float(comparison_value - reference_value), 1),
        "source_key": source_key,
        "sort_order": sort_order,
    }
