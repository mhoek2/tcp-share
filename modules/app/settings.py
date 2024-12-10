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
        self.meta_file = "files.meta"

        # placeholder to illustrate good practice of keeping things dynamic
        self.file_prefix = "file_"
        self.file_encrypted_suffix = "_encrypted"
        self.num_files = 3
        self.num_salts = 50

        # tcp
        self.server_ip = '127.0.0.1'
        self.tcp_port = 43431
        self.allowConnection = 1
        self.bufsize_meta = 1024    # bytes for simple commands and handshakes
        self.bufsize_payload = 4096 # bytes for larger transfers content like text or bytes

        # LAN devices
        self.LAN_devices = [
            { 'hostname':'RGD-ITA-001', 'ip':'10.0.82.23', 'gui': {} },
            { 'hostname':'RGD-ITA-005', 'ip':'10.0.1.63', 'gui': {} },
            { 'hostname':'RGD-ITA-006', 'ip':'10.0.151.181', 'gui': {} },
            { 'hostname':'RGD-ITA-007', 'ip':'10.0.1.57', 'gui': {} }
        ]
