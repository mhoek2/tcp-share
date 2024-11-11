from tkinter import *
import threading
import time
import os

# app core modules
from modules.app.settings import Settings
from modules.app.gui import Gui

# app modules
from modules.crypt import Crypt
from modules.gui.share_files import GUI_ShareFiles
from modules.tcp import TCP
from modules.to_pdf import ToPDF

class Application( Tk ):
    """Base class for this application"""
    def __init__( self ) -> None:
        self.numShareableFiles = 0
        self.prevShareableFiles = 0

        self.settings : Settings = Settings()
        self.tk_root : Gui = Gui( self )
        

        # empty placeholder modules
        self.crypt : Crypt = Crypt( self )
        self.to_pdf : Crypt = ToPDF( self )

        # background worker to check incoming TCP connections
        self.tcp : TCP = TCP( self )
        self.tcp_worker()

        # background worker for appliction
        self.background_worker()

        self.tk_root.mainloop()

    def hasShareableFiles( self ) -> None:
        """Check if there are files available for sharing
        - should be extended to return two booleans:
          1. if files exists
          2. if salts/password file exists"""
          
        num_files : int = 0

        if os.path.exists( self.settings.filesdir ) and not os.path.isfile( self.settings.filesdir ): 
           
           # Checking if the directory is not empty
            if os.listdir( self.settings.filesdir ): 

                # Count sharable files
                
                for filename in os.listdir( self.settings.filesdir ):
                    file_path = os.path.join( self.settings.filesdir, filename )

                    if os.path.isfile( file_path ):
                        num_files += 1

        self.numShareableFiles = num_files
        return True if num_files > 0 else False

    def getShareableFiles( self ) -> None:
        """Return list of files"""
        files = []

        if self.hasShareableFiles():
            for i, filename in enumerate (os.listdir( self.settings.filesdir ) ):
                file_path = os.path.join( self.settings.filesdir, filename )

                if os.path.isfile( file_path ):
                    # need to read the content of the file ..
                    # use hardcoded test data for now
                    files.append( { "filename": filename, "content": "hard-coded content from def app.getShareableFiles()" } )

        return files

    def removeShareableFiles( self ):
        """Remove local shareable files"""
        print("Remove local shareable files")
        if self.hasShareableFiles():
            for filename in os.listdir( self.settings.filesdir ):
                file_path = os.path.join( self.settings.filesdir, filename )

                if os.path.isfile( file_path ):
                    os.unlink( file_path )
        return

    # Keep this in main for readability (flow-chart)
    def tcp_worker( self ) -> None:
        self.tcp_server = threading.Thread( target=self.tcp.start_server, daemon=True )
        self.tcp_server.start()
       
    def background_worker( self ) -> None:
        self.bg_worker = threading.Thread( target=self.background_worker_do, daemon=True )
        self.bg_worker.start()

    def background_worker_do( self ) -> None:
        while True:
            if self.hasShareableFiles() and self.numShareableFiles != self.prevShareableFiles:
                """Files have changed"""
                
                print( f"Files have changed? num files: {self.numShareableFiles}" )

                self.tk_root.after(9, self.tk_root.create_frame( GUI_ShareFiles, self.tk_root.FRAME_SHARE_FILES ) )
                self.tk_root.after(10, self.tk_root.show_frame( self.tk_root.FRAME_SHARE_FILES ) )
                
                self.prevShareableFiles = self.numShareableFiles
            
            elif self.numShareableFiles != self.prevShareableFiles:
                """Files have been removed?"""
                print("Files have been removed?")
                #self.gui.show_frame( self.gui.FRAME_CREATE_FILES )

                self.tk_root.after(10, self.tk_root.show_frame( self.tk_root.FRAME_CREATE_FILES ) )
                self.prevShareableFiles = self.numShareableFiles

            time.sleep(1)

if __name__ == '__main__':
    app = Application()
    