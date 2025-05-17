import random
import os
import PIL
from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_text_m5djxtql = self.__tk_text_m5djxtql(self)
        self.tk_button_m5dk7wyx = self.__tk_button_m5dk7wyx(self)
        self.tk_text_m5dk8eon = self.__tk_text_m5dk8eon(self)
    def __win(self):
        self.title("PDF两两合并器v20250517")
        width = 800
        height = 600

        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.resizable(width=False, height=False)
        file_path = "background.jpg"

        if os.path.exists(file_path):
            self.image = PIL.Image.open(file_path)
            self.resized_image = self.image.resize(
                        (width, height), 
                        PIL.Image.Resampling.LANCZOS
                    )
            self.photo = ImageTk.PhotoImage(self.resized_image)

            label = Label(self, image=self.photo)
            label.place(relwidth=1, relheight=1)
        
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_text_m5djxtql(self,parent):
        text = Text(parent)
        text.place(x=40, y=40, width=320, height=400)
        self.create_bar(parent, text,True, True, 40, 40, 320,400,800,600)
        return text
    def __tk_button_m5dk7wyx(self,parent):
        btn = Button(parent, text="选择PDF并合并", takefocus=False,)
        btn.place(x=500, y=500, width=200, height=40)
        return btn
    def __tk_text_m5dk8eon(self,parent):
        text = Text(parent)
        text.place(x=40, y=480, width=320, height=80)
        return text
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_button_m5dk7wyx.bind('<Button-1>',self.ctl.on_click)
        pass
    def __style_config(self):
        pass
    def update_files(self, paths):
        self.tk_text_m5djxtql.delete("1.0", END)
        self.tk_text_m5djxtql.insert(END, paths)
    def update_results(self, str):
        self.tk_text_m5dk8eon.delete("1.0", END)
        self.tk_text_m5dk8eon.insert(END, str)       
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()