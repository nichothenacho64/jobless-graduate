from __future__ import annotations

import pandas as pd

from src.preparation.abs import clean_abs_display_text, parse_abs_number
from src.preparation.series import is_missing_value
from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_6B_TABLE_COLUMNS,
    SEW_35_SOURCE_KEY,
    SEW_DEGREE_SUPPLY_BASE_YEAR,
    SEW_DEGREE_SUPPLY_YEARS,
)
from src.types import ABSPreparedSheet, ChartMetadata, PreparedRows

SEW_35_TABLE_NUMBER = 35
SEW_35_MEASUREMENT_LABEL = "Estimate ('000)"
SEW_35_QUALIFICATION_FILTER = (
    "highest non-school qualification at bachelor degree level or above"
)
SEW_35_SUBJECT = f"People with a {SEW_35_QUALIFICATION_FILTER}"
SEW_35_POPULATION_GROUP = "Persons"
SEW_35_ROW_LABEL = "Total"
SEW_DEGREE_SUPPLY_BASE_UNIT = "thousands of persons"
SEW_DEGREE_SUPPLY_INDEX_FORMULA = "value / base_value * 100"


def build_chart_6b_table(sew_table_35_sheet: ABSPreparedSheet) -> pd.DataFrame:
    _require_sew_table_35(sew_table_35_sheet)
    source_rows = _select_degree_supply_source_rows(sew_table_35_sheet.table)
    base_value = _select_base_value(source_rows)
    prepared_rows: PreparedRows = []

    for _, row in source_rows.iterrows():
        value = row["estimate_count"]

        if is_missing_value(value):
            continue

        prepared_rows.append(
            {
                "year": int(row["_year"]),
                "bachelor_degree_or_above_count_index": round(float(value) / base_value * 100, 1),
                "source_key": SEW_35_SOURCE_KEY,
            }
        )

    chart_table = pd.DataFrame(prepared_rows).sort_values("year", kind="mergesort")
    chart_table = select_chart_table_schema(chart_table, CHART_6B_TABLE_COLUMNS)
    chart_table.attrs["chart_metadata"] = build_chart_6b_derivation_metadata(
        sew_table_35_sheet,
    )
    return chart_table


def build_chart_6b_derivation_metadata(
    sew_table_35_sheet: ABSPreparedSheet,
) -> ChartMetadata:
    _require_sew_table_35(sew_table_35_sheet)
    source_rows = _select_degree_supply_source_rows(sew_table_35_sheet.table)
    base_value = _select_base_value(source_rows)

    return {
        "base_year": SEW_DEGREE_SUPPLY_BASE_YEAR,
        "base_value": round(base_value, 1),
        "base_unit": SEW_DEGREE_SUPPLY_BASE_UNIT,
        "selected_measurement": SEW_35_MEASUREMENT_LABEL,
        "selected_population_group": SEW_35_POPULATION_GROUP,
        "selected_row_label": SEW_35_ROW_LABEL,
        "qualification_filter": SEW_35_QUALIFICATION_FILTER,
        "formula": SEW_DEGREE_SUPPLY_INDEX_FORMULA,
    }


def _require_sew_table_35(sew_table_35_sheet: ABSPreparedSheet) -> None:
    if sew_table_35_sheet.table_number != SEW_35_TABLE_NUMBER:
        raise ValueError("Chart 6B requires SEW Table 35.")


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
    selected_rows = table.loc[
        (subject == SEW_35_SUBJECT)
        & (row_group == SEW_35_POPULATION_GROUP)
        & (row_label == SEW_35_ROW_LABEL)
        & table["estimate_count"].notna()
    ].copy()
    selected_rows["_year"] = selected_rows["column_header"].map(_parse_year)
    selected_rows = selected_rows.loc[
        selected_rows["_year"].isin(SEW_DEGREE_SUPPLY_YEARS)
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

    missing_years = sorted(set(SEW_DEGREE_SUPPLY_YEARS) - set(years.tolist()))
    if missing_years:
        raise ValueError(
            "SEW Table 35 is missing selected degree-supply rows for years: "
            + ", ".join(map(str, missing_years))
        )


def _select_base_value(source_rows: pd.DataFrame) -> float:
    base_rows = source_rows.loc[source_rows["_year"] == SEW_DEGREE_SUPPLY_BASE_YEAR]

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


def _require_columns(table: pd.DataFrame, columns: set[str]) -> None:
    missing_columns = sorted(columns - set(table.columns))
    if missing_columns:
        raise ValueError(
            "SEW Table 35 is missing required prepared columns: "
            + ", ".join(missing_columns)
        )
