from __future__ import annotations

import re

SHEET_NUMBER_PATTERN = re.compile(r"(?P<sign>-)?(?P<number>\d+(?:\.\d+)?)")

QILT_FOOTNOTE_SYMBOLS = r"[*†‡]+"
QILT_FOOTNOTE_SYMBOL_PATTERN = re.compile(QILT_FOOTNOTE_SYMBOLS)
QILT_TRAILING_FOOTNOTE_PATTERN = re.compile(rf"{QILT_FOOTNOTE_SYMBOLS}$")

ABS_RELIABILITY_MARKERS = frozenset({"*", "**", "#"})
ABS_RELIABILITY_MARKER_PATTERN = re.compile(
    r"(?:\*\*|\*|#)(?=\s*(?:\([a-z]\)\s*)*$)",
    re.IGNORECASE,
)
MISSING_TEXT_VALUES = frozenset({"", "-", "—", "–", "..", "...", "n/a", "na", "n.p.", "n/p", "np"  "nil"})

ABS_TRAILING_FOOTNOTE_PATTERN = re.compile(
    r"(?:\s*\([a-z]\))+(?=\s*(?:$|\|))",
    re.IGNORECASE,
)
ABS_VALUE_TRAILING_NOTE_PATTERN = re.compile(
    r"(?:\s*\([a-z]\)|\s*(?:\*\*|\*|#))+$",
    re.IGNORECASE,
)
ABS_WHOLE_YEAR_DECIMAL_PATTERN = re.compile(r"^(?P<year>\d{4})\.0$")

ABS_PREPARED_SCHEMA = [
    "subject",
    "row_group",
    "row_level",
    "row_parent",
    "row_label",
    "row_path",
    "estimate_count",
    "proportion_percent",
    "rse_estimate_percent",
    "margin_error_proportion",
    "is_reliable",
    "is_suppressed",
    "is_not_available",
]

ABS_MEASUREMENT_COLUMNS = [
    "estimate_count",
    "proportion_percent",
    "rse_estimate_percent",
    "margin_error_proportion",
]
ABS_MEASUREMENT_ALIASES = {
    "moe_proportion_pp": "margin_error_proportion",
    "rse_proportion_percent": "rse_estimate_percent",
}
ABS_PREPARED_INDEX_COLUMNS = [
    "subject",
    "row_group",
    "row_level",
    "row_parent",
    "row_label",
    "row_path",
]
ABS_ROW_IDENTITY_COLUMNS = [
    "table_number",
    "subject",
    "row_group",
    "row_label",
    "row_indent",
    "row_group_indent",
    "source_row",
]
ABS_EMPTY_TEXT_VALUES = frozenset({""})
ABS_DISPLAY_MISSING_TEXT_VALUES = MISSING_TEXT_VALUES - frozenset({"np", "na"})
ABS_AUSTRALIA_HEADER_TOKENS = frozenset({"aust", "australia"})
ABS_TOTAL_HEADER_TOKENS = frozenset({"all", "all persons", "persons", "total"})
ABS_NO_PARENT_SENTINEL = "__ABS_NO_PARENT__"
