from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageTk, ImageDraw
import sys
import os
import math
if sys.platform == "darwin":  
    from Cocoa import NSEvent, NSApplication, NSApp
    from tkmacosx import Button
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

image_path = os.path.join(base_path, "eraser.png")

# VARIABLES
window = Tk()
canvasHeight= 500
canvasWidth = 800
rows=25
columns =20
size = 20
original_size=size
offsetX=0
offsetY=0
color = "red"
array_boxes = []
original_array_boxes = []
Scale_Factor=1.0
Draging=False
last_mouse_x = 0
last_mouse_y = 0
Brush_Size="Small"
def setDefaultVal():
    global canvasHeight, canvasWidth, rows, columns, size, original_size
    global offsetX, offsetY, color, array_boxes, original_array_boxes
    global Scale_Factor, Draging
    global last_mouse_x, last_mouse_y
    canvasHeight= 500
    canvasWidth = 800
    rows=25
    columns =20
    size = 20
    original_size=size
    offsetX=0
    offsetY=0
    color = "red"
    array_boxes = []
    original_array_boxes = []
    Scale_Factor=1.0
    Draging=False
    last_mouse_x = 0
    last_mouse_y = 0
# METHODS 
def export():
    global canvas, array_boxes, offsetY, size, rows, Scale_Factor
    while Scale_Factor<1:
        zoom_in()
    canvas.update_idletasks()

    if not array_boxes:
        print("No drawing to export")
        return


    x_min = array_boxes[0] - size
    x_max = array_boxes[-1]


    y_min = offsetY
    y_max = offsetY + rows * size

    width = int(x_max - x_min)
    height = int(y_max - y_min)


    img = Image.new("RGB", (width, height), (125, 125, 125)) 
    draw = ImageDraw.Draw(img)

    for item in canvas.find_withtag("cell"):
        coords = canvas.coords(item)  
        fill = canvas.itemcget(item, "fill")

        x1 = coords[0] - x_min
        y1 = coords[1] - y_min
        x2 = coords[2] - x_min
        y2 = coords[3] - y_min
        draw.rectangle([x1, y1, x2, y2], fill=fill)


    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    path = os.path.join(desktop, "art.png")
    img.save(path)
    print(f"Drawing exported to Desktop as art.png")


def clear():
    canvas.delete("cell")
def draw_lines():
    h= 0+offsetY
    for _ in range(rows):
        
        for i in range(len(array_boxes)): 
            w=  array_boxes[i] 

            left = w - size +offsetX
            
            
            canvas.create_line(left,h, left+size,h,width=1,fill="black",tag='lines')
            canvas.create_line(left,h,left,h+size +offsetY,width=1,fill="black",tag='lines')

        h+=size 
    canvas.create_line(0,h, left+size,h,width=1,fill="black",tag='lines')
    canvas.create_line(left+size,0, left+size,h,width=1,fill="black",tag='lines')

# MOUSE/CONTROLS METHODS
def Brush_Draw(x,y,left,h,w):
    global Brush_Size,offsetX, array_boxes,offsetY,rows,size,color
    max_height=rows*size + offsetY

    if Brush_Size=="fill":
        stack=[(left,h)]
        Fill_Only_Color=""
        items= canvas.find_overlapping(x,y,x+size,y+size)
        for item in items:
            if "cell" in canvas.gettags(item):
                Fill_Only_Color = canvas.itemcget(item, "fill")
                break
        while stack:

            x1, y1= stack.pop()
            canvas.create_rectangle(x1,y1 ,x1+size,y1+size ,fill=color,outline="",tags = "cell")
            neighbors = [
                    (x1- size, y1),       
                    (x1 +size, y1),       
                    (x1, y1 - size),       
                    (x1, y1 + size)        
                ]
            
            for x,y in neighbors:

                if x >= math.floor(array_boxes[0])-size and x+math.floor(size) <= array_boxes[-1] and y >= math.floor(offsetY) and y+math.floor(size) <= max_height:
                    items= canvas.find_overlapping(x+size/2,y+size/2,x+size/2,y+size/2)
                    
                    if not any("cell" in canvas.gettags(item) for item in items):
                        stack.append((x,y))
                

                    
    
    if Brush_Size=="Small":
        canvas.create_rectangle(left,h ,w+offsetX,h+size,fill=color,outline="",tags = "cell")
    elif Brush_Size=="Medium":
        canvas.create_rectangle(left,h ,w+offsetX,h+size,fill=color,outline="",tags = "cell")
        if left-(w-left)>=array_boxes[0]-size:
            canvas.create_rectangle(left-(w-left),h ,left+offsetX,h+size,fill=color,outline="",tags = "cell")
        if (h-size)>=offsetY:
            canvas.create_rectangle(left,h-(size),w+offsetX,h,fill=color,outline="",tags = "cell")
                    
        if (h-size)>=offsetY and left-(w-left)>=array_boxes[0]-size:
            canvas.create_rectangle(left-(w-left),h-(size),left+offsetX,h,fill=color,outline="",tags = "cell")
    elif Brush_Size=="Large":
        
        canvas.create_rectangle(left,h ,w+offsetX,h+size,fill=color,outline="",tags = "cell")
        if left-(w-left)>=array_boxes[0]-size:
            canvas.create_rectangle(left-(w-left),h ,left+offsetX,h+size,fill=color,outline="",tags = "cell")
        if (h-size)>=offsetY:
            canvas.create_rectangle(left,h-(size),w+offsetX,h,fill=color,outline="",tags = "cell")
                    
        if (h-size)>=offsetY and left-(w-left)>=array_boxes[0]-size:
            canvas.create_rectangle(left-(w-left),h-(size),left+offsetX,h,fill=color,outline="",tags = "cell")
        
        if (h+size*2)<= max_height and left-(w-left)>=array_boxes[0]-size:
            canvas.create_rectangle(left-(w-left),h+(size*2),left+offsetX,h+size,fill=color,outline="",tags = "cell")
        
        if (h+size*2)<= max_height and left+(w-left)>=array_boxes[0]-size:
            canvas.create_rectangle(left+(w-left),h+(size*2),left+offsetX,h+size,fill=color,outline="",tags = "cell")
            
        if (h+size*2)<= max_height and left+offsetX+size<=array_boxes[len(array_boxes)-1]-size:
            canvas.create_rectangle(left+(w-left)*2,h+(size*2),left+offsetX+size,h+size,fill=color,outline="",tags = "cell")

        if h<= max_height and left+offsetX+size<=array_boxes[len(array_boxes)-1]-size:
            canvas.create_rectangle(left+(w-left)*2,h,left+offsetX+size,h+size,fill=color,outline="",tags = "cell")
        if h-size>=offsetY  and left+offsetX+size<=array_boxes[len(array_boxes)-1]-size:
            canvas.create_rectangle(left+(w-left)*2,h-size,left+offsetX+size,h,fill=color,outline="",tags = "cell")
        
        
def Change_Brush_Size(size):
    global Brush_Size
    Brush_Size=size
def Click(event):

    if Draging:
        drag(event) 
        return
    global color,Brush_Size
    x = event.x_root - canvas.winfo_rootx()
    y = event.y_root - canvas.winfo_rooty() 
    if x<0 or y<0 or x> canvas.winfo_width() or y> canvas.winfo_height():
        return
    h= 0+offsetY    
    for _ in range(rows):
        
        for i in range(len(array_boxes)): 
            w=  array_boxes[i] 
            left = w - size +offsetX
            
            if x>left-1 and x<w+1 and y>h-1 and y<h+size:
                if color =="":
                    if Brush_Size=="Small":
                        items= canvas.find_overlapping(x,y,x,y)
                        for item in items:
                            if "cell" in canvas.gettags(item):
                                canvas.delete(item)
                        
                    elif Brush_Size=="Medium":
                        items= canvas.find_overlapping(x,y,x,y)
                        if items and "cell" in canvas.gettags(items[0]):
                            first_item = items[0]
                            x1,y1,x2,y2 = canvas.coords(first_item)
                            items= canvas.find_overlapping(x1-size,y1-size,x2,y2)
                        for item in items:
                            if "cell" in canvas.gettags(item):
                                canvas.delete(item)
                    else:
                        items= canvas.find_overlapping(x,y,x,y)
                        if items and "cell" in canvas.gettags(items[0]):
                            first_item = items[0]
                            x1,y1,x2,y2 = canvas.coords(first_item)
                            items= canvas.find_overlapping(x1-size,y1-size,x2+size,y2+size)
                        for item in items:
                            if "cell" in canvas.gettags(item):
                                canvas.delete(item)
                else:
                    
                    Brush_Draw(x,y,left,h,w)
                    
                   
                    canvas.tag_raise('lines')
                    
    
        h+=size
    
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

    for i,x in enumerate(array_boxes):
        array_boxes[i]+=dx
    offsetY+=dy
    canvas.move("all", dx, dy)

    last_mouse_x = event.x_root
    last_mouse_y = event.y_root

#BUTTON METHODS 
def changecolor(color_name):
    global color
    color = color_name

def zoom_out():
    global size, array_boxes,Scale_Factor,offsetY
    Scale = 0.97
    Scale_Factor *= Scale
    cy = canvas.winfo_height() / 2  
    cx = canvas.winfo_width() / 2  
    for i, x in enumerate(array_boxes):
        array_boxes[i] = cx + (array_boxes[i] - cx) * Scale
    
    size = original_size * Scale_Factor

    offsetY = offsetY * Scale + cy * (1- Scale)


    canvas.scale("all", cx,cy, Scale, Scale)
def zoom_in():
    global size, array_boxes,Scale_Factor,offsetY
    Scale = 1.03
    Scale_Factor *= Scale
    cx = canvas.winfo_width() / 2  
    cy = canvas.winfo_height() / 2  
    for i, x in enumerate(array_boxes):
        array_boxes[i] = cx + (array_boxes[i] - cx) * Scale

    
    size = original_size * Scale_Factor
    offsetY = offsetY * Scale + cy * (1-Scale)
    canvas.scale("all", cx, cy, Scale, Scale)   



def pickcolor():
    color = colorchooser.askcolor(title="Choose a color")
    if color[1]:
        changecolor(color[1])

def SetDragging(value):
    global Draging
    Draging=value
def StartOver(btn):
    canvas.delete("all")
    setDefaultVal()
    setrows.pack(pady=10)
    setcolumns.pack(pady=10)
    Start.pack()
    btn.place_forget()

def Starts():
    global frame, size, rows, columns, original_array_boxes,original_size,Draging
    quit = Button(frame, text="Quits")
    quit.config(command=lambda: StartOver(quit))
    quit.place(x=40,y=730)
    rows = int(setrows.get())
    columns = int(setcolumns.get())
    original_size=size
    setrows.pack_forget()
    setcolumns.pack_forget()
    Start.pack_forget()

    
    window.bind("<Button-1>", onPress) 
    window.bind("<B1-Motion>",Click)
    if sys.platform == "darwin":
        window.bind("<Meta_L>", lambda e: SetDragging(True))        # Command
        window.bind("<KeyRelease-Meta_L>", lambda e: SetDragging(False))
    else:
        window.bind("<Control_L>", lambda e: SetDragging(True))     # Ctrl
        window.bind("<KeyRelease-Control_L>", lambda e: SetDragging(False))


    window.bind_all("<MouseWheel>", lambda e: zoom_in() if e.delta > 0 else zoom_out())
    window.bind("<KeyPress-plus>", lambda event:zoom_in())
    window.bind("<KeyPress-underscore>", lambda event: zoom_out())
  

    window.update()

    x=0
    for _ in range(columns):
        x+=size
        array_boxes.append(x)
        original_array_boxes = array_boxes.copy()

    draw_lines()



# CREATES INTIAL OBJECTS Buttons,Text ect
frame = Frame(window, bg="#03045E",width=150)
frame.pack(side="left",fill="y")
original_image = Image.open(image_path)
resized_image = original_image.resize((100, 100))
img = ImageTk.PhotoImage(resized_image)

# Define a global color variable for all buttons
BUTTON_COLOR = "#90E0EF"

for x in range(5):

    btn = Button(frame, text="", pady=0, padx=0, bg=BUTTON_COLOR)

    btn.config(command=lambda b=btn: (changecolor(b.cget("bg"))))
    save = Button(frame, text="save", pady=0, padx=0, bg=BUTTON_COLOR, command=lambda b=btn: b.config(bg=color, activebackground=color, text=""))
    btn.place(x=50, y=(60*x)+200, width=50, height=50)
    save.place(x=5, y=(60*x)+215, width=40, height=20)

clear_button = Button(frame, text="clear", bg=BUTTON_COLOR, command=clear)
erase_button = Button(frame, command=lambda: changecolor(""), image=img, bg=BUTTON_COLOR, borderwidth=0, highlightthickness=0, padx=0, pady=0, width=100, height=100)
Color_picker = Button(frame, text="Pick color", bg=BUTTON_COLOR, command=pickcolor)
Brush_Small = Button(frame, text="Small", bg=BUTTON_COLOR, command=lambda: Change_Brush_Size("Small"))
Brush_Medium = Button(frame, text="Medium", bg=BUTTON_COLOR, command=lambda: Change_Brush_Size("Medium"))
Brush_Large = Button(frame, text="Large", bg=BUTTON_COLOR, command=lambda: Change_Brush_Size("Large"))
Brush_fill = Button(frame, text="fill", bg=BUTTON_COLOR, command=lambda: Change_Brush_Size("fill"))
Export_button=Button(frame, text="Export", bg=BUTTON_COLOR, command=lambda: export())
erase_button.image = img

Brush_Small.place(relx=0.5, y=600,anchor="center")
Brush_Medium.place(relx=0.5, y=650,anchor="center")
Brush_Large.place(relx=0.5, y=700,anchor="center")
Brush_fill.place(relx=0.5, y=550,anchor="center")
Color_picker.place(relx=0.5, y=20,anchor="center")
erase_button.place(relx=0.5, y=87,anchor="center")
clear_button.place(relx=0.5, y=155,anchor="center")
Export_button.place(relx=0.5, y=785,anchor="center")



window.geometry("1000x800")
window.config(bg="#0077B6")
canvas = Canvas(window,bg="#7D7D7D",bd=0,
    highlightthickness=4,
    highlightbackground="#CAF0F8")
canvas.pack(expand = True, padx = 5,pady =5,fill="both")

def only_numbers(P):
    if P == "": 
        return True
    if not P.isdigit(): 
        return False
    if int(P) > 100:  
        return False
    return True

vcmd = window.register(only_numbers)

setrows = Spinbox(window, from_=0, to=100, validate="key", validatecommand=(vcmd, "%P"), background="#00B4D8")
setrows.pack(pady=10)
setcolumns = Spinbox(window, from_=0, to=100, validate="key", validatecommand=(vcmd, "%P"),background="#00B4D8")
setcolumns.pack(pady=10)

Start = Button(window, text="Start",command=lambda:Starts())
Start.pack()
window.mainloop()
