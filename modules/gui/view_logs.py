from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

from tkinter import *
from tkinter.font import BOLD
from tkinter.scrolledtext import ScrolledText

from modules.logging import Logging

class GUI_ViewLogs( GuiModule ):

    def drawLog( self, frame ):
        header_frame = Frame(frame)
        header_frame.pack(side=TOP, fill='x', pady=0, padx=(0,20))

        table = Frame(header_frame)
        table.pack(fill=BOTH, expand=1)

        # Create the columns
        ip_label = Label(table, text="IP", width=15)
        ip_label.grid(row=0, column=0)
        date_label = Label(table, text="Date", width=15)
        date_label.grid(row=0, column=1)
        content_label = Label(table, text="Content", width=30)
        content_label.grid(row=0, column=2)

        log = self.context.read_write.getLogFile()
        for i, entry in enumerate(log):
            ip_entry = Entry(table, width=15)
            ip_entry.grid(row=i+1, column=0)
            ip_entry.insert(0, f"{entry['ip']}")

            date_entry = Entry(table, width=15)
            date_entry.grid(row=i+1, column=1)
            date_entry.insert(0, entry['comment'])

            content_entry = Entry(table, width=30)
            content_entry.grid(row=i+1, column=2)
            content_entry.insert(0, entry['datetime'])

        num_entries = Label( frame, text=f"Regels: {len(log)}")
        num_entries.pack()

    def refreshPage( self ):
        reload_frame : bool = True # redundant bool ..
        self.gui.show_frame( self.gui.current_frame, reload_frame )
        return

    def on_frame_configure(self, event):
        # Update the scrollregion of the canvas whenever the content frame's size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onStart( self ):

        self.current_position = Vector2( 0, 20 )

        # frame
        frame = Frame( self )
        frame.place(  y = self.current_position.y,
                      width=self.settings.appplication_width, 
                      height=self.settings.appplication_height - 75 )

        # canvas
        self.canvas = Canvas( frame, bg='white' )
        self.canvas.pack( side=LEFT, fill='both', expand=True )

        # scrollbar
        y_scrollbar = Scrollbar( frame, orient=VERTICAL, command=self.canvas.yview )
        y_scrollbar.pack( side=RIGHT, fill=Y )
        self.canvas.configure(yscrollcommand=y_scrollbar.set)

        # canvas, again
        content_frame = Frame( self.canvas )

        # content
        self.drawLog( content_frame )

        # update region of canvas
        self.canvas.create_window((0, 0), window=content_frame, anchor='nw')
        content_frame.update_idletasks()
        self.canvas.config( scrollregion=self.canvas.bbox( "all" ) )
        content_frame.bind( "<Configure>", self.on_frame_configure )

        # footer buttons
        refresh = Button( self, text = "Refresh", 
               command = lambda : self.refreshPage() )
        refresh.place( x = self.settings.appplication_width - 270, 
                      y = self.settings.appplication_height - 40 )

        back = Button( self, text = "Terug", 
               command = lambda : self.gui.goHome() )
        back.place( x = 20, 
                      y = self.settings.appplication_height - 40 )