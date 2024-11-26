from pathlib import Path
from tkinter import IntVar

class Settings:
    def __init__( self ) -> None:
        """Global applictaion settings"""
        self.application_title = "TCP Share"
        self.appplication_width = 400       # winfo_width & winfo_height doesnt work?
        self.appplication_height = 500
        self.application_size = f"{self.appplication_width}x{self.appplication_height}"

        self.rootdir = Path.cwd()
        self.filesdir = f"{self.rootdir}\\files\\"
        self.txt_subdir = "txt"
        self.pdf_subdir = "pdf"
        self.password_file = "passwords.secret"

        # placeholder to illustrate good practice of keeping things dynamic
        self.file_prefix = "file_"
        self.num_files = 3
        self.num_salts = 50;
        self.num_final_salts = self.num_files;

        # tcp
        self.server_ip = '127.0.0.1'
        self.tcp_port = 43431
        self.allowConnection = 1