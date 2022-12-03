#!/usr/bin/env python

import tkinter as tk
import customtkinter as ctk
import os
import platform

if platform.system() == "Linux":
    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

class Main():
    def __init__(self):
        root_tk = tk.Tk()  # create the Tk window like you normally do
        root_tk.geometry("400x240")
        root_tk.title("CustomTkinter Test")

        def button_function():
            print("button pressed")

        # Use CTkButton instead of tkinter Button
        button = ctk.CTkButton(master=root_tk, corner_radius=10, command=button_function)
        button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        root_tk.mainloop()

mc = Main()
