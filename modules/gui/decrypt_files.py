
from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD
from tkinter.scrolledtext import ScrolledText

class GUI_DecryptFiles( GuiModule ):

    def goToViewFiles( self ):
        reload_frame : bool = True # redundant bool ..
        self.gui.show_frame( self.gui.FRAME_VIEW_FILES, reload_frame )

    def hasPasswordFile( self, file ):
        if file['filename'] == self.settings.password_file:
            self.is_encrypted = True

    def getPasswords( self ):
        """This will return a list of password from the file passwords.secret"""
        return 

    def drawDecryptedFile( self, file, password ):
        """This will draw each file in its original decrypted state"""
        return

    def onStart( self ):
        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.read_write.numShareableFiles}")
        header.pack()

        self.is_encrypted = False

        self.current_position = Vector2( 0, 50 )

        # Read file directory and check if 'password.secret' exists
        self.files = self.context.read_write.getTextFiles()
        for file in self.files:
            self.hasPasswordFile( file )

        if not self.is_encrypted:
            print(" There is no password file!? Howd we get here, go back!")

        placeholder = Label( self, text=f"Decrypt and show file content")
        placeholder.pack()

        # Get the passwords from 'password.secret'
        #passwords = self.getPasswords()

        # Finally decrypt and present the contents of the files.
        #for i, file in enumerate( self.files ):
            #self.drawDecryptedFile( file, password[i] )

        back = Button( self, text = "Terug", 
               command = lambda : self.goToViewFiles() )
        back.place( x = 20, 
                    y = self.settings.appplication_height - 40 )

