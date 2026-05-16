from __future__ import annotations

import pandas as pd
from src.parsers.abs_extraction import load_abs_row_indents
# load_abs_row_indents

from src.loaders import load_excel_sheet, resolve_folder_path
from src.parsers.abs_extraction import (
    extract_abs_metadata_sections,
    extract_abs_subtables,
    find_abs_footer_start_row,
    find_abs_measurement_cells,
    find_abs_table_sources,
    find_abs_title,
    infer_abs_row_bounds,
    list_abs_table_sheets,
    parse_abs_sheet_number,
)
from src.sources import ABS_FOLDER_NAME, RAW_SOURCE_DIRS
from src.types import ABSParsedSheet, Folder, SheetTitleList


def parse_abs_sheet(
    folder: Folder, source_file: str, sheet_name: str
) -> ABSParsedSheet:
    raw_sheet = load_excel_sheet(folder, source_file, sheet_name, header=None)

    table_number = parse_abs_sheet_number(sheet_name)
    title = find_abs_title(raw_sheet)
    row_indents = load_abs_row_indents(folder, source_file, sheet_name)
    measurement_cells = find_abs_measurement_cells(raw_sheet)
    footer_start_row_idx = find_abs_footer_start_row(raw_sheet)
    rows = infer_abs_row_bounds(raw_sheet, measurement_cells, footer_start_row_idx)
    subtables = extract_abs_subtables(
        raw_sheet,
        table_number,
        title,
        rows,
        measurement_cells,
        row_indents,
    )
    metadata = extract_abs_metadata_sections(raw_sheet, rows.footer_start)

    return ABSParsedSheet(
        source_file=source_file,
        sheet_name=sheet_name,
        table_number=table_number,
        title=title,
        rows=rows,
        table=raw_sheet,
        subtables=subtables,
        metadata=metadata,
    )


def find_all_abs_sheets(folder: Folder = ABS_FOLDER_NAME) -> pd.DataFrame:
    folder_key = resolve_folder_path(folder).name
    source_files = RAW_SOURCE_DIRS[folder_key]

    sheet_title_list: SheetTitleList = []

    for source_file in find_abs_table_sources(source_files):
        for sheet_name in list_abs_table_sheets(folder, source_file):
            parsed_sheet = parse_abs_sheet(folder, source_file, sheet_name)
            sheet_title_list.append(
                {
                    "Sheet number": parse_abs_sheet_number(sheet_name),
                    "Sheet name": parsed_sheet.sheet_name,
                    "Source file": parsed_sheet.source_file,
                    "Sheet title": parsed_sheet.title,
                }
            )

    return pd.DataFrame(sheet_title_list).set_index("Sheet number")
