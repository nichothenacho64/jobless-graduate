from __future__ import annotations

from typing import Optional

import pandas as pd

from src.constants.qilt import (
    GOS_GENDER_SHORT_TERM_COLUMNS_BY_ROW_LABEL,
    GOS_SHORT_TERM_COMPARISON_COLUMNS,
    QILT_SHORT_MEDIUM_OUTCOME_SPECS,
    TOTAL_ROW_GROUP,
)
from src.preparation.qilt import clean_qilt_display_text
from src.transform.qilt import build_qilt_pair_label, select_qilt_ordered_pair_rows

def build_unequal_distribution_table(
    gos_table: pd.DataFrame,
    gender_table: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    prepared_rows: list[dict[str, object]] = []
    gender_rows = _build_gender_rows(gender_table) if gender_table is not None else None
    inserted_gender_rows = False

    for _, row in gos_table.iterrows():
        row_group = clean_qilt_display_text(row["row_group"])

        if row_group is None or row_group == TOTAL_ROW_GROUP:
            continue

        if row_group == "Gender" and gender_rows is not None:
            if not inserted_gender_rows:
                prepared_rows.extend(gender_rows)
                inserted_gender_rows = True
            continue

        prepared_rows.append(_build_unequal_distribution_row(row))

    if gender_rows is not None and not inserted_gender_rows:
        prepared_rows[0:0] = gender_rows

    subgroup_levels_table = pd.DataFrame(prepared_rows)
    summary_rows = [
        _build_unequal_distribution_summary_row(group_table)
        for _, group_table in subgroup_levels_table.groupby("row_group", sort=False)
    ]
    summary_table = pd.DataFrame(summary_rows)
    summary_table["row_group_order"] = _build_row_group_order(summary_table)

    return (
        summary_table.sort_values(
            ["row_group_order", "row_group"],
            kind="mergesort",
        )
        .reset_index(drop=True)
    )

def _build_unequal_distribution_row(row: pd.Series) -> dict[str, object]:
    prepared_row: dict[str, object] = {
        "row_group": clean_qilt_display_text(row["row_group"]),
        "row_label": clean_qilt_display_text(row["row_label"]),
    }

    for output_column, source_column in GOS_SHORT_TERM_COMPARISON_COLUMNS.items():
        prepared_row[output_column] = row[source_column]

    return prepared_row

def _build_gender_rows(gender_table: pd.DataFrame) -> list[dict[str, object]]:
    male_row: dict[str, object] = {
        "row_group": "Gender",
        "row_label": "Male",
    }
    female_row: dict[str, object] = {
        "row_group": "Gender",
        "row_label": "Female",
    }

    for _, row in gender_table.iterrows():
        row_label = clean_qilt_display_text(row["row_label"])

        if row_label is None:
            continue

        output_column = GOS_GENDER_SHORT_TERM_COLUMNS_BY_ROW_LABEL[row_label]
        male_row[output_column] = row["male_2024"]
        female_row[output_column] = row["female_2024"]

    return [male_row, female_row]

def _build_unequal_distribution_summary_row(group_table: pd.DataFrame) -> dict[str, object]:
    row_group = str(group_table["row_group"].iloc[0])
    summary_row: dict[str, object] = {
        "row_group": row_group,
    }

    full_time_pair = select_qilt_ordered_pair_rows(
        group_table,
        value_column="short_term_full_time_employment",
    )

    if full_time_pair is None:
        summary_row.update(
            {
                "low_row_label": None,
                "high_row_label": None,
                "pair_label": None,
                "comparison_available": False,
                "availability_note": "Comparison unavailable",
            }
        )
        for outcome_key, short_column, _ in QILT_SHORT_MEDIUM_OUTCOME_SPECS:
            summary_row[f"{outcome_key}_low_value"] = None
            summary_row[f"{outcome_key}_high_value"] = None
            summary_row[f"{outcome_key}_gap"] = None
            summary_row[f"{outcome_key}_availability_note"] = "Comparison unavailable"

        return summary_row

    low_row, high_row = full_time_pair
    summary_row.update(
        {
            "low_row_label": low_row["row_label"],
            "high_row_label": high_row["row_label"],
            "pair_label": build_qilt_pair_label(
                low_row["row_label"],
                high_row["row_label"],
            ),
            "comparison_available": True,
            "availability_note": None,
        }
    )

    for outcome_key, short_column, _ in QILT_SHORT_MEDIUM_OUTCOME_SPECS:
        low_value = low_row[short_column]
        high_value = high_row[short_column]
        value_available = pd.notna(low_value) and pd.notna(high_value)

        summary_row[f"{outcome_key}_low_value"] = low_value if value_available else None
        summary_row[f"{outcome_key}_high_value"] = high_value if value_available else None
        summary_row[f"{outcome_key}_gap"] = (
            round(float(high_value - low_value), 1)
            if value_available
            else None
        )
        summary_row[f"{outcome_key}_availability_note"] = (
            None if value_available else "Suppressed or unavailable"
        )

    return summary_row

def _build_row_group_order(summary_table: pd.DataFrame) -> pd.Series:
    ordered_row_groups = (
        summary_table.loc[:, ["row_group", "full_time_employment_gap"]]
        .sort_values(
            ["full_time_employment_gap", "row_group"],
            ascending=[False, True],
            kind="mergesort",
            na_position="last",
        )["row_group"]
        .tolist()
    )
    order_lookup = {
        row_group: order
        for order, row_group in enumerate(ordered_row_groups)
    }
    return summary_table["row_group"].map(order_lookup).astype("Int64")
