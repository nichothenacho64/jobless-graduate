from pathlib import Path
from typing import Optional, cast

import pandas as pd

from src.parsers.constants import ABS_TABLE_SOURCE_KEY_PATTERN
from src.sources import (
    ABS_FOLDER_NAME,
    QILT_2024_GOS_L_SOURCE,
    QILT_2024_GOS_SOURCE,
    QILT_FOLDER_NAME,
    RAW_DIR,
    RAW_DIR_LOOKUP,
    RAW_SOURCE_DIRS,
    SPREADSHEET_SUFFIXES,
)
from src.exceptions import (
    ABSSheetSourceError,
    RawFolderDirectoryError,
    RawFolderNotFoundError,
    SheetNotFoundError,
    SheetNumberNotFoundError,
    SpreadsheetFormatError,
    SpreadsheetNotFoundError,
)
from src.types import ExcelSheet, Folder

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

def initialise_gos_sheet(sheet_number: int) -> ExcelSheet:
    return _initialise_qilt_sheet(QILT_2024_GOS_SOURCE, sheet_number)

def initialise_gos_l_sheet(sheet_number: int) -> ExcelSheet:
    return _initialise_qilt_sheet(QILT_2024_GOS_L_SOURCE, sheet_number)

def initialise_abs_sheet(sheet_number: int) -> ExcelSheet:
    for data_source in RAW_SOURCE_DIRS[ABS_FOLDER_NAME]:
        match = ABS_TABLE_SOURCE_KEY_PATTERN.fullmatch(data_source)
        if match is None:
            continue

        first_sheet = int(match.group("START"))
        last_sheet = int(match.group("END") or first_sheet)
        if first_sheet <= sheet_number <= last_sheet:
            return ExcelSheet(
                folder=ABS_FOLDER_NAME,
                data_source=data_source,
                sheet_name=f"Table {sheet_number}",
            )

    raise ABSSheetSourceError(
        sheet_number,
        RAW_SOURCE_DIRS[ABS_FOLDER_NAME],
    )

def _initialise_qilt_sheet(data_source: str, sheet_number: int) -> ExcelSheet:
    file_name = RAW_SOURCE_DIRS[QILT_FOLDER_NAME][data_source]
    sheet_names = list_excel_sheets(QILT_FOLDER_NAME, file_name)

    if sheet_number < 0 or sheet_number >= len(sheet_names):
        raise SheetNumberNotFoundError(sheet_number, data_source, len(sheet_names))

    sheet_name = sheet_names[sheet_number]

    return ExcelSheet(
        folder=QILT_FOLDER_NAME,
        data_source=data_source,
        sheet_name=sheet_name,
    )
