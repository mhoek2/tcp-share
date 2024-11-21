from fileinput import filename
from pathlib import Path

from modules.app.settings import Settings


class ReadWrite:
    def __init__(self) -> None:
        """This class handles reading from and writing to files."""
        self.settings: Settings = Settings()

        self.numShareableFiles: int = 0
        self.prevShareableFiles: int = 0
        
        self.dir = Path(self.settings.filesdir).resolve()
        self.dir.mkdir(parents=True, exist_ok=True)
        self.textDir = self.dir.joinpath("txt")
        self.textDir.mkdir(parents=True, exist_ok=True)
        self.pdfDir = self.dir.joinpath("pdf")
        self.pdfDir.mkdir(parents=True, exist_ok=True)

    # def hasShareableFiles(self) -> bool:
    #     """Check if there are files available for sharing
    #     - should be extended to return two booleans:
    #       1. if files exists
    #       2. if salts/password file exists"""

    #     num_files = 0

    #     if self.dir.exists() and self.dir.is_dir():
    #         # Checking if the directory is not empty
    #         if any(self.dir.iterdir()):
    #             # Count sharable files
    #             for file in self.dir.iterdir():
    #                 if file.is_file():
    #                     num_files += 1

    #     self.numShareableFiles = num_files
    #     return True if num_files > 0 else False

    # def getShareableFiles(self) -> list:
    #     """Return list of files"""
    #     files = []

    #     if self.hasShareableFiles():
    #         for file in self.dir.iterdir():
    #             if file.is_file():
    #                 file_contents = file.read_text()

    #                 files.append(
    #                     {
    #                         "filename": file.name,
    #                         "content": file_contents,
    #                     }
    #                 )

    #     return files
    
    # def removeShareableFiles(self):
    #     """Remove local shareable files"""
    #     print("Remove local shareable files")
    #     if self.hasShareableFiles():
    #         for file in self.dir.iterdir():
    #             if file.is_file():
    #                 file.unlink()
    #     return
    
    def getFiles(self, path: Path) -> list:
        """Get all files in a certain directory."""
        files = []
        
        if any(path.iterdir()):
            for file in path.iterdir():
                files.append(
                    {
                        "filename": file.name,
                        "contents": file.read_text()
                    }
                )
        
        return files

    def removeFiles(self, path: Path) -> None:
        """Remove all files in a certain directory."""
        for file in path.iterdir():
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
