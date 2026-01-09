from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageTk 
import sys
import os

# --- MAC BUTTON SUPPORT ---
if sys.platform == "darwin":  
    from Cocoa import NSEvent, NSApplication, NSApp
    from tkmacosx import Button

# --- PYINSTALLER IMAGE PATH ---
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

image_path = os.path.join(base_path, "eraser.png")

# ==========================
# VARIABLES
# ==========================
window = Tk()
canvasHeight = 500
canvasWidth = 800
rows = 25
columns = 20
size = 20
original_size = size
offsetX = 0
offsetY = 0
color = "red"
array_boxes = []
original_array_boxes = []
Scale_Factor = 1.0
ColorSaves = [None] * 5
ColorSaveButton = []
Draging = False
last_mouse_x = 0
last_mouse_y = 0

# ==========================
# RESET
# ==========================
def setDefaultVal():
    global canvasHeight, canvasWidth, rows, columns, size, original_size
    global offsetX, offsetY, color, array_boxes, original_array_boxes
    global Scale_Factor, Draging, last_mouse_x, last_mouse_y

    canvasHeight = 500
    canvasWidth = 800
    rows = 25
    columns = 20
    size = 20
    original_size = size
    offsetX = 0
    offsetY = 0
    color = "red"
    array_boxes = []
    original_array_boxes = []
    Scale_Factor = 1.0
    Draging = False
    last_mouse_x = 0
    last_mouse_y = 0

# ==========================
# CANVAS METHODS
# ==========================
def clear():
    canvas.delete("cell")

def draw_lines():
    h = offsetY
    for _ in range(rows):
        for w in array_boxes:
            left = w - size + offsetX
            canvas.create_line(left, h, left + size, h, width=1, fill="black", tag="lines")
            canvas.create_line(left, h, left, h + size, width=1, fill="black", tag="lines")
        h += size

# ==========================
# MOUSE / DRAWING
# ==========================
def Click(event):
    if Draging:
        drag(event)
        return

    x = event.x_root - canvas.winfo_rootx()
    y = event.y_root - canvas.winfo_rooty()

    if x < 0 or y < 0 or x > canvas.winfo_width() or y > canvas.winfo_height():
        return

    h = offsetY
    for _ in range(rows):
        for w in array_boxes:
            left = w - size + offsetX
            if left <= x <= w and h <= y <= h + size:
                if color == "":
                    items = canvas.find_overlapping(x, y, x, y)
                    for item in items:
                        if "cell" in canvas.gettags(item):
                            canvas.delete(item)
                else:
                    canvas.create_rectangle(
                        left, h, w + offsetX, h + size,
                        fill=color, outline="", tags="cell"
                    )
                    canvas.tag_raise("lines")
        h += size

def onPress(event):
    start_drag(event)
    Click(event)

def start_drag(event):
    global last_mouse_x, last_mouse_y
    last_mouse_x = event.x_root
    last_mouse_y = event.y_root

def drag(event):
    global last_mouse_x, last_mouse_y, array_boxes, offsetY

    dx = event.x_root - last_mouse_x
    dy = event.y_root - last_mouse_y

    for i in range(len(array_boxes)):
        array_boxes[i] += dx

    offsetY += dy
    canvas.move("all", dx, dy)

    last_mouse_x = event.x_root
    last_mouse_y = event.y_root

# ==========================
# COLOR
# ==========================
def changecolor(color_name):
    global color
    color = color_name

def pickcolor():
    c = colorchooser.askcolor(title="Choose a color")
    if c[1]:
        changecolor(c[1])

def SetDragging(value):
    global Draging
    Draging = value

# ==========================
# START / RESET
# ==========================
def StartOver(btn):
    canvas.delete("all")
    setDefaultVal()
    setrows.pack(pady=10)
    setcolumns.pack(pady=10)
    Start.pack()
    btn.pack_forget()

def Starts():
    global rows, columns, original_size

    quit_btn = Button(frame, text="Quit")
    quit_btn.config(command=lambda: StartOver(quit_btn))
    quit_btn.place(x=35, y=750)

    rows = int(setrows.get())
    columns = int(setcolumns.get())
    original_size = size

    setrows.pack_forget()
    setcolumns.pack_forget()
    Start.pack_forget()

    window.bind("<Button-1>", onPress)
    window.bind("<B1-Motion>", Click)

    if sys.platform == "darwin":
        window.bind("<Meta_L>", lambda e: SetDragging(True))
        window.bind("<KeyRelease-Meta_L>", lambda e: SetDragging(False))
    else:
        window.bind("<Control_L>", lambda e: SetDragging(True))
        window.bind("<KeyRelease-Control_L>", lambda e: SetDragging(False))

    x = 0
    for _ in range(columns):
        x += size
        array_boxes.append(x)

    draw_lines()

# ==========================
# UI FRAME
# ==========================
frame = Frame(window, bg="#454545", width=150)
frame.pack(side="left", fill="y")

# --- ERASER IMAGE ---
original_image = Image.open(image_path)
resized_image = original_image.resize((100, 100))
img = ImageTk.PhotoImage(resized_image)

# --- COLOR SAVE BUTTONS ---
for i in range(5):
    btn = Button(frame, text="+", bg="#6A6A6A", fg="white")
    btn.place(x=50, y=(60 * i) + 200, width=50, height=50)
    ColorSaveButton.append(btn)

# --- MAIN BUTTONS ---
Color_picker = Button(frame, text="Pick color", command=pickcolor)
Color_picker.place(relx=0.5, y=20, anchor="center")

erase_button = Button(
    frame,
    image=img,
    command=lambda: changecolor(""),
    borderwidth=0
)
erase_button.image = img
erase_button.place(relx=0.5, y=87, anchor="center")

clear_button = Button(frame, text="Clear", command=clear)
clear_button.place(relx=0.5, y=155, anchor="center")

# ==========================
# BRUSH SIZE UI (NO LOGIC)
# ==========================
Label(
    frame,
    text="Brush Size",
    bg="#454545",
    fg="white",
    font=("Helvetica", 11, "bold")
).place(relx=0.5, y=350, anchor="center")

btn_style = {
    "bg": "#6A6A6A",
    "fg": "white",
    "activebackground": "#8A8A8A",
    "bd": 0,
    "font": ("Helvetica", 10, "bold"),
    "cursor": "hand2"
}

Button(frame, text="Small", **btn_style).place(relx=0.5, y=385, anchor="center", width=90, height=32)
Button(frame, text="Medium", **btn_style).place(relx=0.5, y=425, anchor="center", width=90, height=32)
Button(frame, text="Large", **btn_style).place(relx=0.5, y=465, anchor="center", width=90, height=32)

# ==========================
# CANVAS
# ==========================
window.geometry("1000x800")
window.config(bg="#2E2E2E")

canvas = Canvas(window, bg="#9F9F9F", bd=4, relief="solid")
canvas.pack(expand=True, padx=5, pady=5, fill="both")

# ==========================
# INPUTS
# ==========================
def only_numbers(P):
    return P.isdigit() or P == ""

vcmd = window.register(only_numbers)

setrows = Spinbox(window, from_=1, to=100, validate="key", validatecommand=(vcmd, "%P"))
setrows.pack(pady=10)

setcolumns = Spinbox(window, from_=1, to=100, validate="key", validatecommand=(vcmd, "%P"))
setcolumns.pack(pady=10)

Start = Button(window, text="Start", command=Starts)
Start.pack()

window.mainloop()
