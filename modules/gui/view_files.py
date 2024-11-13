from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD

class GUI_ViewFiles( GuiModule ):

    def onStart( self ):
        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.numShareableFiles}")
        header.pack()

        self.current_position = Vector2( 0, 50 )

        button = Button( self, text = "Terug", 
               command = lambda : self.gui.goHome() )
        button.place( x = self.settings.appplication_width - 130, 
                      y = self.settings.appplication_height - 40 )