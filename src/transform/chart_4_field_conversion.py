from __future__ import annotations

import pandas as pd

from src.preparation.qilt import clean_qilt_display_text
from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_4_EXCLUDED_STUDY_AREAS,
    CHART_4_TABLE_COLUMNS,
    GOS_L_6_SOURCE_KEY,
)
from src.types import PreparedRows, QILTPreparedSheet


def build_chart_4_table(gos_l_area_sheet: QILTPreparedSheet) -> pd.DataFrame:
    prepared_rows: PreparedRows = []
    excluded_rows: list[dict[str, object]] = []

    for _, row in gos_l_area_sheet.table.iterrows():
        study_area = clean_qilt_display_text(row["area"])
        if study_area in CHART_4_EXCLUDED_STUDY_AREAS:
            excluded_rows.append(
                {
                    "row_label": study_area,
                    "reason": CHART_4_EXCLUDED_STUDY_AREAS[study_area],
                    "source_key": GOS_L_6_SOURCE_KEY,
                }
            )
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
    chart_table = chart_table.sort_values("study_area", kind="mergesort")
    chart_table = select_chart_table_schema(chart_table, CHART_4_TABLE_COLUMNS)
    chart_table.attrs["chart_metadata"] = {
        "excluded_rows": excluded_rows,
    }
    return chart_table
