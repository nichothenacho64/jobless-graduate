from __future__ import annotations

import pandas as pd

from src.parsers.constants import QILT_YEAR_PATTERN
from src.preparation.qilt import clean_qilt_display_text
from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_2_CONSTANTS,
    GOS_21_SOURCE_KEY,
    GOS_NATIONAL_REPORT_2024_SOURCE_KEY,
    GOS_L_1_SOURCE_KEY,
)
from src.transform.metadata import CHART_2_METADATA
from src.types import PreparedRows, QILTPreparedSheet


GOS_SHORT_TERM_MIN_DISPLAY_YEAR = 2020
GOS_NATIONAL_REPORT_2024_SHORT_TERM_FTE_VALUES = {
    2020: 68.7,
    2021: 68.9,
}


def build_chart_2_table(
    gos_sheet: QILTPreparedSheet,
    gos_l_sheet: QILTPreparedSheet,
) -> pd.DataFrame:
    rows = [
        *_build_gos_short_term_full_time_rows(gos_sheet.table),
        *_build_gos_l_full_time_rows(gos_l_sheet.table),
    ]
    chart_table = pd.DataFrame(rows)
    chart_table["series_order"] = chart_table["series_key"].map(
        CHART_2_CONSTANTS["series_order"],
    )
    chart_table = chart_table.sort_values(
        ["display_year", "series_order"],
        kind="mergesort",
    )
    chart_table = select_chart_table_schema(
        chart_table,
        CHART_2_CONSTANTS["table_columns"],
    )
    chart_table.attrs["chart_metadata"] = CHART_2_METADATA
    return chart_table


def _build_gos_short_term_full_time_rows(gos_table: pd.DataFrame) -> PreparedRows:
    total_rows = gos_table.loc[
        gos_table["row_label"].map(clean_qilt_display_text) == "Total"
    ]
    prepared_rows: PreparedRows = []
    series_key = CHART_2_CONSTANTS["series_keys"]["gos_short_term"]

    for _, row in total_rows.iterrows():
        display_year = _extract_terminal_year(row["row_group"])
        if display_year < GOS_SHORT_TERM_MIN_DISPLAY_YEAR:
            continue

        value_pct = row["full_time_employment"]
        if pd.isna(value_pct):
            continue

        prepared_rows.append(
            {
                "display_year": display_year,
                "series_key": series_key,
                "value_pct": value_pct,
                "source_key": GOS_21_SOURCE_KEY,
            }
        )

    prepared_years = {row["display_year"] for row in prepared_rows}
    report_values = GOS_NATIONAL_REPORT_2024_SHORT_TERM_FTE_VALUES
    for display_year, value_pct in report_values.items():
        if display_year in prepared_years:
            continue

        prepared_rows.append(
            {
                "display_year": display_year,
                "series_key": series_key,
                "value_pct": value_pct,
                "source_key": GOS_NATIONAL_REPORT_2024_SOURCE_KEY,
            }
        )

    return sorted(prepared_rows, key=_display_year_sort_key)


def _display_year_sort_key(row: dict[str, object]) -> int:
    display_year = row["display_year"]
    if not isinstance(display_year, int):
        raise TypeError("Chart 2 display_year values must be integers.")

    return display_year


def _build_gos_l_full_time_rows(gos_l_table: pd.DataFrame) -> PreparedRows:
    prepared_rows: PreparedRows = []

    for _, row in gos_l_table.iterrows():
        display_year = _extract_terminal_year(row["year"])
        prepared_rows.extend(
            [
                {
                    "display_year": display_year,
                    "series_key": CHART_2_CONSTANTS["series_keys"][
                        "gos_l_short_term"
                    ],
                    "value_pct": row["short_term_fte"],
                    "source_key": GOS_L_1_SOURCE_KEY,
                },
                {
                    "display_year": display_year,
                    "series_key": CHART_2_CONSTANTS["series_keys"][
                        "gos_l_medium_term"
                    ],
                    "value_pct": row["medium_term_fte"],
                    "source_key": GOS_L_1_SOURCE_KEY,
                },
            ]
        )

    return prepared_rows


def _extract_terminal_year(value: object) -> int:
    year_matches = QILT_YEAR_PATTERN.findall(str(value))
    return int(year_matches[-1])
