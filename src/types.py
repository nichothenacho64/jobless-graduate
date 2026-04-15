from pathlib import Path
from typing import Literal

type Folder = str | Path

type QILTTableKind = Literal[
    "collection_summary",
    "transition_matrix",
    "single_metric_time_series",
    "metric_rows",
    "wide_multi_year",
    "wide_table",
]
