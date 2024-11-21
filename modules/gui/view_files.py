from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD
from tkinter.scrolledtext import ScrolledText

class GUI_ViewFiles( GuiModule ):

    def drawFile( self, file, frame ):
        header = Label( frame, text=f"{file['filename']}", anchor='w')
        header.pack( side=TOP, fill='x' )

        file['gui']['text'] = ScrolledText( frame , height=7, width=46 ) 
        file['gui']['text'].insert( END, file['contents'] ) 
        file['gui']['text'].config( state=DISABLED )
        file['gui']['text'].pack( side=TOP, pady=5, padx=4 ) 

    def encryptOrDecryptFiles( self, state ):
        print(f"State = {int(state)} aka: {self.crypt_button_text[state]} ")
        
        reload_frame : bool = True # redundant bool ..
        self.gui.show_frame( self.crypt_button_frame[state], reload_frame )

    def hasPasswordFile( self, file ):
        if file['filename'] == self.settings.password_file:
            self.is_encrypted = True


    def on_frame_configure(self, event):
        # Update the scrollregion of the canvas whenever the content frame's size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onStart( self ):
        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.read_write.numShareableFiles}")
        header.pack()

        self.crypt_button_text = [ "Encrypt", "Decrypt" ]
        self.crypt_button_frame = [ self.gui.FRAME_ENCRYPT_FILES, self.gui.FRAME_DECRYPT_FILES ]
        self.is_encrypted = False

        self.current_position = Vector2( 0, 50 )

        # frame
        frame = Frame( self )
        frame.place(  y = self.current_position.y,
                      width=self.settings.appplication_width, 
                      height=self.settings.appplication_height - 125 )

        # canvas
        self.canvas = Canvas( frame, bg='white' )
        self.canvas.pack( side=LEFT, fill='both', expand=True )

        # scrollbar
        y_scrollbar = Scrollbar( frame, orient=VERTICAL, command=self.canvas.yview )
        y_scrollbar.pack( side=RIGHT, fill=Y )
        self.canvas.configure(yscrollcommand=y_scrollbar.set)

        # canvas, again
        content_frame = Frame( self.canvas )

        # content
        self.files = self.context.read_write.getTextFiles()
        for file in self.files:
            self.hasPasswordFile( file )

            file['gui'] = {}
            self.drawFile( file, content_frame )

        # update region of canvas
        self.canvas.create_window((0, 0), window=content_frame, anchor='nw')
        content_frame.update_idletasks()
        self.canvas.config( scrollregion=self.canvas.bbox( "all" ) )
        content_frame.bind( "<Configure>", self.on_frame_configure )

        # footer buttons
        crypt = Button( self, text = self.crypt_button_text[self.is_encrypted], 
               command = lambda : self.encryptOrDecryptFiles( self.is_encrypted ) )
        crypt.place( x = self.settings.appplication_width - 70, 
                      y = self.settings.appplication_height - 40 )

        back = Button( self, text = "Terug", 
               command = lambda : self.gui.goHome() )
        back.place( x = 20, 
                      y = self.settings.appplication_height - 40 )