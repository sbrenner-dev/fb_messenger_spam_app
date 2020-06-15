import tkinter as tk
import fbchat
from tkinter import StringVar
from fbchat._exception import FBchatException

class LoginPage(tk.Frame):

    fbClient = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # info label setup
        info = tk.Label(self, text="Login page")
        info.pack(side="top", fill="x", pady=10)
        
        # Error space label - class variable to set text if needed
        self.error_msg=StringVar()
        self.error = tk.Label(self, textvariable=self.error_msg, fg="red")
        self.error.pack()

        # Text fields - class variables to use in another method
        userLabel = tk.Label(self, text="Username:")
        self.usertext = StringVar()
        self.username = tk.Entry(self, textvariable=self.usertext)
        passLabel = tk.Label(self, text="Password:")
        self.passtext = StringVar()
        self.password = tk.Entry(self, show="•", textvariable=self.passtext) # show • when entering password
        
        # packing
        userLabel.pack()
        self.username.pack()
        self.username.focus_set() # defualt focus here
        passLabel.pack()
        self.password.pack()
                

        # Login button
        login = tk.Button(self, text="Login", command=self.onLogin)
        login.pack(pady=20)
        
        self.password.bind('<KeyRelease>', self.enterHit)

    # bind final action to key-entry on password
    def enterHit(self, event):
        if event.keysym == 'Return':
            self.onLogin()
    
    def onLogin(self):
        self.error_msg.set("") # clear error field
        uid = self.username.get()
        cred = self.password.get()
        try:
            LoginPage.fbClient = fbchat.Client(uid, cred, max_tries=1)
            self.controller.show_frame("SpamPage")
        except FBchatException:
            self.error_msg.set("Username or password incorrect")
            self.passtext.set("")
            self.usertext.set("")
            self.username.focus()