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
    passlist = []
    def __init__(self, username, password):
        self.name = username
        self.password = password
    
    def endecode(self, passw, key):
        i = 0
        result = ''
        lenp = len(passw)
        for j in range(lenp):
            if i >= len(key):
                i -= len(key)
            result += chr(ord(passw[j]) ^ ord(key[i]))
        
        return result

    def addtolist(self, context, key, passw): # context is a string representing the context of the password, key is the initial (plain) password
        self.passlist.append([context, self.endecode(passw, key)])

    def getpass(self, context, key):
        for i in self.passlist:
            if i[1] == context:
                return self.endecode(i[2], key)
        return 'No password found'

    # debug
    # def test(self):
    #     self.addtolist(context='context', key='test')
    #     print(self.getpass('context'))

class Main():
    loggedin = False
    userlist = []
    wrapper = []
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
        label = []

        def register():
            # search if user already exists
            for i in self.userlist:
                if i.name == user_entry.get():
                    label = ctk.CTkLabel(derived, text='User already exists', text_color='red')
                    label.place(relx = 0.5, rely = 0.7, anchor = 'center')
                    return
            
            if pass_entry.get() == pass_confirm_entry.get():
                self.dbinstance.dbadduser(user_entry.get(), pass_entry.get())  
                self.userlist.append(User(username=user_entry.get(), password=pass_entry.get()))
                derived.destroy()
            else:
                label = ctk.CTkLabel(derived, text='Passwords don\'t match', text_color='red')
                label.place(relx = 0.5, rely = 0.7, anchor = 'center')
            
            return

        # username entry
        user_entry = ctk.CTkEntry(derived, width=300, placeholder_text='Username')
        user_entry.place(relx = 0.5, rely = 0.1, anchor = 'center')

        # password entry
        pass_entry = ctk.CTkEntry(derived, width=300, placeholder_text='Password', show='*')
        pass_entry.place(relx = 0.5, rely = 0.3, anchor = 'center')

        # password confirm entry
        pass_confirm_entry = ctk.CTkEntry(derived, width=300, placeholder_text='Confirm password', show='*')
        pass_confirm_entry.place(relx = 0.5, rely = 0.5, anchor = 'center')

        # register button
        register_button = ctk.CTkButton(derived, text='Register', width=30, command = register)
        register_button.place(relx = 0.5, rely = 0.9, anchor = 'center')

        return
    
    # note that even if anyone has access to the database, they won't be able to decode the passwords because they don't have the key
    # the login system is just a proof of concept and only used to separate the tables in the database
    def checklogin(self, user, passw):
        for i in self.userlist:
            if i.name == user:
                if i.password == passw:
                    print('Logged in') # for debug
                    self.loggedin = True
                    self.root_ctk.withdraw()

                    # replace the entries with new ones to reset them completely
                    self.user_entry.grid_remove()
                    self.pass_entry.grid_remove()
                    self.user_entry = ctk.CTkEntry(self.root_ctk, width=300, placeholder_text='Username')
                    self.user_entry.place(relx = 0.5, rely = 0.2, anchor = 'center')
                    self.pass_entry = ctk.CTkEntry(self.root_ctk, width=300, placeholder_text='Password', show='*')
                    self.pass_entry.place(relx = 0.5, rely = 0.4, anchor = 'center')

                    self.loggedinclient(user)
                    return
                else:
                    self.pass_entry.grid_remove()
                    self.pass_entry = ctk.CTkEntry(self.root_ctk, width=300, placeholder_text='Wrong Password', show='*')
                    self.pass_entry.place(relx = 0.5, rely = 0.4, anchor = 'center')
                    return
        
        self.user_entry.grid_remove()
        self.user_entry = ctk.CTkEntry(self.root_ctk, width=300, placeholder_text='User not found')
        self.user_entry.place(relx = 0.5, rely = 0.2, anchor = 'center')
        return

    # if login is successful, open the main window
    def loggedinclient(self, user):
        self.cl = ctk.CTkToplevel(self.root_ctk)
        self.cl.title('Logged in')
        self.cl.geometry('420x240')
        self.cl.minsize(420, 240)

        def quit(self):
            self.loggedin = False
            self.cl.destroy()
            self.user_entry.delete(0, 'end')
            self.pass_entry.delete(0, 'end')
            self.root_ctk.deiconify()
            return
    
        self.cl.protocol('WM_DELETE_WINDOW', lambda: quit(self))

        # load stored strings from database
        self.dbinstance.tableforuser(user)
        self.dbinstance.cursor.execute('SELECT * FROM ' + user)
        tuples = self.dbinstance.cursor.fetchall()
        data = []
        context = []
        obj_user = User(username='default', password='default')
        for u in self.userlist:
            if u.name == user:
                obj_user = u
                break
    
        for i in tuples:
            data.append((i[0], i[1], i[2]))
            context.append(i[1])
        
        dropdown = ctk.CTkOptionMenu(self.cl, width = 300, height = 30, values = context)
        dropdown.place(relx = 0.5, rely = 0.1, anchor = 'center')

        # make an entry for the private key used to encode the string
        key_entry = ctk.CTkEntry(self.cl, width=300, placeholder_text='Key')
        key_entry.place(relx = 0.5, rely = 0.3, anchor = 'center')

        # button to decode the string using the provided key and the endecode function in the User class
        def decode_act():

            for i in data:
                if i[1] == dropdown.get():
                    decrypted = obj_user.endecode(i[2], key_entry.get())
                    label = ctk.CTkLabel(self.cl, text=decrypted)
                    label.place(relx = 0.5, rely = 0.5, anchor = 'center')
                    return
            return
        
        send_it = ctk.CTkButton(self.cl, text='Decode', width=30, command = decode_act)
        send_it.place(relx = 0.25, rely = 0.7, anchor = 'center')

        # button to add a new entry to the database
        add_new = ctk.CTkButton(self.cl, text='Add new entry', width=30, command = lambda: add_new_entry(self, obj_user))
        add_new.place(relx = 0.75, rely = 0.7, anchor = 'center')

        # adds a new entry box between the button and the key entry for the context
        # then adds a new button to add the new entry to the database
        def add_new_entry(self, obj_user):
            # for context
            new_entry = ctk.CTkEntry(self.cl, placeholder_text='Context')
            new_entry.place(relx = 0.25, rely = 0.5, anchor = 'center')

            # for the password to be encoded
            new_entry_p = ctk.CTkEntry(self.cl, placeholder_text='Password to store', show='*')
            new_entry_p.place(relx = 0.75, rely = 0.5, anchor = 'center')

            label = []
            def add_new_entry_act():
                contextn = new_entry.get()
                passn = new_entry_p.get()
                keyn = key_entry.get()

                if contextn == '' or passn == '' or keyn == '':
                    # label with warning message
                    label = ctk.CTkLabel(self.cl, text='Please fill all the fields', text_color='red')
                    label.place(relx = 0.5, rely = 0.85, anchor = 'center')
                    return

                self.dbinstance.dbaddentry(user, contextn, obj_user.endecode(passn, keyn))
                delete_extra()
                return

            add_it = ctk.CTkButton(self.cl, text='Add to DB', width=30, command = add_new_entry_act)
            add_it.place(relx = 0.5, rely = 0.7, anchor = 'center')

            # cancel button
            cancel_it = ctk.CTkButton(self.cl, text='Cancel', width=30, command = delete_extra)
            cancel_it.place(relx = 0.75, rely = 0.85, anchor = 'center')

            self.wrapper = [new_entry, new_entry_p, add_it, cancel_it]
            if label != [] and len(self.wrapper) <= 4:
                self.wrapper.append(label)
            return

        # delete the newly added items
        def delete_extra():
            for i in self.wrapper:
                i.grid_remove()
                i.destroy()
            return

        return

    def __init__(self):
        self.dbinstance = dbset.DB()
        ctk.set_default_color_theme('dark-blue')
        self.root_ctk = ctk.CTk()
        self.root_ctk.minsize(420, 240)
        self.root_ctk.title('rev 1.0')
        self.root_ctk.geometry('420x240')

        self.loaduserlist()

        def getinput():
            self.checklogin(self.user_entry.get(), self.pass_entry.get())
            return

        # user entry
        self.user_entry = ctk.CTkEntry(self.root_ctk, width=300, placeholder_text='Username')
        self.user_entry.place(relx = 0.5, rely = 0.2, anchor = 'center')

        # password entry
        self.pass_entry = ctk.CTkEntry(self.root_ctk, width=300, placeholder_text='Password', show='*')
        self.pass_entry.place(relx = 0.5, rely = 0.4, anchor = 'center')

        # login button
        login_button = ctk.CTkButton(self.root_ctk, text='Login', width=30, command = getinput)
        login_button.place(relx = 0.5, rely = 0.7, anchor = 'center')
        
        # register button
        register_button = ctk.CTkButton(self.root_ctk, text='Register', width=30, command = self.adduser)
        register_button.place(relx = 0.5, rely = 0.9, anchor = 'center')

if __name__ == '__main__':
    mc = Main()
    mc.root_ctk.mainloop()
