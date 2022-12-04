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
    # username = ''
    # password = ''
    passlist = []
    def __init__(self, username, password):
        self.name = username
        self.password = password
        self.test()
    
    def encrypt(self, key):
        hasher = hl.sha256()
        hasher.update(bytes(self.password + key, "utf-8"))
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
    def adduser(self):
        derived = ctk.CTkToplevel(self.root_ctk)
        derived.title("Register form")
        derived.geometry("400x240")

        def register():
            if pass_entry.get() == pass_confirm_entry.get():
                self.userlist.append(User(username=user_entry.get(), password=pass_entry.get()))
                derived.destroy()

        # username entry
        user_entry = ctk.CTkEntry(derived, width=300)
        user_entry.grid(row=0, column=1, padx=10, pady=10)

        # password entry
        pass_entry = ctk.CTkEntry(derived, width=300)
        pass_entry.grid(row=1, column=1, padx=10, pady=10)

        # password confirm entry
        pass_confirm_entry = ctk.CTkEntry(derived, width=300)
        pass_confirm_entry.grid(row=2, column=1, padx=10, pady=10)

        # register button
        register_button = ctk.CTkButton(derived, text="Register", width=30, command = register)
        register_button.grid(row=3, column=1, padx=10, pady=10)

        print("hello")
    
    def checklogin(self):
        return

    def __init__(self):
        ctk.set_default_color_theme("dark-blue")
        self.root_ctk = ctk.CTk()
        self.root_ctk.title("rev 0.1")
        self.root_ctk.geometry("690x420")

        # user entry
        user_entry = ctk.CTkEntry(self.root_ctk, width=300)
        user_entry.grid(row=0, column=1, padx=10, pady=10)

        # password entry
        pass_entry = ctk.CTkEntry(self.root_ctk, width=300)
        pass_entry.grid(row=1, column=1, padx=10, pady=10)

        # login button
        login_button = ctk.CTkButton(self.root_ctk, text="Login", width=30, command = self.checklogin)
        login_button.grid(row=2, column=1, padx=10, pady=10)
        
        # register button
        register_button = ctk.CTkButton(self.root_ctk, text="Register", width=30, command = self.adduser)
        register_button.grid(row=3, column=1, padx=10, pady=10)
    
        self.root_ctk.mainloop()

mc = Main()
