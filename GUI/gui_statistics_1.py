
from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("1280x832")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 832,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    105.0,
    832.0,
    fill="#000000",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=197.0,
    y=212.0,
    width=43.0,
    height=43.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=0.0,
    y=0.0,
    width=105.0,
    height=97.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=154.0,
    y=477.0,
    width=43.0,
    height=43.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=197.0,
    y=336.0,
    width=43.0,
    height=43.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=154.0,
    y=671.0,
    width=43.0,
    height=43.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=197.0,
    y=274.0,
    width=43.0,
    height=43.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=154.0,
    y=539.0,
    width=43.0,
    height=43.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=154.0,
    y=605.0,
    width=43.0,
    height=43.0
)

canvas.create_text(
    493.0,
    10.00006103515625,
    anchor="nw",
    text="Εφαρμογή Στατιστικών",
    fill="#000000",
    font=("Inter", 40 * -1)
)

canvas.create_text(
    154.0,
    158.0,
    anchor="nw",
    text="Πλήθος Δανεισμών",
    fill="#000000",
    font=("Inter", 30 * -1)
)

canvas.create_text(
    252.0,
    220.0,
    anchor="nw",
    text="Ανα συγγραφέα",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    209.0,
    483.0,
    anchor="nw",
    text="Πλήθος βιβλίων ανα μέλος σε συγκεκριμένη χρονική περίοδο",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    252.0,
    282.0,
    anchor="nw",
    text="Ανα Ηλικία",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    209.0,
    547.0,
    anchor="nw",
    text="Κατανομή προτιμήσεων δανεισμού ανά μέλος",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    209.0,
    613.0,
    anchor="nw",
    text="Κατανομή προτιμήσεων δανεισμού όλων των μελών",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    252.0,
    344.0,
    anchor="nw",
    text="Ανα Φύλλο",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    209.0,
    679.0,
    anchor="nw",
    text="Ιστορικό Δανεισμού ανά μέλος",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    114.0,
    19.0,
    anchor="nw",
    text="Επιστροφή στο \nΜενού",
    fill="#000000",
    font=("Inter", 24 * -1)
)
window.resizable(False, False)
window.mainloop()
