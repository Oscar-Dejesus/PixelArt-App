from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageTk
import sys

# Use tkmacosx for rounded buttons on macOS
if sys.platform == "darwin":
    from tkmacosx import Button as RoundedButton
else:
    RoundedButton = Button

# ------------------- Window Setup -------------------
window = Tk()
window.title("Pixel Art App")
window.geometry("1000x800")
window.config(bg="#2b2b2b")  # Dark theme background

# ------------------- Global Variables -------------------
canvasHeight = 500
canvasWidth = 500
rows, columns, size = 25, 20, 20
offsetX, offsetY = 3, 3
color = "red"
array_boxes = []
ColorSaves = [None]*5
ColorSaveButton = []

# ------------------- Functions -------------------
def clear():
    canvas.delete("cell")

def draw_lines():
    h = offsetY
    for _ in range(rows):
        for i in range(len(array_boxes)):
            w = array_boxes[i]
            left = w - size + offsetX
            canvas.create_line(left, h, left + size, h, width=1, fill="#555555", tag='lines')
            canvas.create_line(left, h, left, h + size + offsetY, width=1, fill="#555555", tag='lines')
        h += size

def Click(event):
    global color
    x = event.x_root - canvas.winfo_rootx()
    y = event.y_root - canvas.winfo_rooty()
    h = offsetY
    for _ in range(rows):
        for i in range(len(array_boxes)):
            w = array_boxes[i]
            left = w - size + offsetX
            if x > left-1 and x < w+1 and y > h-1 and y < h+size:
                if color == "":
                    items = canvas.find_overlapping(x, y, x, y)
                    for item in items:
                        if "cell" in canvas.gettags(item):
                            canvas.delete(item)
                else:
                    canvas.create_rectangle(left, h, w+offsetX, h+size, fill=color, outline="", tags="cell")
                    canvas.tag_raise('lines')
        h += size

def changecolor(color_name):
    global color
    color = color_name
    if None not in ColorSaves and color_name != "":
        ColorSaves[-1] = color_name
        ColorSaveButton[0].config(bg=color_name, text="")
    for i, c in reversed(list(enumerate(ColorSaves))):
        if c is None and color_name != "":
            ColorSaves[i] = color_name
            ColorSaveButton[i].config(bg=color_name, text="")
            break

def pickcolor():
    selected_color = colorchooser.askcolor(title="Choose a color")
    if selected_color[1]:
        changecolor(selected_color[1])

def Starts():
    global size, rows, columns, array_boxes

    rows = int(setrows.get())
    columns = int(setcolumns.get())
    size = int(setsize.get())

    # Remove start controls
    setrows.destroy()
    setcolumns.destroy()
    setsize.destroy()
    Start.destroy()

    # Configure canvas
    canvas.config(width=columns*size, height=rows*size)
    canvas.pack(expand=True, padx=20, pady=20)
    window.bind("<Button-1>", Click)
    window.bind("<B1-Motion>", Click)

    # Grid setup
    array_boxes = [(i+1)*size for i in range(columns)]

    # Load eraser image
    original_image = Image.open("eraser.png")
    resized_image = original_image.resize((50, 50))
    img = ImageTk.PhotoImage(resized_image)

    # Configure tool buttons
    clear_button.config(command=clear)
    erase_button.config(image=img, command=lambda: changecolor(""), borderwidth=0)
    erase_button.image = img
    Color_picker.config(command=pickcolor)

    # Pack tool buttons
    clear_button.pack(pady=10, fill=X)
    erase_button.pack(pady=10, fill=X)
    Color_picker.pack(pady=10, fill=X)

    # Saved color buttons
    for i, btn in enumerate(ColorSaveButton):
        btn.config(width=4, height=2, bg="white", command=lambda b=i: changecolor(ColorSaves[b]))
        btn.pack(pady=5)

    draw_lines()

# ------------------- Frames -------------------
control_frame = Frame(window, bg="#2b2b2b")
control_frame.pack(side=LEFT, fill=Y, padx=20, pady=20)

canvas_frame = Frame(window, bg="#2b2b2b")
canvas_frame.pack(side=RIGHT, expand=True, fill=BOTH, padx=20, pady=20)

# ------------------- Widgets -------------------
canvas = Canvas(canvas_frame, width=canvasWidth, height=canvasHeight, bg="#ffffff", bd=4, relief="solid")
canvas.pack(expand=True)

# Start controls
setrows = Spinbox(control_frame, from_=1, to=100, width=5)
setrows.pack(pady=5)
setcolumns = Spinbox(control_frame, from_=1, to=100, width=5)
setcolumns.pack(pady=5)
setsize = Spinbox(control_frame, from_=1, to=100, width=5)
setsize.pack(pady=5)
Start = RoundedButton(control_frame, text="Start", bg="#4CAF50", fg="white", relief="flat", padx=10, pady=5, command=Starts)
Start.pack(pady=10, fill=X)

# Tool buttons
clear_button = RoundedButton(control_frame, text="Clear", bg="#f44336", fg="white", relief="flat", padx=10, pady=5)
erase_button = RoundedButton(control_frame)
Color_picker = RoundedButton(control_frame, text="Pick Color", bg="#2196F3", fg="white", relief="flat", padx=10, pady=5)

# Saved color buttons
for i in range(5):
    btn = RoundedButton(control_frame, text="+")
    ColorSaveButton.append(btn)

# ------------------- Hover Effects -------------------
def add_hover_effect(button, normal_bg, hover_bg):
    button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
    button.bind("<Leave>", lambda e: button.config(bg=normal_bg))

add_hover_effect(Start, "#4CAF50", "#45a049")
add_hover_effect(clear_button, "#f44336", "#d32f2f")
add_hover_effect(Color_picker, "#2196F3", "#1976d2")

window.mainloop()
