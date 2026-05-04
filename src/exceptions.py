from collections.abc import Iterable
from pathlib import Path

from src.formatting import join_sorted


class RawFolderNotFoundError(FileNotFoundError):
    def __init__(self, folder_path: Path, known_folders: Iterable[object]):
        formatted_folders = join_sorted(known_folders)
        super().__init__(
            f"""
            Raw folder not found: {folder_path}
            Known raw folders: {formatted_folders}
            """
        )


class RawFolderDirectoryError(NotADirectoryError):
    def __init__(self, folder_path: Path):
        super().__init__(f"Expected a directory, got: {folder_path}")


class SpreadsheetNotFoundError(FileNotFoundError):
    def __init__(self, file_path: Path):
        super().__init__(f"Spreadsheet not found: {file_path}")


class SpreadsheetFormatError(ValueError):
    def __init__(self, file_suffix: str, supported_formats: Iterable[object]):
        formatted_formats = join_sorted(supported_formats)
        super().__init__(
            f"""
            Unsupported spreadsheet format: {file_suffix}
            Supported formats: {formatted_formats}
            """
        )


class SheetNotFoundError(ValueError):
    def __init__(
        self,
        sheet_name: str,
        file_name: str,
        available_sheets: Iterable[object],
    ):
        formatted_sheets = join_sorted(available_sheets)
        super().__init__(
            f"""
            Sheet not found: {sheet_name!r} in {file_name}
            Available sheets: {formatted_sheets}
            """
        )


class SheetNumberNotFoundError(ValueError):
    def __init__(self, sheet_number: int, data_source: str, sheet_count: int):
        available_range = "none" if sheet_count == 0 else f"0-{sheet_count - 1}"
        super().__init__(
            f"""
            Sheet number not found: {sheet_number} in {data_source}
            Available sheet numbers: {available_range}
            """
        )


class ABSSheetSourceError(ValueError):
    def __init__(self, sheet_number: int, available_sources: Iterable[object]):
        formatted_sources = join_sorted(available_sources)
        super().__init__(
            f"""
            Could not find an ABS workbook containing sheet {sheet_number}.
            Available ABS sources: {formatted_sources}
            """
        )


class EmptyTableError(ValueError):
    def __init__(self, table_name: str):
        super().__init__(f"{table_name} is empty.")
