from __future__ import annotations

import re
from typing import Optional

import pandas as pd

from src.transform.constants import (
    GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS,
    GOS_SHORT_TERM_COMPARISON_COLUMNS,
    QILT_SUBGROUP_DISPLAY_ORDER_BY_ROW_GROUP,
    QILT_SUBGROUP_TEXT_EQUIVALENTS,
    TOTAL_ROW_GROUP,
)
from src.preparation.qilt import clean_qilt_display_text, normalise_qilt_key_text
from src.preparation.series import is_missing_value
from src.types import PreparedRows, QILTValidationComparison

QILT_SHORT_TERM_VALUE_COLUMN = "short_term_value_pct"
QILT_MEDIUM_TERM_VALUE_COLUMN = "medium_term_value_pct"


def build_qilt_full_time_employment_comparison_table(
    gos_table: pd.DataFrame,
    gos_l_table: pd.DataFrame,
    *,
    validate: Optional[QILTValidationComparison] = None,
    how: str = "inner",
) -> pd.DataFrame:
    short_table = _normalise_short_term_full_time_employment_table(gos_table)
    medium_table = _normalise_medium_term_full_time_employment_table(gos_l_table)

    if validate is None:
        return short_table.merge(
            medium_table,
            on="subgroup_key",
            how=how,
            sort=False,
        )

    return short_table.merge(
        medium_table,
        on="subgroup_key",
        how=how,
        sort=False,
        validate=validate,
    )


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


def build_qilt_subgroup_id(subgroup_dimension: object) -> str:
    key_text = normalise_qilt_key_text(subgroup_dimension)
    if key_text is None:
        return "unknown"

    return re.sub(r"[^a-z0-9]+", "_", key_text).strip("_")


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


def select_qilt_subgroup_pair_rows(
    group_table: pd.DataFrame,
    *,
    value_column: str,
) -> Optional[tuple[pd.Series, pd.Series]]:
    selection_table = group_table
    if "row_group" not in selection_table.columns:
        selection_table = selection_table.rename(
            columns={"subgroup_dimension": "row_group"},
        )

    return select_qilt_ordered_pair_rows(selection_table, value_column=value_column)


def calculate_qilt_gap(
    extremes: Optional[tuple[pd.Series, pd.Series]],
    value_column: str,
) -> Optional[float]:
    if extremes is None:
        return None

    low_row, high_row = extremes
    low_value = low_row[value_column]
    high_value = high_row[value_column]

    if is_missing_value(low_value) or is_missing_value(high_value):
        return None

    return round(float(high_value - low_value), 1)


def build_qilt_comparison_label(
    first_group: object,
    second_group: object,
) -> Optional[str]:
    first_label = format_qilt_subgroup_label(first_group)
    second_label = format_qilt_subgroup_label(second_group)

    if first_label is None or second_label is None:
        return None

    return f"{first_label} vs {second_label}"


def build_qilt_subgroup_pair_summary(
    group_table: pd.DataFrame,
    *,
    value_column: str,
) -> dict[str, object]:
    selected_pair = select_qilt_subgroup_pair_rows(
        group_table,
        value_column=value_column,
    )

    if selected_pair is None:
        return {
            "comparison_label": None,
            "lower_group": None,
            "lower_group_pct": None,
            "higher_group": None,
            "higher_group_pct": None,
            "gap_pp": None,
        }

    low_row, high_row = selected_pair
    low_value = low_row[value_column]
    high_value = high_row[value_column]
    value_available = pd.notna(low_value) and pd.notna(high_value)

    return {
        "comparison_label": build_qilt_comparison_label(
            low_row["row_label"],
            high_row["row_label"],
        ),
        "lower_group": format_qilt_subgroup_label(low_row["row_label"]),
        "lower_group_pct": low_value if value_available else None,
        "higher_group": format_qilt_subgroup_label(high_row["row_label"]),
        "higher_group_pct": high_value if value_available else None,
        "gap_pp": round(float(high_value - low_value), 1) if value_available else None,
    }


def build_qilt_gap_sort_order(
    table: pd.DataFrame,
    *,
    gap_table: Optional[pd.DataFrame] = None,
    subgroup_column: str = "subgroup_dimension",
    gap_column: str = "gap_pp",
) -> pd.Series:
    order_source = table if gap_table is None else gap_table
    ordered_dimensions = (
        order_source.loc[:, [subgroup_column, gap_column]]
        .sort_values(
            [gap_column, subgroup_column],
            ascending=[False, True],
            kind="mergesort",
            na_position="last",
        )[subgroup_column]
        .tolist()
    )
    order_lookup = {
        subgroup_dimension: order
        for order, subgroup_dimension in enumerate(ordered_dimensions)
    }
    return pd.Series(
        [
            order_lookup.get(subgroup_dimension)
            for subgroup_dimension in table[subgroup_column]
        ],
        index=table.index,
        dtype="Int64",
    )


def build_qilt_subgroup_gap_sort_order(
    table: pd.DataFrame,
    *,
    value_column: str,
) -> pd.Series:
    gap_rows = [
        {
            "subgroup_dimension": subgroup_dimension,
            "gap_pp": calculate_qilt_gap(
                select_qilt_subgroup_pair_rows(group_table, value_column=value_column),
                value_column,
            ),
        }
        for subgroup_dimension, group_table in table.groupby(
            "subgroup_dimension",
            sort=False,
        )
    ]
    return build_qilt_gap_sort_order(table, gap_table=pd.DataFrame(gap_rows))


def _normalise_short_term_full_time_employment_table(
    gos_table: pd.DataFrame,
) -> pd.DataFrame:
    return _normalise_full_time_employment_table(
        gos_table,
        source_column=GOS_SHORT_TERM_COMPARISON_COLUMNS[
            "short_term_full_time_employment"
        ],
        value_column=QILT_SHORT_TERM_VALUE_COLUMN,
        include_labels=True,
    )


def _normalise_medium_term_full_time_employment_table(
    gos_l_table: pd.DataFrame,
) -> pd.DataFrame:
    return _normalise_full_time_employment_table(
        gos_l_table,
        source_column=GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS[
            "medium_term_full_time_employment"
        ],
        value_column=QILT_MEDIUM_TERM_VALUE_COLUMN,
        include_labels=False,
    )


def _normalise_full_time_employment_table(
    table: pd.DataFrame,
    *,
    source_column: str,
    value_column: str,
    include_labels: bool,
) -> pd.DataFrame:
    prepared_rows: PreparedRows = []

    for _, row in table.iterrows():
        row_group = clean_qilt_display_text(row["row_group"])
        row_label = clean_qilt_display_text(row["row_label"])

        if row_group is None or row_group == TOTAL_ROW_GROUP:
            continue

        prepared_row = {
            "subgroup_key": make_qilt_subgroup_key(row_group, row_label),
            value_column: row[source_column],
        }
        if include_labels:
            prepared_row.update(
                {
                    "subgroup_dimension": row_group,
                    "row_label": row_label,
                }
            )

        prepared_rows.append(prepared_row)

    return pd.DataFrame(prepared_rows)


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

    return {label: order for order, label in enumerate(ordered_labels)}
