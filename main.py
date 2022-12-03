import tkinter as tk
import customtkinter as ctk
import os
import platform
import hashlib as hl

if platform.system() == "Linux":
    #!/usr/bin/env python
    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

class User():
    passlist = []
    def __init__(self, username, password):
        self.name = username
        self.password = password
        self.test()
    
    def encrypt(self, key):
        hasher = hl.sha256()
        hasher.update(bytes(key, "utf-8"))
        return hasher.hexdigest()

    def addtolist(self, context, key): # context is a string representing the context of the password, key is the initial (plain) password
        self.passlist.append([context, self.encrypt(key)])

    def getpass(self, context):
        for i in self.passlist:
            if i[0] == context:
                return i[1]
        return "No password found"

    def test(self):
        self.addtolist(context="context", key="test")
        print(self.getpass("context"))
class Main():
    userlist = []
    def __init__(self):
        ctk.set_default_color_theme("dark-blue")
        root_ctk = ctk.CTk()
        root_ctk.title("rev 0.1")
        root_ctk.geometry("400x240")

        def button_function():
            print("button pressed")
            self.userlist.append(User("test", "test"))

        # Use CTkButton instead of tkinter Button
        button = ctk.CTkButton(master=root_ctk, corner_radius=10, command=button_function)
        button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        root_ctk.mainloop()

mc = Main()
