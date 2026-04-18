from collections.abc import Iterable
from pathlib import Path

from src.formatting import join_sorted

class RawFolderNotFoundError(FileNotFoundError):
    def __init__(self, folder_path: Path, known_folders: Iterable[object]) -> None:
        formatted_folders = join_sorted(known_folders)
        super().__init__(
            f"""
            Raw folder not found: {folder_path}
            Known raw folders: {formatted_folders}
            """
        )

class RawFolderDirectoryError(NotADirectoryError):
    def __init__(self, folder_path: Path) -> None:
        super().__init__(f"Expected a directory, got: {folder_path}")

class SpreadsheetNotFoundError(FileNotFoundError):
    def __init__(self, file_path: Path) -> None:
        super().__init__(f"Spreadsheet not found: {file_path}")

class SpreadsheetFormatError(ValueError):
    def __init__(self, file_suffix: str, supported_formats: Iterable[object]) -> None:
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
    ) -> None:
        formatted_sheets = join_sorted(available_sheets)
        super().__init__(
            f"""
            Sheet not found: {sheet_name!r} in {file_name}
            Available sheets: {formatted_sheets}
            """
        )

class EmptyTableError(ValueError):
    def __init__(self, table_name: str) -> None:
        super().__init__(f"{table_name} is empty.")
