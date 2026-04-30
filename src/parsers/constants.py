from __future__ import annotations

import re

SHEET_WHITESPACE_PATTERN = re.compile(r"\s+")

COLUMN_NAME_NON_ALNUM_PATTERN = re.compile(r"[^0-9A-Za-z]+")
COLUMN_NAME_UNDERSCORE_PATTERN = re.compile(r"_+")

UNNAMED_HEADER_LABEL = "unnamed_header"

QILT_YEAR_PATTERN = re.compile(r"\b20\d{2}\b")

QILT_TITLE_ROW_INDEX = 0
QILT_HEADER_SEARCH_START_ROW = 3
QILT_HEADER_SEARCH_END_ROW_EXCLUSIVE = 8

QILT_SINGLE_METRIC_EXPECTED_ROW_COUNT = 1
QILT_METRIC_ROWS_MAX_ROW_COUNT = 5

QILT_METADATA_LABELS = {
    "Column variables:",
    "Column filters:",
    "Column notes:",
    "Row variables:",
    "Row notes:",
    "Row filters:",
}

QILT_PARTICIPATING_INSTITIONS_LINE = "No. of participating institutions"
