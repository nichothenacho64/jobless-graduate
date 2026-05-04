from __future__ import annotations

from typing import Optional, cast

import pandas as pd

from src.formatting import join_sorted
from src.exceptions import EmptyTableError
from src.parsers.abs import parse_abs_sheet
from src.preparation.cleaners import (
    clean_column_name,
    clean_metadata_sections,
    clean_source_text,
    clean_text,
    clean_text_or_numeric_series,
    clean_text_value,
    clean_missing_text_value,
)
from src.preparation.constants import (
    ABS_AUSTRALIA_HEADER_TOKENS,
    ABS_TOTAL_HEADER_TOKENS,
    ABS_MEASUREMENT_COLUMNS,
    ABS_PREPARED_INDEX_COLUMNS,
    ABS_NO_PARENT_SENTINEL,
    ABS_MEASUREMENT_ALIASES,
    ABS_TRAILING_FOOTNOTE_PATTERN,
    ABS_WHOLE_YEAR_DECIMAL_PATTERN,
    ABS_DISPLAY_MISSING_TEXT_VALUES,
    ABS_PREPARED_SCHEMA,
    ABS_ROW_IDENTITY_COLUMNS,
    ABS_EMPTY_TEXT_VALUES,
    MISSING_TEXT_VALUES,
)
from src.preparation.numbers import coerce_optional_int, parse_sheet_number
from src.preparation.series import (
    coerce_numeric_series,
    is_missing_value,
)
from src.types import ABSParsedSheet, ABSPreparedSheet, Folder, NumericValue


def prepare_abs_sheet(
    folder: Folder, source_file: str, sheet_name: str
) -> ABSPreparedSheet:
    parsed_sheet = parse_abs_sheet(folder, source_file, sheet_name)
    return prepare_abs_parsed_sheet(parsed_sheet)


def prepare_abs_parsed_sheet(parsed_sheet: ABSParsedSheet) -> ABSPreparedSheet:
    cleaned_metadata = clean_metadata_sections(
        parsed_sheet.metadata,
        text_cleaner=_clean_abs_text,
    )

    cleaned_records: list[pd.DataFrame] = []

    for subtable in parsed_sheet.subtables:
        if subtable.parsed_table.empty:
            continue

        records = _normalise_abs_records(subtable.parsed_table)
        cleaned_records.append(records)

    if not cleaned_records:
        raise EmptyTableError("The parsed ABS subtables")

    combined_records = pd.concat(cleaned_records, ignore_index=True)
    prepared = _prepare_normalised_abs_records(combined_records)

    return ABSPreparedSheet(
        source_file=parsed_sheet.source_file,
        sheet_name=parsed_sheet.sheet_name,
        table_number=parsed_sheet.table_number,
        title=parsed_sheet.title,
        table=prepared,
        metadata=cleaned_metadata,
    )


def _prepare_normalised_abs_records(records: pd.DataFrame) -> pd.DataFrame:
    australia_records = _keep_australia_aggregate_rows(records)
    row_hierarchy = _build_abs_row_hierarchy(australia_records)
    hierarchical_records = _attach_abs_row_hierarchy(australia_records, row_hierarchy)
    return _pivot_measurements_to_schema(hierarchical_records)


def clean_abs_display_text(value: object) -> Optional[str]:
    text = clean_source_text(value, missing_text_values=ABS_EMPTY_TEXT_VALUES)
    if text is None:
        return None

    text = ABS_TRAILING_FOOTNOTE_PATTERN.sub("", text).strip()

    year_match = ABS_WHOLE_YEAR_DECIMAL_PATTERN.fullmatch(text)
    if year_match is not None:
        text = year_match.group("year")

    return text or None


def parse_abs_number(value: object) -> Optional[NumericValue]:
    return parse_sheet_number(
        value,
        trailing_note_pattern=ABS_TRAILING_FOOTNOTE_PATTERN,
    )


def _normalise_abs_records(records: pd.DataFrame) -> pd.DataFrame:
    normalised_records = records.copy()
    normalised_records.columns = [
        clean_column_name(column, text_cleaner=_clean_abs_text)
        for column in normalised_records.columns
    ]

    _fail_if_duplicate_columns(normalised_records)

    for column in normalised_records.columns:
        column_series = cast(pd.Series, normalised_records[column])
        normalised_records[column] = _normalise_abs_series(
            column_series,
            column_name=column,
        )

    normalised_records = normalised_records.dropna(axis=0, how="all").reset_index(
        drop=True
    )
    if normalised_records.empty:
        raise EmptyTableError("The cleaned ABS table")

    return normalised_records


def _normalise_abs_series(series: pd.Series, *, column_name: str) -> pd.Series:
    if column_name == "value":
        cleaned_series = series.map(
            lambda value: clean_missing_text_value(
                value,
                missing_text_values=MISSING_TEXT_VALUES,
            )
        )
        return coerce_numeric_series(
            cleaned_series,
            column_name=column_name,
            number_parser=parse_abs_number,
        )

    if column_name == "value_text":
        return series.map(
            lambda value: clean_source_text(
                value,
                missing_text_values=ABS_EMPTY_TEXT_VALUES,
            )
        ).astype("string")

    if column_name in {"is_suppressed", "is_not_available"}:
        cleaned_series = series.map(
            lambda value: clean_text_value(value, text_cleaner=_clean_abs_text)
        )
        return cleaned_series.astype("boolean")

    return clean_text_or_numeric_series(
        series,
        column_name=column_name,
        text_cleaner=_clean_abs_text,
        number_parser=parse_abs_number,
    )


def _keep_australia_aggregate_rows(records: pd.DataFrame) -> pd.DataFrame:
    header_columns = _find_column_header_fields(records)
    if not header_columns:
        raise ValueError(
            "Could not identify ABS column header fields needed to find Australia."
        )

    australia_mask = records.apply(
        _row_is_australia_aggregate,
        axis=1,
        header_columns=header_columns,
    )
    if not bool(australia_mask.any()):
        raise ValueError(
            "Could not identify an Australia aggregate column in the ABS parsed table."
        )

    return records.loc[australia_mask].reset_index(drop=True)


def _find_column_header_fields(records: pd.DataFrame) -> list[str]:
    return sorted(
        column
        for column in records.columns
        if column == "column_header" or column.startswith("column_header_")
    )


def _row_is_australia_aggregate(
    row: pd.Series,
    *,
    header_columns: list[str],
) -> bool:
    header_tokens = _collect_header_tokens(row, header_columns)

    if not any(token in ABS_AUSTRALIA_HEADER_TOKENS for token in header_tokens):
        return False

    non_australia_tokens = [
        token for token in header_tokens if token not in ABS_AUSTRALIA_HEADER_TOKENS
    ]
    return all(token in ABS_TOTAL_HEADER_TOKENS for token in non_australia_tokens)


def _collect_header_tokens(
    row: pd.Series,
    header_columns: list[str],
) -> list[str]:
    tokens: list[str] = []

    for column in header_columns:
        text = _clean_abs_text(row[column])
        if text is None:
            continue

        for part in text.split("|"):
            token = part.strip().casefold().rstrip(".")
            if token:
                tokens.append(token)

    return tokens


def _build_abs_row_hierarchy(records: pd.DataFrame) -> pd.DataFrame:
    _require_columns(
        records,
        set(ABS_ROW_IDENTITY_COLUMNS),
    )

    row_hierarchy = (
        records.loc[:, ABS_ROW_IDENTITY_COLUMNS]
        .drop_duplicates()
        .sort_values("source_row")
        .reset_index(drop=True)
    )
    row_hierarchy["row_level"] = pd.NA
    row_hierarchy["row_parent"] = pd.NA
    row_hierarchy["row_path"] = pd.NA

    group_columns = ["table_number", "subject", "row_group"]
    for _, group in row_hierarchy.groupby(group_columns, dropna=False, sort=False):
        row_stack: list[str] = []

        for row_index, row in group.sort_values("source_row").iterrows():
            if is_missing_value(row["row_label"]):
                continue

            row_label = str(row["row_label"])
            row_indent = coerce_optional_int(row["row_indent"]) or 0
            group_indent = coerce_optional_int(row["row_group_indent"])
            if group_indent is None:
                group_indent = row_indent - 1

            row_level = max(row_indent - group_indent - 1, 0)
            row_parent = (
                row_stack[row_level - 1]
                if row_level > 0 and len(row_stack) >= row_level
                else None
            )
            row_path = " > ".join([*row_stack[:row_level], row_label])

            if len(row_stack) <= row_level:
                row_stack.extend([""] * (row_level - len(row_stack) + 1))

            row_stack[row_level] = row_label
            row_stack = row_stack[: row_level + 1]

            row_hierarchy.at[row_index, "row_level"] = row_level
            row_hierarchy.at[row_index, "row_parent"] = row_parent
            row_hierarchy.at[row_index, "row_path"] = row_path

    if bool(row_hierarchy["row_level"].isna().any()):
        raise ValueError("Could not build an ABS row hierarchy for every prepared row.")

    row_hierarchy["row_level"] = pd.array(
        row_hierarchy["row_level"].tolist(),
        dtype=pd.Int64Dtype(),
    )
    row_hierarchy["row_parent"] = row_hierarchy["row_parent"].astype("string")
    row_hierarchy["row_path"] = row_hierarchy["row_path"].astype("string")

    return row_hierarchy


def _attach_abs_row_hierarchy(
    records: pd.DataFrame,
    row_hierarchy: pd.DataFrame,
) -> pd.DataFrame:
    hierarchy_columns = [
        *ABS_ROW_IDENTITY_COLUMNS,
        "row_level",
        "row_parent",
        "row_path",
    ]

    hierarchical_records = records.merge(
        row_hierarchy.loc[:, hierarchy_columns],
        on=ABS_ROW_IDENTITY_COLUMNS,
        how="left",
        validate="many_to_one",
    )
    if bool(hierarchical_records["row_level"].isna().any()):
        raise ValueError("Could not attach an ABS row hierarchy to every record.")

    return hierarchical_records


def _pivot_measurements_to_schema(records: pd.DataFrame) -> pd.DataFrame:
    _require_columns(
        records,
        {
            "table_number",
            "subject",
            "row_group",
            "row_level",
            "row_parent",
            "row_label",
            "row_path",
            "measurement",
            "value",
            "is_suppressed",
            "is_not_available",
        },
    )

    pivot_source = records.copy()
    pivot_source["_record_order"] = range(len(pivot_source))
    pivot_source["measurement"] = pivot_source["measurement"].map(
        _normalise_measurement_name
    )

    _fail_if_unexpected_measurements(pivot_source)
    _fail_if_duplicate_measurement_rows(pivot_source)

    values = _pivot_measurement_values(pivot_source)
    flags = _pivot_measurement_flags(pivot_source)
    row_order = _pivot_row_order(pivot_source)

    prepared = (
        values.merge(flags, on=ABS_PREPARED_INDEX_COLUMNS, how="left")
        .merge(row_order, on=ABS_PREPARED_INDEX_COLUMNS, how="left")
        .sort_values("_record_order")
        .drop(columns="_record_order")
        .reset_index(drop=True)
    )

    prepared["row_parent"] = (
        prepared["row_parent"].replace(ABS_NO_PARENT_SENTINEL, pd.NA).astype("string")
    )
    prepared["is_suppressed"] = prepared["is_suppressed"].fillna(False).astype(bool)
    prepared["is_not_available"] = (
        prepared["is_not_available"].fillna(False).astype(bool)
    )

    return _select_abs_prepared_schema(prepared)


def _pivot_measurement_values(pivot_source: pd.DataFrame) -> pd.DataFrame:
    values = (
        pivot_source.set_index(ABS_PREPARED_INDEX_COLUMNS + ["measurement"])["value"]
        .unstack("measurement")
        .reset_index()
    )

    for column in ABS_MEASUREMENT_COLUMNS:
        if column not in values.columns:
            values[column] = pd.NA

        values[column] = coerce_numeric_series(
            cast(pd.Series, values[column]),
            column_name=column,
            number_parser=parse_abs_number,
        )

    return values


def _pivot_measurement_flags(pivot_source: pd.DataFrame) -> pd.DataFrame:
    return (
        pivot_source.groupby(
            ABS_PREPARED_INDEX_COLUMNS,
            dropna=False,
            sort=False,
        )[["is_suppressed", "is_not_available"]]
        .any()
        .reset_index()
    )


def _pivot_row_order(pivot_source: pd.DataFrame) -> pd.DataFrame:
    return (
        pivot_source.groupby(
            ABS_PREPARED_INDEX_COLUMNS,
            dropna=False,
            sort=False,
        )["_record_order"]
        .min()
        .reset_index()
    )


def _normalise_measurement_name(value: object) -> object:
    if is_missing_value(value):
        return pd.NA

    measurement = str(value)
    return ABS_MEASUREMENT_ALIASES.get(measurement, measurement)


def _fail_if_unexpected_measurements(pivot_source: pd.DataFrame) -> None:
    unexpected_measurements = sorted(
        set(pivot_source["measurement"].dropna()) - set(ABS_MEASUREMENT_COLUMNS)
    )
    if unexpected_measurements:
        raise ValueError(
            "ABS measurements cannot fit the prepared schema: "
            + ", ".join(unexpected_measurements)
        )


def _fail_if_duplicate_measurement_rows(pivot_source: pd.DataFrame) -> None:
    pivot_source["row_parent"] = pivot_source["row_parent"].fillna(
        ABS_NO_PARENT_SENTINEL
    )

    duplicate_mask = pivot_source.duplicated(
        ABS_PREPARED_INDEX_COLUMNS + ["measurement"],
        keep=False,
    )
    if not bool(duplicate_mask.any()):
        return

    duplicate_rows = pivot_source.loc[
        duplicate_mask,
        ABS_PREPARED_INDEX_COLUMNS + ["measurement"],
    ]
    raise ValueError(
        "ABS Australia values are not unique after filtering; "
        "the prepared schema cannot represent remaining column dimensions. "
        f"Example duplicate: {duplicate_rows.iloc[0].to_dict()}"
    )


def _select_abs_prepared_schema(prepared: pd.DataFrame) -> pd.DataFrame:
    missing_columns = [
        column for column in ABS_PREPARED_SCHEMA if column not in prepared.columns
    ]
    extra_columns = [
        column for column in prepared.columns if column not in ABS_PREPARED_SCHEMA
    ]

    if missing_columns or extra_columns:
        message_parts: list[str] = []
        if missing_columns:
            message_parts.append(f"missing columns: {missing_columns}")
        if extra_columns:
            message_parts.append(f"unexpected columns: {extra_columns}")

        raise ValueError("ABS prepared schema mismatch; " + "; ".join(message_parts))

    return prepared.loc[:, ABS_PREPARED_SCHEMA].reset_index(drop=True)


def _fail_if_duplicate_columns(records: pd.DataFrame) -> None:
    if not records.columns.has_duplicates:
        return

    duplicates = {
        column
        for column, is_duplicate in zip(
            records.columns,
            records.columns.duplicated(),
        )
        if is_duplicate
    }
    raise ValueError(
        f"ABS column cleaning produced duplicate columns: {join_sorted(duplicates)}"
    )


def _require_columns(records: pd.DataFrame, columns: set[str]) -> None:
    missing_columns = sorted(columns - set(records.columns))
    if missing_columns:
        raise ValueError(f"ABS parsed table is missing columns: {missing_columns}")


def _clean_abs_text(value: object) -> Optional[str]:
    text = clean_abs_display_text(value)
    if text is None:
        return None

    return clean_text(text, missing_text_values=ABS_DISPLAY_MISSING_TEXT_VALUES)
