from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *

class GUI_ShareFiles( GuiModule ):

    def send_files( self, server ):
        print( server )
        self.context.tcp.client_send_file(
            server, "text.txt", "my content to send"
        )

    def drawDevice( self, device, i ):
       
        self.device_frame[i] = Frame( self, bg="white", padx=10, pady=10 )
        self.device_frame[i].place( x = 20, 
                            y = self.current_position.y,
                            width = (self.settings.appplication_width - 40 ), 
                            height = 45 ) 
        frame = self.device_frame[i]

        self.buttons[i] = Button( frame, text = device[0], 
                command = lambda param=( device[1], self.settings.tcp_port ): self.send_files(param) )
        self.buttons[i].place( y = 0 )

        i += 1

        pos_x = self.current_position.x + 100
        self.buttons[i] = Button( frame, text = "Get allow connection", 
                command = lambda param=( device[1], self.settings.tcp_port ): self.context.tcp.get_allow_receive( param ) )
        self.buttons[i].place( x = pos_x,
                               y =0 )

        self.current_position.y += 55

    def onStart( self ):
        self.header = Label( self, text=f"Start Text {self.context.numShareableFiles}")
        self.header.pack()
                                               
        LAN_devices = []
        LAN_devices.append( ("LOCAL", "127.0.0.1" ) )
        LAN_devices.append( ("RGD-ITA-001", "10.0.40.126" ) )
        LAN_devices.append( ("RGD-ITA-005", "10.0.1.63" ) )
        LAN_devices.append( ("RGD-ITA-002", "10.0.1.52" ) )
        LAN_devices.append( ("RGD-ITA-006", "10.0.151.181" ) )

        # do it like this for now
        self.buttons = {}
        self.device_frame = {}
        self.current_position = Vector2( 0, 50 )

        for i, device in enumerate( LAN_devices ):
            i = self.drawDevice( device, i )

        button = Button( self, text = "RESET", 
               command = lambda : self.context.removeShareableFiles() )
        button.pack()