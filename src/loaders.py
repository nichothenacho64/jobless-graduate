from src.exceptions import (
    RawFolderNotFoundError,
    RawFolderDirectoryError,
    SpreadsheetNotFoundError,
    SpreadsheetFormatError,
    SheetNotFoundError,
)

from src.utils import (
    RAW_DIR,
    RAW_DIR_LOOKUP,
    SUPPORTED_SPREADSHEET_SUFFIXES,
)

from src.utils import join_sorted

from pathlib import Path
import pandas as pd

def resolve_folder_path(folder: str | Path) -> Path: # ! for both folders or path objects
    if isinstance(folder, Path):
        folder_path = folder
    else:
        folder_path = RAW_DIR_LOOKUP.get(folder, RAW_DIR / folder)

    if not folder_path.exists():
        known_folders = join_sorted(RAW_DIR_LOOKUP)
        raise RawFolderNotFoundError(folder_path, known_folders)

    if not folder_path.is_dir():
        raise RawFolderDirectoryError(folder_path)

    return folder_path

def load_excel_sheet(
    folder: str | Path,
    file_name: str,
    sheet_name: str,
) -> pd.DataFrame:
    folder_path = resolve_folder_path(folder)
    file_path = folder_path / file_name

    if not file_path.exists():
        raise SpreadsheetNotFoundError(file_path)

    if file_path.suffix.lower() not in SUPPORTED_SPREADSHEET_SUFFIXES:
        supported_formats = join_sorted(SUPPORTED_SPREADSHEET_SUFFIXES)
        raise SpreadsheetFormatError(file_path.suffix, supported_formats)

    excel_file = pd.ExcelFile(file_path)

    if sheet_name not in excel_file.sheet_names:
        available_sheets = join_sorted(excel_file.sheet_names)
        raise SheetNotFoundError(sheet_name, file_path.name, available_sheets)

    return pd.read_excel(file_path, sheet_name=sheet_name)

# TODO: later implementation
# get all sheet names inside of a spreadsheet (helper function)
