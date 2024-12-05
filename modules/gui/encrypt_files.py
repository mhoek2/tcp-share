
from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD
from tkinter.scrolledtext import ScrolledText

class GUI_EncryptFiles( GuiModule ):

    def goToViewFiles( self ):
        reload_frame : bool = True # redundant bool ..
        self.gui.show_frame( self.gui.FRAME_VIEW_FILES, reload_frame )

    def Encrypt( self ):
        """At this point, 50 keys are going to generated, of which 3 are randomly chosen.
        Then the contents of the files should be overwritten with the output of the encryption
        Libary of choice, also the passwords used must be stored in a file called passwords.secret .."""
        self.context.crypt.encrypt_files()
        self.gui.goHome()
        return

    def onStart( self ):
        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.read_write.numShareableFiles}")
        header.pack()
        
        self.current_position = Vector2( 0, 50 )
        
        is_encrypted = self.context.read_write.hasPasswordsFile()

        if is_encrypted:
            placeholder = Label( self, text=f"Files are already encrypted")
            placeholder.pack()
        else:
            encrypt = Button( self, text = "Encrypt", 
                   command = lambda : self.Encrypt() )
            encrypt.place( x = self.settings.appplication_width - 70, 
                          y = self.settings.appplication_height - 40 )

        back = Button( self, text = "Terug", 
               command = lambda : self.goToViewFiles() )
        back.place( x = 20, 
                      y = self.settings.appplication_height - 40 )