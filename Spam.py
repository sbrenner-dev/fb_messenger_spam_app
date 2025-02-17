import fbchat
import tkinter as tk
from Login import LoginPage
from tkinter import StringVar

class SpamPage(tk.Frame):
    def __init__(self, parent, controller):

        self.cache_list = [] # defining cache list for this page

        tk.Frame.__init__(self, parent) # initialize frame
        self.controller = controller # set frame-switchin controller

        # info label
        info = tk.Label(self, text="Time to spam!")
        info.pack(side="top", fill="x", pady=2)

        # error message
        self.error_msg=StringVar()
        self.error = tk.Label(self, textvariable=self.error_msg, fg="red")
        self.error.pack()

        # friend entry
        friend_label = tk.Label(self, text="Friend:")
        friend_label.pack()
        self.friendtxt = StringVar()
        self.friend = tk.Entry(self, textvariable=self.friendtxt)
        self.friend.bind('<KeyRelease>', self.onChange)
        self.friend.pack()

        # remaining entries - spam time, message
        msg_info = tk.Label(self, text="Message:")
        msg_info.pack()
        self.msgtxt = StringVar()
        self.msg_box = tk.Entry(self, textvariable=self.msgtxt)
        self.msg_box.pack()

        # spam info
        spam_info = tk.Label(self, text="Number of times to spam:")
        spam_info.pack()
        self.spamtxt = StringVar()
        self.spam_times = tk.Entry(self, textvariable=self.spamtxt)
        self.spam_times.pack()
        self.spam_times.bind('<KeyRelease>', self.enterHit) # bind enter/return key to this field

        # sent notification
        self.sent_txt = StringVar()
        self.sentlabel = tk.Label(self, textvariable=self.sent_txt, fg="green")
        self.sentlabel.pack(side="bottom")

        # submission button
        submit = tk.Button(self, text="Spam!", command=self.onSubmit)
        submit.pack(side="bottom", pady=10)

        # clear button
        clear = tk.Button(self, text="Clear entries", command=self.clear)
        clear.pack(side="bottom")
    
    # clear button functionality
    def clear(self):
        """ Clears all relevant fields in this frame """
        self.spamtxt.set("")
        self.msgtxt.set("")
        self.friendtxt.set("")
        self.sent_txt.set("")
        self.friend.focus()

    # button functionality
    def onSubmit(self):
        """ Handles the submission for this page.
            Clears all relevant fields, and provides an error message if necessary.
            Tries to find the FB friend entered and spam-message the first one found.
                On error, repeats the same error message."""
        self.error_msg.set("")
        self.sent_txt.set("")
        if self.friend.get() == "" or self.msg_box.get() == "" or self.spam_times.get() == "":
            self.error_msg.set("Some field(s) entered incorrectly")
            self.clear()
        else:
            try:
                uid = LoginPage.fbClient.searchForUsers(self.friend.get())[0].uid
                for _ in range(int(self.spam_times.get())):
                    LoginPage.fbClient.sendMessage(self.msg_box.get(), thread_id=uid)
                self.sent_txt.set("Sent!")
            except:
                self.error_msg.set("Some field(s) entered incorrectly")
                self.clear()

    # function for when user changes friend field
    # caches search to local list, uses in place of continual search until relevant results are out
    def onChange(self, event):
        """ Handles an on-change event for the friend text field.
            Implements an autocomplete function based on a chached list of friend names,
                based on the progressive string entered.
            Once the cached list is depleted, the fbchat function is called again
                to search for a new cache list.
            Actual auto-complete fill is handled at the end of the method."""
        # backspace only matters for resetting cache
        if len(event.keysym) == 1 or event.keysym == 'space' or event.keysym == 'BackSpace':
            name = self.friend.get() # value
            pos = len(name) # position
            if not len(self.cache_list) or self.friendtxt.get() == "":
                # either cache list is empty or there is no entry in friend field
                self.cache_list = LoginPage.fbClient.searchForUsers(name)
            
            if len(self.cache_list) and not (event.keysym == 'BackSpace'):

                # update cache list based on text entered
                while len(self.cache_list) and not (self.cache_list[0].name.startswith(self.friendtxt.get())):
                    del self.cache_list[0]
                if not len(self.cache_list): # list is empty
                    # reset cache list because no matches left
                    self.cache_list = LoginPage.fbClient.searchForUsers(name)

                # autocomplete fill 
                self.friend.delete(0, tk.END) # remove
                self.friend.insert(0, self.cache_list[0].name) # insert autocomplete
                self.friend.select_range(pos, tk.END) # highlight from typed point to end
                self.friend.icursor(pos) # position cursor at last typed point
    
    # bind final action to key-entry on password
    def enterHit(self, event):
        """ Handles a key hit on a field
        
            Specifically, handles enter/return hit on last field in this frame"""
        if event.keysym == 'Return':
            self.onSubmit()
