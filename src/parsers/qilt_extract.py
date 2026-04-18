from __future__ import annotations

from typing import Optional

import pandas as pd

from src.constants.parsing import UNNAMED_HEADER_LABEL
from src.constants.qilt import (
    QILT_HEADER_SEARCH_END_ROW_EXCLUSIVE,
    QILT_HEADER_SEARCH_START_ROW,
    QILT_METADATA_LABELS,
    QILT_TITLE_ROW_INDEX,
)
from src.exceptions import EmptyTableError
from src.parsers.sheets import (
    build_column_names,
    clean_cell_text,
    count_nonempty_cells,
    drop_trailing_blank_rows,
    get_row_texts,
)
from src.types import Metadata


def _is_qilt_metadata_label(text: str) -> bool:
    return text in QILT_METADATA_LABELS or text.endswith(":")


def find_title(raw_sheet: pd.DataFrame) -> str:
    for value in raw_sheet.iloc[QILT_TITLE_ROW_INDEX].tolist():
        text = clean_cell_text(value)
        if text:
            return text

    raise ValueError("Could not extract a title from the QILT sheet.")


def find_header_row(raw_sheet: pd.DataFrame) -> int:
    search_stop = min(len(raw_sheet), QILT_HEADER_SEARCH_END_ROW_EXCLUSIVE)

    for row_index in range(QILT_HEADER_SEARCH_START_ROW, search_stop):
        if count_nonempty_cells(raw_sheet.iloc[row_index]) > 0:  # the header is at row 3
            return row_index

    raise ValueError("Could not identify the QILT header row.")


def find_footer_start_row(raw_sheet: pd.DataFrame, start_row_index: int) -> Optional[int]:
    for row_index in range(start_row_index, len(raw_sheet)):
        current_row_texts = get_row_texts(raw_sheet.iloc[row_index])

        if any(_is_qilt_metadata_label(text) for text in current_row_texts):
            return row_index
    else:
        return None


def find_data_end_row(
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


def extract_table(
    raw_sheet: pd.DataFrame,
    header_row_index: int,
    data_start_row_index: int,
    data_end_row_index: int,
) -> pd.DataFrame:
    header_row = raw_sheet.iloc[header_row_index]
    column_names = build_column_names(header_row)

    table = raw_sheet.iloc[data_start_row_index : data_end_row_index + 1].copy()
    table.columns = column_names
    table = table.reset_index(drop=True)

    table = table.dropna(axis=1, how="all")
    table = drop_trailing_blank_rows(table)

    if table.empty:
        raise EmptyTableError("The extracted QILT core table")

    return table


def extract_metadata_sections(
    raw_sheet: pd.DataFrame,
    footer_start_row_index: Optional[int],
) -> Metadata:
    if footer_start_row_index is None:
        return {}

    metadata: Metadata = {}
    current_section: Optional[str] = None

    for row_index in range(footer_start_row_index, len(raw_sheet)):
        current_row_texts = get_row_texts(raw_sheet.iloc[row_index])

        if not current_row_texts:
            continue

        first_text = current_row_texts[0]

        if _is_qilt_metadata_label(first_text):
            current_section = first_text
            metadata[current_section] = []
            continue

        if current_section is not None:
            metadata[current_section].append(" | ".join(current_row_texts))

    return metadata


def _extract_row_variable_labels(metadata: Metadata) -> list[str]:
    raw_row_variables = metadata.get("Row variables:", [])
    row_variable_labels: list[str] = []

    for raw_label in raw_row_variables:
        label = raw_label.split(":", maxsplit=1)[0].strip()
        if label:
            row_variable_labels.append(label)

    return row_variable_labels


def rename_dimension_columns(table: pd.DataFrame, metadata: Metadata) -> pd.DataFrame:
    row_label_columns: list[str] = []

    for column in table.columns:
        column_name = str(column)

        if not column_name.startswith(UNNAMED_HEADER_LABEL + "_"):
            break

        row_label_columns.append(column_name)

    if not row_label_columns:
        return table

    rename_map: dict[str, str] = {}
    row_variable_labels = _extract_row_variable_labels(metadata)

    row_label_column_count = len(row_label_columns)
    first_row_label_column = row_label_columns[0]

    if row_label_column_count == 1:
        has_single_row_variable_label = len(row_variable_labels) == 1

        if has_single_row_variable_label:
            first_row_variable_label = row_variable_labels[0]
            rename_map[first_row_label_column] = first_row_variable_label
        else:
            rename_map[first_row_label_column] = "Row label"

        return table.rename(columns=rename_map)

    second_row_label_column = row_label_columns[1]
    additional_row_label_columns = row_label_columns[2:]

    rename_map[first_row_label_column] = "Row group"
    rename_map[second_row_label_column] = "Row label"

    for row_dimension_number, row_label_column in enumerate(additional_row_label_columns, start=3):
        rename_map[row_label_column] = f"Row dimension {row_dimension_number}"

    return table.rename(columns=rename_map)
