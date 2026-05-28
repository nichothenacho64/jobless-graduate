from __future__ import annotations

from collections.abc import Hashable

import pandas as pd

from src.preparation.series import is_missing_value
from src.preparation.qilt import clean_qilt_display_text
from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_6_CONSTANTS,
    GOS_L_6_SOURCE_KEY,
    GOS_L_26_SOURCE_KEY,
)
from src.transform.metadata import CHART_6_METADATA
from src.types import QILTPreparedSheet


def build_chart_6_table(
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
    merged_table["fit_metric_key"] = CHART_6_CONSTANTS["work_fit_metric_key"]
    merged_table["employment_source_key"] = GOS_L_6_SOURCE_KEY
    merged_table["fit_source_key"] = GOS_L_26_SOURCE_KEY

    chart_table = _exclude_non_plotted_rows(merged_table)
    chart_table = chart_table.loc[
        :,
        CHART_6_CONSTANTS["table_columns"],
    ].sort_values("study_area", kind="mergesort")
    chart_table = select_chart_table_schema(
        chart_table,
        CHART_6_CONSTANTS["table_columns"],
    )
    chart_table.attrs["chart_metadata"] = CHART_6_METADATA
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
                CHART_6_CONSTANTS["underutilisation_columns"]["short_term"]
            ],
            "medium_term_underutilisation_pct": table[
                CHART_6_CONSTANTS["underutilisation_columns"]["medium_term"]
            ],
        }
    )


def _exclude_non_plotted_rows(
    table: pd.DataFrame,
) -> pd.DataFrame:
    excluded_index_labels: list[Hashable] = []
    excluded_study_areas = CHART_6_CONSTANTS["excluded_study_areas"]

    for row_index, row in table.iterrows():
        study_area = str(row["study_area"])
        if study_area in excluded_study_areas:
            excluded_index_labels.append(row_index)
            continue

        if is_missing_value(row["underutilisation_reduction_pp"]):
            excluded_index_labels.append(row_index)

    return table.drop(index=excluded_index_labels).copy()
