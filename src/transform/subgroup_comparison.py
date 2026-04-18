from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Optional

import pandas as pd

from src.constants.project import (
    QILT_2024_GOS_L_SOURCE,
    QILT_2024_GOS_SOURCE,
    QILT_FOLDER_NAME,
)
from src.constants.qilt import (
    GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS,
    GOS_L_SUBGROUP_SHEET_NAME,
    GOS_SHORT_TERM_COMPARISON_COLUMNS,
    GOS_SUBGROUP_SHEET_NAME,
    SUBGROUP_LONG_OUTCOME_SPECS,
    TOTAL_ROW_GROUP,
)
from src.preparation.qilt import (
    clean_qilt_display_text,
    normalise_qilt_key_text,
    prepare_qilt_sheet,
)
from src.types import ExcelSheet, MetricComparison

def load_subgroup_comparison_table(*, include_total: bool = True) -> pd.DataFrame:
    gos_sheet = ExcelSheet(
        folder=QILT_FOLDER_NAME,
        data_source=QILT_2024_GOS_SOURCE,
        sheet_name=GOS_SUBGROUP_SHEET_NAME,
    )
    gos_l_sheet = ExcelSheet(
        folder=QILT_FOLDER_NAME,
        data_source=QILT_2024_GOS_L_SOURCE,
        sheet_name=GOS_L_SUBGROUP_SHEET_NAME,
    )

    gos_table = prepare_qilt_sheet(
        gos_sheet.folder,
        gos_sheet.file_name,
        gos_sheet.sheet_name,
    ).table
    gos_l_table = prepare_qilt_sheet(
        gos_l_sheet.folder,
        gos_l_sheet.file_name,
        gos_l_sheet.sheet_name,
    ).table

    return build_subgroup_comparison_table_from_tables(
        gos_table,
        gos_l_table,
        include_total=include_total,
    )

def build_subgroup_comparison_table_from_tables(
    gos_table: pd.DataFrame,
    gos_l_table: pd.DataFrame,
    *,
    include_total: bool = True,
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

def build_subgroup_chart_table(
    comparison_table: pd.DataFrame,
    *,
    include_total: bool = False,
) -> pd.DataFrame:
    chart_table = comparison_table.copy()

    if not include_total:
        chart_table = chart_table.loc[
            chart_table["row_group"] != TOTAL_ROW_GROUP
        ].reset_index(drop=True)

    chart_table["chart_label"] = _format_subgroup_chart_labels(chart_table)
    return chart_table

def build_subgroup_gap_summary_table(chart_table: pd.DataFrame) -> pd.DataFrame:
    summary_rows: list[dict[str, object]] = []

    for row_group, group_table in chart_table.groupby("row_group", sort=False):
        for outcome_key, short_column, medium_column, _ in SUBGROUP_LONG_OUTCOME_SPECS:
            short_gap = float(
                group_table[short_column].max() - group_table[short_column].min()
            )
            medium_gap = float(
                group_table[medium_column].max() - group_table[medium_column].min()
            )

            summary_rows.append(
                {
                    "row_group": row_group,
                    "outcome_key": outcome_key,
                    "short_term_gap": round(short_gap, 1),
                    "medium_term_gap": round(medium_gap, 1),
                }
            )

    return pd.DataFrame(summary_rows)

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

def _format_subgroup_chart_labels(chart_table: pd.DataFrame) -> list[str]:
    labels: list[str] = []
    previous_group: str | None = None

    for _, row in chart_table.iterrows():
        row_group = str(row["row_group"])
        row_label = str(row["row_label"])

        if row_group != previous_group:
            labels.append(f"{row_group}: {row_label}")
            previous_group = row_group
            continue

        labels.append(f"  {row_label}")

    return labels

def _normalise_subgroup_table_for_comparison(
    table: pd.DataFrame,
    *,
    metric_columns: Mapping[str, str],
) -> pd.DataFrame:
    prepared_rows: list[dict[str, object]] = []

    for _, row in table.iterrows():
        row_group = clean_qilt_display_text(row["row_group"])
        row_label = clean_qilt_display_text(row["row_label"])
        subgroup_key = _make_subgroup_key(row_group, row_label)

        prepared_row: dict[str, object] = {
            "row_group": row_group,
            "row_label": row_label,
            "subgroup_key": subgroup_key,
        }

        for output_column, source_column in metric_columns.items():
            prepared_row[output_column] = row[source_column]

        prepared_rows.append(prepared_row)

    return pd.DataFrame(prepared_rows)

def _make_subgroup_key(row_group: object, row_label: object) -> Optional[tuple[str, str]]:
    row_group_key = normalise_qilt_key_text(row_group)
    row_label_key = normalise_qilt_key_text(row_label)

    if row_group_key is None or row_label_key is None:
        return None

    return (row_group_key, row_label_key)
