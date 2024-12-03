import random
from typing import TYPE_CHECKING

from cryptography.fernet import Fernet

# app core modules
from modules.app.read_write import ReadWrite
from modules.app.settings import Settings

if TYPE_CHECKING:
    from main import Application


class Crypt:
    def __init__(self, context) -> None:
        self.context: "Application" = context
        self.settings: Settings = context.settings
        self.encrypted_suffix = self.settings.file_encrypted_suffix

        self.files_range = range(0, self.settings.num_files)

        # self.test_encrypt()
        # self.test_decrypt()

    def test_encrypt(self) -> None:
        # 1. Generate the keys for encryption
        keys = self.generate_keys()
        # 2. Write the keys to a file
        self.context.read_write.writePasswordsFile(keys)
        # 3. Read the passwords file and assign its contents to a variable
        contents = self.context.read_write.getPasswordsFile()
        # 4. Get the current amount of text files (excluding already
        #      encrypted files and the password file itself)
        amount = len(self.context.read_write.getTextFiles())
        # 5. Pick {amount} keys, so that there are as many keys as there
        #      are files.
        picked_keys = self.pick_keys(contents, amount)
        # 6. Write the picked keys back to the passwords file, overwriting
        #      the previous version (that still contained all the keys).
        self.context.read_write.writePasswordsFile(picked_keys)
        # 7. Encrypt all text files.
        self.encrypt_files()

    def test_decrypt(self) -> None:
        self.decrypt_files()

    def generate_keys(self) -> list:
        output_keys = []
        for i in range(0, self.settings.num_salts):
            key = Fernet.generate_key()
            output_keys.append(key.decode())
        return output_keys

    def pick_keys(self, contents, amount: int) -> list:
        output_picked_keys = []
        for i in range(0, amount):
            choice = random.choice(contents)
            output_picked_keys.append(choice)
        return output_picked_keys

    # def read_txt(self):
    #     with open("fake_Nick_file.txt") as f:
    #         fake_file = f.read()
    #         return fake_file

    def read_password_file(self, i: int) -> str:
        key_list = []
        # with open("Picked_keys.txt") as f:
        #     contents = f.readlines()
        contents = self.context.read_write.getPasswordsFile()
        for line in contents:
            key_list.append(line)
        return key_list[i]

    # def read_encrypted_file(self):
    #     with open("Encrypted_text.txt") as f:
    #         encrypted_txt = f.read()
    #         return encrypted_txt

    def encrypt_files(self) -> None:
        files = self.context.read_write.getTextFiles()

        for i, file in enumerate(files):
            encrypted_contents = self.encrypt_txt(file, i)

            new_filename = file["filename"].replace(
                ".txt", f"{self.encrypted_suffix}.txt"
            )
            self.context.read_write.writeTextFile(
                new_filename, encrypted_contents.decode()
            )

    def encrypt_txt(self, file: ReadWrite.FilesDict, i: int) -> bytes:
        unencrypted_txt = file["contents"].decode()
        password = self.read_password_file(i)
        f = Fernet(password)
        encrypted_txt = f.encrypt(unencrypted_txt.encode())

        return encrypted_txt

    def decrypt_files(self) -> None:
        files = self.context.read_write.getEncryptedTextFiles()

        for i, file in enumerate(files):
            decrypted_contents = self.decrypt_txt(file, i)

            new_filename = file["filename"].replace(self.encrypted_suffix, "_decrypted")
            self.context.read_write.writeTextFile(
                new_filename, decrypted_contents.decode()
            )

    def decrypt_txt(self, file: ReadWrite.FilesDict, i: int) -> bytes:
        key = self.read_password_file(i)
        f = Fernet(key)
        encrypted_txt = file["contents"]
        decrypted_data = f.decrypt(encrypted_txt)
        return decrypted_data
