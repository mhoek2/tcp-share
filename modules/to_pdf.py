from typing import TYPE_CHECKING

# app core modules
from fpdf import FPDF

from modules.app.read_write import ReadWrite
from modules.app.settings import Settings

if TYPE_CHECKING:
    from main import Application


class ToPDF:
    def __init__(self, context) -> None:
        self.context: "Application" = context
        self.settings: Settings = context.settings
        self.read_write: ReadWrite = context.read_write

    def txt_to_pdf(self):
        files = []
        is_encrypted = self.context.read_write.hasPasswordsFile()

        if is_encrypted:
            # decrypt the files before reading
            self.context.crypt.decrypt_files()

        files = self.context.read_write.getTextFilesByAuth()

        for file in files:
            # Initialize PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Courier", size=12)

            pdf.multi_cell(0, 10, txt=file["contents"].decode())
            
            output_filename = file["filename"].replace("txt", "pdf")
            output = pdf.output(dest="S").encode("latin1")

            self.context.read_write.writePdfFile(output_filename, output)

        if is_encrypted:
            # re-encrypt the files
            self.context.crypt.encrypt_files()