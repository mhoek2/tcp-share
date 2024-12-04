
from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD
from tkinter.scrolledtext import ScrolledText

class GUI_DecryptFiles( GuiModule ):

    def goToViewFiles( self ):
        reload_frame : bool = True # redundant bool ..
        self.gui.show_frame( self.gui.FRAME_VIEW_FILES, reload_frame )

    def Decrypt( self ):
        """This will draw each file in its original decrypted state"""
        self.context.crypt.decrypt_files()
        self.context.read_write.removePasswordFile()
        self.gui.goHome()
        return

    def onStart( self ):
        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.read_write.numShareableFiles}")
        header.pack()
        
        self.current_position = Vector2( 0, 50 )
        
        self.is_encrypted = self.context.read_write.hasPasswordsFile()
        if not self.is_encrypted:
            placeholder = Label( self, text=f"Files are not encrypted")
            placeholder.pack()
        else:
            decrypt = Button( self, text = "Decrypt", 
                    command = lambda : self.Decrypt() )
            decrypt.place( x = self.settings.appplication_width - 70, 
                            y = self.settings.appplication_height - 40 )

        back = Button( self, text = "Terug", 
               command = lambda : self.goToViewFiles() )
        back.place( x = 20, 
                    y = self.settings.appplication_height - 40 )

