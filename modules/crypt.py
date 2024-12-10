import random
from typing import TYPE_CHECKING

from cryptography.fernet import Fernet

if TYPE_CHECKING:
    from main import Application


class Crypt:
    def __init__(self, context: "Application") -> None:
        self.context = context
        self.settings = context.settings
        self.encrypted_suffix = self.settings.file_encrypted_suffix

    def generate_keys(self) -> list[str]:
        """
        Generate and return a list of 50 keys (or whatever the value of
        the num_salts setting is.)
        """
        return [Fernet.generate_key().decode() for _ in range(self.settings.num_salts)]

    def pick_keys(self, contents: list[str], amount: int) -> list[str]:
        """
        Pick a given number of keys and return them.
        (In principle, the amount of keys is equal to the amount of
        unencrypted text files.)
        """
        return random.sample(contents, amount)

    def get_password_from_file(self, i: int) -> str:
        """Read the passwords file and return the i-th key."""
        contents = self.context.read_write.getKeys()
        return contents[i]

    def make_passwords_file(self, amount: int) -> None:
        """
        Make the passwords file, but only if it has not already been made
        (and already contains the correct amount of passwords).
        """
        existing_keys = self.context.read_write.getKeys()
        if self.context.read_write.hasPasswordsFile() and len(existing_keys) == amount:
            return

        # Generate the keys for encryption and write the keys to a file.
        self.context.read_write.writePasswordsFile(self.generate_keys())

        # Pick the given number of passwords (i) from the file,
        #   and overwrite the file with those picked passwords.
        self.context.read_write.writePasswordsFile(
            self.pick_keys(self.context.read_write.getKeys(), amount)
        )

    def encrypt_files(self) -> None:
        """
        Encrypt all (unencrypted) text files one by one.
        It first calls the make_passwords_file function.
        """
        files = self.context.read_write.getTextFiles()

        self.make_passwords_file(len(files))

        for i, file in enumerate(files):
            encrypted_contents = self.encrypt_text(file["contents"], i)

            new_filename = file["filename"].replace(
                ".txt", f"{self.encrypted_suffix}.txt"
            )
            self.context.read_write.writeTextFile(
                new_filename, encrypted_contents.decode()
            )

    def encrypt_text(self, text: bytes, i: int) -> bytes:
        """
        Encrypt text with the given password (retrieved with get_password_from_file)
        and return the encrypted text.
        """
        return Fernet(self.get_password_from_file(i)).encrypt(text)

    def decrypt_files(self) -> None:
        """
        Decrypt all text files one by one.
        (For now, the decrypted files are being saved with the suffix _decrypted,
        but this can be changed to save without any suffix—
        overwriting the original text files, if those were present.)
        It may be handy to first check whether the passwords file actually exists.
        """
        files = self.context.read_write.getEncryptedTextFiles()

        for i, file in enumerate(files):
            decrypted_contents = self.decrypt_text(file["contents"], i)

            new_filename = file["filename"].replace(self.encrypted_suffix, "")
            self.context.read_write.writeTextFile(
                new_filename, decrypted_contents.decode()
            )

        self.context.read_write.removePasswordsFile()

    def decrypt_text(self, text: bytes, i: int) -> bytes:
        """
        Decrypt text with the given password (retrieved with get_password_from_file)
        and return the decrypted text.
        """
        return Fernet(self.get_password_from_file(i)).decrypt(text)
