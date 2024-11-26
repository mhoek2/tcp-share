from cgitb import text
from sre_parse import State
from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD

import subprocess
from pathlib import Path

class GUI_ShareFiles( GuiModule ):

    def openSendChoiceModal( self, server ):
        # Create a new Toplevel window (modal)
        modal = Toplevel( self.gui )
        modal.title( f"Keuze" )
        modal.grab_set()

        Label(modal, text=f"Tekstbestanden of PDF's versturen naar \n {server[0]}:{server[1]}?").pack( pady=10 )
    
        Button( modal, text="Tekst", command=lambda: 
               self.sendChoiceModalCallback( server, modal, "Tekst" ) ).pack( side=LEFT, padx=20, pady=20 )

        Button( modal, text="PDF", command=lambda: 
               self.sendChoiceModalCallback( server, modal, "PDF" ) ).pack( side=RIGHT, padx=20, pady=20 )

    def sendChoiceModalCallback( self, server, modal, choice ):
        if choice == "PDF":
            print( f"Create and send pdf! {server}")
            self.send_pdf_file( server )
        else:
            print( f"Send txt! {server}")
            self.send_txt_files( server )

        modal.destroy()

    def send_txt_files( self, server ):
        files = self.context.read_write.getTextFiles()
        
        print(f"Attempt to share files to: {server}")
        print(files)

        for file in files:
            self.context.tcp.client_send_file( server, file['filename'], file['contents'].decode() )

    def send_pdf_file( self, server ):
        files = self.context.read_write.getPdfFiles()
        
        print(f"Attempt to share PDF files to: {server}")

        for file in files:
            self.context.tcp.client_send_file( server, file['filename'], file['contents'] )

    def updateDevice( self, device ):
        is_online = True if self.context.tcp.ping_device( device['ip'] ) else False
        is_allowing = False

        device['gui']['send'].config( state=DISABLED )

        if is_online:
            is_allowing = self.context.tcp.get_allow_receive( (device['ip'], self.settings.tcp_port) ) 

            if is_allowing:
                device['gui']['status'].config( text="Ready")
                device['gui']['status_indicator'].config( bg="#00ff00" )
                device['gui']['send'].config( state=NORMAL )
            else:
                device['gui']['status'].config( text="Refusing")
                device['gui']['status_indicator'].config( bg="#fc8c03" )
        else:
            device['gui']['status'].config( text="Offline")
            device['gui']['status_indicator'].config( bg="#ff0000" )

        print( f"Device {device['hostname']} on IP {device['ip']} online: {is_online} allowing: {is_allowing}" )

    def updateDevices( self ):
        for device in self.LAN_devices:
            self.updateDevice( device )

    def drawDevice( self, device ):   
        device['gui']['frame'] = Frame( self, bg="white", padx=0, pady=0 )
        device['gui']['frame'].place( x = 20, 
                            y = self.current_position.y,
                            width = (self.settings.appplication_width - 40 ), 
                            height = 45 ) 
        frame = device['gui']['frame']

        device['gui']['status_indicator'] = Frame( frame, bg="#d1d1d1", padx=0, pady=0 )
        device['gui']['status_indicator'].place( x=-0, y=-0, width=3, heigh =45 ) 

        pos_x = 10
        device['gui']['send'] = Button( frame, text = device['hostname'], state=DISABLED,
                command = lambda param=( device['ip'], self.settings.tcp_port ): self.openSendChoiceModal(param) )
        device['gui']['send'].place( y=10, x=pos_x )

        device['gui']['status'] = Label( frame, text=f"-")
        device['gui']['status'].place( x = 300, y = 10 ) 

        self.current_position.y += 55

    def allowConnectionCheckboxCallback( self ):
        self.settings.allowConnection = self.allowCon.get()

    def goToViewFiles( self ):
        reload_frame : bool = True # redundant bool ..
        self.gui.show_frame( self.gui.FRAME_VIEW_FILES, reload_frame )

    def openPDFFolderInExplorer( self ):
        print( f"open pdf folder: {self.context.read_write.pdfDir}" )

        folder_path = self.context.read_write.pdfDir

        folder_path.mkdir(parents=True, exist_ok=True)

        subprocess.run(['explorer', folder_path])

    def create_pdf( self ):
        self.context.to_pdf.txt_to_pdf()
        print("create pdf")

    def drawBrowseButtons( self ) -> None:
        browse_txt = Button( self, text = "browse txt", 
               command = lambda : self.goToViewFiles() )
        browse_txt.place( x = (self.settings.appplication_width / 2 ) - 125, 
                      y = self.current_position.y )

        # If PDF files exist, draw browse button
        # Otherwise draw the create button
        #
        # Note: It is allowed to create variable 'browse_pdf' 
        # in the scope of the if else block and use it afterwards in python
        # it seems ..
        if self.context.read_write.hasPdfFiles():
            browse_pdf = Button( self, text = "browse pdf", 
                   command = lambda : self.openPDFFolderInExplorer() )
        else:
            browse_pdf = Button( self, text = "create pdf", 
                   command = lambda : self.create_pdf() )

        browse_pdf.place( x = (self.settings.appplication_width / 2 ) + 25, 
                          y = self.current_position.y )        
        
        self.current_position.y += 25

    def _debugClearFiles( self ) -> None:
        """Debug function to clear all files 'txt' and 'pdf'"""
        self.context.read_write.removeTextFiles()
        self.context.read_write.removePdfFiles()

    def onStart( self ):
        lan_info = Label( self, text=f"LAN Address: {self.settings.server_ip}:{self.settings.tcp_port}" )
        lan_info.configure(font=("Helvetica", 14, "bold"))
        lan_info.pack()

        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.read_write.numShareableFiles}")
        header.pack()
                    
        self.LAN_devices = []
        self.LAN_devices.append( { 'hostname':'RGD-ITA-001', 'ip':'10.0.82.23', 'gui': {} } )
        self.LAN_devices.append( { 'hostname':'RGD-ITA-005', 'ip':'10.0.1.63', 'gui': {} } )
        self.LAN_devices.append( { 'hostname':'RGD-ITA-007', 'ip':'10.0.1.57', 'gui': {} } )
        self.LAN_devices.append( { 'hostname':'RGD-ITA-006', 'ip':'10.0.151.181', 'gui': {} } )

        self.device_frame = {}
        self.current_position = Vector2( 0, 50 )

        self.drawBrowseButtons()

        self.allowCon = IntVar( value=self.settings.allowConnection )
        c1 = Checkbutton( self, text='Verbindingen Toestaan',variable=self.allowCon, onvalue=1, offvalue=0, 
                        command=lambda : self.allowConnectionCheckboxCallback() )
        c1.place( x = 15, y =  self.current_position.y )

        self.current_position.y += 25

        # force LAN device status refresh
        refresh = Button( self, text = "Refresh", 
               command = lambda : self.context.bg_worker_force_gui_update() )
        refresh.place( x = 30, y = self.current_position.y )

        self.current_position.y += 40

        for device in self.LAN_devices:
            self.drawDevice( device )

        # force a gui pass in bg_worker to ping LAN devices
        self.context.bg_worker_force_gui_update()

        button = Button( self, text = "Opnieuw Beginnen", 
               command = lambda : self._debugClearFiles() )
        button.place( x = self.settings.appplication_width - 130, 
                      y = self.settings.appplication_height - 40 )

