from pathlib import Path
import os
import json 
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
        self.qrDir = self.dir.joinpath(self.settings.qr_subdir)

    def getFiles(self, path: Path, count_only: bool = False) -> list:
        """Get all files in a certain directory."""
        files = []

        if any(path.glob("*")):
            for file in path.glob("*"):
                if file.is_file():
                    # Do not read the file if count_only is true
                    contents = None if count_only else file.read_bytes()
                    files.append({"filename": file.name, "contents": contents})

        return files

    def removeFiles(self, path: Path) -> None:
        """Remove all files in a certain directory."""
        for file in path.glob("*"):
            if file.is_file():
                file.unlink()

    def hasTextFiles(self) -> bool:
        """Check if there are any text files."""
        files = self.getTextFiles()
        self.numShareableFiles = len(files)
        return bool(files)

    def getTextFiles(self) -> list:
        """Get all text files."""

        files = [   item
            for item in self.getFiles(self.textDir)
            if any(
                os.path.splitext(item["filename"])[1] == f".{keyword}"
                for keyword in ["txt"]
            )
        ]

        return files

    def getTransferFiles(self) -> list:
        """Get all text files."""
        return self.getFiles(self.textDir)

    def removeTransferFiles(self) -> None:
        """Remove all text files."""
        self.removeFiles(self.textDir)

    def hasPdfFiles(self) -> bool:
        """Check if there are any text files."""
        files = self.getFiles(self.pdfDir, True)
        self.numPDFFiles = len(files)
        return bool(files)

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

    def hasMetaFile(self) -> bool:
        """Check whether the passwords file exists."""
        file_path = self.textDir.joinpath(self.settings.meta_file)
        return file_path.exists() and file_path.is_file and file_path.stat().st_size > 0

    def getMetaFile(self) -> list:
        """Get the contents of the password file."""
        file_path = self.textDir.joinpath(self.settings.meta_file)

        if self.hasMetaFile():
            return json.loads(file_path.read_text())
        else:
            return {}

    def writeMetaFile( self , contents ):
        file_path = self.textDir.joinpath(self.settings.meta_file)
        self.writeFile(file_path, json.dumps(contents))