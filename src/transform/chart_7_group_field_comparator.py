from __future__ import annotations

import pandas as pd

from src.preparation.qilt import clean_qilt_display_text
from src.transform.chart_helpers import (
    build_qilt_comparison_row,
    select_chart_table_schema,
)
from src.transform.constants import (
    CHART_7_CONSTANTS,
    GOS_2_SOURCE_KEY,
    GOS_8_SOURCE_KEY,
    GOS_L_6_SOURCE_KEY,
    GOS_L_160_SOURCE_KEY,
    GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS,
    GOS_SHORT_TERM_COMPARISON_COLUMNS,
    MEDIUM_TERM_TIME_WINDOW,
    SHORT_TERM_TIME_WINDOW,
    TOTAL_ROW_GROUP,
)
from src.transform.metadata import CHART_7_METADATA
from src.transform.qilt import (
    QILT_MEDIUM_TERM_VALUE_COLUMN,
    QILT_SHORT_TERM_VALUE_COLUMN,
    build_qilt_full_time_employment_comparison_table,
    build_qilt_subgroup_gap_sort_order,
    build_qilt_subgroup_id,
    select_qilt_subgroup_pair_rows,
)
from src.types import PreparedRows, QILTPreparedSheet

DISCIPLINE_DIMENSION = "Study area"
DISCIPLINE_TOTAL_LABEL = "All undergraduate fields"
NON_STUDY_AREA_ROWS = frozenset({TOTAL_ROW_GROUP, "Standard deviation"})


def build_chart_7_table(
    gos_sheet: QILTPreparedSheet,
    gos_l_sheet: QILTPreparedSheet,
    gos_area_sheet: QILTPreparedSheet,
    gos_l_area_sheet: QILTPreparedSheet,
) -> pd.DataFrame:
    demographic_table = _build_demographic_comparator_table(gos_sheet, gos_l_sheet)
    discipline_table = _build_discipline_comparator_table(
        gos_area_sheet,
        gos_l_area_sheet,
        sort_order_start=_next_sort_order(demographic_table),
    )
    chart_table = pd.concat(
        [demographic_table, discipline_table],
        ignore_index=True,
    )
    chart_table = chart_table.sort_values(
        ["sort_order", "time_window_order"],
        kind="mergesort",
    )
    chart_table = select_chart_table_schema(
        chart_table,
        CHART_7_CONSTANTS["table_columns"],
    )
    chart_table.attrs["chart_metadata"] = CHART_7_METADATA
    return chart_table


def _build_demographic_comparator_table(
    gos_sheet: QILTPreparedSheet,
    gos_l_sheet: QILTPreparedSheet,
) -> pd.DataFrame:
    comparison_table = build_qilt_full_time_employment_comparison_table(
        gos_sheet.table,
        gos_l_sheet.table,
        validate="one_to_one",
    )
    comparison_table["sort_order"] = build_qilt_subgroup_gap_sort_order(
        comparison_table,
        value_column=QILT_SHORT_TERM_VALUE_COLUMN,
    )
    summary_rows = [
        _build_comparator_rows(group_table)
        for _, group_table in comparison_table.groupby("subgroup_dimension", sort=False)
    ]
    chart_table = pd.DataFrame(row for group_rows in summary_rows for row in group_rows)
    chart_table = chart_table.sort_values(
        ["sort_order", "time_window_order"],
        kind="mergesort",
    )
    return chart_table


def _build_comparator_rows(group_table: pd.DataFrame) -> PreparedRows:
    subgroup_dimension = str(group_table["subgroup_dimension"].iloc[0])
    selector_id = build_qilt_subgroup_id(subgroup_dimension)
    sort_order = group_table["sort_order"].iloc[0]
    selected_pair = select_qilt_subgroup_pair_rows(
        group_table,
        value_column=QILT_SHORT_TERM_VALUE_COLUMN,
    )

    if selected_pair is None:
        return []

    low_row, high_row = selected_pair
    return [
        _build_chart_7_comparator_row(
            low_row,
            high_row,
            selector_id=selector_id,
            subgroup_dimension=subgroup_dimension,
            value_column=QILT_SHORT_TERM_VALUE_COLUMN,
            time_window=SHORT_TERM_TIME_WINDOW,
            time_window_order=0,
            source_key=GOS_8_SOURCE_KEY,
            sort_order=sort_order,
            comparison_kind="demographic",
        ),
        _build_chart_7_comparator_row(
            low_row,
            high_row,
            selector_id=selector_id,
            subgroup_dimension=subgroup_dimension,
            value_column=QILT_MEDIUM_TERM_VALUE_COLUMN,
            time_window=MEDIUM_TERM_TIME_WINDOW,
            time_window_order=1,
            source_key=GOS_L_160_SOURCE_KEY,
            sort_order=sort_order,
            comparison_kind="demographic",
        ),
    ]


def _build_chart_7_comparator_row(
    reference_row: pd.Series,
    comparison_row: pd.Series,
    *,
    selector_id: str,
    subgroup_dimension: str,
    value_column: str,
    time_window: str,
    time_window_order: int,
    source_key: str,
    sort_order: object,
    comparison_kind: str,
) -> dict[str, object]:
    comparison = build_qilt_comparison_row(
        reference_row,
        comparison_row,
        subgroup_dimension=subgroup_dimension,
        value_column=value_column,
        time_window=time_window,
        time_window_order=time_window_order,
        source_key=source_key,
    )
    comparison["selector_id"] = selector_id
    comparison["sort_order"] = sort_order
    comparison["comparison_kind"] = comparison_kind
    return comparison


def _build_discipline_comparator_table(
    gos_area_sheet: QILTPreparedSheet,
    gos_l_area_sheet: QILTPreparedSheet,
    *,
    sort_order_start: int,
) -> pd.DataFrame:
    short_table = _normalise_discipline_full_time_employment_table(
        gos_area_sheet.table,
        source_column=GOS_SHORT_TERM_COMPARISON_COLUMNS[
            "short_term_full_time_employment"
        ],
        value_column=QILT_SHORT_TERM_VALUE_COLUMN,
    )
    medium_table = _normalise_discipline_full_time_employment_table(
        gos_l_area_sheet.table,
        source_column=GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS[
            "medium_term_full_time_employment"
        ],
        value_column=QILT_MEDIUM_TERM_VALUE_COLUMN,
    )

    _raise_for_mismatched_discipline_areas(short_table, medium_table)
    short_total_row = _select_single_discipline_row(
        short_table,
        TOTAL_ROW_GROUP,
        source_key=GOS_2_SOURCE_KEY,
    )
    medium_total_row = _select_single_discipline_row(
        medium_table,
        TOTAL_ROW_GROUP,
        source_key=GOS_L_6_SOURCE_KEY,
    )
    study_areas = _select_study_areas(short_table)
    ordered_study_areas = _sort_study_areas_by_short_term_gap(
        short_table,
        short_total_row,
        study_areas,
    )

    summary_rows = [
        _build_discipline_comparator_rows(
            study_area,
            short_table,
            medium_table,
            short_total_row,
            medium_total_row,
            sort_order=sort_order_start + sort_offset,
        )
        for sort_offset, study_area in enumerate(ordered_study_areas)
    ]
    return pd.DataFrame(row for group_rows in summary_rows for row in group_rows)


def _normalise_discipline_full_time_employment_table(
    table: pd.DataFrame,
    *,
    source_column: str,
    value_column: str,
) -> pd.DataFrame:
    prepared_rows: PreparedRows = []

    for _, row in table.iterrows():
        study_area = clean_qilt_display_text(row["area"])
        if study_area is None:
            continue

        row_label = (
            DISCIPLINE_TOTAL_LABEL
            if study_area == TOTAL_ROW_GROUP
            else study_area
        )
        prepared_rows.append(
            {
                "study_area": study_area,
                "row_label": row_label,
                value_column: row[source_column],
            }
        )

    return pd.DataFrame(prepared_rows)


def _raise_for_mismatched_discipline_areas(
    short_table: pd.DataFrame,
    medium_table: pd.DataFrame,
) -> None:
    short_areas = set(short_table["study_area"].tolist())
    medium_areas = set(medium_table["study_area"].tolist())

    if short_areas == medium_areas:
        return

    raise ValueError(
        "Chart 7 discipline study-area labels do not align between "
        f"{GOS_2_SOURCE_KEY!r} and {GOS_L_6_SOURCE_KEY!r}; "
        f"only in short-term source: {sorted(short_areas - medium_areas)}; "
        f"only in medium-term source: {sorted(medium_areas - short_areas)}."
    )


def _select_single_discipline_row(
    table: pd.DataFrame,
    study_area: str,
    *,
    source_key: str,
) -> pd.Series:
    matching_rows = table.loc[table["study_area"] == study_area]

    if len(matching_rows) != 1:
        raise ValueError(
            f"Cannot find exactly one Chart 7 discipline row for "
            f"{study_area!r} in {source_key!r}."
        )

    return matching_rows.iloc[0]


def _select_study_areas(table: pd.DataFrame) -> list[str]:
    study_areas = [
        study_area
        for study_area in table["study_area"].tolist()
        if study_area not in NON_STUDY_AREA_ROWS
    ]

    if not study_areas:
        raise ValueError("No Chart 7 discipline study areas were found.")

    return study_areas


def _sort_study_areas_by_short_term_gap(
    short_table: pd.DataFrame,
    short_total_row: pd.Series,
    study_areas: list[str],
) -> list[str]:
    gap_rows = []

    for study_area in study_areas:
        short_study_row = _select_single_discipline_row(
            short_table,
            study_area,
            source_key=GOS_2_SOURCE_KEY,
        )
        _raise_for_missing_discipline_values(
            short_study_row,
            short_total_row,
            value_column=QILT_SHORT_TERM_VALUE_COLUMN,
            study_area=study_area,
        )
        short_gap = abs(
            float(
                short_study_row[QILT_SHORT_TERM_VALUE_COLUMN]
                - short_total_row[QILT_SHORT_TERM_VALUE_COLUMN]
            )
        )
        gap_rows.append({"study_area": study_area, "gap_pp": short_gap})

    gap_table = pd.DataFrame(gap_rows)
    return (
        gap_table.sort_values(
            ["gap_pp", "study_area"],
            ascending=[False, True],
            kind="mergesort",
        )["study_area"]
        .tolist()
    )


def _build_discipline_comparator_rows(
    study_area: str,
    short_table: pd.DataFrame,
    medium_table: pd.DataFrame,
    short_total_row: pd.Series,
    medium_total_row: pd.Series,
    *,
    sort_order: int,
) -> PreparedRows:
    short_study_row = _select_single_discipline_row(
        short_table,
        study_area,
        source_key=GOS_2_SOURCE_KEY,
    )
    medium_study_row = _select_single_discipline_row(
        medium_table,
        study_area,
        source_key=GOS_L_6_SOURCE_KEY,
    )
    _raise_for_missing_discipline_values(
        short_study_row,
        short_total_row,
        value_column=QILT_SHORT_TERM_VALUE_COLUMN,
        study_area=study_area,
    )
    _raise_for_missing_discipline_values(
        medium_study_row,
        medium_total_row,
        value_column=QILT_MEDIUM_TERM_VALUE_COLUMN,
        study_area=study_area,
    )

    if (
        short_study_row[QILT_SHORT_TERM_VALUE_COLUMN]
        <= short_total_row[QILT_SHORT_TERM_VALUE_COLUMN]
    ):
        short_reference_row = short_study_row
        short_comparison_row = short_total_row
        medium_reference_row = medium_study_row
        medium_comparison_row = medium_total_row
    else:
        short_reference_row = short_total_row
        short_comparison_row = short_study_row
        medium_reference_row = medium_total_row
        medium_comparison_row = medium_study_row

    selector_id = build_qilt_subgroup_id(f"{DISCIPLINE_DIMENSION} {study_area}")
    return [
        _build_chart_7_comparator_row(
            short_reference_row,
            short_comparison_row,
            selector_id=selector_id,
            subgroup_dimension=DISCIPLINE_DIMENSION,
            value_column=QILT_SHORT_TERM_VALUE_COLUMN,
            time_window=SHORT_TERM_TIME_WINDOW,
            time_window_order=0,
            source_key=GOS_2_SOURCE_KEY,
            sort_order=sort_order,
            comparison_kind="discipline",
        ),
        _build_chart_7_comparator_row(
            medium_reference_row,
            medium_comparison_row,
            selector_id=selector_id,
            subgroup_dimension=DISCIPLINE_DIMENSION,
            value_column=QILT_MEDIUM_TERM_VALUE_COLUMN,
            time_window=MEDIUM_TERM_TIME_WINDOW,
            time_window_order=1,
            source_key=GOS_L_6_SOURCE_KEY,
            sort_order=sort_order,
            comparison_kind="discipline",
        ),
    ]


def _raise_for_missing_discipline_values(
    study_area_row: pd.Series,
    total_row: pd.Series,
    *,
    value_column: str,
    study_area: str,
) -> None:
    missing_labels = [
        row["row_label"]
        for row in (study_area_row, total_row)
        if pd.isna(row[value_column])
    ]

    if missing_labels:
        raise ValueError(
            f"Missing Chart 7 discipline {value_column!r} values for "
            f"{study_area!r}: {missing_labels}."
        )


def _next_sort_order(table: pd.DataFrame) -> int:
    if table.empty:
        return 0

    return int(table["sort_order"].max()) + 1
