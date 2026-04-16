from __future__ import annotations

from collections.abc import Callable
import re
from typing import Optional

import math
import pandas as pd

type NumericValue = int | float
type NumericConverter = Callable[[NumericValue], NumericValue]
type NullableNumericDtype = pd.Int64Dtype | pd.Float64Dtype

SHEET_WHITESPACE_PATTERN = re.compile(r"\s+")
SHEET_NUMBER_PATTERN = re.compile(r"(?P<sign>-)?(?P<number>\d+(?:\.\d+)?)")

TextCleaner = Callable[[object], Optional[str]]
NumberParser = Callable[[object], Optional[NumericValue]]


__all__ = [
    "clean_column_name",
    "clean_metadata_sections",
    "clean_text",
    "clean_text_value",
    "coerce_numeric_series",
    "parse_sheet_number",
    "series_is_numeric_like",
    "series_is_text_like",
]

def _is_missing_scalar(value: object) -> bool:
    if value is None or value is pd.NA or value is pd.NaT:
        return True

    return isinstance(value, float) and math.isnan(value)

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
    if _is_missing_scalar(value):
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

    return text


def clean_metadata_sections(
    metadata: dict[str, list[str]],
    *,
    text_cleaner: TextCleaner,
) -> dict[str, list[str]]:
    cleaned_metadata: dict[str, list[str]] = {}

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


def parse_sheet_number(
    value: object,
    *,
    trailing_note_pattern: Optional[re.Pattern[str]] = None,
    number_pattern: re.Pattern[str] = SHEET_NUMBER_PATTERN,
    allow_parentheses_negative: bool = True,
    strip_commas: bool = True,
    strip_percent: bool = True,
) -> Optional[NumericValue]:
    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        if math.isnan(value):
            return None
        return value

    normalised_text = _normalise_sheet_number_text(
        value,
        trailing_note_pattern=trailing_note_pattern,
        allow_parentheses_negative=allow_parentheses_negative,
        strip_commas=strip_commas,
        strip_percent=strip_percent,
    )
    if normalised_text is None:
        return None

    text, is_parentheses_negative = normalised_text

    number_match = number_pattern.fullmatch(text)
    if number_match is None:
        return None

    number_text = number_match.group("number")
    has_minus_sign = number_match.group("sign") == "-"

    return _finalise_parsed_number(
        number_text,
        has_minus_sign=has_minus_sign,
        is_negative=is_parentheses_negative,
    )

def _normalise_sheet_number_text(
    value: object,
    *,
    trailing_note_pattern: Optional[re.Pattern[str]],
    allow_parentheses_negative: bool,
    strip_commas: bool,
    strip_percent: bool,
) -> Optional[tuple[str, bool]]:
    if not isinstance(value, str):
        return None

    text = value.strip()
    if not text:
        return None

    is_negative = False

    if allow_parentheses_negative and text.startswith("(") and text.endswith(")"):
        is_negative = True
        text = text[1:-1].strip()

    if strip_commas:
        text = text.replace(",", "")

    if strip_percent:
        text = text.rstrip("%")

    if trailing_note_pattern is not None:
        text = trailing_note_pattern.sub("", text).strip()

    text = text.replace("−", "-")
    if not text:
        return None

    return text, is_negative


def _finalise_parsed_number(
    number_text: str,
    *,
    has_minus_sign: bool,
    is_negative: bool,
) -> NumericValue:
    parsed_number = float(number_text)

    if has_minus_sign or is_negative:
        parsed_number *= -1

    if parsed_number.is_integer():
        return int(parsed_number)

    return parsed_number


def series_is_text_like(series: pd.Series) -> bool:
    for value in series.tolist():
        if pd.isna(value):
            continue
        if not isinstance(value, str):
            return False

    return True


def series_is_numeric_like(
    series: pd.Series,
    *,
    number_parser: NumberParser,
) -> bool:
    non_null_values = [value for value in series.tolist() if not pd.isna(value)]
    if not non_null_values:
        return False

    for value in non_null_values:
        if number_parser(value) is None:
            return False

    return True

def resolve_nullable_numeric_dtype(
    values: list[NumericValue],
) -> tuple[NullableNumericDtype, NumericConverter]:
    if not values:
        return pd.Float64Dtype(), float

    if all(float(value).is_integer() for value in values):
        return pd.Int64Dtype(), int

    return pd.Float64Dtype(), float

def coerce_numeric_series(
    series: pd.Series,
    *,
    column_name: str,
    number_parser: NumberParser,
) -> pd.Series:
    parsed_values: list[Optional[NumericValue]] = []
    numeric_values: list[NumericValue] = []

    for value in series.tolist():
        if _is_missing_scalar(value):
            parsed_values.append(None)
            continue

        parsed_number = number_parser(value)
        if parsed_number is None:
            raise ValueError(f"Column {column_name!r} was expected to be numeric-like.")

        parsed_values.append(parsed_number)
        numeric_values.append(parsed_number)

    dtype, converter = resolve_nullable_numeric_dtype(numeric_values)

    final_values: list[Optional[NumericValue]] = []
    for value in parsed_values:
        if value is None:
            final_values.append(None)
            continue

        final_values.append(converter(value))

    return pd.Series(
        pd.array(final_values, dtype=dtype),
        index=series.index,
        name=series.name,
    )
