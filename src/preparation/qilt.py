from __future__ import annotations

from dataclasses import replace
from typing import Optional, cast

import pandas as pd

from src.preparation.constants import (
    MISSING_TEXT_VALUES,
    QILT_FOOTNOTE_SYMBOL_PATTERN,
    QILT_TRAILING_FOOTNOTE_PATTERN,
)
from src.transform.constants import QILT_SUBGROUP_TEXT_EQUIVALENTS
from src.exceptions import EmptyTableError
from src.parsers.qilt import QILTParsedSheet, parse_qilt_sheet
from src.preparation.cleaners import (
    clean_column_name,
    clean_metadata_sections,
    clean_source_text,
    clean_text,
    clean_text_or_numeric_series,
)
from src.preparation.numbers import parse_sheet_number
from src.types import Folder, NumericValue

def prepare_qilt_table(folder: Folder, file_name: str, sheet_name: str) -> pd.DataFrame:
    parsed_sheet = parse_qilt_sheet(folder, file_name, sheet_name)
    return clean_qilt_parsed_sheet(parsed_sheet).table

def prepare_qilt_sheet(folder: Folder, file_name: str, sheet_name: str) -> QILTParsedSheet:
    parsed_sheet = parse_qilt_sheet(folder, file_name, sheet_name)
    return clean_qilt_parsed_sheet(parsed_sheet)

def clean_qilt_parsed_sheet(parsed_sheet: QILTParsedSheet) -> QILTParsedSheet:
    cleaned_metadata = clean_metadata_sections(parsed_sheet.metadata, text_cleaner=_clean_qilt_text)
    cleaned_table = clean_qilt_table(parsed_sheet.table)
    return replace(
        parsed_sheet,
        table=cleaned_table,
        metadata=cleaned_metadata,
    )

def clean_qilt_table(table: pd.DataFrame) -> pd.DataFrame:
    cleaned_table = table.copy()
    cleaned_columns: list[str] = []

    for column in cleaned_table.columns:
        cleaned_column = clean_column_name(column, text_cleaner=_clean_qilt_text)
        cleaned_columns.append(cleaned_column)

    cleaned_table.columns = cleaned_columns

    for column_name in cleaned_table.columns:
        column_series = cast(pd.Series, cleaned_table[column_name])
        cleaned_table[column_name] = _clean_qilt_series(
            column_series,
            column_name=column_name,
        )

    cleaned_table = cleaned_table.dropna(axis=0, how="all").dropna(axis=1, how="all")
    cleaned_table = cleaned_table.reset_index(drop=True)

    if cleaned_table.empty:
        raise EmptyTableError("The cleaned QILT table")

    return cleaned_table

def _clean_qilt_series(series: pd.Series, *, column_name: str) -> pd.Series:
    return clean_text_or_numeric_series(
        series,
        column_name=column_name,
        text_cleaner=_clean_qilt_text,
        number_parser=parse_qilt_number,
    )

def _clean_qilt_text(value: object) -> Optional[str]:
    return clean_text(value, missing_text_values=MISSING_TEXT_VALUES)

def parse_qilt_number(value: object) -> Optional[NumericValue]:
    return parse_sheet_number(
        value,
        trailing_note_pattern=QILT_TRAILING_FOOTNOTE_PATTERN,
    )

def clean_qilt_display_text(value: object) -> Optional[str]:
    text = clean_source_text(value)
    if text is None:
        return None

    text = QILT_FOOTNOTE_SYMBOL_PATTERN.sub("", text)
    return clean_text(text, missing_text_values=frozenset({""}))

def normalise_qilt_key_text(value: object) -> Optional[str]:
    text = clean_qilt_display_text(value)
    if text is None:
        return None

    equivalent_text = QILT_SUBGROUP_TEXT_EQUIVALENTS.get(text, text)
    return equivalent_text.lower()
