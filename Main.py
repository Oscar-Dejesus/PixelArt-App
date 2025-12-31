from tkinter import *
from tkinter import colorchooser
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
    global color 
    color = color_name
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
    canvas.config(width = columns*size,height = rows*size)
    window.bind("<Button-1>", Click) 
    window.bind("<B1-Motion>",Click)
    canvas.pack(expand = True, padx = 5,pady =5)
    window.update()

    x=0
    for _ in range(columns):
        x+=size
        array_boxes.append(x)
  
    img= PhotoImage(file="eraser.png")
    img_big = img.zoom(2,2)
    clear_button = Button(window,text="clear",command =clear)
    blue_button = Button(window,text="Blue",command= lambda:changecolor("blue"))
    red_button = Button(window,text="Red",command= lambda:changecolor("red"))
    erase_button = Button(window,command= lambda:changecolor(""),image=img_big,width = 100,height = 100,bg="#000000")
    erase_button.image = img_big  
    Color_picker = Button(window,text="Pick color",command= pickcolor)
    Color_picker.pack()
    erase_button.place(x=900,y=170)
    blue_button.place(x=900,y=20)
    red_button.place(x=900,y=70)
    clear_button.place(x=900,y = 120)
    
    draw_lines()


Start = Button(window, text="Start",command=lambda:Starts())
Start.pack()

window.geometry("1000x800")
canvas = Canvas(window,width=canvasWidth,height = canvasHeight,bg="white")


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
