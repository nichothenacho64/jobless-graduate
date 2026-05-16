from __future__ import annotations

from collections.abc import Hashable

import pandas as pd

from src.preparation.series import is_missing_value
from src.preparation.qilt import clean_qilt_display_text
from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_5_EXCLUDED_STUDY_AREAS,
    CHART_5_MEDIUM_TERM_UNDERUTILISATION_COLUMN,
    CHART_5_SHORT_TERM_UNDERUTILISATION_COLUMN,
    CHART_5_TABLE_COLUMNS,
    CHART_5_WORK_FIT_METRIC_KEY,
    GOS_L_6_SOURCE_KEY,
    GOS_L_26_SOURCE_KEY,
)
from src.types import QILTPreparedSheet


def build_chart_5_table(
    employment_sheet: QILTPreparedSheet,
    fit_sheet: QILTPreparedSheet,
) -> pd.DataFrame:
    employment_table = _normalise_employment_table(employment_sheet.table)
    fit_table = _normalise_fit_table(fit_sheet.table)
    merged_table = employment_table.merge(
        fit_table,
        on="study_area",
        how="inner",
        validate="one_to_one",
        sort=False,
    )

    merged_table["fte_gain_pp"] = (
        merged_table["medium_term_fte_pct"] - merged_table["short_term_fte_pct"]
    ).round(1)
    merged_table["underutilisation_reduction_pp"] = (
        merged_table["short_term_underutilisation_pct"]
        - merged_table["medium_term_underutilisation_pct"]
    ).round(1)
    merged_table["fit_metric_key"] = CHART_5_WORK_FIT_METRIC_KEY
    merged_table["employment_source_key"] = GOS_L_6_SOURCE_KEY
    merged_table["fit_source_key"] = GOS_L_26_SOURCE_KEY

    chart_table, excluded_rows = _exclude_non_plotted_rows(merged_table)
    chart_table = chart_table.loc[
        :,
        CHART_5_TABLE_COLUMNS,
    ].sort_values("study_area", kind="mergesort")
    chart_table = select_chart_table_schema(chart_table, CHART_5_TABLE_COLUMNS)
    chart_table.attrs["chart_metadata"] = {
        "fit_metric_key": CHART_5_WORK_FIT_METRIC_KEY,
        "employment_source_key": GOS_L_6_SOURCE_KEY,
        "fit_metric_source_key": GOS_L_26_SOURCE_KEY,
        "fit_metric_direction": "lower_underutilisation_is_better",
        "fit_change_formula": (
            "short_term_underutilisation_pct - medium_term_underutilisation_pct"
        ),
        "fit_metric_source_columns": {
            "short_term_underutilisation_pct": (
                CHART_5_SHORT_TERM_UNDERUTILISATION_COLUMN
            ),
            "medium_term_underutilisation_pct": (
                CHART_5_MEDIUM_TERM_UNDERUTILISATION_COLUMN
            ),
        },
        "excluded_rows": excluded_rows,
    }
    return chart_table


def _normalise_employment_table(table: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "study_area": table["area"].map(clean_qilt_display_text),
            "short_term_fte_pct": table["short_term_full_time_employed"],
            "medium_term_fte_pct": table["medium_term_full_time_employed"],
        }
    )


def _normalise_fit_table(table: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "study_area": table["area"].map(clean_qilt_display_text),
            "short_term_underutilisation_pct": table[
                CHART_5_SHORT_TERM_UNDERUTILISATION_COLUMN
            ],
            "medium_term_underutilisation_pct": table[
                CHART_5_MEDIUM_TERM_UNDERUTILISATION_COLUMN
            ],
        }
    )


def _exclude_non_plotted_rows(
    table: pd.DataFrame,
) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    excluded_rows: list[dict[str, object]] = []
    excluded_index_labels: list[Hashable] = []

    for row_index, row in table.iterrows():
        study_area = str(row["study_area"])
        if study_area in CHART_5_EXCLUDED_STUDY_AREAS:
            excluded_rows.append(
                {
                    "row_label": study_area,
                    "reason": CHART_5_EXCLUDED_STUDY_AREAS[study_area],
                    "source_keys": [GOS_L_6_SOURCE_KEY, GOS_L_26_SOURCE_KEY],
                }
            )
            excluded_index_labels.append(row_index)
            continue

        if is_missing_value(row["underutilisation_reduction_pp"]):
            excluded_rows.append(
                {
                    "row_label": study_area,
                    "reason": "source_underutilisation_values_missing",
                    "columns": ["underutilisation_reduction_pp"],
                    "source_key": GOS_L_26_SOURCE_KEY,
                    "source_columns": [
                        CHART_5_SHORT_TERM_UNDERUTILISATION_COLUMN,
                        CHART_5_MEDIUM_TERM_UNDERUTILISATION_COLUMN,
                    ],
                }
            )
            excluded_index_labels.append(row_index)

    return table.drop(index=excluded_index_labels).copy(), excluded_rows
