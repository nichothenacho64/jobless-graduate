from __future__ import annotations

from typing import Optional

import pandas as pd

from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_7_TABLE_COLUMNS,
    CHART_7_HIGHER_GROUP_ROLE,
    CHART_7_LOWER_GROUP_ROLE,
    GOS_8_SOURCE_KEY,
    GOS_L_160_SOURCE_KEY,
    MEDIUM_TERM_TIME_WINDOW,
    SHORT_TERM_TIME_WINDOW,
)
from src.transform.qilt import (
    QILT_MEDIUM_TERM_VALUE_COLUMN,
    QILT_SHORT_TERM_VALUE_COLUMN,
    build_qilt_comparison_label,
    build_qilt_full_time_employment_comparison_table,
    build_qilt_subgroup_gap_sort_order,
    build_qilt_subgroup_id,
    format_qilt_subgroup_label,
    select_qilt_subgroup_pair_rows,
)
from src.types import QILTPreparedSheet


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
    group_role_order = {
        CHART_7_LOWER_GROUP_ROLE: 0,
        CHART_7_HIGHER_GROUP_ROLE: 1,
    }
    chart_table["_group_role_order"] = [
        group_role_order[group_role]
        for group_role in chart_table["group_role"]
    ]
    chart_table = chart_table.sort_values(
        ["sort_order", "time_window_order", "_group_role_order"],
        kind="mergesort",
    ).drop(columns="_group_role_order")
    return select_chart_table_schema(chart_table, CHART_7_TABLE_COLUMNS)


def _build_comparator_rows(group_table: pd.DataFrame) -> list[dict[str, object]]:
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
    comparison_label = build_qilt_comparison_label(
        low_row["row_label"],
        high_row["row_label"],
    )
    return [
        *_build_group_rows(
            low_row,
            selector_id=selector_id,
            selector_label=subgroup_dimension,
            comparison_label=comparison_label,
            group_role=CHART_7_LOWER_GROUP_ROLE,
            sort_order=sort_order,
        ),
        *_build_group_rows(
            high_row,
            selector_id=selector_id,
            selector_label=subgroup_dimension,
            comparison_label=comparison_label,
            group_role=CHART_7_HIGHER_GROUP_ROLE,
            sort_order=sort_order,
        ),
    ]


def _build_group_rows(
    row: pd.Series,
    *,
    selector_id: str,
    selector_label: str,
    comparison_label: Optional[str],
    group_role: str,
    sort_order: object,
) -> list[dict[str, object]]:
    group_label = format_qilt_subgroup_label(row["row_label"])
    return [
        {
            "selector_id": selector_id,
            "selector_label": selector_label,
            "subgroup_dimension": selector_label,
            "comparison_label": comparison_label,
            "group_role": group_role,
            "group_label": group_label,
            "time_window": SHORT_TERM_TIME_WINDOW,
            "time_window_order": 0,
            "value_pct": row[QILT_SHORT_TERM_VALUE_COLUMN],
            "source_key": GOS_8_SOURCE_KEY,
            "sort_order": sort_order,
        },
        {
            "selector_id": selector_id,
            "selector_label": selector_label,
            "subgroup_dimension": selector_label,
            "comparison_label": comparison_label,
            "group_role": group_role,
            "group_label": group_label,
            "time_window": MEDIUM_TERM_TIME_WINDOW,
            "time_window_order": 1,
            "value_pct": row[QILT_MEDIUM_TERM_VALUE_COLUMN],
            "source_key": GOS_L_160_SOURCE_KEY,
            "sort_order": sort_order,
        },
    ]
