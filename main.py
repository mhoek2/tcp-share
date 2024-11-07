from tkinter import *
import threading
import time
import os

# app core modules
from modules.app.settings import Settings
from modules.app.gui import Gui

# app modules
from modules.crypt import Crypt
from modules.tcp import TCP
from modules.to_pdf import ToPDF

class Application( Tk ):
    """Base class for this application"""
    def __init__( self ) -> None:
        self.settings : Settings = Settings()
        self.tk_root : Gui = Gui( self )
          
        # empty placeholder modules
        self.crypt : Crypt = Crypt( self )
        self.tcp : Crypt = TCP( self )
        self.to_pdf : Crypt = ToPDF( self )

        self.custom_loop_thread = threading.Thread( target=self.tcploop, daemon=True )
        self.custom_loop_thread.start()

        self.tk_root.mainloop()

    def hasShareableFiles( self ) -> None:
        """Check if there are files available for sharing
        - should be extended to return two booleans:
          1. if files exists
          2. if salts/password file exists"""
        if os.path.exists( self.settings.filesdir ) and not os.path.isfile( self.settings.filesdir ): 
           
           # Checking if the directory is not empty
            if os.listdir( self.settings.filesdir ): 
                return True

        return False

    def tcploop( self ) -> None:
        """Loop in a seperate thread"""
        while True:
            self.tcp.update()
            continue
            
if __name__ == '__main__':
    app = Application()

    