from __future__ import annotations

import pandas as pd

from src.loaders import list_excel_sheets, load_excel_sheet
from src.types import Folder, QILTParsedSheet, QILTRowBounds, SheetTitleList
from src.parsers.qilt_extraction import (
    classify_qilt_table,
    extract_metadata_sections,
    extract_table,
    find_data_end_row,
    find_footer_start_row,
    find_header_row,
    find_title,
    rename_dimension_columns,
)


def parse_qilt_sheet(
    folder: Folder, file_name: str, sheet_name: str
) -> QILTParsedSheet:
    raw_sheet = load_excel_sheet(folder, file_name, sheet_name, header=None)

    title = find_title(raw_sheet)
    header_row_idx = find_header_row(raw_sheet)
    footer_start_row_idx = find_footer_start_row(raw_sheet, header_row_idx + 1)
    data_first_row_idx = header_row_idx + 1
    data_last_row_idx = find_data_end_row(
        raw_sheet,
        data_first_row_idx,
        footer_start_row_idx,
    )

    rows = QILTRowBounds(
        header=header_row_idx,
        data_first=data_first_row_idx,
        data_last=data_last_row_idx,
        footer_start=footer_start_row_idx,
    )

    table = extract_table(raw_sheet, rows.header, rows.data_first, rows.data_last)
    metadata = extract_metadata_sections(raw_sheet, rows.footer_start)
    classification = classify_qilt_table(table)
    table = rename_dimension_columns(table, metadata)

    return QILTParsedSheet(
        sheet_name=sheet_name,
        title=title,
        rows=rows,
        classification=classification,
        table=table,
        metadata=metadata,
    )


def find_all_qilt_sheets(folder: Folder, file_name: str) -> pd.DataFrame:
    sheet_title_list: SheetTitleList = []
    all_sheet_names = list_excel_sheets(folder, file_name)

    for sheet_number, sheet_name in enumerate(all_sheet_names):
        parsed_sheet = parse_qilt_sheet(folder, file_name, sheet_name)
        sheet_title_list.append(
            {
                "Sheet number": sheet_number,
                "Sheet name": sheet_name,
                "Sheet title": parsed_sheet.title,
            }
        )

    return pd.DataFrame(sheet_title_list).set_index("Sheet number")
