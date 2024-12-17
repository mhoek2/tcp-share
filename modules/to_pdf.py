from typing import TYPE_CHECKING

# app core modules
from fpdf import FPDF

from modules.app.read_write import ReadWrite
from modules.app.settings import Settings
from modules.logging import Logging

if TYPE_CHECKING:
    from main import Application


class ToPDF:
    def __init__(self, context) -> None:
        self.context: "Application" = context
        self.settings: Settings = context.settings
        self.read_write: ReadWrite = context.read_write

    def log_to_pdf(self) -> None:
        log = self.context.read_write.getLogFile()

        get_device = lambda ip: next((device for device in self.settings.LAN_devices if device['ip'] == ip), { 'hostname':'n/a', 'ip':ip })
        
        entries_sorted = []
        current_ip : str = False
        for i,entry in enumerate(log):
            if current_ip != entry['ip']:
                current_ip = entry['ip']
                entries_sorted.append( { 'device': get_device( entry['ip'] ), 
                                         'entries': [] } )

            entries_sorted[len(entries_sorted)-1]['entries'].append( i )

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        


        for i, device in enumerate(entries_sorted):
            pdf.set_font("Courier", style='B', size=14)
            pdf.cell(0, 10, txt=f"{device['device']['hostname']} - {device['device']['ip']}", ln=True)
            
            pdf.set_font("Courier", size=12)
            for i, entry_id in enumerate(device['entries']):
               entry = log[entry_id]
               pdf.cell(0, 10, txt=f"[{entry['datetime']}]: {entry['file']} - {entry['comment']}", ln=True)

            continue

        output_filename = self.settings.log_file.replace(".", "_");

        output = pdf.output(dest="S").encode("latin1")

        date_time = Logging.get_date_time().replace(":", "-")
        output_filename = f"{output_filename}_{date_time}.pdf"

        self.context.read_write.writePdfFile( output_filename, output)
        self.context.log.log_file( output_filename, f"Log to PDF Created" )
        return

    def txt_to_pdf(self) -> None:
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
            self.context.log.log_file( output_filename, f"PDF Created" )

        if is_encrypted:
            # re-encrypt the files
            self.context.crypt.encrypt_files()