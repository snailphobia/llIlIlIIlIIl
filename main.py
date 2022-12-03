import tkinter as tk
import customtkinter as ctk
import os
import platform

if platform.system() == "Linux":
    #!/usr/bin/env python
    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

class Main():
    def __init__(self):
        ctk.set_default_color_theme("dark-blue")
        root_ctk = ctk.CTk()
        root_ctk.title("rev 0.1")
        root_ctk.geometry("400x240")

        def button_function():
            print("button pressed")

        # Use CTkButton instead of tkinter Button
        button = ctk.CTkButton(master=root_ctk, corner_radius=10, command=button_function)
        button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        root_ctk.mainloop()

mc = Main()
