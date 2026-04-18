from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, Optional

import pandas as pd

from src.constants.files import RAW_SOURCE_DIRS

type Folder = str | Path
type NumericValue = int | float
type Metadata = dict[str, list[str]]
type NullableNumericDtype = pd.Int64Dtype | pd.Float64Dtype

type QILTTableKind = Literal[
    "collection_summary",
    "transition_matrix",
    "single_metric_time_series",
    "metric_rows",
    "wide_multi_year",
    "wide_table",
]

type NumericConverter = Callable[[NumericValue], NumericValue]
type TextCleaner = Callable[[object], Optional[str]]
type NumberParser = Callable[[object], Optional[NumericValue]]

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
    classification: str
    table: pd.DataFrame
    metadata: Metadata
