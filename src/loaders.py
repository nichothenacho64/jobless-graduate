from pathlib import Path

# TODO: First before other files

"""
- Define the path for raw files from QILT, ABS, and ACEN directories
- Describe supported input formats such as CSV, XLSX, ODS (but not PDFS)
- Return loaded tables with Pandas dataframes
- Note where to add helper wrappers for reading and writing tables
"""

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
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
    RAW_DIR / "ACEN",
]

RAW_SOURCE_DIRS = {
    "qilt": QILT_RAW_DIRS,
    "abs": ABS_RAW_DIRS,
    "acen": ACEN_RAW_DIRS,
}
