from __future__ import annotations

from typing import Optional

import pandas as pd

from src.constants.parsing import SHEET_WHITESPACE_PATTERN, UNNAMED_HEADER_LABEL


def clean_cell_text(value: object) -> str:
    if isinstance(value, float) and pd.isna(value):
        return ""

    return str(value).strip()


def get_row_texts(row: pd.Series) -> list[str]:
    texts: list[str] = []

    for value in row.tolist():
        text = clean_cell_text(value)
        if text:
            texts.append(text)

    return texts


def count_nonempty_cells(row: pd.Series) -> int:
    nonempty_cell_count = 0

    for value in row.tolist():
        if clean_cell_text(value):
            nonempty_cell_count += 1

    return nonempty_cell_count


def find_next_nonblank_row(raw_sheet: pd.DataFrame, start_row_index: int) -> Optional[int]:
    for row_index in range(start_row_index, len(raw_sheet)):
        row = raw_sheet.iloc[row_index]

        if count_nonempty_cells(row) > 0:
            return row_index

    return None


def drop_trailing_blank_rows(table: pd.DataFrame) -> pd.DataFrame:
    end_index = len(table) - 1

    while end_index >= 0:
        row = table.iloc[end_index]

        if count_nonempty_cells(row) > 0:
            break

        end_index -= 1

    row_stop = end_index + 1
    trimmed_table = table.iloc[:row_stop]

    return trimmed_table.reset_index(drop=True)


def build_column_names(header_row: pd.Series) -> list[str]:
    column_names: list[str] = []
    unnamed_column_index = 0
    header_label_counts: dict[str, int] = {}

    for raw_value in header_row.tolist():
        header_label = clean_cell_text(raw_value)

        if header_label:
            header_label = SHEET_WHITESPACE_PATTERN.sub(" ", header_label)
        else:
            header_label = f"{UNNAMED_HEADER_LABEL}_{unnamed_column_index}"
            unnamed_column_index += 1

        header_label_count = header_label_counts.get(header_label, 0) + 1
        header_label_counts[header_label] = header_label_count

        if header_label_count == 1:
            column_name = header_label
        else:
            column_name = f"{header_label}_{header_label_count}"

        column_names.append(column_name)

    return column_names

