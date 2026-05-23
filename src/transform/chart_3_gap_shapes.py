from __future__ import annotations

import pandas as pd

from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_3_TABLE_COLUMNS,
    GOS_8_SOURCE_KEY,
    GOS_L_160_SOURCE_KEY,
    MEDIUM_TERM_TIME_WINDOW,
    SHORT_TERM_TIME_WINDOW,
)
from src.transform.qilt import (
    QILT_MEDIUM_TERM_VALUE_COLUMN,
    QILT_SHORT_TERM_VALUE_COLUMN,
    build_qilt_full_time_employment_comparison_table,
    build_qilt_gap_sort_order,
    format_qilt_subgroup_label,
    select_qilt_subgroup_pair_rows,
)
from src.types import PreparedRows, QILTPreparedSheet


def build_chart_3_table(
    gos_sheet: QILTPreparedSheet,
    gos_l_sheet: QILTPreparedSheet,
) -> pd.DataFrame:
    comparison_table = build_qilt_full_time_employment_comparison_table(
        gos_sheet.table,
        gos_l_sheet.table,
        validate="one_to_one",
        how="left",
    )
    summary_rows = [
        _build_gap_shape_rows(group_table)
        for _, group_table in comparison_table.groupby("subgroup_dimension", sort=False)
    ]
    summary_table = pd.DataFrame(
        row for group_rows in summary_rows for row in group_rows
    )
    short_term_rows = summary_table.loc[
        summary_table["time_window"] == SHORT_TERM_TIME_WINDOW
    ]
    summary_table["sort_order"] = build_qilt_gap_sort_order(
        summary_table,
        gap_table=short_term_rows,
        gap_column="signed_gap_pp",
    )
    chart_table = summary_table.sort_values(
        ["sort_order", "time_window_order"],
        kind="mergesort",
    ).reset_index(drop=True)
    chart_table = select_chart_table_schema(chart_table, CHART_3_TABLE_COLUMNS)
    chart_table.attrs["chart_metadata"] = {
        "signed_gap_direction": "comparison_group_pct - reference_group_pct",
        "reference_group_rule": "group_with_lower_short_term_full_time_employment",
    }
    return chart_table


def build_chart_3_plot_table(chart_table: pd.DataFrame) -> pd.DataFrame:
    ordered_table = chart_table.sort_values(
        ["sort_order", "time_window_order"],
        kind="mergesort",
    ).reset_index(drop=True)
    index_columns = [
        "sort_order",
        "subgroup_dimension",
        "reference_group",
        "comparison_group",
    ]
    gap_table = ordered_table.pivot(
        index=index_columns,
        columns="time_window",
        values="signed_gap_pp",
    ).reset_index()
    gap_table.columns.name = None
    plot_table = gap_table.sort_values(
        ["sort_order", "subgroup_dimension"],
        kind="mergesort",
    ).reset_index(drop=True)
    return plot_table.loc[
        :,
        [
            *index_columns,
            SHORT_TERM_TIME_WINDOW,
            MEDIUM_TERM_TIME_WINDOW,
        ],
    ]


def _build_gap_shape_rows(group_table: pd.DataFrame) -> PreparedRows:
    subgroup_dimension = str(group_table["subgroup_dimension"].iloc[0])
    selected_pair = select_qilt_subgroup_pair_rows(
        group_table,
        value_column=QILT_SHORT_TERM_VALUE_COLUMN,
    )

    if selected_pair is None:
        raise ValueError(
            f"Cannot derive Chart 3 comparison for {subgroup_dimension!r}."
        )

    reference_row, comparison_row = selected_pair
    _raise_for_missing_fixed_pair_values(
        reference_row,
        comparison_row,
        value_column=QILT_MEDIUM_TERM_VALUE_COLUMN,
        subgroup_dimension=subgroup_dimension,
    )
    return [
        _build_fixed_gap_row(
            reference_row,
            comparison_row,
            subgroup_dimension=subgroup_dimension,
            value_column=QILT_SHORT_TERM_VALUE_COLUMN,
            time_window=SHORT_TERM_TIME_WINDOW,
            time_window_order=0,
            source_key=GOS_8_SOURCE_KEY,
        ),
        _build_fixed_gap_row(
            reference_row,
            comparison_row,
            subgroup_dimension=subgroup_dimension,
            value_column=QILT_MEDIUM_TERM_VALUE_COLUMN,
            time_window=MEDIUM_TERM_TIME_WINDOW,
            time_window_order=1,
            source_key=GOS_L_160_SOURCE_KEY,
        ),
    ]


def _build_fixed_gap_row(
    reference_row: pd.Series,
    comparison_row: pd.Series,
    *,
    subgroup_dimension: str,
    value_column: str,
    time_window: str,
    time_window_order: int,
    source_key: str,
) -> dict[str, object]:
    reference_value = reference_row[value_column]
    comparison_value = comparison_row[value_column]

    return {
        "subgroup_dimension": subgroup_dimension,
        "time_window": time_window,
        "time_window_order": time_window_order,
        "reference_group": format_qilt_subgroup_label(reference_row["row_label"]),
        "reference_group_pct": reference_value,
        "comparison_group": format_qilt_subgroup_label(comparison_row["row_label"]),
        "comparison_group_pct": comparison_value,
        "signed_gap_pp": round(float(comparison_value - reference_value), 1),
        "source_key": source_key,
    }


def _raise_for_missing_fixed_pair_values(
    reference_row: pd.Series,
    comparison_row: pd.Series,
    *,
    value_column: str,
    subgroup_dimension: str,
) -> None:
    missing_groups = [
        format_qilt_subgroup_label(row["row_label"])
        for row in (reference_row, comparison_row)
        if pd.isna(row[value_column])
    ]

    if missing_groups:
        raise ValueError(
            f"Missing Chart 3 {value_column!r} values for "
            f"{subgroup_dimension!r}: {missing_groups}."
        )
