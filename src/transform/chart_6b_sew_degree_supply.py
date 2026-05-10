from __future__ import annotations

import pandas as pd

from src.preparation.abs import clean_abs_display_text, parse_abs_number
from src.preparation.series import is_missing_value
from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_6B_TABLE_COLUMNS,
    SEW_35_SOURCE_KEY,
    SEW_DEGREE_SUPPLY_BASE_YEAR,
)
from src.types import ABSPreparedSheet


def build_chart_6b_table(sew_table_35_sheet: ABSPreparedSheet) -> pd.DataFrame:
    source_rows = _select_person_total_rows(sew_table_35_sheet.table)
    base_value = _select_base_value(source_rows)
    prepared_rows: list[dict[str, object]] = []

    for _, row in source_rows.iterrows():
        parsed_year = parse_abs_number(row["column_header"])
        value = row["estimate_count"]

        if parsed_year is None or is_missing_value(value):
            continue

        prepared_rows.append(
            {
                "year": int(parsed_year),
                "index_2016_100": round(float(value) / base_value * 100, 1),
                "source_key": SEW_35_SOURCE_KEY,
            }
        )

    chart_table = pd.DataFrame(prepared_rows).sort_values("year", kind="mergesort")
    return select_chart_table_schema(chart_table, CHART_6B_TABLE_COLUMNS)


def _select_person_total_rows(table: pd.DataFrame) -> pd.DataFrame:
    row_group = table["row_group"].map(clean_abs_display_text)
    row_label = table["row_label"].map(clean_abs_display_text)
    selected_rows = table.loc[
        (row_group == "Persons")
        & (row_label == "Total")
        & table["estimate_count"].notna()
    ].copy()

    if selected_rows.empty:
        raise ValueError("SEW Table 35 has no Persons/Total estimate rows.")

    return selected_rows


def _select_base_value(source_rows: pd.DataFrame) -> float:
    years = source_rows["column_header"].map(parse_abs_number)
    base_rows = source_rows.loc[years == SEW_DEGREE_SUPPLY_BASE_YEAR]

    if base_rows.empty:
        raise ValueError(
            f"SEW Table 35 has no {SEW_DEGREE_SUPPLY_BASE_YEAR} base-year value."
        )

    base_value = base_rows["estimate_count"].iloc[0]
    if is_missing_value(base_value) or float(base_value) == 0:
        raise ValueError(
            "SEW Table 35 "
            f"{SEW_DEGREE_SUPPLY_BASE_YEAR} base-year value is unavailable."
        )

    return float(base_value)
