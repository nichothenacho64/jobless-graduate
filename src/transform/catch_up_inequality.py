from __future__ import annotations

from collections.abc import Iterable, Mapping
import pandas as pd

from src.constants.qilt import (
    GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS,
    GOS_SHORT_TERM_COMPARISON_COLUMNS,
    QILT_SHORT_MEDIUM_OUTCOME_SPECS,
    TOTAL_ROW_GROUP,
)
from src.preparation.qilt import clean_qilt_display_text
from src.transform.qilt import (
    build_qilt_pair_label,
    make_qilt_subgroup_key,
    select_qilt_ordered_pair_rows,
)
from src.types import MetricComparison


def build_catch_up_levels_table(
    gos_table: pd.DataFrame,
    gos_l_table: pd.DataFrame,
    *,
    include_total: bool = False,
) -> pd.DataFrame:
    metric_comparisons = _pair_metric_columns(
        GOS_SHORT_TERM_COMPARISON_COLUMNS,
        GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS,
    )

    prepared_gos_table = _normalise_subgroup_table_for_comparison(
        gos_table,
        metric_columns=GOS_SHORT_TERM_COMPARISON_COLUMNS,
    )
    prepared_gos_l_table = _normalise_subgroup_table_for_comparison(
        gos_l_table,
        metric_columns=GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS,
    )

    comparison_table = prepared_gos_table.merge(
        prepared_gos_l_table[
            [
                "subgroup_key",
                *[
                    metric_comparison.medium_term_column
                    for metric_comparison in metric_comparisons
                ],
            ]
        ],
        on="subgroup_key",
        how="inner",
        sort=False,
    )

    _append_change_columns(
        comparison_table,
        metric_comparisons=metric_comparisons,
    )

    if not include_total:
        comparison_table = _exclude_total_subgroup_rows(comparison_table)

    final_columns = _get_comparison_output_columns(metric_comparisons)
    final_table = comparison_table.loc[:, final_columns].copy()
    return final_table.reset_index(drop=True)


def build_catch_up_gap_width_table(levels_table: pd.DataFrame) -> pd.DataFrame:
    summary_rows: list[dict[str, object]] = []

    for row_group, group_table in levels_table.groupby("row_group", sort=False):
        for outcome_key, short_column, medium_column in QILT_SHORT_MEDIUM_OUTCOME_SPECS:
            short_term_extremes = select_qilt_ordered_pair_rows(
                group_table,
                value_column=short_column,
            )
            medium_term_extremes = select_qilt_ordered_pair_rows(
                group_table,
                value_column=medium_column,
            )

            if short_term_extremes is None or medium_term_extremes is None:
                summary_rows.append(
                    {
                        "row_group": row_group,
                        "outcome_key": outcome_key,
                        "short_term_gap": None,
                        "medium_term_gap": None,
                        "gap_closure": None,
                        "short_term_low_label": None,
                        "short_term_high_label": None,
                        "medium_term_low_label": None,
                        "medium_term_high_label": None,
                    }
                )
                continue

            short_term_low_row, short_term_high_row = short_term_extremes
            medium_term_low_row, medium_term_high_row = medium_term_extremes

            short_gap = float(
                short_term_high_row[short_column] - short_term_low_row[short_column]
            )
            medium_gap = float(
                medium_term_high_row[medium_column] - medium_term_low_row[medium_column]
            )

            summary_rows.append(
                {
                    "row_group": row_group,
                    "outcome_key": outcome_key,
                    "short_term_gap": round(short_gap, 1),
                    "medium_term_gap": round(medium_gap, 1),
                    "gap_closure": round(short_gap - medium_gap, 1),
                    "short_term_low_label": short_term_low_row["row_label"],
                    "short_term_high_label": short_term_high_row["row_label"],
                    "medium_term_low_label": medium_term_low_row["row_label"],
                    "medium_term_high_label": medium_term_high_row["row_label"],
                }
            )

    summary_table = pd.DataFrame(summary_rows)
    summary_table["row_group_order"] = _build_gap_width_row_group_order(summary_table)
    outcome_order_lookup = {
        outcome_key: order
        for order, (outcome_key, _, _) in enumerate(QILT_SHORT_MEDIUM_OUTCOME_SPECS)
    }
    summary_table["outcome_order"] = summary_table["outcome_key"].map(
        outcome_order_lookup
    )
    summary_table = summary_table.sort_values(
        ["row_group_order", "outcome_order"],
        kind="mergesort",
    ).reset_index(drop=True)

    full_time_labels = (
        summary_table.loc[
            summary_table["outcome_key"] == "full_time_employment",
            [
                "row_group",
                "short_term_low_label",
                "short_term_high_label",
            ],
        ]
        .rename(
            columns={
                "short_term_low_label": "reference_low_label",
                "short_term_high_label": "reference_high_label",
            }
        )
        .assign(
            pair_label=lambda table: pd.Series(
                [
                    build_qilt_pair_label(low_label, high_label)
                    for low_label, high_label in zip(
                        table["reference_low_label"],
                        table["reference_high_label"],
                    )
                ],
                index=table.index,
            )
        )
        .reset_index(drop=True)
    )

    return summary_table.merge(
        full_time_labels,
        on="row_group",
        how="left",
        sort=False,
    ).drop(columns="outcome_order")


def _pair_metric_columns(
    short_term_metric_columns: Mapping[str, str],
    medium_term_metric_columns: Mapping[str, str],
) -> list[MetricComparison]:
    short_term_columns_by_metric = _index_columns_by_metric_name(
        short_term_metric_columns.keys(),
        expected_prefix="short_term_",
    )
    medium_term_columns_by_metric = _index_columns_by_metric_name(
        medium_term_metric_columns.keys(),
        expected_prefix="medium_term_",
    )

    if tuple(short_term_columns_by_metric) != tuple(medium_term_columns_by_metric):
        raise ValueError("Short-term and medium-term comparison columns do not align.")

    return [
        MetricComparison(
            metric_key=metric_key,
            short_term_column=short_term_column,
            medium_term_column=medium_term_columns_by_metric[metric_key],
        )
        for metric_key, short_term_column in short_term_columns_by_metric.items()
    ]


def _index_columns_by_metric_name(
    columns: Iterable[str],
    *,
    expected_prefix: str,
) -> dict[str, str]:
    grouped_columns: dict[str, str] = {}

    for column in columns:
        if not column.startswith(expected_prefix):
            raise ValueError(
                f"Comparison column {column!r} does not start with {expected_prefix!r}."
            )

        metric_name = column.removeprefix(expected_prefix)
        grouped_columns[metric_name] = column

    return grouped_columns


def _append_change_columns(
    table: pd.DataFrame,
    *,
    metric_comparisons: list[MetricComparison],
) -> None:
    for metric_comparison in metric_comparisons:
        table[metric_comparison.change_column] = (
            table[metric_comparison.medium_term_column]
            - table[metric_comparison.short_term_column]
        ).round(1)


def _exclude_total_subgroup_rows(table: pd.DataFrame) -> pd.DataFrame:
    return table.loc[table["row_group"] != TOTAL_ROW_GROUP].copy()


def _get_comparison_output_columns(
    metric_comparisons: list[MetricComparison],
) -> list[str]:
    final_columns = ["row_group", "row_label"]

    for metric_comparison in metric_comparisons:
        final_columns.extend(
            [
                metric_comparison.short_term_column,
                metric_comparison.medium_term_column,
                metric_comparison.change_column,
            ]
        )

    return final_columns


def _normalise_subgroup_table_for_comparison(
    table: pd.DataFrame,
    *,
    metric_columns: Mapping[str, str],
) -> pd.DataFrame:
    prepared_rows: list[dict[str, object]] = []

    for _, row in table.iterrows():
        row_group = clean_qilt_display_text(row["row_group"])
        row_label = clean_qilt_display_text(row["row_label"])
        subgroup_key = make_qilt_subgroup_key(row_group, row_label)

        prepared_row: dict[str, object] = {
            "row_group": row_group,
            "row_label": row_label,
            "subgroup_key": subgroup_key,
        }

        for output_column, source_column in metric_columns.items():
            prepared_row[output_column] = row[source_column]

        prepared_rows.append(prepared_row)

    return pd.DataFrame(prepared_rows)


def _build_gap_width_row_group_order(summary_table: pd.DataFrame) -> pd.Series:
    ordered_row_groups = (
        summary_table.loc[
            summary_table["outcome_key"] == "full_time_employment",
            ["row_group", "short_term_gap"],
        ]
        .sort_values(
            ["short_term_gap", "row_group"],
            ascending=[False, True],
            kind="mergesort",
            na_position="last",
        )["row_group"]
        .tolist()
    )
    order_lookup = {
        row_group: order for order, row_group in enumerate(ordered_row_groups)
    }
    return summary_table["row_group"].map(order_lookup).astype("Int64")
