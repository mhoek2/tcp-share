# app core modules
from modules.app.settings import Settings

from tkinter import *
from tkinter.font import BOLD

import qrcode
import os 
from modules.translate import Translate

class QRCode:
    def __init__( self, context ) -> None:
        self.context = context
        self.settings : Settings = context.settings
        self.translate : Translate = self.context.translate

    def openQrCodeModal( self, filename ) -> None:
        """Instantiate a modal which displays 
        available QR code images for each text file.
        The QR codes contain various translated version of the text file"""
        modal = Toplevel( self.context.tk_root )
        modal.title( f"QR Codes" )
        modal.grab_set()

        # move modal on top of main window
        x = self.context.tk_root.winfo_x()
        y = self.context.tk_root.winfo_y()
        modal.geometry("+%d+%d" %(x-50,y+10))

        Label(modal, text=f"QR Codes for {filename}").pack( pady=10 )

        for lang in self.translate.languages:
            qr_code_language : Translate.Language_t = lang
            filename =  os.path.splitext(filename)[0]
            filename = filename.replace(self.settings.file_encrypted_suffix, "")
            
            file_path = self.context.read_write.qrDir.joinpath( f"{filename}_{qr_code_language['api_id']}.png" ) 
            print(file_path)

            if not file_path.is_file():
                print( f"Error: file not found - {file_path}")
                continue

            qr_code_image = PhotoImage(file=file_path)

            label = Label( modal, image=qr_code_image)
            label.pack( side=LEFT )
            label.image = qr_code_image  

    def create_qr_code_for_file_lang( self, file, lang : Translate.Language_t ):
        """Create a QR code of the translated content of a file"""
        valid, text = self.translate.translate_text_file_content( file, lang )

        if not valid:
            print( text )
            return

        filename : str = file['filename'];

        qr = qrcode.QRCode(
            version=1, box_size=5, border=4,
            error_correction=qrcode.constants.ERROR_CORRECT_L
        )
        qr.add_data( text )
        qr.make( fit=True )
        img = qr.make_image( fill_color=lang['color'], back_color="black" )

        filename = os.path.splitext(filename)[0] # use os lib for now
        file_path = self.context.read_write.qrDir.joinpath( f"{filename}_{lang['api_id']}.png" ) 
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        img.save( file_path )

        return

    def create_qr_codes( self ) -> None:
        if not self.context.read_write.hasTextFiles():
            print("No text files to create a QR code from")
            return

        files = self.context.read_write.getTextFiles()

        for lang in self.translate.languages:
            for file in files:
                self.create_qr_code_for_file_lang( file, lang )

        return