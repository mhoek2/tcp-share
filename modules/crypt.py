# app core modules
from modules.app.read_write import ReadWrite
from modules.app.settings import Settings
from cryptography.fernet import Fernet
import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Application

class Crypt:
    def __init__( self, context ) -> None:
        self.context: "Application" = context
        self.settings : Settings = context.settings
        self.suffix = self.context.settings.file_encrypted_suffix
        # self.test_encrypt()
        # self.test_decrypt()

    def test_encrypt(self):
        keys = self.generate_key()
        with open('Generated_keys.txt', 'w') as f:
            for line in keys:
                f.write(line)
                f.write('\n')
        with open("Generated_keys.txt") as f:
            contents = f.readlines()
        picked_keys = self.pick_keys(contents)
        with open('Picked_keys.txt', 'w') as f:
            for line in picked_keys:
                f.write(line)
        self.encrypt_files()

    def test_decrypt(self):
        self.decrypt_files()

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

    def read_txt(self):
        with open("fake_Nick_file.txt") as f:
            fake_file = f.read()
            return fake_file

    def read_password_file(self):
        key_list = []
        with open("Picked_keys.txt") as f:
            contents = f.readlines()
        for line in contents:
            key_list.append(line)
        return key_list[0] # TO-DO: make dynamic

    def read_encrypted_file(self):
        with open("Encrypted_text.txt") as f:
            encrypted_txt = f.read()
            return encrypted_txt

    def encrypt_files(self) -> None:
        files = self.context.read_write.getTextFiles()

        for file in files:
            encrypted_contents = self.encrypt_txt(file)
            
            new_filename = file["filename"].replace(".txt", f"{self.suffix}.txt")
            self.context.read_write.writeTextFile(new_filename, encrypted_contents.decode())

    def encrypt_txt(self, file: ReadWrite.FilesDict) -> bytes:
        unencrypted_txt = file['contents'].decode()
        password = self.read_password_file()
        f = Fernet(password)
        encrypted_txt = f.encrypt(unencrypted_txt.encode())
        
        return encrypted_txt
    
    def decrypt_files(self) -> None:
        files = self.context.read_write.getEncryptedTextFiles()
        
        for file in files:
            decrypted_contents = self.decrypt_txt(file)
            
            new_filename = file["filename"].replace(self.suffix, "_decrypted")
            print(new_filename)
            self.context.read_write.writeTextFile(
                new_filename, decrypted_contents.decode()
            )

    def decrypt_txt(self, file: ReadWrite.FilesDict) -> bytes:
        key = self.read_password_file()
        f = Fernet(key)
        encrypted_txt = file["contents"]
        decrypted_data = f.decrypt(encrypted_txt)
        return decrypted_data
