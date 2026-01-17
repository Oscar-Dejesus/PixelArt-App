from tkinter import *
from tkinter import colorchooser

# ----------------------
# Pixel Art App - Visual Mockup
# ----------------------

CELL_SIZE = 20
ROWS = 20
COLS = 20

window = Tk()
window.title("Pixel Art App")
window.geometry("900x600")
window.configure(bg="#2E2E2E")

# ----------------------
# Sidebar (Tools Panel)
# ----------------------
sidebar = Frame(window, width=200, bg="#1F1F1F", relief='raised', bd=2)
sidebar.pack(side=LEFT, fill=Y)

Label(sidebar, text="Pixel Tools", bg="#1F1F1F", fg="white",
      font=("Segoe UI", 14, "bold"), pady=20).pack()

# Color preview box
color_preview = Frame(sidebar, bg="#ff3b3b", width=100, height=40, relief='sunken', bd=2)
color_preview.pack(pady=10)

# Buttons mockup
btn_frame = Frame(sidebar, bg="#1F1F1F")
btn_frame.pack(pady=20)

Button(btn_frame, text="Pick Color", width=15, bg="#3A3A3A", fg="white", relief='flat').pack(pady=5)
Button(btn_frame, text="Clear Canvas", width=15, bg="#AA3333", fg="white", relief='flat').pack(pady=5)
Button(btn_frame, text="Small Brush", width=15, bg="#3A3A3A", fg="white", relief='flat').pack(pady=5)
Button(btn_frame, text="Medium Brush", width=15, bg="#3A3A3A", fg="white", relief='flat').pack(pady=5)
Button(btn_frame, text="Large Brush", width=15, bg="#3A3A3A", fg="white", relief='flat').pack(pady=5)
Button(btn_frame, text="Fill Tool", width=15, bg="#3A3A3A", fg="white", relief='flat').pack(pady=5)

# ----------------------
# Canvas area (visual only)
# ----------------------
canvas_frame = Frame(window, bg="#B0B0B0", relief='sunken', bd=2)
canvas_frame.pack(side=RIGHT, expand=True, fill=BOTH, padx=10, pady=10)

canvas = Canvas(canvas_frame, bg="#E0E0E0", highlightthickness=0)
canvas.pack(expand=True, fill=BOTH)

# Draw mockup grid for visual effect
for r in range(ROWS):
    for c in range(COLS):
        x1 = c * CELL_SIZE
        y1 = r * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="#888")

window.mainloop()
