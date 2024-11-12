from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD

class GUI_CreateFiles( GuiModule ):
    def onStart( self ):
        lan_info = Label( self, text=f"LAN Address: {self.settings.server_ip}:{self.settings.tcp_port}" )
        lan_info.configure(font=("Helvetica", 14, "bold"))
        lan_info.pack()

        header = Label( self, text="Create files.." )
        header.pack()

        button = Button( self, text = "Home", 
               command = lambda : self.gui.show_frame( self.gui.FRAME_SHARE_FILES ) )
        button.pack()