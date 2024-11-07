from modules.gui.gui_module import GuiModule

from tkinter import *

class GUI_CreateFiles( GuiModule ):
    def onStart( self ):
        header = Label( self, text="Create files.." )
        header.pack()

        button = Button( self, text = "Home", 
               command = lambda : self.gui.show_frame( self.gui.FRAME_SHARE_FILES ) )
        button.pack()