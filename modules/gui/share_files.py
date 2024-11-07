from modules.gui.gui_module import GuiModule

from tkinter import *

class GUI_ShareFiles( GuiModule ):
    def onStart( self ):
        header = Label( self, text="Share files..")
        header.pack()

        button = Button( self, text = "Create", 
               command = lambda : self.gui.show_frame( self.gui.FRAME_CREATE_FILES ) )
        button.pack()
