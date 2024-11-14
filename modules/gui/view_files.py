from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD
from tkinter.scrolledtext import ScrolledText

class GUI_ViewFiles( GuiModule ):

    def drawFile( self, file ):
        header = Label( self, text=f"{file['filename']}")
        header.place( x = 0, y = self.current_position.y )

        self.current_position.y += 25

        file['gui']['text'] = ScrolledText( self , height=8, width=46 ) 
        file['gui']['text'].insert( END, file['content'] ) 
        file['gui']['text'].config( state=DISABLED )
        file['gui']['text'].place( x = 5, y = self.current_position.y ) 

        self.current_position.y += 135

    def encryptOrDecryptFiles( self, state ):
        print(f"State = {int(state)} aka: {self.crypt_button_text[state]} ")
        
        reload_frame : bool = True # redundant bool ..
        self.gui.show_frame( self.crypt_button_frame[state], reload_frame )

    def hasPasswordFile( self, file ):
        if file['filename'] == self.settings.password_file:
            self.is_encrypted = True

    def onStart( self ):
        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.read_write.numShareableFiles}")
        header.pack()

        self.crypt_button_text = [ "Encrypt", "Decrypt" ]
        self.crypt_button_frame = [ self.gui.FRAME_ENCRYPT_FILES, self.gui.FRAME_DECRYPT_FILES ]
        self.is_encrypted = False

        self.current_position = Vector2( 0, 50 )

        self.files = self.context.read_write.getShareableFiles()
        for file in self.files:
            self.hasPasswordFile( file )

            file['gui'] = {}
            self.drawFile( file )

        crypt = Button( self, text = self.crypt_button_text[self.is_encrypted], 
               command = lambda : self.encryptOrDecryptFiles( self.is_encrypted ) )
        crypt.place( x = self.settings.appplication_width - 70, 
                      y = self.settings.appplication_height - 40 )

        back = Button( self, text = "Terug", 
               command = lambda : self.gui.goHome() )
        back.place( x = 20, 
                      y = self.settings.appplication_height - 40 )