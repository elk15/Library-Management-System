
# ----------- Author: EvanSar --------- #

#Module, Libraries and Packages Imports
from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

#File Imports
from stat_graphs_gui import *
from MainGUI import LibraryGUI

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"GUI\assets\frame0")

class StatisticsMenuGUI:

    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    def __init__(self,window):
        self.window = window
        self.window.geometry("1280x832")
        self.window.configure(bg = "#FFFFFF")

        self.canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 832,
        width = 1280,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            105.0,
            832.0,
            fill="#000000",
            outline="")

        self.canvas.create_rectangle(
            200.0,
            209.0,
            243.0,
            252.0,
            fill="#A7A8A7",
            outline="")

        self.button_image_1 = PhotoImage( # "Back to Menu" button
            file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.launch_main_menu,
            relief="flat"
        )
        self.button_1.place(
            x=0.0,
            y=0.0,
            width=105.0,
            height=97.0
        )

        self.canvas.create_rectangle(
            114.0,
            398.0,
            157.0,
            441.0,
            fill="#A7A8A7",
            outline="")

        self.canvas.create_rectangle(
            200.0,
            333.0,
            243.0,
            376.0,
            fill="#A7A8A7",
            outline="")

        self.canvas.create_rectangle(
            114.0,
            592.0,
            157.0,
            635.0,
            fill="#A7A8A7",
            outline="")

        self.canvas.create_rectangle(
            200.0,
            271.0,
            243.0,
            314.0,
            fill="#A7A8A7",
            outline="")

        self.canvas.create_rectangle(
            114.0,
            460.0,
            157.0,
            503.0,
            fill="#A7A8A7",
            outline="")

        self.canvas.create_rectangle(
            114.0,
            526.0,
            157.0,
            569.0,
            fill="#A7A8A7",
            outline="")

        self.canvas.create_text(
            491.0,
            22.0,
            anchor="nw",
            text="Statistics",
            fill="#000000",
            font=("Inter", 40 * -1)
        )

        self.canvas.create_text(
            157.0,
            155.0,
            anchor="nw",
            text="Borrowed Books",
            fill="#000000",
            font=("Inter", 25 * -1)
        )

        self.canvas.create_text(
            255.0,
            217.0,
            anchor="nw",
            text="By a Single Author",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            169.0,
            404.0,
            anchor="nw",
            text="Number of borrowed books by a single member",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            255.0,
            279.0,
            anchor="nw",
            text="Distribution Graph for all Authors",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            169.0,
            468.0,
            anchor="nw",
            text="Book Genre Preference within a Timeframe",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            169.0,
            534.0,
            anchor="nw",
            text="Single Member Book Genre Preference",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            255.0,
            341.0,
            anchor="nw",
            text="Distribution Graph for all Ages",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            169.0,
            600.0,
            anchor="nw",
            text="Member Borrowing History",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            114.0,
            34.0,
            anchor="nw",
            text="Back to Menu",
            fill="#000000",
            font=("Inter", 24 * -1)
        )

        self.button_image_2 = PhotoImage( # Launch "Statistics" Application Button
            file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.launch_statistics_application,
            relief="flat"
        )
        self.button_2.place(
            x=571.0,
            y=715,
            width=238.0,
            height=42.0
        )

        self.canvas.create_text(
            580.0,
            685.0,
            anchor="nw",
            text="Launch Application",
            fill="#000000",
            font=("Inter", 25 * -1)
        )

        self.canvas.create_text(
            114.0,
            115.0,
            anchor="nw",
            text="This app generates statistics according to user input for the following",
            fill="#000000",
            font=("Inter", 25 * -1)
        )
        

    def launch_statistics_application(self):
        db_filename = './library.db'
        root = tk.Tk()
        LibraryStatisticsGUI(db_filename, root)
        root.mainloop()


    def launch_main_menu(self):
        MainMenu = tk.Tk()
        LibraryGUI(MainMenu)
        MainMenu.mainloop()



if __name__ == "__main__":
    window = tk.Tk()
    StatisticsMenuGUI(window)
    window.mainloop()



