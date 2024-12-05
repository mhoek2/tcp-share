# app core modules
from typing import final

from modules.app.settings import Settings
from cryptography.fernet import Fernet
import random

class Crypt:
    def __init__( self, context ) -> None:
        self.context = context
        self.settings : Settings = context.settings
        
        self.password_file = self.context.read_write.textDir.joinpath( self.settings.password_file )
       
        #self.encrypt_files()
        #self.decrypt_files()


    def encrypt_files(self):
        files = self.context.read_write.getTextFiles()

        # create passwords
        keys = self.generate_key()
        with open( self.password_file, 'w') as f:
            for line in keys:
                f.write(line)
                f.write('\n')

        # read passwords
        with open(self.password_file) as f:
            contents = f.readlines()

        # pick keys and write
        picked_keys = self.pick_keys(contents)
        with open(self.password_file, 'w') as f:
            for line in picked_keys:
                f.write(line)
  
        for i, file in enumerate( files ):
            data = self.encrypt_txt( i, file )

            filepath = self.context.read_write.textDir.joinpath( file['filename'] )
            with open( filepath, 'w') as f:
                f.write( data.decode() )

    def decrypt_files(self):
        files = self.context.read_write.getTextFiles()

        for i, file in enumerate( files ):
            decrypted_txt = self.decrypt_txt( file, i )
           
            filepath = self.context.read_write.textDir.joinpath( file['filename'] )
            with open( filepath, 'w') as f:
                f.write( decrypted_txt.decode() )


    def generate_key(self):
        output_keys = []
        for i in range(0, 50):
            key = Fernet.generate_key()
            output_keys.append(key.decode())
        return output_keys

    def pick_keys(self, contents):
        output_picked_keys = []
        for i in range(0, 3):
            choice = (random.choice(contents))
            output_picked_keys.append(choice)
        return output_picked_keys

    def read_password_file( self, index ):
        key_list = []
        with open(self.password_file) as f:
            contents = f.readlines()
        for line in contents:
            key_list.append(line)
        return key_list[index]

    def read_encrypted_file( self, file ):
        filepath = self.context.read_write.textDir.joinpath( file['filename'] )
        with open(filepath) as f:
            encrypted_txt = f.read()
            return encrypted_txt

    def encrypt_txt(self, index, file):
        unencrypted_txt = file['contents'].decode()
        password = self.read_password_file( index )
        f = Fernet(password)
        encrypted_txt = f.encrypt(unencrypted_txt.encode())
        return encrypted_txt

    def decrypt_txt(self, file, index ):
        key = self.read_password_file( index )
        f = Fernet(key)
        encrypted_txt = self.read_encrypted_file( file )
        decrypted_data = f.decrypt(encrypted_txt.encode())
        return decrypted_data

