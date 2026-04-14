from pathlib import Path
from collections.abc import Iterable
import re

FOLDER_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = FOLDER_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

QILT_RAW_DIR = RAW_DIR / "QILT"
ABS_RAW_DIR = RAW_DIR / "ABS"
ABS_EXTRAS_RAW_DIR = ABS_RAW_DIR / "Extras"

SPREADSHEET_SUFFIXES = {".xlsx", ".xls", ".xlsm", ".ods"}

QILT_2024_GOS_FILE_NAME = "2024_GOS_National_Report_Tables.xlsx"
QILT_2024_GOS_L_FILE_NAME = "2024_GOS-L_National_Report_Tables.xlsx"

ABS_TABLE_PATTERN = re.compile(r"\bT(?P<START>\d+)(?:_T(?P<END>\d+))?\b", re.IGNORECASE)

def join_sorted(values: Iterable[object]) -> str:
    return ", ".join(sorted(str(value) for value in values))

def _normalise_file_stem(stem: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", stem.upper()).strip("-")

def _abs_source_key(file_path: Path) -> str:
    table_match = ABS_TABLE_PATTERN.search(file_path.stem)
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


def _collect_abs_source_files(abs_directory: Path) -> dict[str, str]:
    abs_files: dict[str, str] = {}
    file_paths = sorted(abs_directory.iterdir())
    
    for file_path in file_paths:
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in SPREADSHEET_SUFFIXES:
            continue

        source_key = _abs_source_key(file_path)
        abs_files[source_key] = file_path.name

    return abs_files

RAW_SOURCE_DIRS: dict[str, dict[str, str]] = {
    "QILT": {
        "QILT-2024-GOS": QILT_2024_GOS_FILE_NAME,
        "QILT-2024-GOS-L": QILT_2024_GOS_L_FILE_NAME,
    },
    "ABS": _collect_abs_source_files(ABS_RAW_DIR),
    "ABS_EXTRAS": {
        # ?? for later files
    },
}

RAW_DIR_LOOKUP: dict[str, Path] = {
    QILT_RAW_DIR.name: QILT_RAW_DIR,
    ABS_RAW_DIR.name: ABS_RAW_DIR,
    ABS_EXTRAS_RAW_DIR.name: ABS_EXTRAS_RAW_DIR,
    "qilt": QILT_RAW_DIR,
    "abs": ABS_RAW_DIR,
    "abs_extras": ABS_EXTRAS_RAW_DIR,
}
