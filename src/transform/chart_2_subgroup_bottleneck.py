from __future__ import annotations

from typing import Optional

import pandas as pd

from src.preparation.qilt import clean_qilt_display_text
from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_2_TABLE_COLUMNS,
    GOS_5_SOURCE_KEY,
    GOS_8_SOURCE_KEY,
    GOS_GENDER_SHORT_TERM_COLUMNS_BY_ROW_LABEL,
    GOS_SHORT_TERM_COMPARISON_COLUMNS,
    TOTAL_ROW_GROUP,
)
from src.transform.qilt import build_qilt_subgroup_pair_summary
from src.types import PreparedRows, QILTPreparedSheet


def build_chart_2_table(
    gos_sheet: QILTPreparedSheet,
    gender_sheet: Optional[QILTPreparedSheet] = None,
) -> pd.DataFrame:
    gender_table = gender_sheet.table if gender_sheet is not None else None
    prepared_rows: PreparedRows = []
    gender_rows = _build_gender_rows(gender_table) if gender_table is not None else None
    inserted_gender_rows = False

    for _, row in gos_sheet.table.iterrows():
        row_group = clean_qilt_display_text(row["row_group"])

        if row_group is None or row_group == TOTAL_ROW_GROUP:
            continue

        if row_group == "Gender" and gender_rows is not None:
            if not inserted_gender_rows:
                prepared_rows.extend(gender_rows)
                inserted_gender_rows = True
            continue

        prepared_rows.append(_build_demographic_row(row))

    if gender_rows is not None and not inserted_gender_rows:
        prepared_rows[0:0] = gender_rows

    subgroup_table = pd.DataFrame(prepared_rows)
    summary_rows = [
        _build_chart_2_summary_row(group_table)
        for _, group_table in subgroup_table.groupby("subgroup_dimension", sort=False)
    ]
    chart_table = pd.DataFrame(summary_rows)
    chart_table["sort_order"] = _build_sort_order(chart_table)
    chart_table = chart_table.sort_values(
        ["sort_order", "subgroup_dimension"],
        kind="mergesort",
    ).reset_index(drop=True)
    return select_chart_table_schema(chart_table, CHART_2_TABLE_COLUMNS)


def _build_demographic_row(row: pd.Series) -> dict[str, object]:
    return {
        "subgroup_dimension": clean_qilt_display_text(row["row_group"]),
        "row_label": clean_qilt_display_text(row["row_label"]),
        "full_time_employment": row[
            GOS_SHORT_TERM_COMPARISON_COLUMNS["short_term_full_time_employment"]
        ],
        "source_key": GOS_8_SOURCE_KEY,
    }


def _build_gender_rows(gender_table: pd.DataFrame) -> PreparedRows:
    male_row: dict[str, object] = {
        "subgroup_dimension": "Gender",
        "row_label": "Male",
        "source_key": GOS_5_SOURCE_KEY,
    }
    female_row: dict[str, object] = {
        "subgroup_dimension": "Gender",
        "row_label": "Female",
        "source_key": GOS_5_SOURCE_KEY,
    }

    for _, row in gender_table.iterrows():
        row_label = clean_qilt_display_text(row["row_label"])

        if row_label is None:
            continue

        output_column = GOS_GENDER_SHORT_TERM_COLUMNS_BY_ROW_LABEL[row_label]
        if output_column != "short_term_full_time_employment":
            continue

        male_row["full_time_employment"] = row["male_2024"]
        female_row["full_time_employment"] = row["female_2024"]

    return [male_row, female_row]


def _build_chart_2_summary_row(group_table: pd.DataFrame) -> dict[str, object]:
    subgroup_dimension = str(group_table["subgroup_dimension"].iloc[0])
    source_key = str(group_table["source_key"].iloc[0])
    summary_row: dict[str, object] = {
        "subgroup_dimension": subgroup_dimension,
        "source_key": source_key,
    }

    pair_summary = build_qilt_subgroup_pair_summary(
        group_table,
        value_column="full_time_employment",
    )
    pair_summary.pop("comparison_label")
    summary_row.update(pair_summary)
    return summary_row


def _build_sort_order(chart_table: pd.DataFrame) -> pd.Series:
    ordered_dimensions = (
        chart_table.loc[:, ["subgroup_dimension", "gap_pp"]]
        .sort_values(
            ["gap_pp", "subgroup_dimension"],
            ascending=[False, True],
            kind="mergesort",
            na_position="last",
        )["subgroup_dimension"]
        .tolist()
    )
    order_lookup = {
        subgroup_dimension: order
        for order, subgroup_dimension in enumerate(ordered_dimensions)
    }
    return chart_table["subgroup_dimension"].map(order_lookup).astype("Int64")
