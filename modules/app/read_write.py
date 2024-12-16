import json
from pathlib import Path

from typing import TypedDict

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

        self.passwords_file = self.textDir.joinpath(self.settings.password_file)

        self.encrypted_suffix = self.settings.file_encrypted_suffix
        self.exceptions = [self.encrypted_suffix, self.settings.password_file]


        self.meta_file = self.textDir.joinpath(self.settings.meta_file)
        self.log_file = self.textDir.joinpath(self.settings.log_file)

        self.devices_cfg = Path(self.settings.devices_file).resolve()

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

        return bool(files)

    def hasTextFiles(self) -> bool:
        """Check if there are any unencrypted text files."""
        files = self.getTextFilesByAuth()

        self.numShareableFiles = len(files)
        return bool(files)

    def hasEncryptedTextFiles(self) -> bool:
        """Checks if there are any encrypted text files."""
        return bool(
            [
                item
                for item in self.getFiles(self.textDir, True)
                if self.encrypted_suffix in item["filename"]
            ]
        )

    def hasPasswordsFile(self) -> bool:
        """Check whether the passwords file exists."""
        return self.passwords_file.exists() and self.passwords_file.is_file and self.passwords_file.stat().st_size > 0
    
    def removePasswordFile( self ) -> None:
        if self.passwords_file.is_file():
            self.passwords_file.unlink()

    def hasPdfFiles(self) -> bool:
        """Check if there are any PDF files."""
        files = self.getFiles(self.pdfDir, True)
        self.numPDFFiles = len(files)
        return bool(files)

    def getAllTextFiles(self) -> list[FilesDict]:
        """Return all text files, making no distinction between the types of files."""
        return self.getFiles(self.textDir)

    def getTextFiles(self) -> list[FilesDict]:
        """Get all unencrypted text files."""
        return [
            item
            for item in self.getFiles(self.textDir)
            if item["filename"].endswith(".txt")
            and not any(keyword in item["filename"] for keyword in self.exceptions)
        ]

    def getEncryptedTextFiles(self) -> list[FilesDict]:
        """Get all encrypted text files."""
        return [
            item
            for item in self.getFiles(self.textDir)
            if self.encrypted_suffix in item["filename"]
        ]

    def getTransferFiles( self ) -> list[FilesDict]:
        files = self.getTextFilesByAuth()

        # get additional files ( log, meta, and passwords )
        for item in self.getAllTextFiles():
            if item["filename"].endswith(".txt"):
                continue

            # make sure .log file is first item.
            if item["filename"].endswith(".log"):
                files.insert( 0, item )
            else: 
                files.append( item )

        return files

    def getTextFilesByAuth( self ) -> list[FilesDict]:
        """Get encrypted or decrypted files based on crypt state"""
        files = []

        if self.hasPasswordsFile():
            files = self.getEncryptedTextFiles()
        else:
            files = self.getTextFiles()

        return files

    def getKeys(self) -> list[str]:
        """Get the contents of the password file."""
        if not self.hasPasswordsFile():
            return []

        return json.loads(self.passwords_file.read_text())

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

    def writePasswordsFile(self, contents: list[str]) -> None:
        """Write to the passwords file."""
        self.writeFile(self.passwords_file, json.dumps(contents))

    def writePdfFile(self, file_name: str, contents: bytes) -> None:
        """Write a pdf file."""
        file_path = self.pdfDir.joinpath(file_name)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_bytes(contents)
        print(f"{file_path} saved succesfully!")

    def removeFiles(self, path: Path) -> None:
        """Remove all files in a certain directory."""
        if path.is_dir():
            for file in path.glob("*"):
                if file.is_file():
                    file.unlink()

    def removeTransferFiles(self) -> None:
        """
        Remove all text files (including encrypted files, decrypted
        files and the passwords file).
        """
        if self.hasAnyTextFiles:
            self.removeFiles(self.textDir)

    def removeUnencryptedTextFiles(self) -> None:
        """Remove only unencrypted text files."""
        if self.hasTextFiles():
            for file in self.textDir.glob("*"):
                if file.is_file():
                    if not any(keyword in file.name for keyword in self.exceptions):
                        file.unlink()

    def removePasswordsFile(self) -> None:
        """Remove the file containing all the keys."""
        if self.passwords_file.exists() and self.passwords_file.is_file():
            self.passwords_file.unlink()

    def removePdfFiles(self) -> None:
        """Remove all pdf files."""
        if self.hasPdfFiles:
            self.removeFiles(self.pdfDir)

    def removeQRFiles(self) -> None:
        """Remove all qr files."""
        self.removeFiles(self.qrDir)

    def hasMetaFile(self) -> bool:
        """Check whether the passwords file exists."""
        return self.meta_file.exists() and self.meta_file.is_file and self.meta_file.stat().st_size > 0

    def getMetaFile(self) -> list:
        """Get the contents of the password file."""
        if self.hasMetaFile():
            return json.loads(self.meta_file.read_text())
        else:
            return {}

    def writeMetaFile( self , contents ):
        self.writeFile(self.meta_file, json.dumps(contents))

    def hasLogFile(self) -> bool:
        """Check whether the log file exists."""
        return self.log_file.exists() and self.log_file.is_file and self.log_file.stat().st_size > 0

    def getLogFile(self) -> list:
        """Get the contents of the log file."""
        if self.hasLogFile():
            return json.loads(self.log_file.read_text())
        else:
            return []

    def writeLogFile( self , contents ):
        self.writeFile(self.log_file, json.dumps(contents))

    def getDevicesFromFile( self ):
        if not self.devices_cfg.exists() or not self.devices_cfg.is_file or self.devices_cfg.stat().st_size == 0:
            self.writeFile( self.devices_cfg, '[{ "hostname":"example", "ip":"192.168.1.50" }]')

        return json.loads( self.devices_cfg.read_text() )