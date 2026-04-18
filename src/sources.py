from __future__ import annotations

import re
from pathlib import Path

from src.constants.parsing import SPREADSHEET_SUFFIXES

def _normalise_file_stem(stem: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", stem.upper()).strip("-")

def _find_abs_source_key(file_path: Path) -> str:
    abs_table_pattern = re.compile(r"\bT(?P<START>\d+)(?:_T(?P<END>\d+))?\b", re.IGNORECASE)
    
    table_match = abs_table_pattern.search(file_path.stem)
    if table_match is not None:
        start_table = int(table_match.group("START"))
        end_table = table_match.group("END")
        if end_table is None:
            return f"SWE-T{start_table}"

        end_table = int(end_table)
        return f"SWE-T{start_table}-{end_table}"

    if "DIL" in file_path.stem.upper():
        return "SWE-DIL"

    return f"SWE-{_normalise_file_stem(file_path.stem)}"

def find_abs_source_files(abs_directory: Path) -> dict[str, str]:
    if not abs_directory.exists() or not abs_directory.is_dir():
        return {}

    allowed_suffixes = {suffix.lower() for suffix in SPREADSHEET_SUFFIXES}
    abs_files: dict[str, str] = {}

    for file_path in sorted(abs_directory.iterdir()):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in allowed_suffixes:
            continue

        source_key = _find_abs_source_key(file_path)
        abs_files[source_key] = file_path.name

    return abs_files
