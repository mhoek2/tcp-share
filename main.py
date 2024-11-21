from cgi import print_exception
from tkinter import *
import threading
import time

# app core modules
from modules.app.settings import Settings
from modules.app.gui import Gui
from modules.app.read_write import ReadWrite

# app modules
from modules.crypt import Crypt
from modules.gui.share_files import GUI_ShareFiles
from modules.gui.view_files import GUI_ViewFiles
from modules.tcp import TCP
from modules.to_pdf import ToPDF

class Application( Tk ):
    """Base class for this application"""
    def __init__( self, pytest=False ) -> None:
        self.settings : Settings = Settings()
        self.tcp : TCP = TCP( self ) 
        self.read_write : ReadWrite = ReadWrite()

        self.tk_root : Gui = Gui( self )
        
        # empty placeholder modules
        self.crypt : Crypt = Crypt( self )
        self.to_pdf : ToPDF = ToPDF( self )

        if not pytest:
            # background worker to check incoming TCP connections
            self.tcp_worker()

            # background worker for appliction
            self.bg_worker()

            self.tk_root.mainloop()

    #
    # Keep the following in main for readability (flow-chart)
    #

    # TCP thread: The socket server to allow incoming connections:
    def tcp_worker( self ) -> None:
        self.tcp_server = threading.Thread( target=self.tcp.start_server, daemon=True )
        self.tcp_server.start()
      
    # Background thread: 
    # - Continuesly scan 'files' folder  for changes
    # - Run GUI updates
    def bg_worker( self ) -> None:
        self.bg_worker_tick = 0
        self.bg_worker_force_gui = False

        self.bg_worker = threading.Thread( target=self.bg_worker_do, daemon=True )
        self.bg_worker.start()

    def bg_worker_force_gui_update( self ):
        """"Force a pass in the background worker to enter the GUI pass"""
        self.bg_worker_force_gui = True

    def bg_worker_do( self ) -> None:
        while True:
            print( self.bg_worker_tick )

            #
            # scan 'files' folder to track changes
            #
            if self.read_write.hasShareableFiles() and self.read_write.numShareableFiles != self.read_write.prevShareableFiles:
                """Files found - Files have changed"""
                
                print( f"Files have changed? num files: {self.read_write.numShareableFiles}" )

                # reload the current frame/page
                if self.tk_root.current_frame > self.tk_root.FRAME_CREATE_FILES:
                    reload_frame : bool = True # redundant bool ..
                    self.tk_root.after(10, self.tk_root.show_frame( self.tk_root.current_frame, reload_frame ) )
                
                # go home if previously ther were no files    
                else:
                    self.tk_root.after(10, self.tk_root.goHome() )

                self.read_write.prevShareableFiles = self.read_write.numShareableFiles
            
            elif self.read_write.numShareableFiles != self.read_write.prevShareableFiles:
                """NO files found - Files have been removed?"""
                print("Files have been removed?")

                self.tk_root.after(10, self.tk_root.goHome() )
                self.read_write.prevShareableFiles = self.read_write.numShareableFiles

            #
            # A GUI update pass, force or every x secconds
            #
            if self.bg_worker_tick % 10 == 0 or self.bg_worker_force_gui:
                if self.tk_root.is_frame_active( self.tk_root.FRAME_SHARE_FILES ):
                    self.tk_root.after(10, self.tk_root.frames[ self.tk_root.FRAME_SHARE_FILES ].updateDevices() )
                    print("x")

                if self.bg_worker_force_gui:
                    self.bg_worker_force_gui = False

            self.bg_worker_tick += 1
            time.sleep(1)

if __name__ == '__main__':
    app = Application()
    