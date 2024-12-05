from cgi import print_exception
from tkinter import *
import threading
import time

# app core modules
from modules.app.settings import Settings
from modules.app.gui import Gui
from modules.app.read_write import ReadWrite
from modules.translate import Translate

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

        self.translate : Translate = Translate( self )
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

    #
    # perhaps 'has_files' and 'file_count_changed' should be moved to modules/app/read_write.py?
    #
    def has_files( self ) -> bool:
        """Check if files in 'txt' or 'pdf' exist.
        'hasTextFiles()' and 'hasPdfFiles()' updates the current file count as well."""
        try:
            has_text_files = self.read_write.hasTextFiles()
            has_pdf_files = self.read_write.hasPdfFiles()
            
            return has_text_files or has_pdf_files
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def file_count_changed( self ) -> bool:
        """Deteriminte wheter the file count has changed since previous iteration."""
        if self.read_write.numShareableFiles != self.read_write.prevShareableFiles:
            print( f"Files have changed? num txt files: {self.read_write.numShareableFiles}" )
            return True

        if self.read_write.numPDFFiles != self.read_write.prevPDFFiles:
            print( f"Files have changed? num pdf files: {self.read_write.numPDFFiles}" )
            return True

        return False

    def update_previous_file_count( self ) -> None:
        """This method sets the file count to the current count. 
        This is useful for tracking changes in file counts across operations."""
        self.read_write.prevShareableFiles = self.read_write.numShareableFiles
        self.read_write.prevPDFFiles = self.read_write.numPDFFiles

    def bg_worker_do( self ) -> None:
        """Background worker that continuously monitors and updates the application state.

        This method performs the following actions in an infinite loop:
        - Checks for changes in the file count and takes following actions:
            - If there are changes and files exist while not on the creation page, it reloads the current frame.
            - If there are no files or on the creation page, it navigates back to the home frame.
        - Updates the recorded file count for the next iteration comparisons.
        - Periodically refreshes device data every 10 ticks when in the share files frame.
        - If a forced device update is triggered, it updates devices immediately.
    
        The loop sleeps for one second between iterations to manage the frequency.
        """
        while True:
            print( self.bg_worker_tick )

            # Monitor changes in the file count by comparing the current count with the previous iteration.
            # If files exist and the current page handles file reading, reload the current frame.
            # If the file count is zero or the application is on the creation page, call goHome().
            # The goHome() function will determine whether to display the create_files frame or the share_files frame.
            has_files = self.has_files()
            num_changed = self.file_count_changed()

            if num_changed:
                if has_files and self.tk_root.current_frame > self.tk_root.FRAME_CREATE_FILES:
                    # reload the current frame/page
                    reload_frame : bool = True # redundant bool ..
                    self.tk_root.after( 10, self.tk_root.show_frame( self.tk_root.current_frame, reload_frame ) )
                
                else:
                    self.tk_root.after( 10, self.tk_root.goHome() )
                
                self.update_previous_file_count()

            # Update the device list every X seconds when the share_files frame is open.
            # If self.bg_worker_force_gui is True, trigger an earlier update.
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
    