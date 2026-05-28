from __future__ import annotations

import pandas as pd

from src.preparation.abs import clean_abs_display_text, parse_abs_number
from src.preparation.series import is_missing_value
from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_1A_CONSTANTS,
    SEW_35_SOURCE_KEY,
)
from src.transform.metadata import CHART_1A_METADATA
from src.types import ABSPreparedSheet, PreparedRows


def build_chart_1a_table(sew_table_35_sheet: ABSPreparedSheet) -> pd.DataFrame:
    _require_sew_table_35(sew_table_35_sheet)
    source_rows = _select_degree_supply_source_rows(sew_table_35_sheet.table)
    base_value = _select_base_value(source_rows)
    prepared_rows: PreparedRows = []

    for _, row in source_rows.iterrows():
        source_value = row["estimate_count"]

        if is_missing_value(source_value):
            continue

        population = float(source_value) * 1000

        prepared_rows.append(
            {
                "year": int(row["_year"]),
                "bachelor_degree_or_above_holders_population": round(population),
                "bachelor_degree_or_above_holders_increase_pct": round(
                    (float(source_value) - base_value) / base_value * 100,
                    1,
                ),
                "source_key": SEW_35_SOURCE_KEY,
            }
        )

    chart_table = pd.DataFrame(prepared_rows).sort_values("year", kind="mergesort")
    chart_table = select_chart_table_schema(
        chart_table,
        CHART_1A_CONSTANTS["table_columns"],
    )
    chart_table.attrs["chart_metadata"] = CHART_1A_METADATA
    return chart_table


def _require_sew_table_35(sew_table_35_sheet: ABSPreparedSheet) -> None:
    if sew_table_35_sheet.table_number != CHART_1A_CONSTANTS["source_table_number"]:
        raise ValueError("Chart 1A requires SEW Table 35.")


def _select_degree_supply_source_rows(table: pd.DataFrame) -> pd.DataFrame:
    _require_columns(
        table,
        {
            "subject",
            "row_group",
            "row_label",
            "column_header",
            "estimate_count",
        },
    )

    subject = table["subject"].map(clean_abs_display_text)
    row_group = table["row_group"].map(clean_abs_display_text)
    row_label = table["row_label"].map(clean_abs_display_text)
    qualification_filter = CHART_1A_CONSTANTS["qualification_filter"]
    selected_subject = f"People with a {qualification_filter}"
    selected_rows = table.loc[
        (subject == selected_subject)
        & (row_group == CHART_1A_CONSTANTS["population_group"])
        & (row_label == CHART_1A_CONSTANTS["row_label"])
        & table["estimate_count"].notna()
    ].copy()
    selected_rows["_year"] = selected_rows["column_header"].map(_parse_year)
    selected_rows = selected_rows.loc[
        selected_rows["_year"].isin(CHART_1A_CONSTANTS["years"])
    ].copy()

    if selected_rows.empty:
        raise ValueError(
            "SEW Table 35 has no Estimate ('000) rows for the "
            "bachelor degree or above Persons/Total source row."
        )

    _require_expected_years(selected_rows)

    return selected_rows.sort_values("_year", kind="mergesort")


def _parse_year(value: object) -> object:
    parsed_year = parse_abs_number(value)
    if parsed_year is None:
        return pd.NA

    return int(parsed_year)


def _require_expected_years(source_rows: pd.DataFrame) -> None:
    years = source_rows["_year"].dropna().astype(int)
    duplicate_years = years.loc[years.duplicated()].drop_duplicates().tolist()
    if duplicate_years:
        raise ValueError(
            "SEW Table 35 has multiple selected degree-supply rows for years: "
            + ", ".join(map(str, duplicate_years))
        )

    missing_years = sorted(set(CHART_1A_CONSTANTS["years"]) - set(years.tolist()))
    if missing_years:
        raise ValueError(
            "SEW Table 35 is missing selected degree-supply rows for years: "
            + ", ".join(map(str, missing_years))
        )


def _select_base_value(source_rows: pd.DataFrame) -> float:
    base_year = CHART_1A_CONSTANTS["base_year"]
    base_rows = source_rows.loc[source_rows["_year"] == base_year]

    if base_rows.empty:
        raise ValueError(
            f"SEW Table 35 has no {base_year} base-year value."
        )

    base_value = base_rows["estimate_count"].iloc[0]
    if is_missing_value(base_value) or float(base_value) == 0:
        raise ValueError(
            "SEW Table 35 "
            f"{base_year} base-year value is unavailable."
        )

    return float(base_value)


def _require_columns(table: pd.DataFrame, columns: set[str]) -> None:
    missing_columns = sorted(columns - set(table.columns))
    if missing_columns:
        raise ValueError(
            "SEW Table 35 is missing required prepared columns: "
            + ", ".join(missing_columns)
        )
