from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageTk 
import sys
import os

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
ColorSaves = [None]*5
ColorSaveButton = []
Draging=False
last_mouse_x = 0
last_mouse_y = 0
Brush_Size="Small"
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
def Brush_Draw(left,h,w):
    global Brush_Size,offsetX, array_boxes,offsetY,rows,size
    max_height=rows*size + offsetY
    if Brush_Size=="Small":
        canvas.create_rectangle(left,h ,w+offsetX,h+size,fill=color,outline="",tags = "cell")
    elif Brush_Size=="Meduim":
        canvas.create_rectangle(left,h ,w+offsetX,h+size,fill=color,outline="",tags = "cell")
        if left-(w-left)>=array_boxes[0]-size:
            canvas.create_rectangle(left-(w-left),h ,left+offsetX,h+size,fill=color,outline="",tags = "cell")
        if (h-size)>=offsetY:
            canvas.create_rectangle(left,h-(size),w+offsetX,h,fill=color,outline="",tags = "cell")
                    
        if (h-size)>=offsetY and left-(w-left)>=array_boxes[0]-size:
            canvas.create_rectangle(left-(w-left),h-(size),left+offsetX,h,fill=color,outline="",tags = "cell")
    else:
        
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
                    
                    Brush_Draw(left,h,w)
                    
                   
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
def StartOver(btn):
    canvas.delete("all")
    setDefaultVal()
    setrows.pack(pady=10)
    setcolumns.pack(pady=10)
    Start.pack()
    btn.pack_forget()

def Starts():
    global frame, size, rows, columns, original_array_boxes,original_size,Draging
    quit = Button(frame, text="Quits")
    quit.config(command=lambda: StartOver(quit))
    quit.place(x=35,y=750)
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
frame = Frame(window, bg="#454545",width=150)
frame.pack(side="left",fill="y")
original_image = Image.open(image_path)
resized_image = original_image.resize((100, 100))
img = ImageTk.PhotoImage(resized_image)
for x in range(5):
    btn = Button(frame, text="+",pady=0,padx=0)
    btn.config(command=lambda b=btn: changecolor(b.cget("bg")))
    btn.place(x=50, y=(60*x)+200,width=50,height = 50)
    ColorSaveButton.append(btn)
clear_button = Button(frame,text="clear",command =clear)
erase_button = Button(frame,command= lambda:changecolor(""),image=img,borderwidth=0,highlightthickness=0,padx=0, pady=0,width=100,height =100)
Color_picker = Button(frame,text="Pick color",command= pickcolor)
Brush_Small= Button(frame,text="Small",command= lambda: Change_Brush_Size("Small"))
Brush_Meduim= Button(frame,text="Meduim",command= lambda: Change_Brush_Size("Meduim"))
Brush_Large= Button(frame,text="Large",command= lambda: Change_Brush_Size("Large"))
erase_button.image = img

Brush_Small.place(relx=0.5, y=600,anchor="center")
Brush_Meduim.place(relx=0.5, y=650,anchor="center")
Brush_Large.place(relx=0.5, y=700,anchor="center")
Color_picker.place(relx=0.5, y=20,anchor="center")
erase_button.place(relx=0.5, y=87,anchor="center")
clear_button.place(relx=0.5, y=155,anchor="center")




window.geometry("1000x800")
window.config(bg="#2E2E2E")
canvas = Canvas(window,bg="#9F9F9F",bd= 4,relief="solid")
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

setrows = Spinbox(window, from_=0, to=100, validate="key", validatecommand=(vcmd, "%P"))
setrows.pack(pady=10)
setcolumns = Spinbox(window, from_=0, to=100, validate="key", validatecommand=(vcmd, "%P"))
setcolumns.pack(pady=10)

Start = Button(window, text="Start",command=lambda:Starts())
Start.pack()
window.mainloop()
