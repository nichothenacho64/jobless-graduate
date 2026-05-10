from __future__ import annotations

import re
from pathlib import Path

QILT_FOLDER_NAME = "QILT"
ABS_FOLDER_NAME = "ABS"
ABS_EXTRAS_FOLDER_NAME = "Extras"
ABS_EXTRAS_FOLDER_KEY = "ABS_EXTRAS"

QILT_FOLDER_ALIAS = "qilt"
ABS_FOLDER_ALIAS = "abs"
ABS_EXTRAS_FOLDER_ALIAS = "abs_extras"

QILT_2024_GOS_SOURCE = "QILT-2024-GOS"
QILT_2024_GOS_L_SOURCE = "QILT-2024-GOS-L"

FOLDER_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = FOLDER_DIR / "assets"
DATA_DIR = FOLDER_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

QILT_RAW_DIR = RAW_DIR / QILT_FOLDER_NAME
ABS_RAW_DIR = RAW_DIR / ABS_FOLDER_NAME
ABS_EXTRAS_RAW_DIR = ABS_RAW_DIR / ABS_EXTRAS_FOLDER_NAME

QILT_2024_GOS_FILE_NAME = "2024_GOS_National_Report_Tables.xlsx"
QILT_2024_GOS_L_FILE_NAME = "2024_GOS-L_National_Report_Tables.xlsx"

SPREADSHEET_SUFFIXES = {".xlsx", ".xls", ".xlsm", ".ods"}

def _find_abs_source_key(file_path: Path) -> str:
    abs_table_pattern = re.compile(r"\bT(?P<START>\d+)(?:_T(?P<END>\d+))?\b", re.IGNORECASE)
    
    table_match = abs_table_pattern.search(file_path.stem)
    if table_match is not None:
        start_table = int(table_match.group("START"))
        end_table = table_match.group("END")
        if end_table is None:
            return f"SEW-T{start_table}"

        end_table = int(end_table)
        return f"SEW-T{start_table}-{end_table}"

    if "DIL" in file_path.stem.upper():
        return "SEW-DIL"

    normalised_file_stem = re.sub(r"[^A-Z0-9]+", "-", file_path.stem.upper()).strip("-")
    return f"SEW-{normalised_file_stem}"

def find_abs_source_files(abs_directory: Path) -> dict[str, str]:
    if not abs_directory.exists() or not abs_directory.is_dir():
        return {}

    allowed_suffixes = {suffix.lower() for suffix in SPREADSHEET_SUFFIXES}
    abs_files: dict[str, str] = {}

    for file_path in sorted(abs_directory.iterdir()):
        if not file_path.is_file():
            continue
        if file_path.name.startswith("~$"):
            continue
        if file_path.suffix.lower() not in allowed_suffixes:
            continue

        source_key = _find_abs_source_key(file_path)
        abs_files[source_key] = file_path.name

    return abs_files

RAW_SOURCE_DIRS: dict[str, dict[str, str]] = {
    QILT_FOLDER_NAME: {
        QILT_2024_GOS_SOURCE: QILT_2024_GOS_FILE_NAME,
        QILT_2024_GOS_L_SOURCE: QILT_2024_GOS_L_FILE_NAME,
    },
    ABS_FOLDER_NAME: find_abs_source_files(ABS_RAW_DIR),
}

RAW_DIR_LOOKUP: dict[str, Path] = {
    QILT_RAW_DIR.name: QILT_RAW_DIR,
    ABS_RAW_DIR.name: ABS_RAW_DIR,
    ABS_EXTRAS_RAW_DIR.name: ABS_EXTRAS_RAW_DIR,
    QILT_FOLDER_ALIAS: QILT_RAW_DIR,
    ABS_FOLDER_ALIAS: ABS_RAW_DIR,
    ABS_EXTRAS_FOLDER_ALIAS: ABS_EXTRAS_RAW_DIR,
}
