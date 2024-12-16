from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD
from tkinter.scrolledtext import ScrolledText

from modules.translate import Translate

class GUI_ViewFiles( GuiModule ):

    def drawFile( self, file, frame ):
        header_frame = Frame(frame)
        header_frame.pack(side=TOP, fill='x', pady=0, padx=(0,20))

        header = Label( header_frame, text=f"{file['filename']}", anchor='w')
        header.pack( side=LEFT, fill='x' )

        # QR button
        qr_image = PhotoImage( file=self.settings.rootdir.joinpath( "assets\\qr_button.png" ) )
        file['gui'] = {}
        file['gui']['qr'] = Button( header_frame, image=qr_image, state=NORMAL,
                command = lambda param=file['filename']: self.context.qrcode.openQrCodeModal(param) )
        file['gui']['qr'].pack( side=RIGHT, )
        file['gui']['qr'].image = qr_image

        file['gui']['text'] = ScrolledText( frame , height=7, width=46 ) 
        file['gui']['text'].insert( END, file['contents'] ) 
        file['gui']['text'].config( state=DISABLED )
        file['gui']['text'].pack( side=TOP, pady=5, padx=4 )

    def Encrypt( self ):
        """At this point, 50 keys are going to generated, of which 3 are randomly chosen.
        Then the contents of the files should be overwritten with the output of the encryption
        Libary of choice, also the passwords used must be stored in a file called passwords.secret .."""
        self.context.crypt.encrypt_files()
        return

    def Decrypt( self ):
        """This will draw each file in its original decrypted state"""
        self.context.crypt.decrypt_files()
        return

    def encryptOrDecryptFiles( self, is_encrypted ):
        print(f"State = {int(is_encrypted)} aka: {self.crypt_button_text[is_encrypted]} ")
        
        if is_encrypted:
            self.Decrypt()
        else:
            self.Encrypt()

        self.gui.goHome()
        #reload_frame : bool = True # redundant bool ..
        #self.gui.show_frame( self.FRAME_VIEW_FILES, reload_frame )


    def on_frame_configure(self, event):
        # Update the scrollregion of the canvas whenever the content frame's size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onStart( self ):
        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.read_write.numShareableFiles}")
        header.pack()

        language : Translate.Language_t = self.context.translate.getCurrentLanguage()
        lang = Label( self, text=f"Taal: {language['name']}")
        lang.pack()

        self.crypt_button_text = [ "Encrypt", "Decrypt" ]
        is_encrypted = self.context.read_write.hasPasswordsFile()

        self.current_position = Vector2( 0, 80 )

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
        files = self.context.read_write.getTextFilesByAuth()

        for file in files:
            self.drawFile( file, content_frame )

        # update region of canvas
        self.canvas.create_window((0, 0), window=content_frame, anchor='nw')
        content_frame.update_idletasks()
        self.canvas.config( scrollregion=self.canvas.bbox( "all" ) )
        content_frame.bind( "<Configure>", self.on_frame_configure )

        # footer buttons
        crypt = Button( self, text = self.crypt_button_text[is_encrypted], 
               command = lambda : self.encryptOrDecryptFiles( is_encrypted ) )
        crypt.place( x = self.settings.appplication_width - 70, 
                      y = self.settings.appplication_height - 40 )

        # translate button
        refresh = Button( self, text = "Translate", 
               command = lambda : self.context.translate.openTranslateModal() )
        refresh.place( x = self.settings.appplication_width - 270, 
                      y = self.settings.appplication_height - 40 )

        back = Button( self, text = "Terug", 
               command = lambda : self.gui.goHome() )
        back.place( x = 20, 
                      y = self.settings.appplication_height - 40 )