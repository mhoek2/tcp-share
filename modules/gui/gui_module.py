from typing import TYPE_CHECKING

# app core modules
from modules.app.settings import Settings

from tkinter import *

if TYPE_CHECKING:
    from main import Application
    from modules.app.gui import Gui

class GuiModule( Frame ):
    """Base class that GUI modules inherit from 
    prevents complexity and ensures compatibility"""
    def __init__( self, gui, context ) -> None:
        Frame.__init__(self, gui.container )

        self.context : 'Application' = context;
        self.settings : Settings = context.settings
        self.gui : 'Gui' = gui

        # call the inherited GUI module's entry point
        self.onStart()