from __future__ import annotations

import re
from typing import Optional

import pandas as pd

from src.parsers.constants import (
    COLUMN_NAME_NON_ALNUM_PATTERN,
    COLUMN_NAME_UNDERSCORE_PATTERN,
    SHEET_WHITESPACE_PATTERN,
)
from src.preparation.series import (
    coerce_numeric_series,
    is_missing_value,
    series_is_numeric_like,
    series_is_text_like,
)
from src.types import Metadata, NumberParser, TextCleaner

def clean_text(
    value: object,
    *,
    missing_text_values: frozenset[str],
    whitespace_pattern: re.Pattern[str] = SHEET_WHITESPACE_PATTERN,
) -> Optional[str]:
    text = str(value).strip()
    text = whitespace_pattern.sub(" ", text)

    if text.lower() in missing_text_values:
        return None

    return text or None

def clean_text_value(value: object, *, text_cleaner: TextCleaner) -> object:
    if is_missing_value(value):
        return pd.NA

    if isinstance(value, str):
        text = text_cleaner(value)
        if text is None:
            return pd.NA
        return text

    return value

def clean_source_text(
    value: object,
    *,
    missing_text_values: frozenset[str] = frozenset({""}),
) -> Optional[str]:
    if is_missing_value(value):
        return None

    return clean_text(value, missing_text_values=missing_text_values)

def clean_missing_text_value(
    value: object,
    *,
    missing_text_values: frozenset[str],
) -> object:
    if is_missing_value(value):
        return pd.NA

    if isinstance(value, str):
        text = clean_text(value, missing_text_values=missing_text_values)
        return pd.NA if text is None else text

    return value

def clean_text_or_numeric_series(
    series: pd.Series,
    *,
    column_name: str,
    text_cleaner: TextCleaner,
    number_parser: NumberParser,
) -> pd.Series:
    cleaned_series = series.map(
        lambda value: clean_text_value(value, text_cleaner=text_cleaner)
    )

    if series_is_numeric_like(cleaned_series, number_parser=number_parser):
        return coerce_numeric_series(
            cleaned_series,
            column_name=column_name,
            number_parser=number_parser,
        )

    if series_is_text_like(cleaned_series):
        return cleaned_series.astype("string")

    return cleaned_series

def clean_column_name(
    column_name: object,
    *,
    text_cleaner: TextCleaner,
) -> str:
    text = text_cleaner(column_name)
    if text is None:
        raise ValueError("Column names cannot be empty after cleaning.")

    standardised_text = text.strip().lower()
    standardised_text = COLUMN_NAME_NON_ALNUM_PATTERN.sub("_", standardised_text)
    standardised_text = COLUMN_NAME_UNDERSCORE_PATTERN.sub("_", standardised_text)
    standardised_text = standardised_text.strip("_")

    if not standardised_text:
        raise ValueError("Column names cannot be empty after standardisation.")

    return standardised_text

def clean_metadata_sections(
    metadata: Metadata,
    *,
    text_cleaner: TextCleaner,
) -> Metadata:
    cleaned_metadata: Metadata = {}

    for raw_section_label, raw_lines in metadata.items():
        section_label = text_cleaner(raw_section_label)
        if section_label is None:
            continue

        cleaned_lines: list[str] = []
        for raw_line in raw_lines:
            line = text_cleaner(raw_line)
            if line is not None:
                cleaned_lines.append(line)

        if cleaned_lines:
            cleaned_metadata[section_label] = cleaned_lines

    return cleaned_metadata
