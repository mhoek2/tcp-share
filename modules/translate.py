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

    def __init__( self, context ) -> None:
        self.context = context
        self.settings : Settings = context.settings

        self.LANG_NL = 0
        self.LANG_DE = 1
        self.LANG_FR = 2

        self.languages: List[ self.Language_t ] = [
            { 'short': 'NL', 'name': 'Nederlands', 'api_id': 'nl' },
            { 'short': 'DE', 'name': 'Duits', 'api_id': 'de' },
            { 'short': 'FR', 'name': 'Frans', 'api_id': 'fr' },
        ]

        self.default_language_id = self.LANG_NL
        self.default_language = self.languages [ self.default_language_id ]

    def getCurrentLanguage( self ) -> Language_t:
        meta = self.context.read_write.getMetaFile()

        for i, language in enumerate(self.languages):
            if 'language' in meta and meta['language'] == language['api_id']:
                return language

        return self.default_language

    def modalCallback( self, modal, lang_id ):
        files = self.context.read_write.getTextFiles()
        meta = self.context.read_write.getMetaFile()

        if lang_id >= len( self.languages ):
            print("Error: language index out of bounds")
            return

        in_lang = meta['language'] if 'language' in meta else "nl"
        out_lang = self.languages[ lang_id ]['api_id']

        print( f"translate from {in_lang} to {out_lang}:{self.languages[ lang_id ]['name']}")

        #is_encrypted = self.context.read_write.hasPasswordsFile()
        #
        #if is_encrypted:
        #    self.context.crypt.decrypt_files()
        #    self.context.read_write.removePasswordFile()

        valid : bool = True # gets overwritten by the API

        for i, file in enumerate( files ):
            valid, data = self.translate_text( file['contents'], in_lang=in_lang, out_lang=out_lang )
            print(data)

            # only store the contents if it was a valid output
            if valid:
                filepath = self.context.read_write.textDir.joinpath( file['filename'] )
                with open( filepath, 'w') as f:
                    f.write( data )

        #if is_encrypted:
        #    self.context.crypt.encrypt_files()

        # store the new language api_id. eg 'nl', 'de', 'fr'
        if valid:
            meta['language'] = out_lang
            self.context.read_write.writeMetaFile( meta )

        modal.destroy()

    def openTranslateModal( self ) -> None:
        modal = Toplevel( self.context.tk_root )
        modal.title( f"Vertalen" )
        modal.grab_set()

        Label(modal, text=f"Tekstbestand vertalen").pack( pady=10 )
        
        meta = self.context.read_write.getMetaFile()

        for i, language in enumerate(self.languages):
            # disable current language button
            button_state = DISABLED if 'language' in meta and meta['language'] == language['api_id'] else NORMAL
            
            Button( modal, text=f"{self.languages[i]['name']}:{i}", state=button_state, 
                   command=lambda param=modal, lang_id=i: self.modalCallback( param, lang_id ) ).pack( side=LEFT, padx=20, pady=20 )

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