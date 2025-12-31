    btn = Button(window, text="+", width=80)
            btn.config(command=lambda b=btn: changecolor(b.cget("bg")))
            btn.place(relx=0, rely=x/5, relheight=1/5)
            ColorSaveButton.append(btn)