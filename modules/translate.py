# app core modules
from typing import List, TypedDict
from modules.app.settings import Settings

from tkinter import *
from tkinter.font import BOLD

import requests

class Translate:
    class Language_t(TypedDict):
        lang_id: int
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
        for i, l in enumerate(self.languages):  l['lang_id'] = i

        self.default_language : self.Language_t = self.languages [ self.LANG_NL ]

    def getDefaultLanguage( self ) -> Language_t:
        return self.default_language;

    def getLanguageByID( self, lang_id : int ) -> Language_t:
        return self.languages[lang_id]

    def getLanguageID( self, lang : Language_t ) -> int:
        return lang['lang_id']

    def getCurrentLanguage( self ) -> Language_t:
        """Get the current language of the files, stored in the meta file"""
        meta = self.context.read_write.getMetaFile()

        for lang in self.languages:
            if 'language' in meta and meta['language'] == lang['api_id']:
                return lang

        return self.getDefaultLanguage()

    def update_meta_language( self, lang : Language_t ):
        """Store the language api_id in meta file. eg 'nl', 'de', 'fr'"""
        meta = self.context.read_write.getMetaFile()
        meta['language'] = lang['api_id']

        self.context.read_write.writeMetaFile( meta )

    def modalCallback( self, modal, lang : Language_t ):
        files = self.context.read_write.getTextFiles()

        if not lang:
            print("Error: language is undefined")
            return

        is_encrypted = self.context.read_write.hasPasswordsFile()

        if is_encrypted:
            # decrypt the files before reading
            self.context.crypt.decrypt_files()

        valid : bool = True
        for file in files:
            valid, text = self.translate_text_file_content( file, lang )

            if valid:
                self.context.read_write.writeTextFile( file['filename'], text )
            else:
                print( text )

        if is_encrypted:
            # re-encrypt the files
            self.context.crypt.encrypt_files()

        if valid:
            self.update_meta_language( lang )

        self.context.bg_worker_force_file_update()

        modal.destroy()

    def openTranslateModal( self ) -> None:
        modal = Toplevel( self.context.tk_root )
        modal.title( f"Vertalen" )
        modal.grab_set()

        Label(modal, text=f"Tekstbestand vertalen").pack( pady=10 )
        
        current_language : self.Language_t = self.getCurrentLanguage()

        for lang in self.languages:
            # disable current language button
            button_state = DISABLED if current_language['api_id'] == lang['api_id'] else NORMAL
            
            Button( modal, text=f"{lang['name']}", state=button_state, 
                command=lambda param=modal, lang=lang: self.modalCallback( param, lang ) ).pack( side=LEFT, padx=20, pady=20 )

    def translate_text_file_content( self, file, out_lang : Language_t ):
        """Translate"""
        filename : str  = file['filename'];
        text: str = file['contents'].decode('utf-8', errors='ignore');
        valid : bool = False

        in_lang : self.Language_t = self.getCurrentLanguage()
        print( f"translate from {in_lang} to {out_lang}:{out_lang['name']}")

        if in_lang != out_lang:
            valid, text = self.translate_text( text, in_lang, out_lang )
        else:
            text = text
            valid = True # content is already in the requrested language

        if not valid:
            text = "Text not succesfully translated during QR code generation"
        
        return valid, text

    def translate_text( self, text : str, in_lang : Language_t, out_lang : Language_t ) -> str:
        """Use this free curl for now
        This can be replaced with a better more stable API in the future"""
        url = "https://api.mymemory.translated.net/get"
    
        params = {
            "q": text,
            "langpair": f"{in_lang['api_id']}|{out_lang['api_id']}"
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