from __future__ import annotations

from typing import Optional

import pandas as pd

from src.constants.qilt import (
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

    return (row_group_key, row_label_key)


def select_qilt_ordered_pair_rows(
    group_table: pd.DataFrame,
    *,
    value_column: str,
) -> Optional[tuple[pd.Series, pd.Series]]:
    valid_rows = group_table.loc[
        group_table["row_label"].notna() & group_table[value_column].notna()
    ].copy()

    if len(valid_rows) < 2:
        return None

    row_group = clean_qilt_display_text(valid_rows["row_group"].iloc[0])
    valid_rows["row_label_order"] = valid_rows["row_label"].map(
        lambda value: _build_qilt_subgroup_order_key(row_group, value)
    )
    sorted_rows = valid_rows.sort_values(
        [value_column, "row_label_order"],
        kind="mergesort",
    )
    return (
        sorted_rows.iloc[0],
        sorted_rows.iloc[-1],
    )


def _build_qilt_subgroup_order_key(
    row_group: object,
    row_label: object,
) -> tuple[int, str]:
    row_group_text = clean_qilt_display_text(row_group)
    row_label_text = format_qilt_subgroup_label(row_label)
    if row_group_text is not None:
        ordered_labels = QILT_SUBGROUP_DISPLAY_ORDER_BY_ROW_GROUP.get(row_group_text, ())
    else:
        ordered_labels = ()
    label_order_lookup = {
        label: order
        for order, label in enumerate(ordered_labels)
    }
    default_order = len(label_order_lookup)
    key = row_label_text if row_label_text is not None else ""
    order = label_order_lookup.get(key, default_order)
    return (
        order,
        key,
    )
