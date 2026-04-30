from __future__ import annotations

import pandas as pd

from src.parsers.constants import QILT_YEAR_PATTERN
from src.transform.constants import (
    GOS_AGGREGATE_SHORT_TERM_COMPARISON_COLUMNS,
    GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS,
)
from src.preparation.qilt import clean_qilt_display_text

def build_transition_problem_table(
    gos_table: pd.DataFrame,
    gos_l_table: pd.DataFrame,
) -> pd.DataFrame:
    prepared_gos_table = _prepare_transition_short_term_table(gos_table)
    prepared_gos_l_table = _prepare_transition_medium_term_table(gos_l_table)

    transition_table = prepared_gos_table.merge(
        prepared_gos_l_table[
            [
                "year",
                *GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS.keys(),
            ]
        ],
        on="year",
        how="inner",
        sort=False,
    )

    final_columns = [
        "year",
        "period_label",
        *GOS_AGGREGATE_SHORT_TERM_COMPARISON_COLUMNS.keys(),
        *GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS.keys(),
    ]
    return transition_table.loc[:, final_columns].sort_values("year").reset_index(drop=True)

def _prepare_transition_short_term_table(gos_table: pd.DataFrame) -> pd.DataFrame:
    total_rows = gos_table.loc[
        gos_table["row_label"].map(clean_qilt_display_text) == "Total"
    ].copy()
    total_rows["year"] = total_rows["row_group"].map(_extract_terminal_year)
    total_rows["period_label"] = total_rows["year"].astype(str)

    prepared_rows: list[dict[str, object]] = []

    for _, row in total_rows.iterrows():
        prepared_row: dict[str, object] = {
            "year": row["year"],
            "period_label": row["period_label"],
        }

        for output_column, source_column in GOS_AGGREGATE_SHORT_TERM_COMPARISON_COLUMNS.items():
            prepared_row[output_column] = row[source_column]

        prepared_rows.append(prepared_row)

    return pd.DataFrame(prepared_rows)

def _prepare_transition_medium_term_table(gos_l_table: pd.DataFrame) -> pd.DataFrame:
    prepared_rows: list[dict[str, object]] = []

    for _, row in gos_l_table.iterrows():
        prepared_row: dict[str, object] = {
            "year": _extract_terminal_year(row["year"]),
        }

        for output_column, source_column in GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS.items():
            prepared_row[output_column] = row[source_column]

        prepared_rows.append(prepared_row)

    return pd.DataFrame(prepared_rows)

def _extract_terminal_year(value: object) -> int:
    year_matches = QILT_YEAR_PATTERN.findall(str(value))
    return int(year_matches[-1])
