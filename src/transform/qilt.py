from __future__ import annotations

from typing import Optional

import pandas as pd

from src.transform.constants import (
    QILT_SUBGROUP_DISPLAY_ORDER_BY_ROW_GROUP,
    QILT_SUBGROUP_TEXT_EQUIVALENTS,
)
from src.preparation.qilt import clean_qilt_display_text, normalise_qilt_key_text

def build_qilt_pair_label(
    low_label: object,
    high_label: object,
) -> Optional[str]:
    low_text = format_qilt_subgroup_label(low_label)
    high_text = format_qilt_subgroup_label(high_label)

    if low_text is None or high_text is None:
        return None

    return f"{low_text} vs {high_text}"

def format_qilt_subgroup_label(value: object) -> Optional[str]:
    text = clean_qilt_display_text(value)

    if text is None:
        return None

    return QILT_SUBGROUP_TEXT_EQUIVALENTS.get(text, text)

def make_qilt_subgroup_key(
    row_group: object,
    row_label: object,
) -> Optional[tuple[str, str]]:
    row_group_key = normalise_qilt_key_text(row_group)
    row_label_key = normalise_qilt_key_text(row_label)

    if row_group_key is None or row_label_key is None:
        return None

    return row_group_key, row_label_key

def select_qilt_ordered_pair_rows(
    group_table: pd.DataFrame,
    *,
    value_column: str,
) -> Optional[tuple[pd.Series, pd.Series]]:
    has_row_label = group_table["row_label"].notna()
    has_value = group_table[value_column].notna()

    valid_rows = group_table.loc[has_row_label & has_value].copy()

    if len(valid_rows) < 2:
        return None

    row_group = valid_rows["row_group"].iloc[0]
    valid_rows["row_label_order"] = [
        _build_qilt_subgroup_order_key(
            row_group=row_group,
            row_label=row_label,
        )
        for row_label in valid_rows["row_label"]
    ]

    sorted_rows = valid_rows.sort_values(
        by=[value_column, "row_label_order"],
        kind="mergesort",
    )

    lowest_row = sorted_rows.iloc[0]
    highest_row = sorted_rows.iloc[-1]
    return lowest_row, highest_row

def _build_qilt_subgroup_order_key(
    row_group: object,
    row_label: object,
) -> tuple[int, str]:
    row_group_text = clean_qilt_display_text(row_group)
    row_label_text = format_qilt_subgroup_label(row_label)

    label_order_lookup = _build_qilt_subgroup_label_order_lookup(row_group_text)

    label_key = row_label_text or ""
    default_order = len(label_order_lookup)
    label_order = label_order_lookup.get(label_key, default_order)

    return label_order, label_key

def _build_qilt_subgroup_label_order_lookup(
    row_group_text: Optional[str],
) -> dict[str, int]:
    if row_group_text is None:
        return {}

    ordered_labels = QILT_SUBGROUP_DISPLAY_ORDER_BY_ROW_GROUP.get(
        row_group_text,
        (),
    )

    return {
        label: order
        for order, label in enumerate(ordered_labels)
    }
