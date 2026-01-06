from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageTk 
import sys
import os
import objc
from Cocoa import NSEvent, NSApplication, NSApp
if sys.platform == "darwin":  
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
ColorSaves = [None]*5
ColorSaveButton = []
Draging=False
last_mouse_x = 0
last_mouse_y = 0
def setDefaultVal():
    global canvasHeight, canvasWidth, rows, columns, size, original_size
    global offsetX, offsetY, color, array_boxes, original_array_boxes
    global Scale_Factor, ColorSaves, ColorSaveButton, Draging
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
def Click(event): 
    if Draging:
        drag(event)
        return
    global color
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
                    items= canvas.find_overlapping(x,y,x,y)
                    for item in items:
                        if "cell" in canvas.gettags(item):
                            canvas.delete(item)
                            
                else:
                    canvas.create_rectangle(left,h ,w+offsetX,h+size,fill=color,outline="",tags = "cell")
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
    global color, ColorSaves, ColorSaveButton
    color = color_name
    if None not in ColorSaves and color_name is not "":
        ColorSaves[-1]=color_name
        ColorSaveButton[0].config(bg=color_name,text ="")
    for i, c in reversed(list(enumerate(ColorSaves))):
        if c is None and color_name is not "":
            ColorSaves[i]= color_name
            ColorSaveButton[i].config(bg=color_name,text="")
            break

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
def DeleteAll(btn):

    
    canvas.delete("all")
    setDefaultVal()
    setrows.pack(pady=10)
    setcolumns.pack(pady=10)
    Start.pack()
    btn.pack_forget()

def Starts():
    global frame, size, rows, columns, original_array_boxes,original_size,Draging
    quit = Button(frame, text="Quits")
    quit.config(command=lambda: DeleteAll(quit))
    quit.place(x=35,y=750)
    rows = int(setrows.get())
    columns = int(setcolumns.get())
    original_size=size
    setrows.pack_forget()
    setcolumns.pack_forget()
    Start.pack_forget()

    
    window.bind("<Button-1>", onPress) 
    window.bind("<B1-Motion>",Click)
    window.bind("<Meta_L>", lambda event: SetDragging(True))
    window.bind("<KeyRelease-Meta_L>", lambda event: SetDragging(False))

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



# CREATES INTIAL OBJECTS 
frame = Frame(window, bg="lightgray",width=150)
frame.pack(side="left",fill="y")
original_image = Image.open(image_path)
resized_image = original_image.resize((100, 100))
img = ImageTk.PhotoImage(resized_image)
clear_button = Button(frame,text="clear",command =clear)
erase_button = Button(frame,command= lambda:changecolor(""),image=img,borderwidth=0,highlightthickness=0,padx=0, pady=0,width=100,height =100)
erase_button.image = img
Color_picker = Button(frame,text="Pick color",command= pickcolor)
Color_picker.place(relx=0.5, y=20,anchor="center")
erase_button.place(relx=0.5, y=87,anchor="center")
clear_button.place(relx=0.5, y=155,anchor="center")
for x in range(5):
    btn = Button(frame, text="+", width=50,height = 50)
    btn.config(command=lambda b=btn: changecolor(b.cget("bg")))
    btn.place(x=50, y=(60*x)+200)
    ColorSaveButton.append(btn)


window.geometry("1000x800")
window.config(bg="#676767")
canvas = Canvas(window,width=canvasWidth,height = canvasHeight,bg="#9F9F9F",bd= 4,relief="solid")
canvas.pack(expand = True, padx = 5,pady =5)

def only_numbers(P):
    if P == "": 
        return True
    if not P.isdigit(): 
        return False
    if int(P) > 100:  
        return False
    return True

vcmd = window.register(only_numbers)

setrows = Spinbox(window, from_=0, to=100, validate="key", validatecommand=(vcmd, "%P"))
setrows.pack(pady=10)
setcolumns = Spinbox(window, from_=0, to=100, validate="key", validatecommand=(vcmd, "%P"))
setcolumns.pack(pady=10)

Start = Button(window, text="Start",command=lambda:Starts())
Start.pack()
window.mainloop()
