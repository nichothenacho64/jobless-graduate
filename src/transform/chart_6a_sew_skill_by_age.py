from __future__ import annotations

import pandas as pd

from src.preparation.abs import clean_abs_display_text, format_abs_column_label
from src.transform.chart_helpers import select_chart_table_schema
from src.transform.constants import (
    CHART_6A_TABLE_COLUMNS,
    SEW_32_SOURCE_KEY,
    SEW_AGE_GROUP_ORDER,
    SEW_SKILL_LEVEL_ORDER,
)
from src.types import ABSPreparedSheet


def build_chart_6a_table(sew_table_32_sheet: ABSPreparedSheet) -> pd.DataFrame:
    prepared_rows: list[dict[str, object]] = []

    for _, row in sew_table_32_sheet.table.iterrows():
        age_group = clean_abs_display_text(row["row_label"])
        skill_level = format_abs_column_label(row["column_header"])

        if row["row_group"] != "Age group (years)":
            continue
        if age_group is None or age_group not in SEW_AGE_GROUP_ORDER:
            continue
        if skill_level is None or skill_level not in SEW_SKILL_LEVEL_ORDER:
            continue

        prepared_rows.append(
            {
                "age_group": age_group,
                "age_order": SEW_AGE_GROUP_ORDER[age_group],
                "skill_level": skill_level,
                "skill_order": SEW_SKILL_LEVEL_ORDER[skill_level],
                "share_pct": row["proportion_percent"],
                "source_key": SEW_32_SOURCE_KEY,
            }
        )

    chart_table = pd.DataFrame(prepared_rows).sort_values(
        ["age_order", "skill_order"],
        kind="mergesort",
    )
    return select_chart_table_schema(chart_table, CHART_6A_TABLE_COLUMNS)
