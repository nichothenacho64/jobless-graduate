from __future__ import annotations

from collections.abc import Mapping

import pandas as pd

from src.loaders import (
    initialise_abs_sheet,
    initialise_gos_l_sheet,
    initialise_gos_sheet,
)
from src.preparation.abs import prepare_abs_sheet
from src.preparation.qilt import prepare_qilt_sheet
from src.transform.chart_1a_degree_supply import build_chart_1a_table
from src.transform.chart_1b_skill_by_age import build_chart_1b_table
from src.transform.chart_2_transition_window import build_chart_2_table
from src.transform.chart_3_subgroup_bottleneck import build_chart_3_table
from src.transform.chart_4_gap_shapes import build_chart_4_table
from src.transform.chart_5_field_conversion import build_chart_5_table
from src.transform.chart_6_work_fit import build_chart_6_table
from src.transform.chart_7_group_field_comparator import build_chart_7_table
from src.transform.constants import (
    CHART_1A_ID,
    CHART_1B_ID,
    CHART_2_ID,
    CHART_3_ID,
    CHART_4_ID,
    CHART_5_ID,
    CHART_6_ID,
    CHART_7_ID,
    CHART_TABLE_IDS_BY_NUMBER,
    GOS_2_SOURCE_KEY,
    GOS_5_SOURCE_KEY,
    GOS_8_SOURCE_KEY,
    GOS_21_SOURCE_KEY,
    GOS_L_1_SOURCE_KEY,
    GOS_L_6_SOURCE_KEY,
    GOS_L_26_SOURCE_KEY,
    GOS_L_160_SOURCE_KEY,
    SEW_32_SOURCE_KEY,
    SEW_35_SOURCE_KEY,
)
from src.types import (
    ABSPreparedSheet,
    ExcelSheet,
    NumericValue,
    PreparedSheet,
    PreparedSheetType,
    QILTPreparedSheet,
    SheetPreparer,
)


def prepare_sheets(
    sheet_specs: Mapping[str, ExcelSheet],
    prepare_sheet: SheetPreparer,
) -> dict[str, PreparedSheetType]:
    return {
        source_key: prepare_sheet(sheet.folder, sheet.file_name, sheet.sheet_name)
        for source_key, sheet in sheet_specs.items()
    }


def prepare_all_sources() -> dict[str, PreparedSheetType]:
    qilt_sheet_specs = {
        GOS_21_SOURCE_KEY: initialise_gos_sheet(21),
        GOS_2_SOURCE_KEY: initialise_gos_sheet(2),
        GOS_5_SOURCE_KEY: initialise_gos_sheet(5),
        GOS_8_SOURCE_KEY: initialise_gos_sheet(8),
        GOS_L_1_SOURCE_KEY: initialise_gos_l_sheet(1),
        GOS_L_6_SOURCE_KEY: initialise_gos_l_sheet(6),
        GOS_L_26_SOURCE_KEY: initialise_gos_l_sheet(26),
        GOS_L_160_SOURCE_KEY: initialise_gos_l_sheet(160),
    }

    abs_sheet_specs = {
        SEW_32_SOURCE_KEY: initialise_abs_sheet(32),
        SEW_35_SOURCE_KEY: initialise_abs_sheet(35),
    }

    prepared_qilt_sheets = prepare_sheets(qilt_sheet_specs, prepare_qilt_sheet)
    prepared_abs_sheets = prepare_sheets(abs_sheet_specs, prepare_abs_sheet)
    return {**prepared_qilt_sheets, **prepared_abs_sheets}


def build_chart_tables(
    prepared_sources: Mapping[str, PreparedSheetType],
) -> dict[str, pd.DataFrame]:
    gos_21 = _get_sheet_source(prepared_sources, GOS_21_SOURCE_KEY, QILTPreparedSheet)
    gos_2 = _get_sheet_source(prepared_sources, GOS_2_SOURCE_KEY, QILTPreparedSheet)
    gos_8 = _get_sheet_source(prepared_sources, GOS_8_SOURCE_KEY, QILTPreparedSheet)
    gos_5 = _get_sheet_source(prepared_sources, GOS_5_SOURCE_KEY, QILTPreparedSheet)

    gos_l_1 = _get_sheet_source(prepared_sources, GOS_L_1_SOURCE_KEY, QILTPreparedSheet)
    gos_l_6 = _get_sheet_source(prepared_sources, GOS_L_6_SOURCE_KEY, QILTPreparedSheet)
    gos_l_26 = _get_sheet_source(
        prepared_sources, GOS_L_26_SOURCE_KEY, QILTPreparedSheet
    )
    gos_l_160 = _get_sheet_source(
        prepared_sources, GOS_L_160_SOURCE_KEY, QILTPreparedSheet
    )

    sew_32 = _get_sheet_source(prepared_sources, SEW_32_SOURCE_KEY, ABSPreparedSheet)
    sew_35 = _get_sheet_source(prepared_sources, SEW_35_SOURCE_KEY, ABSPreparedSheet)

    chart_1a_table = build_chart_1a_table(sew_35)
    chart_1b_table = build_chart_1b_table(sew_32)
    chart_2_table = build_chart_2_table(gos_21, gos_l_1)
    chart_3_table = build_chart_3_table(gos_8, gos_5)
    chart_4_table = build_chart_4_table(gos_8, gos_l_160)
    chart_5_table = build_chart_5_table(gos_l_6)
    chart_6_table = build_chart_6_table(gos_l_6, gos_l_26)
    chart_7_table = build_chart_7_table(gos_8, gos_l_160, gos_2, gos_l_6)

    return {
        CHART_1A_ID: chart_1a_table,
        CHART_1B_ID: chart_1b_table,
        CHART_2_ID: chart_2_table,
        CHART_3_ID: chart_3_table,
        CHART_4_ID: chart_4_table,
        CHART_5_ID: chart_5_table,
        CHART_6_ID: chart_6_table,
        CHART_7_ID: chart_7_table,
    }


def _get_sheet_source(
    prepared_sources: Mapping[str, PreparedSheet],
    source_key: str,
    source_type: type[PreparedSheetType],
) -> PreparedSheetType:
    prepared_source = prepared_sources[source_key]
    if not isinstance(prepared_source, source_type):
        raise TypeError(
            f"{source_key!r} is not a prepared {source_type.__name__} source."
        )

    return prepared_source


def get_chart_table(
    chart_number: NumericValue,
    chart_tables: Mapping[str, pd.DataFrame],
) -> pd.DataFrame:
    if chart_number == 1:
        raise KeyError("Chart 1 is split into 1.1 (1a) and 1.2 (1b).")

    try:
        chart_id = CHART_TABLE_IDS_BY_NUMBER[chart_number]
    except KeyError:
        raise KeyError(f"Unknown chart number: {chart_number!r}.") from None

    return chart_tables[chart_id]
