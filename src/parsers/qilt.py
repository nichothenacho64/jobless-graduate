from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Optional

import pandas as pd

from src.exceptions import SheetNotFoundError
from src.loaders import list_excel_sheets, resolve_spreadsheet_path
from src.types import Folder, QILTTableKind
from src.parsers.sheets import (
    build_column_names,
    count_nonempty_cells,
    drop_trailing_blank_rows,
    find_next_nonblank_row,
    clean_cell_text,
    get_row_texts,
)

from src.utils import UNNAMED_HEADER_LABEL

QILT_METADATA_LABELS = {
    "Column variables:",
    "Column filters:",
    "Column notes:",
    "Row variables:",
    "Row notes:",
}

YEAR_PATTERN = re.compile(r"\b20\d{2}\b")

QILT_TITLE_ROW_INDEX = 0

QILT_HEADER_SEARCH_START_ROW = 3
QILT_HEADER_SEARCH_END_ROW_EXCLUSIVE = 8

SINGLE_METRIC_EXPECTED_ROW_COUNT = 1
METRIC_ROWS_MAX_ROW_COUNT = 5

QILT_PARTICIPATING_INSTITIONS_LINE = "No. of participating institutions"

@dataclass(slots=True)
class QILTRowBounds:
    header: int
    data_first: int
    data_last: int
    footer_start: Optional[int]

@dataclass(slots=True)
class QILTParsedSheet:
    name: str
    title: str
    rows: QILTRowBounds
    classification: str
    table: pd.DataFrame
    metadata: dict[str, list[str]]

def parse_qilt_sheet(folder: Folder, file_name: str, sheet_name: str) -> QILTParsedSheet:
    file_path = resolve_spreadsheet_path(folder, file_name)
    sheet_names = list_excel_sheets(folder, file_name)

    if sheet_name not in sheet_names:
        raise SheetNotFoundError(sheet_name, file_path.name, sheet_names)

    raw_sheet = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    title = _find_title(raw_sheet)
    header_row_idx = _find_header_row(raw_sheet)
    footer_start_row_idx = _find_footer_start_row(raw_sheet, header_row_idx + 1)
    data_first_row_idx = header_row_idx + 1
    data_last_row_idx = _find_data_end_row(
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
    table = _extract_table(raw_sheet, rows.header, rows.data_first, rows.data_last)

    metadata = _extract_metadata_sections(raw_sheet, rows.footer_start)
    classification = _classify_qilt_table(table)

    return QILTParsedSheet(
        name=sheet_name,
        title=title,
        rows=rows,
        classification=classification,
        table=table,
        metadata=metadata,
    )

# def parse_qilt_table(folder: Folder, file_name: str, sheet_name: str) -> pd.DataFrame:
#     return parse_qilt_sheet(folder, file_name, sheet_name).table

def _find_title(raw_sheet: pd.DataFrame) -> str:
    for value in raw_sheet.iloc[QILT_TITLE_ROW_INDEX].tolist():
        text = clean_cell_text(value)
        if text:
            return text

    raise ValueError("Could not extract a title from the QILT sheet.")

def _find_header_row(raw_sheet: pd.DataFrame) -> int:
    search_stop = min(len(raw_sheet), QILT_HEADER_SEARCH_END_ROW_EXCLUSIVE)

    for row_index in range(QILT_HEADER_SEARCH_START_ROW, search_stop):
        row = raw_sheet.iloc[row_index]

        if count_nonempty_cells(row) < 2:
            continue

        next_nonblank_row_index = find_next_nonblank_row(raw_sheet, row_index + 1)

        if next_nonblank_row_index is None:
            continue

        next_row = raw_sheet.iloc[next_nonblank_row_index]

        if count_nonempty_cells(next_row) >= 2:
            return row_index

    raise ValueError("Could not identify the QILT header row.")

def _find_footer_start_row(raw_sheet: pd.DataFrame, start_row_index: int) -> Optional[int]:
    for row_index in range(start_row_index, len(raw_sheet)):
        current_row_texts = get_row_texts(raw_sheet.iloc[row_index])

        if any(text in QILT_METADATA_LABELS for text in current_row_texts):
            return row_index

    return None

def _find_data_end_row(
    raw_sheet: pd.DataFrame,
    data_start_row_index: int,
    footer_start_row_index: Optional[int],
) -> int:
    if footer_start_row_index is None:
        end_row_index = len(raw_sheet) - 1
    else:
        end_row_index = footer_start_row_index - 1

    while end_row_index >= data_start_row_index:
        row = raw_sheet.iloc[end_row_index]

        if count_nonempty_cells(row) > 0:
            return end_row_index

        end_row_index -= 1

    raise ValueError("Could not identify the end of the QILT data block.")

def _extract_table(
    raw_sheet: pd.DataFrame, 
    header_row_index: int, 
    data_start_row_index: int, 
    data_end_row_index: int, 
)-> pd.DataFrame: 
    header_row = raw_sheet.iloc[header_row_index] 
    column_names = build_column_names(header_row) 
    
    table = raw_sheet.iloc[data_start_row_index : data_end_row_index + 1].copy() 
    table.columns = column_names 
    table = table.reset_index(drop=True)
    
    table = table.dropna(axis=1, how="all") 
    table = drop_trailing_blank_rows(table) 
    
    if table.empty: 
        raise ValueError("The extracted QILT core table is empty.") 
    
    return table

def _extract_metadata_sections(raw_sheet: pd.DataFrame, footer_start_row_index: Optional[int]) -> dict[str, list[str]]:
    if footer_start_row_index is None:
        return {}

    metadata: dict[str, list[str]] = {}
    current_section: Optional[str] = None

    for row_index in range(footer_start_row_index, len(raw_sheet)):
        current_row_texts = get_row_texts(raw_sheet.iloc[row_index])

        if not current_row_texts:
            continue

        first_text = current_row_texts[0]

        if first_text in QILT_METADATA_LABELS:
            current_section = first_text
            metadata[current_section] = []
            continue

        if current_section is not None:
            metadata[current_section].append(" | ".join(current_row_texts))

    return metadata

def _classify_qilt_table(table: pd.DataFrame) -> QILTTableKind:
    column_names = [str(column) for column in table.columns]
    data_columns = [column for column in column_names if not column.startswith(UNNAMED_HEADER_LABEL + "_")]

    row_count = len(table)
    
    year_column_flags = [_looks_like_year_column(column) for column in data_columns]
    
    all_data_columns_are_years = all(year_column_flags)
    any_data_column_is_year = any(year_column_flags)

    if any(QILT_PARTICIPATING_INSTITIONS_LINE in column for column in column_names):
        return "collection_summary"

    if _column_contains_value(table, "Original Study Level"):
        return "transition_matrix"

    if row_count == SINGLE_METRIC_EXPECTED_ROW_COUNT and all_data_columns_are_years:
        return "single_metric_time_series"

    if row_count <= METRIC_ROWS_MAX_ROW_COUNT and all_data_columns_are_years:
        return "metric_rows"

    if any_data_column_is_year:
        return "wide_multi_year"

    return "wide_table"

def _column_contains_value(table: pd.DataFrame, target: str) -> bool:
    for column in table.columns:
        values = table[column].dropna().astype(str).str.strip()
        if (values == target).any():
            return True

    return False

def _looks_like_year_column(column_name: str) -> bool:
    return YEAR_PATTERN.search(column_name) is not None
