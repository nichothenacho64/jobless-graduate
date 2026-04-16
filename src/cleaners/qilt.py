from __future__ import annotations

from dataclasses import replace
from typing import Optional
import re

import pandas as pd

from src.cleaners.sheets import (
    clean_column_name,
    clean_metadata_sections,
    clean_text,
    clean_text_value,
    coerce_numeric_series,
    parse_sheet_number,
    series_is_numeric_like,
    series_is_text_like,
)
from src.parsers.qilt import QILTParsedSheet
from src.utils import UNNAMED_HEADER_LABEL

QILT_MISSING_TEXT_VALUES = frozenset(
    {"", "-", "—", "–", "..", "...", "n/a", "na", "n.p.", "n/p", "np", "nil"}
)
QILT_TRAILING_FOOTNOTE_PATTERN = re.compile(r"[*†‡]+$")

def clean_qilt_parsed_sheet(parsed_sheet: QILTParsedSheet) -> QILTParsedSheet:
    cleaned_metadata = clean_metadata_sections(parsed_sheet.metadata, text_cleaner=_clean_qilt_text)
    return replace(
        parsed_sheet,
        table=clean_qilt_table(parsed_sheet.table),
        metadata=cleaned_metadata
    )

def clean_qilt_table(table: pd.DataFrame) -> pd.DataFrame:
    cleaned_table = table.copy()
    cleaned_columns: list[str] = []
    
    for column in cleaned_table.columns:
        cleaned_column = clean_column_name(column, text_cleaner=_clean_qilt_text)
        cleaned_columns.append(cleaned_column)

    cleaned_table.columns = cleaned_columns

    for column_name in cleaned_table.columns:
        cleaned_table[column_name] = _clean_qilt_series(
            cleaned_table[column_name],
            column_name=column_name,
        )

    cleaned_table = cleaned_table.dropna(axis=0, how="all").dropna(axis=1, how="all")
    cleaned_table = cleaned_table.reset_index(drop=True)

    if cleaned_table.empty:
        raise ValueError("The cleaned QILT table is empty.")

    return cleaned_table

def get_qilt_value_columns(table: pd.DataFrame) -> list[str]:
    value_columns: list[str] = []
    unnamed_prefix = f"{UNNAMED_HEADER_LABEL}_"

    for column in table.columns:
        column_name = str(column)

        if column_name.startswith(unnamed_prefix):
            continue

        value_columns.append(column_name)

    return value_columns


def _clean_qilt_series(series: pd.Series, *, column_name: str) -> pd.Series:
    cleaned_series = series.map(
        lambda value: clean_text_value(value, text_cleaner=_clean_qilt_text)
    )

    if series_is_numeric_like(cleaned_series, number_parser=_parse_qilt_number):
        return coerce_numeric_series(
            cleaned_series,
            column_name=column_name,
            number_parser=_parse_qilt_number,
        )

    if series_is_text_like(cleaned_series):
        return cleaned_series.astype("string")

    return cleaned_series


def _clean_qilt_text(value: object) -> Optional[str]:
    return clean_text(value, missing_text_values=QILT_MISSING_TEXT_VALUES)


def _parse_qilt_number(value: object) -> Optional[int | float]:
    return parse_sheet_number(
        value,
        trailing_note_pattern=QILT_TRAILING_FOOTNOTE_PATTERN,
    )