from __future__ import annotations

import re

QILT_FOOTNOTE_SYMBOLS = r"[*†‡]+"
QILT_FOOTNOTE_SYMBOL_PATTERN = re.compile(QILT_FOOTNOTE_SYMBOLS)
QILT_TRAILING_FOOTNOTE_PATTERN = re.compile(rf"{QILT_FOOTNOTE_SYMBOLS}$")
QILT_YEAR_PATTERN = re.compile(r"\b20\d{2}\b")

QILT_TITLE_ROW_INDEX = 0
QILT_HEADER_SEARCH_START_ROW = 3
QILT_HEADER_SEARCH_END_ROW_EXCLUSIVE = 8

QILT_SINGLE_METRIC_EXPECTED_ROW_COUNT = 1
QILT_METRIC_ROWS_MAX_ROW_COUNT = 5

GOS_SUBGROUP_SHEET_NAME = "EMP_UG_ALL_2Y_DG"
GOS_L_SUBGROUP_SHEET_NAME = "STMT_UG_ALL_1Y_SG"
TOTAL_ROW_GROUP = "Total"

GOS_SOURCE_LABEL = "GOS"
GOS_L_SOURCE_LABEL = "GOS-L"

QILT_MISSING_TEXT_VALUES = frozenset(
    {"", "-", "—", "–", "..", "...", "n/a", "na", "n.p.", "n/p", "np", "nil"}
)

QILT_METADATA_LABELS = {
    "Column variables:",
    "Column filters:",
    "Column notes:",
    "Row variables:",
    "Row notes:",
    "Row filters:",
}

QILT_PARTICIPATING_INSTITIONS_LINE = "No. of participating institutions"

GOS_SHORT_TERM_COMPARISON_COLUMNS = {
    "short_term_full_time_employment": "full_time_employment_2024",
    "short_term_overall_employment": "overall_employment_2024",
    "short_term_labour_force_participation": "labour_force_participation_rate_2024",
}

GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS = {
    "medium_term_full_time_employment": "medium_term_full_time_employed",
    "medium_term_overall_employment": "medium_term_overall_employed",
    "medium_term_labour_force_participation": "medium_term_labour_force_participation",
}

QILT_SUBGROUP_TEXT_EQUIVALENTS = {
    "30 years or under": "30 and under",
    "Over 30 years": "Over 30",
    "Internal/Mixed study mode": "Internal/Mixed",
    "External study mode": "External",
    "Language other than English": "Other",
}

SUBGROUP_LONG_OUTCOME_SPECS: tuple[tuple[str, str, str, str], ...] = (
    (
        "full_time_employment",
        "short_term_full_time_employment",
        "medium_term_full_time_employment",
        "full_time_employment_change",
    ),
    (
        "overall_employment",
        "short_term_overall_employment",
        "medium_term_overall_employment",
        "overall_employment_change",
    ),
    (
        "labour_force_participation",
        "short_term_labour_force_participation",
        "medium_term_labour_force_participation",
        "labour_force_participation_change",
    ),
)

QILT_OUTCOME_TITLES = {
    "full_time_employment": "Full-time employment",
    "overall_employment": "Overall employment",
    "labour_force_participation": "Labour-force participation",
}

QILT_OUTCOME_SHORT_TITLES = {
    "full_time_employment": "Full-time",
    "overall_employment": "Overall",
    "labour_force_participation": "LFP",
}