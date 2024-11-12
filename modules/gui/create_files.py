from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD

class GUI_CreateFiles( GuiModule ):
    def allowConnectionCheckboxCallback( self ):
        self.settings.allowConnection = self.allowCon.get()

    def onStart( self ):
        lan_info = Label( self, text=f"LAN Address: {self.settings.server_ip}:{self.settings.tcp_port}" )
        lan_info.configure(font=("Helvetica", 14, "bold"))
        lan_info.pack()

        header = Label( self, text="Create files.." )
        header.pack()

        self.current_position = Vector2( 0, 50 )

        self.allowCon = IntVar( value=self.settings.allowConnection )
        c1 = Checkbutton( self, text='Verbindingen Toestaan',variable=self.allowCon, onvalue=1, offvalue=0, 
                        command=lambda : self.allowConnectionCheckboxCallback() )
        c1.place( x = 15, y =  self.current_position.y )