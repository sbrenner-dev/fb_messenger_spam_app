import tkinter as tk
from tkinter import font as tkfont
from Login import LoginPage
from Spam import SpamPage

class SpamApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # general setup
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Frame init
        self.frames = {}
        for F in (LoginPage, SpamPage):
            page_name = F.__name__ # getting name of page to use as an index
            frame = F(parent=container, controller=self) # initializing page frame for tk window
            self.frames[page_name] = frame # adding to frames list
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.center(250, 300)
        self.show_frame("LoginPage") # initial page to show
        self.title("Spam your friends!")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def center(self, width, height):
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))