# app core modules
from modules.app.settings import Settings
from pathlib import Path
from fpdf import FPDF
from modules.app.read_write import ReadWrite


class ToPDF:
    def __init__(self, context) -> None:
        self.context = context
        self.settings: Settings = context.settings
        self.read_write: ReadWrite = context.read_write
        #self.txt_to_pdf()


    def txt_to_pdf(self):
        if not self.read_write.hasTextFiles():
            return

        files = self.read_write.getTextFiles()
        for file in files:
            # Initialize PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Courier", size=12)

            file_pathlib = Path(f"{self.settings.filesdir}{file['filename']}")
            file_contents = file_pathlib.read_text()
            #pdf.cell(0, 10, txt=file_contents.strip(), ln=True)
            pdf.multi_cell(0, 10, txt=file_contents)

            output_filename = file['filename'].replace("txt", "pdf")
            pdf.output(f"{self.settings.pdf_filesdir}{output_filename}")