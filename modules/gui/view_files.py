from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD

class GUI_ViewFiles( GuiModule ):


    def drawFile( self, file ):
        header = Label( self, text=f"{file['filename']}")
        header.place( x = 0, y = self.current_position.y )

        self.current_position.y += 25

        text = Text( self , height=8, width=40) 
        text.insert(END, file['content']) 
        scroll = Scrollbar( self ) 
        text.configure( yscrollcommand=scroll.set ) 
        text.place( x = 0, y = self.current_position.y ) 

        self.current_position.y += 135

    def onStart( self ):
        header = Label( self, text=f"Aantal bestanden gevonden: {self.context.read_write.numShareableFiles}")
        header.pack()

        self.current_position = Vector2( 0, 50 )

        button = Button( self, text = "Terug", 
               command = lambda : self.gui.goHome() )
        button.place( x = self.settings.appplication_width - 130, 
                      y = self.settings.appplication_height - 40 )

        # display files:
        files = self.context.read_write.getShareableFiles()

        for file in files:
            file['gui'] = {}
            self.drawFile( file )