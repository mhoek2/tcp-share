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

        log = self.context.read_write.getLogFile()

        get_device = lambda ip: next((device for device in self.settings.LAN_devices if device['ip'] == ip), None)

        # sort by device
        entries_sorted = []
        current_ip : str = False
        for i,entry in enumerate(log):
            if current_ip != entry['ip']:
                current_ip = entry['ip']
                entries_sorted.append( { 'device': get_device( entry['ip'] ), 
                                         'entries': [] } )

            entries_sorted[len(entries_sorted)-1]['entries'].append( i )

        for i, device in enumerate(entries_sorted):
            device_header = Frame(header_frame)
            device_header.pack( side=TOP, fill='x', padx=(10,0), pady=(20, 0) )

            device_hostname = Label( device_header, text=f"{device['device']['hostname']}")
            device_hostname.configure(font=("Helvetica", 12, "bold"))
            device_hostname.pack( side=LEFT)

            device_ip = Label( device_header, text=f"{device['device']['ip']}")
            device_ip.configure(font=("Helvetica", 9, "normal"))
            device_ip.pack( side=LEFT)

            table = Frame(header_frame)
            table.pack(side=TOP, fill=BOTH, expand=1)

            # Create the columns
            file_label = Label(table, text="File", width=15)
            file_label.grid(row=0, column=0)
            comment_label = Label(table, text="Comment", width=15)
            comment_label.grid(row=0, column=1)
            date_label = Label(table, text="Date", width=30)
            date_label.grid(row=0, column=2)

            for i, entry_id in enumerate(device['entries']):
                entry = log[entry_id]

                file = Entry(table, width=15)
                file.grid(row=i+1, column=0)
                file.insert(0, f"{entry['file']}")

                comment = Entry(table, width=15)
                comment.grid(row=i+1, column=1)
                comment.insert(0, entry['comment'])

                date = Entry(table, width=30)
                date.grid(row=i+1, column=2)
                date.insert(0, entry['datetime'])

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