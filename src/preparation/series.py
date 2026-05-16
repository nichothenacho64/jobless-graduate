from __future__ import annotations

import math
from typing import Optional

import pandas as pd
import numpy as np

from src.types import NullableNumericDtype, NumberParser, NumericConverter, NumericValue


def is_missing_value(value: object) -> bool:
    if value is None or value is pd.NA or value is pd.NaT:
        return True

    return isinstance(value, float) and math.isnan(value)


def is_missing_scalar(value: object) -> bool:
    value_is_missing = is_missing_value(value)
    if isinstance(value_is_missing, (bool, np.bool_)):
        return bool(value_is_missing)

    return False


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


def format_row_key_value(value: object) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


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
        if is_missing_value(value):
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
