from __future__ import annotations

from collections.abc import Mapping, Sequence

import pandas as pd

from src.transform.constants import DISCIPLINE_FAMILY_CONSTANTS
from src.transform.qilt import format_qilt_subgroup_label


def select_chart_table_schema(
    table: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    expected_columns = list(columns)
    missing_columns = [
        column for column in expected_columns if column not in table.columns
    ]
    extra_columns = [
        column for column in table.columns if column not in expected_columns
    ]

    if missing_columns or extra_columns:
        message_parts: list[str] = []
        if missing_columns:
            message_parts.append(f"missing columns: {missing_columns}")
        if extra_columns:
            message_parts.append(f"unexpected columns: {extra_columns}")

        raise ValueError("Chart table schema mismatch; " + "; ".join(message_parts))

    return table.loc[:, expected_columns].reset_index(drop=True)


def build_qilt_comparison_row(
    reference_row: pd.Series,
    comparison_row: pd.Series,
    *,
    subgroup_dimension: str,
    value_column: str,
    time_window: str,
    time_window_order: int,
    source_key: str,
) -> dict[str, object]:
    reference_value = reference_row[value_column]
    comparison_value = comparison_row[value_column]

    return {
        "subgroup_dimension": subgroup_dimension,
        "time_window": time_window,
        "time_window_order": time_window_order,
        "reference_group": format_qilt_subgroup_label(reference_row["row_label"]),
        "reference_group_pct": reference_value,
        "comparison_group": format_qilt_subgroup_label(comparison_row["row_label"]),
        "comparison_group_pct": comparison_value,
        "signed_gap_pp": round(float(comparison_value - reference_value), 1),
        "source_key": source_key,
    }


def add_discipline_family_colour_fields(
    table: pd.DataFrame,
    colour_measure_columns: Sequence[str],
) -> pd.DataFrame:
    chart_table = add_discipline_family(table)
    colour_key_by_family = build_family_colour_key_by_family(
        chart_table,
        colour_measure_columns,
    )
    return add_family_colour_key(chart_table, colour_key_by_family)


def add_discipline_family(table: pd.DataFrame) -> pd.DataFrame:
    if "study_area" not in table.columns:
        raise ValueError(
            "Cannot add discipline-family fields; missing columns: ['study_area']"
        )

    family_by_study_area = _build_discipline_family_lookup()
    study_areas = list(dict.fromkeys(table["study_area"].tolist()))
    missing_study_areas = [
        study_area
        for study_area in study_areas
        if study_area not in family_by_study_area
    ]
    if missing_study_areas:
        raise ValueError(
            "Cannot add discipline-family fields; "
            "unmapped study_area values: "
            f"{missing_study_areas}"
        )

    chart_table = table.copy()
    chart_table["discipline_family"] = chart_table["study_area"].map(
        family_by_study_area
    )
    return chart_table


def build_family_colour_key_by_family(
    table: pd.DataFrame,
    colour_measure_columns: Sequence[str],
) -> dict[str, str]:
    colour_columns = list(colour_measure_columns)
    required_columns = ["discipline_family", *colour_columns]
    missing_columns = [
        column for column in required_columns if column not in table.columns
    ]
    if missing_columns:
        raise ValueError(
            "Cannot build discipline-family colour keys; "
            f"missing columns: {missing_columns}"
        )

    chart_table = table.copy()
    row_scores = chart_table.loc[:, colour_columns].mean(axis="columns")
    family_scores = row_scores.groupby(chart_table["discipline_family"]).mean()
    return _rank_family_colour_keys(family_scores)


def add_family_colour_key(
    table: pd.DataFrame,
    family_colour_key_by_family: Mapping[str, str],
) -> pd.DataFrame:
    if "discipline_family" not in table.columns:
        raise ValueError(
            "Cannot add discipline-family colour key; "
            "missing columns: ['discipline_family']"
        )

    families = list(dict.fromkeys(table["discipline_family"].tolist()))
    missing_families = [
        family for family in families if family not in family_colour_key_by_family
    ]
    if missing_families:
        raise ValueError(
            "Cannot add discipline-family colour key; "
            f"missing colour keys for families: {missing_families}"
        )

    chart_table = table.copy()
    chart_table["family_colour_key"] = chart_table["discipline_family"].map(
        family_colour_key_by_family
    )
    return chart_table


def _build_discipline_family_lookup() -> dict[str, str]:
    family_by_study_area: dict[str, str] = {}

    for family, study_areas in DISCIPLINE_FAMILY_CONSTANTS["families"].items():
        for study_area in study_areas:
            if study_area in family_by_study_area:
                existing_family = family_by_study_area[study_area]
                raise ValueError(
                    "Duplicate study_area in discipline family mapping: "
                    f"{study_area!r} belongs to both "
                    f"{existing_family!r} and {family!r}."
                )

            family_by_study_area[study_area] = family

    return family_by_study_area


def _rank_family_colour_keys(family_scores: pd.Series) -> dict[str, str]:
    if family_scores.isna().any():
        families = family_scores[family_scores.isna()].index.tolist()
        raise ValueError(
            "Cannot rank discipline-family colour fields; "
            f"missing family scores for: {families}"
        )

    family_order = {
        family: family_index
        for family_index, family in enumerate(
            DISCIPLINE_FAMILY_CONSTANTS["families"].keys()
        )
    }
    ranked_families = sorted(
        family_scores.index.tolist(),
        key=lambda family: (-family_scores[family], family_order[family]),
    )

    colour_key_by_family: dict[str, str] = {}
    for rank, family in enumerate(ranked_families, start=1):
        try:
            colour_key_by_family[family] = DISCIPLINE_FAMILY_CONSTANTS[
                "colour_keys_by_rank"
            ][rank]
        except KeyError:
            raise ValueError(
                "Missing family colour key for discipline-family rank "
                f"{rank}."
            ) from None

    return colour_key_by_family
