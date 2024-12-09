# app core modules
from typing import List, TypedDict
from modules.app.settings import Settings

from tkinter import *
from tkinter.font import BOLD

import requests

class Translate:
    class Language_t(TypedDict):
        short: str
        name: str
        api_id: str
        color: str

    def __init__( self, context ) -> None:
        self.context = context
        self.settings : Settings = context.settings

        self.LANG_NL : int = 0
        self.LANG_DE : int = 1
        self.LANG_FR : int = 2

        self.languages: List[ self.Language_t ] = [
            { 'short': 'NL', 'name': 'Nederlands', 'api_id': 'nl', 'color':'green' },
            { 'short': 'DE', 'name': 'Duits', 'api_id': 'de', 'color':'yellow' },
            { 'short': 'FR', 'name': 'Frans', 'api_id': 'fr', 'color':'red' },
        ]

        self.default_language_id : int = self.LANG_NL
        self.default_language : self.Language_t = self.languages [ self.default_language_id ]

    def getLanguage( self, lang_id ) -> Language_t:
        return self.languages[lang_id]

    def getCurrentLanguage( self ) -> Language_t:
        meta = self.context.read_write.getMetaFile()

        for i, language in enumerate(self.languages):
            if 'language' in meta and meta['language'] == language['api_id']:
                return language

        return self.default_language

    def update_meta_language( self, lang_id ):
        """Store the language api_id in meta file. eg 'nl', 'de', 'fr'"""
        meta = self.context.read_write.getMetaFile()
        meta['language'] = self.languages[ lang_id ]['api_id']

        self.context.read_write.writeMetaFile( meta )

    def modalCallback( self, modal, lang_id ):
        files = self.context.read_write.getTextFiles()

        if lang_id >= len( self.languages ):
            print("Error: language index out of bounds")
            return

        #is_encrypted = self.context.read_write.hasPasswordsFile()
        #
        #if is_encrypted:
        #    self.context.crypt.decrypt_files()
        #    self.context.read_write.removePasswordFile()

        valid : bool = True

        for file in files:
            valid, text = self.translate_text_file_content( file, lang_id )

            if valid:
                self.context.read_write.writeTextFile( file['filename'], text )
            else:
                print( text )

        #if is_encrypted:
        #    self.context.crypt.encrypt_files()

        if valid:
            self.update_meta_language( lang_id )

        self.context.bg_worker_force_file_update()

        modal.destroy()

    def openTranslateModal( self ) -> None:
        modal = Toplevel( self.context.tk_root )
        modal.title( f"Vertalen" )
        modal.grab_set()

        Label(modal, text=f"Tekstbestand vertalen").pack( pady=10 )
        
        current_language : self.Language_t = self.getCurrentLanguage()

        for lang_id, language in enumerate(self.languages):
            # disable current language button
            button_state = DISABLED if current_language['api_id'] == language['api_id'] else NORMAL
            
            Button( modal, text=f"{language['name']}", state=button_state, 
                command=lambda param=modal, lang_id=lang_id: self.modalCallback( param, lang_id ) ).pack( side=LEFT, padx=20, pady=20 )

    def translate_text_file_content( self, file, lang_id ):
        """Translate"""
        filename : str  = file['filename'];
        text: str = file['contents'].decode('utf-8', errors='ignore');
        valid : bool = False

        current_language : self.Language_t = self.getCurrentLanguage()
        qr_code_language : self.Language_t = self.languages[lang_id]

        in_lang = current_language['api_id']
        out_lang = qr_code_language['api_id']
        print( f"translate from {in_lang} to {out_lang}:{self.languages[ lang_id ]['name']}")

        if in_lang != out_lang:
            valid, text = self.translate_text( text, in_lang, out_lang )
        else:
            text = text
            valid = True # content is already in the requrested language

        if not valid:
            text = "Text not succesfully translated during QR code generation"
        
        return valid, text

    def translate_text( self, text, in_lang, out_lang ) -> str:
        """Use this free curl for now
        This can be replaced with a better more stable API in the future"""
        url = "https://api.mymemory.translated.net/get"
    
        params = {
            "q": text,
            "langpair": f"{in_lang}|{out_lang}"
        }

        valid : bool = False # default state

        try:
            response = requests.get(url, params=params)
        
            if response.status_code == 200:
                translation = response.json()

                valid = True
                output = translation['responseData']['translatedText']

                if output == "PLEASE SELECT TWO DISTINCT LANGUAGES":
                    valid = False

                return valid, output
            else:
                return valid, f"Error: {response.status_code}, Message: {response.text}"

        except requests.exceptions.RequestException as e:
            return valid, f"An error occurred: {e}"