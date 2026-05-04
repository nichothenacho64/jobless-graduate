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

ABS_CONTENTS_SHEET_NAME = "Contents"
ABS_TITLE_ROW_INDEX = 2
ABS_HEADER_FIRST_ROW_INDEX = 4
ABS_FOOTER_NOTE_PATTERN = re.compile(r"^\([a-z]\)")
ABS_FOOTER_PREFIXES = ("*", "#", "©")
ABS_FOOTER_WORD_MARKERS = ("na ", "np ")
ABS_TABLE_LABEL_PATTERN = re.compile(
    r"^Table\s+(?P<NUMBER>\d+)\b\s*(?P<TITLE>.*)$",
    re.IGNORECASE,
)
ABS_TABLE_SOURCE_KEY_PATTERN = re.compile(r"^SEW-T(?P<START>\d+)(?:-(?P<END>\d+))?$")
ABS_MEASUREMENT_LABELS = {
    "Estimate ('000)": "estimate_count",
    "ESTIMATE ('000)": "estimate_count",
    "Proportion (%)": "proportion_percent",
    "Proportion (%)(a)": "proportion_percent",
    "Relative Standard Error of estimate (%)": "rse_estimate_percent",
    "Relative Standard Error of proportion (%)": "rse_estimate_percent",
    "95% Margin of Error of proportion (±)": "margin_error_proportion",
    "95% Margin of error of proportion (±)": "margin_error_proportion",
}

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
