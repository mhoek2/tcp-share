from pathlib import Path
from typing import TypedDict

from modules.app.settings import Settings


class ReadWrite:
    def __init__(self) -> None:
        """This class handles reading from and writing to files."""
        self.settings: Settings = Settings()

        self.numShareableFiles: int = 0
        self.prevShareableFiles: int = 0

        self.dir = Path(self.settings.filesdir).resolve()
        self.textDir = self.dir.joinpath(self.settings.txt_subdir)
        self.pdfDir = self.dir.joinpath(self.settings.pdf_subdir)

    class FilesDict(TypedDict):
        filename: str
        contents: bytes

    def getFiles(self, path: Path, count_only: bool = False) -> list:
        """Get all files in a certain directory."""
        files: list[ReadWrite.FilesDict] = []

        if any(path.glob("*")):
            for file in path.glob("*"):
                if file.is_file():
                    # Do not read the file if count_only is true
                    contents = "".encode() if count_only else file.read_bytes()
                    files.append({"filename": file.name, "contents": contents})

        return files

    def removeFiles(self, path: Path) -> None:
        """Remove all files in a certain directory."""
        for file in path.glob("*"):
            if file.is_file():
                file.unlink()

    def hasTextFiles(self) -> bool:
        """Check if there are any text files."""
        files = self.getFiles(self.textDir, True)
        self.numShareableFiles = len(files)
        return bool(files)

    def getTextFiles(self) -> list:
        """Get all text files."""
        files = self.getFiles(self.textDir)

        suffix = self.settings.file_encrypted_suffix
        return list(filter(lambda item: suffix not in item["filename"], files))

    def getEncryptedTextFiles(self) -> list:
        """Get all encrypted text files."""
        files = self.getFiles(self.textDir)

        suffix = self.settings.file_encrypted_suffix
        return list(filter(lambda item: suffix in item["filename"], files))

    def removeTextFiles(self) -> None:
        """Remove all text files."""
        if self.hasTextFiles:
            self.removeFiles(self.textDir)

    def hasPdfFiles(self) -> bool:
        """Check if there are any text files."""
        return bool(self.getFiles(self.pdfDir, True))

    def getPdfFiles(self) -> list:
        """Get all text files."""
        return self.getFiles(self.pdfDir)

    def removePdfFiles(self) -> None:
        """Remove all pdf files."""
        if self.hasPdfFiles:
            self.removeFiles(self.pdfDir)

    def writeFile(self, path: Path, contents: str) -> None:
        """Function to write content to files."""

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(contents)
        print(f"{path} saved with following contents:\n{contents}")

    def writeTextFile(self, file_name: str, contents: str):
        """Write a text file."""
        file_path = self.textDir.joinpath(file_name)
        self.writeFile(file_path, contents)

    def writePdfFile(self, file_name: str, contents: bytes):
        """Write a text file."""
        file_path = self.pdfDir.joinpath(file_name)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_bytes(contents)
        print(f"{file_path} saved succesfully!")
