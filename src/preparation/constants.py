from __future__ import annotations

import re

SHEET_NUMBER_PATTERN = re.compile(r"(?P<sign>-)?(?P<number>\d+(?:\.\d+)?)")

QILT_FOOTNOTE_SYMBOLS = r"[*†‡]+"
QILT_FOOTNOTE_SYMBOL_PATTERN = re.compile(QILT_FOOTNOTE_SYMBOLS)
QILT_TRAILING_FOOTNOTE_PATTERN = re.compile(rf"{QILT_FOOTNOTE_SYMBOLS}$")

QILT_MISSING_TEXT_VALUES = frozenset(
    {"", "-", "—", "–", "..", "...", "n/a", "na", "n.p.", "n/p", "np", "nil"}
)
