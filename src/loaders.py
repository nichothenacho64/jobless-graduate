from pathlib import Path
from typing import Optional, cast

import pandas as pd

from src.constants import RAW_DIR, RAW_DIR_LOOKUP
from src.parsers.constants import SPREADSHEET_SUFFIXES
from src.exceptions import (
    RawFolderDirectoryError,
    RawFolderNotFoundError,
    SheetNotFoundError,
    SpreadsheetFormatError,
    SpreadsheetNotFoundError,
)
from src.types import Folder

def resolve_folder_path(folder: Folder) -> Path:  # ! for both folders or path objects
    if isinstance(folder, Path):
        folder_path = folder
    else:
        folder_path = RAW_DIR_LOOKUP.get(folder, RAW_DIR / folder)

    if not folder_path.exists():
        raise RawFolderNotFoundError(folder_path, RAW_DIR_LOOKUP)

    if not folder_path.is_dir():
        raise RawFolderDirectoryError(folder_path)

    return folder_path

def resolve_spreadsheet_path(folder: Folder, file_name: str) -> Path:
    folder_path = resolve_folder_path(folder)
    file_path = folder_path / file_name

    if not file_path.exists():
        raise SpreadsheetNotFoundError(file_path)

    if file_path.suffix.lower() not in SPREADSHEET_SUFFIXES:
        raise SpreadsheetFormatError(file_path.suffix, SPREADSHEET_SUFFIXES)

    return file_path

def open_excel_file(folder: Folder, file_name: str) -> tuple[Path, pd.ExcelFile]:
    file_path = resolve_spreadsheet_path(folder, file_name)
    excel_file = pd.ExcelFile(file_path)
    return file_path, excel_file

def list_excel_sheets(folder: Folder, file_name: str) -> list[str]:
    _, excel_file = open_excel_file(folder, file_name)
    return cast(list[str], excel_file.sheet_names)

def load_excel_sheet(
    folder: Folder,
    file_name: str,
    sheet_name: str,
    *,
    header: Optional[int] = 0,
) -> pd.DataFrame:
    file_path, excel_file = open_excel_file(folder, file_name)

    sheet_names = cast(list[str], excel_file.sheet_names)

    if sheet_name not in sheet_names:
        raise SheetNotFoundError(sheet_name, file_path.name, sheet_names)

    return excel_file.parse(sheet_name=sheet_name, header=header)
