from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageTk 
import sys
if sys.platform == "darwin":  
    from tkmacosx import Button

window = Tk()
canvasHeight= 500
canvasWidth = 400
rows=25
columns =20
size = 20
offsetX=3
offsetY=3
color = "red"
array_boxes = []
ColorSaves = [None]*5
ColorSaveButton = []
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
def Click(event): 
    global color
    x = event.x_root - canvas.winfo_rootx()
    y = event.y_root - canvas.winfo_rooty() 
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
    
    


def pickcolor():
    color = colorchooser.askcolor(title="Choose a color")
    if color[1]:
        changecolor(color[1])
def Starts():
    global size, rows, columns
    rows = int(setrows.get())
    columns = int(setcolumns.get())
    size = int(setsize.get())

    setrows.destroy()
    setcolumns.destroy()
    Start.destroy()
    setsize.destroy()
    canvas.config(width = columns*size,height =rows*size,highlightthickness=0)
    window.bind("<Button-1>", Click) 
    window.bind("<B1-Motion>",Click)
    
    window.update()

    x=0
    for _ in range(columns):
        x+=size
        array_boxes.append(x)
    original_image = Image.open("eraser.png")
    resized_image = original_image.resize((100, 100))
    img = ImageTk.PhotoImage(resized_image)
   
    clear_button = Button(window,text="clear",command =clear)
    erase_button = Button(window,command= lambda:changecolor(""),image=img,borderwidth=0,highlightthickness=0,padx=0, pady=0,width=100,height =100)
    erase_button.image = img
    Color_picker = Button(window,text="Pick color",command= pickcolor)
    Color_picker.place(relx=.99,y=20, anchor='ne')
    erase_button.place(relx=.99, y=50, anchor='ne')
    clear_button.place(relx=.98, y=155, anchor='ne')
    
    for x in range(5):
        btn = Button(window, text="+", width=100)
        btn.config(command=lambda b=btn: changecolor(b.cget("bg")))
        btn.place(relx=0, rely=x/5, relheight=1/5)
        ColorSaveButton.append(btn)


    draw_lines()


Start = Button(window, text="Start",command=lambda:Starts())
Start.pack()

window.geometry("1000x800")
window.config(bg="#676767")
canvas = Canvas(window,width=canvasWidth,height = canvasHeight,bg="#9F9F9F",bd= 4,relief="solid")
canvas.pack(expand = True, padx = 5,pady =5)

def only_numbers(P):
    if P == "":  # allow empty
        return True
    if not P.isdigit():  # reject non-digits
        return False
    if int(P) > 100:  # reject numbers above 100
        return False
    return True

vcmd = window.register(only_numbers)

setrows = Spinbox(window, from_=0, to=100, validate="key", validatecommand=(vcmd, "%P"))
setrows.pack(pady=10)
setcolumns = Spinbox(window, from_=0, to=100, validate="key", validatecommand=(vcmd, "%P"))
setcolumns.pack(pady=10)
setsize = Spinbox(window, from_=0, to=100, validate="key", validatecommand=(vcmd, "%P"))
setsize.pack(pady=10)
window.mainloop()
