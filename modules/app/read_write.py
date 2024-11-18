import os
from pathlib import Path

from modules.app.settings import Settings


class ReadWrite:
    def __init__(self) -> None:
        """This class handles reading from and writing to files."""
        self.settings: Settings = Settings()

        self.numShareableFiles: int = 0
        self.prevShareableFiles: int = 0
        self.dir = self.settings.filesdir

    def hasShareableFiles(self) -> bool:
        """Check if there are files available for sharing
        - should be extended to return two booleans:
          1. if files exists
          2. if salts/password file exists"""

        num_files = 0

        if os.path.exists(self.dir) and not os.path.isfile(self.dir):
            # Checking if the directory is not empty
            if os.listdir(self.dir):
                # Count sharable files
                for filename in os.listdir(self.dir):
                    file_path = os.path.join(self.dir, filename)

                    if os.path.isfile(file_path):
                        num_files += 1

        self.numShareableFiles = num_files
        return True if num_files > 0 else False

    def getShareableFiles(self) -> list:
        """Return list of files"""
        files = []

        if self.hasShareableFiles():
            for i, filename in enumerate(os.listdir(self.dir)):
                file_path = os.path.join(self.dir, filename)

                if os.path.isfile(file_path):
                    file_pathlib = Path(file_path)
                    file_contents = file_pathlib.read_text()

                    files.append(
                        {
                            "filename": filename,
                            "content": file_contents,
                        }
                    )

        return files

    def removeShareableFiles(self):
        """Remove local shareable files"""
        print("Remove local shareable files")
        if self.hasShareableFiles():
            for filename in os.listdir(self.dir):
                file_path = os.path.join(self.dir, filename)

                if os.path.isfile(file_path):
                    os.unlink(file_path)
        return

    def writeFiles(self, path: Path | str, content: str):
        """Function to write content to files."""
        if isinstance(path, str):
            path = Path(path) if Path(path).is_absolute() else Path(self.dir).joinpath(path)

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content)
        print(f"{path} saved with following contents:\n{content}")
