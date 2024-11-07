from pathlib import Path

class Settings:
    def __init__( self ) -> None:
        """Global applictaion settings"""
        self.application_title = "TCP Share"
        self.application_size = "400x500"

        self.rootdir = Path.cwd()
        self.filesdir = f"{self.rootdir}\\files\\"

        # placeholder to illustrate good practice of keeping things dynamic
        self.num_files = 3
        self.num_salts = 50;
        self.num_final_salts = self.num_files;