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

        # self.test_encrypt()
        # self.test_decrypt()

    def test_encrypt(self) -> None:
        """
        Function to test generating the keys.
        (Basically obsolete now, as encrypt_files does the same.)
        """
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
        """
        Function to test decrypting the files.
        Also basically obsolete now, especially as it only calls decrypt_files()
        """
        self.decrypt_files()

    def generate_keys(self) -> list[str]:
        """
        Generate and return a list of 50 keys (or whatever the value of
        the num_salts setting is.)
        """
        output_keys: list[str] = []
        for _ in range(0, self.settings.num_salts):
            key = Fernet.generate_key()
            output_keys.append(key.decode())
        return output_keys

    def pick_keys(self, contents: list[str], amount: int) -> list[str]:
        """
        Pick a given number of keys and return them.
        (In principle, the amount of keys is equal to the amount of
        unencrypted text files.)
        """
        output_picked_keys: list[str] = []
        for _ in range(0, amount):
            choice = random.choice(contents)
            output_picked_keys.append(choice)
            contents.remove(choice)
        return output_picked_keys

    def get_password_from_file(self, i: int) -> str:
        """Read the passwords file and return the i-th key."""
        contents = self.context.read_write.getPasswordsFile()
        return contents[i]

    def make_passwords_file(self, amount: int) -> None:
        """
        Make the passwords file, but only if it has not already been made
        (and already contains the correct amount of passwords).
        """
        if (
            self.context.read_write.hasPasswordsFile
            and len(self.context.read_write.getPasswordsFile()) == amount
        ):
            return
        # Generate the keys for encryption and write the keys to a file.
        self.context.read_write.writePasswordsFile(self.generate_keys())

        # Pick the given number of passwords (i) from the file,
        #   and overwrite the file with those picked passwords.
        self.context.read_write.writePasswordsFile(
            self.pick_keys(self.context.read_write.getPasswordsFile(), amount)
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

            new_filename = file["filename"].replace(self.encrypted_suffix, "_decrypted")
            self.context.read_write.writeTextFile(
                new_filename, decrypted_contents.decode()
            )

    def decrypt_text(self, text: bytes, i: int) -> bytes:
        """
        Decrypt text with the given password (retrieved with get_password_from_file)
        and return the decrypted text.
        """
        return Fernet(self.get_password_from_file(i)).decrypt(text)
