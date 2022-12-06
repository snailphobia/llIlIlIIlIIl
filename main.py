import customtkinter as ctk
import os
import platform
import hashlib as hl
# import pymysql as sql
import dbset

if platform.system() == 'Linux':
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
        # self.test()
    
    def encrypt(self, key):
        hasher = hl.sha256()
        hasher.update(bytes(self.password + key, 'utf-8')) # in this case key will be the context concatenated to the database hash
        return hasher.hexdigest()

    def addtolist(self, context, key): # context is a string representing the context of the password, key is the initial (plain) password
        self.passlist.append([context, self.encrypt(context + key)])

    def getpass(self, context):
        for i in self.passlist:
            if i[0] == context:
                return i[1]
        return 'No password found'

    def test(self):
        self.addtolist(context='context', key='test')
        print(self.getpass('context'))

class Main():
    loggedin = False
    userlist = []

    def loaduserlist(self):
        # load userlist from database from users table
        self.dbinstance.cursor.execute('SELECT * FROM users')
        for i in self.dbinstance.cursor.fetchall():
            self.userlist.append(User(i[0], i[1]))
        return

    def adduser(self):
        derived = ctk.CTkToplevel(self.root_ctk)
        derived.title('Register form')
        derived.geometry('420x240')

        def register():
            # search if user already exists
            for i in self.userlist:
                if i.name == user_entry.get():
                    print('User already exists') # replace with label
                    return
            
            if pass_entry.get() == pass_confirm_entry.get():
                self.dbinstance.dbadduser(user_entry.get(), pass_entry.get())  
                self.userlist.append(User(username=user_entry.get(), password=pass_entry.get()))
                derived.destroy()
            
            return

        # username entry
        user_entry = ctk.CTkEntry(derived, width=300, placeholder_text='Username')
        user_entry.place(relx = 0.5, rely = 0.1, anchor = 'center')

        # password entry
        pass_entry = ctk.CTkEntry(derived, width=300, placeholder_text='Password')
        pass_entry.place(relx = 0.5, rely = 0.3, anchor = 'center')

        # password confirm entry
        pass_confirm_entry = ctk.CTkEntry(derived, width=300, placeholder_text='Confirm password')
        pass_confirm_entry.place(relx = 0.5, rely = 0.5, anchor = 'center')

        # register button
        register_button = ctk.CTkButton(derived, text='Register', width=30, command = register)
        register_button.place(relx = 0.5, rely = 0.7, anchor = 'center')

        return
    
    # note that even if anyone has access to the database, they won't be able to decrypt the passwords because they don't have the key
    # the login system is just a proof of concept and only used to separate the tables in the database
    def checklogin(self, user, passw):
        for i in self.userlist:
            if i.name == user:
                if i.password == passw:
                    print('Logged in') # replace with label
                    self.loggedin = True
                    self.root_ctk.withdraw()
                    self.loggedinclient()
                    return
                else:
                    print('Wrong password') # replace with label
                    return
        print('User not found') # replace with label
        return

    # if login is successful, open the main window
    def loggedinclient(self):
        self.cl = ctk.CTkToplevel(self.root_ctk)
        self.cl.title('Logged in')
        self.cl.geometry('420x200')

        def quit(self):
            self.loggedin = False
            self.cl.destroy()
            self.root_ctk.deiconify()
            return

        self.cl.protocol('WM_DELETE_WINDOW', lambda: quit(self))
        self.cl.mainloop()
        

    def __init__(self):
        self.dbinstance = dbset.DB()
        ctk.set_default_color_theme('dark-blue')
        self.root_ctk = ctk.CTk()
        self.root_ctk.title('rev 0.6')
        self.root_ctk.geometry('420x200')

        self.loaduserlist()

        def getinput():
            self.checklogin(user_entry.get(), pass_entry.get())
            return

        # user entry
        user_entry = ctk.CTkEntry(self.root_ctk, width=300, placeholder_text='Username')
        user_entry.place(relx = 0.5, rely = 0.2, anchor = 'center')

        # password entry
        pass_entry = ctk.CTkEntry(self.root_ctk, width=300, placeholder_text='Password')
        pass_entry.place(relx = 0.5, rely = 0.4, anchor = 'center')

        # login button
        login_button = ctk.CTkButton(self.root_ctk, text='Login', width=30, command = getinput)
        login_button.place(relx = 0.5, rely = 0.6, anchor = 'center')
        
        # register button
        register_button = ctk.CTkButton(self.root_ctk, text='Register', width=30, command = self.adduser)
        register_button.place(relx = 0.5, rely = 0.8, anchor = 'center')

if __name__ == '__main__':
    mc = Main()
    mc.root_ctk.mainloop()
