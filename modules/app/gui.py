from typing import TYPE_CHECKING

# app core modules
from modules.app.settings import Settings

# import GUI modules
from modules.gui.create_files import *
from modules.gui.share_files import *
from modules.gui.view_files import *
from modules.gui.view_logs import *

import tkinter as tk

if TYPE_CHECKING:
    from main import Application

class Gui( tk.Tk ):
    def __init__( self, context ) -> None:
        """Create a window using Tkinter, setup title, dimension 
        and main container frame"""
        super().__init__()

        self.context : 'Application' = context;
        self.settings : Settings = context.settings

        self.title( self.settings.application_title )
        self.geometry( self.settings.application_size )

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        self.current_frame = 0

        self.load_frames()

        self.goHome()

    def create_frame( self, module, i ):
        frame = module( self, self.context )
        frame.grid(row = 0, column = 0, sticky ="nsew")
        self.frames[i] = frame

    def load_frames( self ) -> None:
        """Register the GUI frames and define a name macro for each"""

        # Order needs to match with adjacent for loop Class names
        self.FRAME_CREATE_FILES = 0;
        self.FRAME_SHARE_FILES = 1;
        self.FRAME_VIEW_FILES = 2;
        self.FRAME_VIEW_LOGS = 3;

        # Register each GUI module in the self.frames dictionary
        # - If you want to extend this, create a new GUI_* class, 
        #   and import the class at the start of this file
        for i, module in enumerate((GUI_CreateFiles,
                                    GUI_ShareFiles,
                                    GUI_ViewFiles,
                                    GUI_ViewLogs)):
            self.create_frame( module, i)

    def is_frame_active( self, index ):
        return True if index == self.current_frame else False   

    def show_frame( self, index, reload_frame=False ):
        """Hide other frames and show the frame by the index"""

        if reload_frame:
            self.create_frame( type(self.frames[index]), index)
        
        frame = self.frames[index]
        frame.tkraise()
        self.current_frame = index

    def get_frame_index_for_file_sharing( self ) -> int:
        """Return the index of 'create_files' or 'share_files' frame/page
        based on the presence of files"""

        index : int = 0

        if self.context.has_files():
            index = self.FRAME_SHARE_FILES
        else:
            index = self.FRAME_CREATE_FILES
            
        return index

    def goHome( self ):
        """Determine whether to display the 'create_files' or 'share_files' frame/page."""
        reload_frame : bool = True # redundant bool ..
        self.show_frame( self.get_frame_index_for_file_sharing(), reload_frame )
        return