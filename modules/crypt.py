# app core modules
from typing import final

from modules.app.settings import Settings
from cryptography.fernet import Fernet
import random

class Crypt:
    def __init__( self, context ) -> None:
        self.context = context
        self.settings : Settings = context.settings
        self.test_encrypt()
        self.test_decrypt()

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
        final_encrypted_txt = self.encrypt_txt()
        with open('Encrypted_text.txt', 'w') as f:
            f.write(final_encrypted_txt.decode())
            print(final_encrypted_txt)

    def test_decrypt(self):
        decrypted_txt = self.decrypt_txt()
        print(decrypted_txt)

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
        return key_list[0]

    def read_encrypted_file(self):
        with open("Encrypted_text.txt") as f:
            encrypted_txt = f.read()
            return encrypted_txt

    def encrypt_txt(self):
        unencrypted_txt = self.read_txt()
        password = self.read_password_file()
        f = Fernet(password)
        encrypted_txt = f.encrypt(unencrypted_txt.encode())
        return encrypted_txt

    def decrypt_txt(self):
        key = self.read_password_file()
        f = Fernet(key)
        encrypted_txt = self.read_encrypted_file()
        decrypted_data = f.decrypt(encrypted_txt.encode())
        return decrypted_data

