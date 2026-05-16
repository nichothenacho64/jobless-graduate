from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, Optional, TypeVar

import numpy as np
import pandas as pd

from src.sources import RAW_SOURCE_DIRS

Folder = str | Path
NumericValue = int | float
Metadata = dict[str, list[str]]
ChartMetadata = dict[str, object]
PreparedRows = list[dict[str, object]]
NullableNumericDtype = pd.Int64Dtype | pd.Float64Dtype
SheetTitleList = list[dict[str, int | str]]
BodyRowKind = Literal["label", "values"]
NumericConverter = Callable[[NumericValue], NumericValue]
TextCleaner = Callable[[object], Optional[str]]
NumberParser = Callable[[object], Optional[NumericValue]]
MissingValues = dict[str, list[dict[str, object]]]

QILTTableKind = Literal[
    "collection_summary",
    "transition_matrix",
    "single_metric_time_series",
    "metric_rows",
    "wide_multi_year",
    "wide_table",
]

ABSMeasurement = Literal[
    "estimate_count",
    "proportion_percent",
    "rse_estimate_percent",
    "rse_proportion_percent",
    "margin_error_proportion",
]

QILTValidationComparison = Literal[
    "one_to_one",
    "1:1",
    "one_to_many",
    "1:m",
    "many_to_one",
    "m:1",
    "many_to_many",
    "m:m",
]


@dataclass(frozen=True, slots=True)
class AxisSpec:
    minimum: float
    maximum: float
    tick_step: float

    @property
    def limits(self) -> tuple[float, float]:
        return (self.minimum, self.maximum)

    @property
    def ticks(self) -> np.ndarray:
        return np.arange(
            self.minimum,
            self.maximum + self.tick_step,
            self.tick_step,
        )


@dataclass
class ExcelSheet:
    folder: Folder
    data_source: str
    sheet_name: str

    @property
    def file_name(self) -> str:
        folder = self.folder.name if isinstance(self.folder, Path) else self.folder
        return RAW_SOURCE_DIRS[folder][self.data_source]


@dataclass(frozen=True)
class MetricComparison:
    metric_key: str
    short_term_column: str
    medium_term_column: str

    @property
    def change_column(self) -> str:
        return f"{self.metric_key}_change"


@dataclass(slots=True)
class QILTRowBounds:
    header: int
    data_first: int
    data_last: int
    footer_start: Optional[int]


@dataclass(slots=True)
class QILTParsedSheet:
    sheet_name: str
    title: str
    rows: QILTRowBounds
    classification: QILTTableKind
    table: pd.DataFrame
    metadata: Metadata


@dataclass(slots=True)
class QILTPreparedSheet:
    sheet_name: str
    title: str
    rows: QILTRowBounds
    classification: QILTTableKind
    table: pd.DataFrame
    metadata: Metadata


@dataclass(frozen=True, slots=True)
class ABSMeasurementCell:
    row: int
    col: int
    measurement: ABSMeasurement
    measurement_label: str


@dataclass(slots=True)
class ABSSourceBounds:
    row_first: int
    row_last: int
    col_first: int
    col_last: int


@dataclass(slots=True)
class ABSRowBounds:
    header_first: int
    header_last: int
    body_first: int
    body_last: int
    footer_start: Optional[int]


@dataclass(slots=True)
class ABSParsedTable:
    value_kind: ABSMeasurement
    source_measurement_label: str
    subject_label: Optional[str]
    source_bounds: ABSSourceBounds
    row_bounds: ABSRowBounds
    raw_table: pd.DataFrame
    parsed_table: pd.DataFrame


@dataclass(slots=True)
class ABSParsedSheet:
    source_file: str
    sheet_name: str
    table_number: int
    title: str
    rows: ABSRowBounds
    table: pd.DataFrame
    subtables: list[ABSParsedTable]
    metadata: Metadata


@dataclass(slots=True)
class ABSPreparedSheet:
    source_file: str
    sheet_name: str
    table_number: int
    title: str
    table: pd.DataFrame
    metadata: Metadata


PreparedSheetType = TypeVar("PreparedSheetType", QILTPreparedSheet, ABSPreparedSheet)
PreparedSheet = QILTPreparedSheet | ABSPreparedSheet
SheetPreparer = Callable[[Folder, str, str], PreparedSheetType]
