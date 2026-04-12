from typing import Iterable
from pathlib import Path
from pprint import pprint

FOLDER_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = FOLDER_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

QILT_RAW_DIRS = [
    RAW_DIR / "2024_GOS_National_Report_Tables",
    RAW_DIR / "2024_GOS-L_National_Report_Tables",
]

ABS_RAW_DIRS = [
    RAW_DIR / "2025_Education_and_work",
    RAW_DIR / "SEW_2011_to_2025",
]

ACEN_RAW_DIRS = [
    RAW_DIR / "ACEN",  # ?? a placeholder for now
]

RAW_SOURCE_DIRS = {
    "qilt": QILT_RAW_DIRS,
    "abs": ABS_RAW_DIRS,
    "acen": ACEN_RAW_DIRS,
}

# TODO: change for more specific referencing
# which file is which is unclear using dictionary keys 

RAW_DIR_LOOKUP: dict[str, Path] = {}
SUPPORTED_SPREADSHEET_SUFFIXES = {".xlsx", ".xls", ".xlsm", ".ods"}

for directories in RAW_SOURCE_DIRS.values():
    for directory in directories:
        RAW_DIR_LOOKUP[directory.name] = directory

def join_sorted(values: Iterable[object]) -> str:
    return ", ".join(sorted(str(value) for value in values))
