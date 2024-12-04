import json
from pathlib import Path
from typing import TypedDict

from modules.app.settings import Settings


class ReadWrite:
    def __init__(self) -> None:
        """This class handles reading from and writing to files."""
        self.settings: Settings = Settings()

        self.numShareableFiles: int = 0
        self.prevShareableFiles: int = 0

        self.numPDFFiles: int = 0
        self.prevPDFFiles: int = 0

        self.dir = Path(self.settings.filesdir).resolve()
        self.textDir = self.dir.joinpath(self.settings.txt_subdir)
        self.pdfDir = self.dir.joinpath(self.settings.pdf_subdir)

        self.suffix = self.settings.file_encrypted_suffix

    class FilesDict(TypedDict):
        filename: str
        contents: bytes

    def getFiles(self, path: Path, count_only: bool = False) -> list[FilesDict]:
        """Get all files in a certain directory."""
        files: list[ReadWrite.FilesDict] = []

        if any(path.glob("*")):
            for file in path.glob("*"):
                if file.is_file():
                    # Do not read the file if count_only is true
                    if count_only:
                        contents = b""
                    elif file.suffix == ".pdf":
                        contents = file.read_bytes()
                    else:
                        contents = file.read_text().encode()

                    files.append({"filename": file.name, "contents": contents})

        return files
    
    def hasAnyTextFiles(self) -> bool:
        """Check whether there are any text files, regardless of the type."""
        files = self.getFiles(self.textDir, True)
        
        self.numShareableFiles = len(files) # decide whether to leave it here …
        return bool(files)

    def hasTextFiles(self) -> bool:
        """Check if there are any unencrypted text files."""
        files = [
            item
            for item in self.getFiles(self.textDir, True)
            if not any(
                keyword in item["filename"]
                for keyword in [self.suffix, self.settings.password_file, "_decrypted"]
            )
        ]

        self.numShareableFiles = len(files) # … or here
        return bool(files)

    def hasEncryptedTextFiles(self) -> bool:
        """Checks if there are any encrypted text files."""
        return bool(
            [
                item
                for item in self.getFiles(self.textDir)
                if self.suffix in item["filename"]
            ]
        )

    def hasPasswordsFile(self) -> bool:
        """Check whether the passwords file exists."""
        file = Path(self.textDir).joinpath(self.settings.password_file)

        return file.exists() and file.is_file and file.stat().st_size > 0

    def hasPdfFiles(self) -> bool:
        """Check if there are any PDF files."""
        files = self.getFiles(self.pdfDir, True)
        self.numPDFFiles = len(files)
        return bool(files)
    
    def getAllTextFiles(self) -> list[FilesDict]:
        """Return all text files, making no distinction between the types of files"""
        return self.getFiles(self.textDir)

    def getTextFiles(self) -> list[FilesDict]:
        """Get all unencrypted text files."""
        return [
            item
            for item in self.getFiles(self.textDir)
            if not any(
                keyword in item["filename"]
                for keyword in [self.suffix, self.settings.password_file, "_decrypted"]
            )
        ]

    def getEncryptedTextFiles(self) -> list[FilesDict]:
        """Get all encrypted text files."""
        return [
            item
            for item in self.getFiles(self.textDir)
            if self.suffix in item["filename"]
        ]

    def getPasswordsFile(self) -> list:
        """Get the contents of the password file."""
        file_path = self.textDir.joinpath(self.settings.password_file)

        return json.loads(file_path.read_text())

    def getPdfFiles(self) -> list[FilesDict]:
        """Get all PDF files."""
        return self.getFiles(self.pdfDir)

    def writeFile(self, path: Path, contents: str) -> None:
        """Function to write content to files."""

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(contents)
        print(f"{path} saved with following contents:\n{contents}")

    def writeTextFile(self, file_name: str, contents: str) -> None:
        """Write a text file."""
        file_path = self.textDir.joinpath(file_name)
        self.writeFile(file_path, contents)

    def writePasswordsFile(self, contents: list) -> None:
        """Write to a passwords file."""
        file_path = self.textDir.joinpath(self.settings.password_file)
        self.writeFile(file_path, json.dumps(contents))

    def writePdfFile(self, file_name: str, contents: bytes) -> None:
        """Write a pdf file."""
        file_path = self.pdfDir.joinpath(file_name)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_bytes(contents)
        print(f"{file_path} saved succesfully!")

    def removeFiles(self, path: Path) -> None:
        """Remove all files in a certain directory."""
        for file in path.glob("*"):
            if file.is_file():
                file.unlink()

    def removeTextFiles(self) -> None:
        """
        Remove all text files (including encrypted files, decrypted
        files and the passwords file).
        """
        if self.hasTextFiles:
            self.removeFiles(self.textDir)

    def removePdfFiles(self) -> None:
        """Remove all pdf files."""
        if self.hasPdfFiles:
            self.removeFiles(self.pdfDir)
