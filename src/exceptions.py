from pathlib import Path

class RawFolderNotFoundError(FileNotFoundError):
    def __init__(self, folder_path: Path, known_folders: str) -> None:
        super().__init__(
            f"""
            Raw folder not found: {folder_path}
            Known raw folders: {known_folders}
            """
        )

class RawFolderDirectoryError(NotADirectoryError):
    def __init__(self, folder_path: Path) -> None:
        super().__init__(f"Expected a directory, got: {folder_path}")


class SpreadsheetNotFoundError(FileNotFoundError):
    def __init__(self, file_path: Path) -> None:
        super().__init__(f"Spreadsheet not found: {file_path}")


class SpreadsheetFormatError(ValueError):
    def __init__(self, file_suffix: str, supported_formats: str) -> None:
        super().__init__(
            f"""
            Unsupported spreadsheet format: {file_suffix}
            Supported formats: {supported_formats}
            """
        )

class SheetNotFoundError(ValueError):
    def __init__(
        self,
        sheet_name: str,
        file_name: str,
        available_sheets: str,
    ) -> None:
        super().__init__(
            f"""
            Sheet not found: {sheet_name!r} in {file_name}
            Available sheets: {available_sheets}
            """
        )
