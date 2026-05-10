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
    build_qilt_subgroup_pair_summary,
    build_qilt_subgroup_id,
)
from src.types import QILTPreparedSheet


def build_chart_3_table(
    gos_sheet: QILTPreparedSheet,
    gos_l_sheet: QILTPreparedSheet,
) -> pd.DataFrame:
    comparison_table = build_qilt_full_time_employment_comparison_table(
        gos_sheet.table,
        gos_l_sheet.table,
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
    )
    chart_table = summary_table.sort_values(
        ["sort_order", "time_window_order"],
        kind="mergesort",
    ).reset_index(drop=True)
    return select_chart_table_schema(chart_table, CHART_3_TABLE_COLUMNS)


def build_chart_3_plot_table(chart_table: pd.DataFrame) -> pd.DataFrame:
    ordered_table = chart_table.sort_values(
        ["sort_order", "time_window_order"],
        kind="mergesort",
    ).reset_index(drop=True)
    index_columns = ["sort_order", "comparison_id", "subgroup_dimension"]
    gap_table = ordered_table.pivot(
        index=index_columns,
        columns="time_window",
        values="gap_pp",
    ).reset_index()
    lower_group_table = (
        ordered_table.pivot(
            index=index_columns,
            columns="time_window",
            values="lower_group",
        )
        .rename(
            columns={
                SHORT_TERM_TIME_WINDOW: f"{SHORT_TERM_TIME_WINDOW}_lower_group",
                MEDIUM_TERM_TIME_WINDOW: f"{MEDIUM_TERM_TIME_WINDOW}_lower_group",
            }
        )
        .reset_index()
    )
    plot_table = gap_table.merge(
        lower_group_table,
        on=index_columns,
        how="left",
        sort=False,
        validate="one_to_one",
    )
    plot_table = plot_table.sort_values(
        ["sort_order", "subgroup_dimension"],
        kind="mergesort",
    ).reset_index(drop=True)
    return plot_table.loc[
        :,
        [
            *index_columns,
            SHORT_TERM_TIME_WINDOW,
            MEDIUM_TERM_TIME_WINDOW,
            f"{SHORT_TERM_TIME_WINDOW}_lower_group",
            f"{MEDIUM_TERM_TIME_WINDOW}_lower_group",
        ],
    ]


def _build_gap_shape_rows(group_table: pd.DataFrame) -> list[dict[str, object]]:
    subgroup_dimension = str(group_table["subgroup_dimension"].iloc[0])
    comparison_id = build_qilt_subgroup_id(subgroup_dimension)
    short_summary = build_qilt_subgroup_pair_summary(
        group_table,
        value_column=QILT_SHORT_TERM_VALUE_COLUMN,
    )
    medium_summary = build_qilt_subgroup_pair_summary(
        group_table,
        value_column=QILT_MEDIUM_TERM_VALUE_COLUMN,
    )

    return [
        {
            "comparison_id": comparison_id,
            "subgroup_dimension": subgroup_dimension,
            **short_summary,
            "time_window": SHORT_TERM_TIME_WINDOW,
            "time_window_order": 0,
            "source_key": GOS_8_SOURCE_KEY,
        },
        {
            "comparison_id": comparison_id,
            "subgroup_dimension": subgroup_dimension,
            **medium_summary,
            "time_window": MEDIUM_TERM_TIME_WINDOW,
            "time_window_order": 1,
            "source_key": GOS_L_160_SOURCE_KEY,
        },
    ]
