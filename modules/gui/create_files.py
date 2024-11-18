from pathlib import Path
from typing import TypedDict
from modules.app.helper import Vector2

from modules.gui.gui_module import GuiModule

import tkinter as tk
# from tkinter.font import BOLD


class GUI_CreateFiles(GuiModule):
    class WidgetDict(TypedDict):
        header: tk.Label
        textbox: tk.Text

    def allowConnectionCheckboxCallback(self):
        self.settings.allowConnection = self.allowCon.get()

    def drawWidgets(self, range):
        prefix = self.context.settings.file_prefix
        self.widgets: list[GUI_CreateFiles.WidgetDict] = []

        for i in range:
            self.widgets.append(
                {
                    "header": tk.Label(self, text=f"{prefix}{(i + 1)}"),
                    "textbox": tk.Text(self, height=6, width=40),
                }
            )

        for widget in self.widgets:
            widget["header"].place(x=0, y=self.current_position.y)
            self.current_position.y += 25
            scroll = tk.Scrollbar(self)
            widget["textbox"].configure(yscrollcommand=scroll.set)
            widget["textbox"].place(x=0, y=self.current_position.y)
            self.current_position.y += 112

    def saveFiles(self):
        for widget in self.widgets:
            file_name = f"{self.context.settings.filesdir}{widget['header']['text']}.txt"
            file_path = Path(file_name)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_content = widget["textbox"].get(1.0, "end-1c")
            file_path.write_text(file_content)
            print(f"{file_path} saved with following contents:\n{file_content}\n----------------")

    def onStart(self):
        lan_info = tk.Label(
            self,
            text=f"LAN Address: {self.settings.server_ip}:{self.settings.tcp_port}",
        )
        lan_info.configure(font=("Helvetica", 14, "bold"))
        lan_info.pack()

        header = tk.Label(self, text="Create files..")
        header.pack()

        self.current_position = Vector2(0, 50)

        self.allowCon = tk.IntVar(value=self.settings.allowConnection)
        c1 = tk.Checkbutton(
            self,
            text="Verbindingen Toestaan",
            variable=self.allowCon,
            onvalue=1,
            offvalue=0,
            command=lambda: self.allowConnectionCheckboxCallback(),
        )
        c1.place(x=15, y=self.current_position.y)

        self.current_position.y += 25


        numfiles = range(0, self.context.settings.num_files)
        self.drawWidgets(numfiles)

        save_button = tk.Button(self, text="Opslaan", command=self.saveFiles)
        save_button.place(
            x=self.settings.appplication_width - 64,
            y=self.settings.appplication_height - 40,
        )
        # back_button.update()
        # print(back_button.winfo_width())
