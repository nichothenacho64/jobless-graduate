from __future__ import annotations

from pathlib import Path

from src.sources import find_abs_source_files

FOLDER_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = FOLDER_DIR / "assets"
DATA_DIR = FOLDER_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

QILT_RAW_DIR = RAW_DIR / "QILT"
ABS_RAW_DIR = RAW_DIR / "ABS"
ABS_EXTRAS_RAW_DIR = ABS_RAW_DIR / "Extras"

QILT_2024_GOS_FILE_NAME = "2024_GOS_National_Report_Tables.xlsx"
QILT_2024_GOS_L_FILE_NAME = "2024_GOS-L_National_Report_Tables.xlsx"

RAW_SOURCE_DIRS: dict[str, dict[str, str]] = {
    "QILT": {
        "QILT-2024-GOS": QILT_2024_GOS_FILE_NAME,
        "QILT-2024-GOS-L": QILT_2024_GOS_L_FILE_NAME,
    },
    "ABS": find_abs_source_files(ABS_RAW_DIR),
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
