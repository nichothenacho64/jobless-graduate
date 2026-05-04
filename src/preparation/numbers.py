from __future__ import annotations

import math
import re
from typing import Any, Optional, cast

from src.preparation.constants import SHEET_NUMBER_PATTERN
from src.preparation.series import is_missing_value
from src.types import NumericValue


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

    return _clean_parsed_number(
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


def _clean_parsed_number(
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


def coerce_optional_int(value: object) -> Optional[int]:
    if is_missing_value(value):
        return None

    return int(cast(Any, value))
