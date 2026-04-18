from __future__ import annotations

import re
from typing import Optional

import pandas as pd

from src.constants.parsing import (
    COLUMN_NAME_NON_ALNUM_PATTERN,
    COLUMN_NAME_UNDERSCORE_PATTERN,
    SHEET_WHITESPACE_PATTERN,
)
from src.preparation.series import is_missing_value
from src.types import Metadata, TextCleaner


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
