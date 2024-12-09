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

        Label(modal, text=f"QR Codes for {filename}").pack( pady=10 )

        for lang_id, language in enumerate(self.translate.languages):
            qr_code_language = self.translate.languages[lang_id]
            filename =  os.path.splitext(filename)[0]
            file_path = self.context.read_write.qrDir.joinpath( f"{filename}_{qr_code_language['api_id']}.png" ) 
            print(file_path)

            qr_code_image = PhotoImage(file=file_path)

            label = Label( modal, image=qr_code_image)
            label.pack( side=LEFT )
            label.image = qr_code_image  

    def create_qr_code_for_file_lang( self, file, lang_id ):
        """Create a QR code of the translated content of a file"""
        valid, text = self.translate.translate_text_file_content( file, lang_id )

        if not valid:
            print( text )
            return

        language: Translate.Language_t = self.translate.getLanguage( lang_id )
        filename : str = file['filename'];

        qr = qrcode.QRCode(
            version=1, box_size=5, border=4,
            error_correction=qrcode.constants.ERROR_CORRECT_L
        )
        qr.add_data( text )
        qr.make( fit=True )
        img = qr.make_image( fill_color=language['color'], back_color="black" )

        filename = os.path.splitext(filename)[0] # use os lib for now
        file_path = self.context.read_write.qrDir.joinpath( f"{filename}_{language['api_id']}.png" ) 
        img.save( file_path )

        return

    def create_qr_codes( self ) -> None:
        if not self.context.read_write.hasTextFiles():
            print("No text files to create a QR code from")
            return

        files = self.context.read_write.getTextFiles()

        for lang_id, language in enumerate( self.translate.languages ):
            for file in files:
                self.create_qr_code_for_file_lang( file, lang_id )

        return