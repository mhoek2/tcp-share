from pathlib import Path

class Settings:
    def __init__( self ) -> None:
        """Global applictaion settings"""
        self.application_title = "TCP Share"
        self.appplication_width = 400       # winfo_width & winfo_height doesnt work?
        self.appplication_height = 500
        self.application_size = f"{self.appplication_width}x{self.appplication_height}"

        self.rootdir = Path.cwd()
        self.filesdir = f"{self.rootdir}\\files\\"

        # placeholder to illustrate good practice of keeping things dynamic
        self.num_files = 3
        self.num_salts = 50;
        self.num_final_salts = self.num_files;

        # tcp
        self.server_ip = '10.0.1.63'
        self.tcp_port = 43431