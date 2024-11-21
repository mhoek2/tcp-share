import os
from pathlib import Path

from modules.app.settings import Settings


class ReadWrite:
    def __init__(self) -> None:
        """This class handles reading from and writing to files."""
        self.settings: Settings = Settings()

        self.numShareableFiles: int = 0
        self.prevShareableFiles: int = 0

        self.numPDFFiles: int = 0
        self.prevnumPDFFiles: int = 0

        self.dir = self.settings.filesdir

    def getFiles( self, path_str: str, count_only: bool = False ) -> list:
        """Return list of files"""
        files = []
        num_files = 0

        if not os.path.exists( path_str ) or os.path.isfile( path_str ):
            return

        for i, filename in enumerate( os.listdir( path_str ) ):
            file_path = os.path.join( path_str, filename )

            if os.path.isfile( file_path ):
                num_files += 1

                # count files
                if count_only: 
                    files.append( num_files )
                    continue

                # read files
                file_pathlib = Path( file_path )
                file_contents = file_pathlib.read_text()

                files.append(
                    {
                        "filename": filename,
                        "content": file_contents,
                    }
                )

        return files

    def removeFiles( self, path_str: str ):
        """Remove files in dir"""
        for filename in os.listdir( path_str ):
            file_path = os.path.join( path_str, filename )

            if os.path.isfile( file_path ):
                os.unlink( file_path )

        return

    def writeFiles(self, path_str: str, content: str):
        """Function to write content to files."""
        path = Path(path_str) if Path(path_str).is_absolute() else Path(self.dir).joinpath(path_str)

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content)
        print(f"{path} saved with following contents:\n{content}")

    #
    # Wrapper functions
    #
    def hasTextFiles( self ) -> bool:
        """Are ther any files in files dir"""
        count_only : bool = True
        files : list = self.getFiles( self.settings.filesdir, count_only )
       
        self.numShareableFiles = len( files )
        return True if self.numShareableFiles > 0 else False
    
    def hasPDFFiles( self ) -> bool:
        """Are ther any files in PDF files dir"""
        count_only : bool = True
        files : list = self.getFiles( self.settings.pdf_filesdir, count_only )
        
        self.numPDFFiles = len( files )
        return True if self.numPDFFiles > 0 else False

    def getTextFiles( self ) -> list:
        return self.getFiles( self.settings.filesdir )

    def getPDFFiles( self ) -> list:
        return self.getFiles( self.settings.pdf_filesdir )

    def removeTextFiles( self ):
        self.removeFiles( self.settings.filesdir )

    def removePDFFiles( self ):
        self.removeFiles( self.settings.pdf_filesdir )