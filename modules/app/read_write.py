import os

from modules.app.settings import Settings


class ReadWrite:
    def __init__(self) -> None:
        """This class handles reading from and writing to files."""
        self.settings: Settings = Settings()

        self.numShareableFiles: int = 0
        self.prevShareableFiles: int = 0

    def hasShareableFiles(self) -> bool:
        """Check if there are files available for sharing
        - should be extended to return two booleans:
          1. if files exists
          2. if salts/password file exists"""

        num_files = 0

        if os.path.exists(self.settings.filesdir) and not os.path.isfile(
            self.settings.filesdir
        ):
            # Checking if the directory is not empty
            if os.listdir(self.settings.filesdir):
                # Count sharable files

                for filename in os.listdir(self.settings.filesdir):
                    file_path = os.path.join(self.settings.filesdir, filename)

                    if os.path.isfile(file_path):
                        num_files += 1

        self.numShareableFiles = num_files
        return True if num_files > 0 else False

    def getShareableFiles(self) -> list:
        """Return list of files"""
        files = []

        if self.hasShareableFiles():
            for i, filename in enumerate(os.listdir(self.settings.filesdir)):
                file_path = os.path.join(self.settings.filesdir, filename)

                if os.path.isfile(file_path):
                    # need to read the content of the file ..
                    # use hardcoded test data for now
                    files.append(
                        {
                            "filename": filename,
                            "content": "hard-coded content from def app.getShareableFiles()",
                        }
                    )

        return files

    def removeShareableFiles(self):
        """Remove local shareable files"""
        print("Remove local shareable files")
        if self.hasShareableFiles():
            for filename in os.listdir(self.settings.filesdir):
                file_path = os.path.join(self.settings.filesdir, filename)

                if os.path.isfile(file_path):
                    os.unlink(file_path)
        return
