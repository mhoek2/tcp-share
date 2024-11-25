from pathlib import Path

from modules.app.settings import Settings


class ReadWrite:
    def __init__(self) -> None:
        """This class handles reading from and writing to files."""
        self.settings: Settings = Settings()

        self.numShareableFiles: int = 0
        self.prevShareableFiles: int = 0

        self.dir = Path(self.settings.filesdir).resolve()
        self.textDir = self.dir.joinpath("txt")
        self.pdfDir = self.dir.joinpath("pdf")

    def getFiles(self, path: Path) -> list:
        """Get all files in a certain directory."""
        files = []

        if any(path.glob("*")):
            for file in path.glob("*"):
                if file.is_file():
                    files.append({"filename": file.name, "contents": file.read_text()})

        return files

    def removeFiles(self, path: Path) -> None:
        """Remove all files in a certain directory."""
        for file in path.glob("*"):
            if file.is_file():
                file.unlink()

    def hasTextFiles(self) -> bool:
        """Check if there are any text files."""
        files = self.getFiles(self.textDir)
        self.numShareableFiles = len(files)
        return bool(files)

    def getTextFiles(self) -> list:
        """Get all text files."""
        return self.getFiles(self.textDir)

    def removeTextFiles(self) -> None:
        """Remove all text files."""
        if self.hasTextFiles:
            self.removeFiles(self.textDir)

    def hasPdfFiles(self) -> bool:
        """Check if there are any text files."""
        return bool(self.getFiles(self.pdfDir))

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
