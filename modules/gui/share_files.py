from cgitb import text
from sre_parse import State
from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD

class GUI_ShareFiles( GuiModule ):

    def send_files( self, server ):
        files = self.context.getShareableFiles()
        
        print(f"Attempt to share files to: {server}")
        print(files)

        for file in files:
            self.context.tcp.client_send_file( server, file['filename'], file['content'] )

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
        j = 0;
        device['gui']['send'] = Button( frame, text = device['hostname'], state=DISABLED,
                command = lambda param=( device['ip'], self.settings.tcp_port ): self.send_files(param) )
        device['gui']['send'].place( y=10, x=pos_x )

        j += 1

        device['gui']['status'] = Label( frame, text=f"-")
        device['gui']['status'].place( x = 300, y = 10 ) 

        self.current_position.y += 55

    def allowConnectionCheckboxCallback( self ):
        self.settings.allowConnection = self.allowCon.get()

    def goToViewFiles( self ):
        reload_frame : bool = True # redundant bool ..
        self.gui.show_frame( self.gui.FRAME_VIEW_FILES, reload_frame )

    def onStart( self ):
        lan_info = Label( self, text=f"LAN Address: {self.settings.server_ip}:{self.settings.tcp_port}" )
        lan_info.configure(font=("Helvetica", 14, "bold"))
        lan_info.pack()

        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.numShareableFiles}")
        header.pack()
                    
        self.LAN_devices = []
        self.LAN_devices.append( { 'hostname':'RGD-ITA-001', 'ip':'10.0.40.126', 'gui': {} } )
        self.LAN_devices.append( { 'hostname':'RGD-ITA-005', 'ip':'10.0.1.63', 'gui': {} } )
        self.LAN_devices.append( { 'hostname':'RGD-ITA-007', 'ip':'10.0.1.57', 'gui': {} } )
        self.LAN_devices.append( { 'hostname':'RGD-ITA-006', 'ip':'10.0.151.181', 'gui': {} } )

        self.device_frame = {}
        self.current_position = Vector2( 0, 50 )

        browse = Button( self, text = "browse", 
               command = lambda : self.goToViewFiles() )
        browse.place( x = (self.settings.appplication_width / 2 ) - 25, 
                      y = self.current_position.y )

        self.current_position.y += 25

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
               command = lambda : self.context.removeShareableFiles() )
        button.place( x = self.settings.appplication_width - 130, 
                      y = self.settings.appplication_height - 40 )

