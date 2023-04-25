from turtle import bgcolor
import customtkinter
import tkinter
from config        import *
from Utils.imports import *
from time import sleep
from GUI.ASL_GUI import App
import os
from random import randint

PATH = os.path.dirname(os.path.realpath(__file__))
dir_path = '%s\\ASL_Learning\\' %  os.environ['APPDATA'] 
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

#Can change this later for themes
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class LoginPage(customtkinter.CTk):
    def __init__(self, EXPORT_list : list):
        super().__init__()

        #Size of window and title
        self.geometry("460x410")
        self.title("ASL Learning App")
        self.resizable(False, False)

        #Handy closing function to stop all running processes even when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.del_list = []
        self.EXPORT_list = EXPORT_list
        self.wrong_count = 0
        self.wrong_label_active: bool = False
        self.pass_nonmatch_active : bool = False
        self.login_window()
 
    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

    def login_window(self):
        StateHandler().change_state(WindowState.HOME, self.del_list)
        self.grid_columnconfigure(0, weight=1)

        len_users = len(Config().users)
        #len_users = 2
        #users = ["ow", "pain"]

        #len_users = 2 #remove for Keith stuff
        self.frame_right = customtkinter.CTkScrollableFrame(master=self)
        self.frame_left = customtkinter.CTkFrame(master=self)
        self.frame_left.grid(row = 0, column = 1, sticky="nswe", padx=7, pady=5)
        self.frame_right.grid(row=1, column=1, sticky="nswe", padx=7, pady=5)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, width=100, font=("Segoe UI", 50), height=60, text="User Login", corner_radius=6)
        self.label_1.grid(row= 0, column = 0, padx = 100, pady = 30, sticky = "n")

        self.del_list.append(customtkinter.CTkLabel(master=self, font=("Segoe UI", 24), fg_color = "grey32", text="Select User:", corner_radius=6))
        self.del_list[-1].place(relx = 0.355, rely = 0.285)

        for i in range(len_users):
            btn = customtkinter.CTkButton(master=self.frame_right, text=Config().users[i], corner_radius=6, width=200, command = lambda l = i: self.load_user(Config().users[l])) #Do Keith stuff here
            #btn = customtkinter.CTkButton(master=self.frame_right, text=users[i], corner_radius=6, width=200, command = lambda l = i: self.load_user(users[l]))
            btn.grid(row = i, column = 0, padx = 118, pady = 20)
            self.del_list.append(btn)

        self.del_list.append(customtkinter.CTkButton(master=self, text="New User", corner_radius=6, width=200, height = 40, command = self.new_user))
        self.del_list[-1].grid(row = 2, column = 1, padx = 8, pady = 1, sticky = "w")

        self.del_list.append(customtkinter.CTkButton(master=self, text="Delete User", corner_radius=6, width=200, height = 40, command = lambda l = i: self.del_window(Config().users[l])))
        self.del_list[-1].grid(row = 2, column = 1, padx = 8, pady = 1, sticky = "e")

        self.del_list.append(self.frame_right)
        self.del_list.append(self.frame_left)

    def del_window(self, user): # ripped your load_user keegan and changed a bit to make this work
        self.frame_right.grid_forget()
        self.del_list = StateHandler().change_state(WindowState.HOME, self.del_list)

        self.password = ""
        self.show_pass = customtkinter.StringVar(self, "off")

        self.frame_middle = customtkinter.CTkFrame(master = self)
        self.frame_middle.grid_columnconfigure(0, weight=1)
        self.frame_middle.grid(row = 0, column = 0, sticky="nswe", padx=7, pady=5)

        self.sure_label = customtkinter.CTkLabel(master=self.frame_middle, font=("Segoe UI", 50), text="Are you sure?", corner_radius=6)
        self.sure_label.grid(row = 0, column = 0, padx = 5, pady = 20)

        self.user_name = customtkinter.CTkLabel(master=self.frame_middle, font=("Segoe UI", 24), fg_color = "grey32", text=user, corner_radius=6)
        self.user_name.grid(row = 1, column = 0, padx = 5, pady = 3)

        self.password = customtkinter.CTkEntry(master = self.frame_middle, font=("Segoe UI", 16), placeholder_text = "Password", width = 200, show = "*", textvariable = self.password)
        self.password.grid(row = 2, column = 0, padx = 5, pady = 30)

        self.show_password_cbox = customtkinter.CTkCheckBox(master=self.frame_middle, font=("Segoe UI", 12), text = "Show password", variable = self.show_pass, command = self.show_password, onvalue = "on", offvalue = "off")
        self.show_password_cbox.grid(row = 3, column = 0, padx = 5, pady = 0)

        self.confirm_button = customtkinter.CTkButton(master=self.frame_middle, text="Confirm", corner_radius=6, width=200, height = 40, command = self.del_user)
        self.confirm_button.grid(row = 5, column = 0, padx = 8, pady = (50,0), sticky = "e")

        self.back_button = customtkinter.CTkButton(master=self.frame_middle, text="Back", corner_radius=6, width=200, height = 40, command = self.back_login)
        self.back_button.grid(row = 5, column = 0, padx = 8, pady = (50,0), sticky = "w")
        self.wrong_label_active = False

    def load_user(self, user):
        self.frame_right.grid_forget()
        self.del_list = StateHandler().change_state(WindowState.HOME, self.del_list)

        self.password = ""
        self.show_pass = customtkinter.StringVar(self, "off")

        self.frame_middle = customtkinter.CTkFrame(master = self)
        self.frame_middle.grid_columnconfigure(0, weight=1)
        self.frame_middle.grid(row = 0, column = 0, sticky="nswe", padx=7, pady=5)

        self.sure_label = customtkinter.CTkLabel(master=self.frame_middle, font=("Segoe UI", 50), text="Welcome!", corner_radius=6)
        self.sure_label.grid(row = 0, column = 0, padx = 5, pady = 20)

        self.user_name = customtkinter.CTkLabel(master=self.frame_middle, font=("Segoe UI", 24), fg_color = "grey32", text=user, corner_radius=6)
        self.user_name.grid(row = 1, column = 0, padx = 5, pady = 3)

        self.password = customtkinter.CTkEntry(master = self.frame_middle, font=("Segoe UI", 16), placeholder_text = "Password", width = 200, show = "*", textvariable = self.password)
        self.password.grid(row = 2, column = 0, padx = 5, pady = 30)

        self.show_password_cbox = customtkinter.CTkCheckBox(master=self.frame_middle, font=("Segoe UI", 12), text = "Show password", variable = self.show_pass, command = self.show_password, onvalue = "on", offvalue = "off")
        self.show_password_cbox.grid(row = 3, column = 0, padx = 5, pady = 0)

        self.confirm_button = customtkinter.CTkButton(master=self.frame_middle, text="Login", corner_radius=6, width=200, height = 40, command = self.user_login)
        self.confirm_button.grid(row = 5, column = 0, padx = 8, pady = 50, sticky = "e")

        self.back_button = customtkinter.CTkButton(master=self.frame_middle, text="Back", corner_radius=6, width=200, height = 40, command = self.back_login)
        self.back_button.grid(row = 5, column = 0, padx = 8, pady = 50, sticky = "w")
        self.wrong_label_active = False

    def show_password(self):
        if(self.show_pass.get() == "on"):
            self.password.configure(show='')
        else:
            self.password.configure(show='*')

    def back_login(self):
        self.frame_middle.grid_forget()
        self.frame_middle.destroy()

        self.login_window()

    def user_login(self):
        Config().set_password(self.password.get())
        cfg = Config().load(self.user_name.cget("text"), self.password.get())
        
        if cfg == False:
            if not self.wrong_label_active: 
                self.wrong_label_active = True
                self.password.configure(border_color="#FF0000")

                self.wrong_label = customtkinter.CTkLabel(master=self.frame_middle, font=("Segoe UI", 18), text="Wrong password", corner_radius=6)
                self.del_list.append(self.wrong_label)
                self.del_list[-1].grid(row = 4, column = 0, padx = 5, pady = 10)
            else:
                wrong_list = {
                    0 : "Wrong password",
                    1 : "Nope",
                    2 : "Try Again",
                    3 : "Is CapsLock On?",
                    4 : "Not Quite",
                    5 : "Good try though",
                    6 : "You'll get it eventually",
                    7 : "uhhh, no"
                }
                self.wrong_label.configure(text=wrong_list[randint(0,7)])
                return
        else:
            self.EXPORT_list[0] = True
            self.EXPORT_list[1] = self.user_name.cget("text")
            self.destroy() # EXTREMELY CURSED

    def new_user(self):
        self.pass_nonmatch_active = False
        self.frame_right.grid_forget()
        self.del_list = StateHandler().change_state(WindowState.HOME, self.del_list)

        self.frame_user = customtkinter.CTkFrame(master=self)
        self.frame_user.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)
        self.frame_user.grid_columnconfigure(0, weight=1)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_user, font=("Segoe UI", 50), text="New User", corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 0, pady = 30)

        self.username = customtkinter.CTkEntry(master=self.frame_user, corner_radius=6, width=200, placeholder_text="username")
        self.username.grid(row= 2, column = 0, padx = 150, pady = 25)

        self.password = customtkinter.CTkEntry(master=self.frame_user, corner_radius=6, width=200, placeholder_text="password")
        self.password.grid(row= 3, column = 0, padx = 150, pady = 10)

        self.password_confirm = customtkinter.CTkEntry(master=self.frame_user, corner_radius=6, width=200, placeholder_text="confirm password")
        self.password_confirm.grid(row = 4, column = 0, padx = 150, pady = 10)

        self.f_button = customtkinter.CTkButton(master=self.frame_user, text="Create", corner_radius=6, height = 40, width=200, command=self.button_create)
        self.f_button.grid(row= 6, column = 0, padx = 8, pady = (50,0), sticky='es')

        self.e_button = customtkinter.CTkButton(master=self.frame_user, text="Back", corner_radius=6, height = 40, width=200, command=self.button_back)
        self.e_button.grid(row= 6, column = 0, padx = 8, pady = (50,0), sticky='ws')

    def button_create(self):
        if self.password.get() != self.password_confirm.get():
            self.password_confirm.configure(border_color="#FF0000")
           
            if not self.pass_nonmatch_active:
                self.wrong_label = customtkinter.CTkLabel(master=self.frame_user, font=("Segoe UI", 18), text="Passwords don't match", corner_radius=6)

                self.f_button.grid_configure(pady=(23,0))
                self.e_button.grid_configure(pady=(23,0))

                self.del_list.append(self.wrong_label)
                self.del_list[-1].grid(row = 5, column = 0, padx = 5, pady = (10,0))
                self.pass_nonmatch_active = True
            else:
                wrong_list = {
                    0 : "No match",
                    1 : "Okay but which one?",
                    2 : "Passwords don't match",
                    3 : "Not the same",
                    4 : "Do it again.",
                    5 : "You have given me two\ncompletely different things.",
                    6 : "This isn't the full app you know",
                    7 : "Stop it.",
                    8 : "You just like reading these don't you",
                    9 : "Ha! You DO!",
                    10 : "Okay well im done talking to you.",
                    11 : "Make them match or I go away.",
                    12 : "Fine be like that.",
                    13 : " ",
                    14 : " ",
                    15 : " ",
                    16 : "REALLY????",
                    17 : "YOU KNOW WHAT?",
                    18 : "ONE MORE TIME I DARE YOU"
                }

                self.wrong_count+=1
                if self.wrong_count == 19:
                    self.destroy()
                    return

                self.wrong_label.configure(text=wrong_list[self.wrong_count])
                
                return
        else:
            Config().set_password(self.password.get())
            Config().add_user(self.username.get(), self.password.get())

            self.frame_user.grid_forget()
            self.frame_user.destroy()
            self.login_window()

    def button_back(self):
        self.frame_user.grid_forget()
        self.frame_user.destroy()
        self.login_window()

    def del_user(self):
        Config().set_password(self.password.get())
        cfg = Config().load(self.user_name.cget("text"), self.password.get())
        
        if cfg == False:
            if not self.wrong_label_active: 
                self.wrong_label_active = True
                self.password.configure(border_color="#FF0000")

                self.wrong_label = customtkinter.CTkLabel(master=self.frame_middle, font=("Segoe UI", 18), text="Wrong password", corner_radius=6)
                self.del_list.append(self.wrong_label)
                self.del_list[-1].grid(row = 4, column = 0, padx = 5, pady = (10,0))
            else:
                wrong_list = {
                    0 : "Wrong password",
                    1 : "Maybe you shouldn't go",
                    2 : "Hey its not right, maybe reconsider while you\n find the right one?",
                    3 : "Gonna be with us a bit longer",
                    4 : "You shouldn't delete other peoples accounts,\nhence the password requirement",
                    5 : "We hope you enjoyed using the App, but thats\n not the right password",
                    6 : "Not quite",
                    7 : "Are you sure?"
                }
                self.wrong_label.configure(text=wrong_list[randint(0,7)])
                return
        else:
            Config().delete_user(self.user_name.cget("text"), self.password.get())
            if self.wrong_label_active: 
                self.wrong_label.configure(text="Goodbye :)!")
                sleep(3)
            self.EXPORT_list[0] = False
            self.destroy()
