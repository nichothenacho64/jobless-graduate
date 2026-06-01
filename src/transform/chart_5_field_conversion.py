from __future__ import annotations

import pandas as pd

from src.preparation.qilt import clean_qilt_display_text
from src.transform.chart_helpers import (
    add_discipline_family_colour_fields,
    select_chart_table_schema,
)
from src.transform.constants import (
    CHART_5_CONSTANTS,
    DISCIPLINE_FAMILY_CONSTANTS,
    GOS_L_6_SOURCE_KEY,
)
from src.transform.metadata import CHART_5_METADATA
from src.types import PreparedRows, QILTPreparedSheet


def build_chart_5_table(gos_l_area_sheet: QILTPreparedSheet) -> pd.DataFrame:
    prepared_rows: PreparedRows = []
    excluded_study_areas = CHART_5_CONSTANTS["excluded_study_areas"]

    for _, row in gos_l_area_sheet.table.iterrows():
        study_area = clean_qilt_display_text(row["area"])
        if study_area in excluded_study_areas:
            continue

        prepared_rows.append(
            {
                "study_area": study_area,
                "short_term_fte_pct": row["short_term_full_time_employed"],
                "medium_term_fte_pct": row["medium_term_full_time_employed"],
                "source_key": GOS_L_6_SOURCE_KEY,
            }
        )

    chart_table = pd.DataFrame(prepared_rows)
    chart_table = add_discipline_family_colour_fields(
        chart_table,
        DISCIPLINE_FAMILY_CONSTANTS["colour_columns"],
    )
    chart_table = chart_table.sort_values("study_area", kind="mergesort")
    chart_table = select_chart_table_schema(
        chart_table,
        CHART_5_CONSTANTS["table_columns"],
    )
    chart_table.attrs["chart_metadata"] = CHART_5_METADATA
    return chart_table
