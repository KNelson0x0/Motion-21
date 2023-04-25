import customtkinter
import tkinter
from config        import *
from Utils.states    import BorderColor, CameraState, WindowState, LetterState, EventHandler, StateHandler
from GUI.ASL_GUI import App
import os

PATH = os.path.dirname(os.path.realpath(__file__))
dir_path = '%s\\ASL_Learning\\' %  os.environ['APPDATA'] 
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

#Can change this later for themes
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class LoginPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Size of window and title
        self.geometry("460x410")
        self.title("ASL Learning App")
        self.resizable(False, False)

        #Handy closing function to stop all running processes even when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.del_list = []

        self.LoginWindow()
 

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


    def LoginWindow(self):
        StateHandler().change_state(WindowState.HOME, self.del_list)
        self.grid_columnconfigure(0, weight=1)

        #len_users = len(Config().users)


        len_users = 2 #remove for Keith stuff
        self.frame_right = customtkinter.CTkScrollableFrame(master=self)
        self.frame_left = customtkinter.CTkFrame(master=self)
        self.frame_left.grid(row = 0, column = 1, sticky="nswe", padx=7, pady=5)
        self.frame_right.grid(row=1, column=1, sticky="nswe", padx=7, pady=5)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, width=100, font=("Segoe UI", 50), height=60, text="User Login", corner_radius=6)
        self.label_1.grid(row= 0, column = 0, padx = 100, pady = 30, sticky = "n")

        self.del_list.append(customtkinter.CTkLabel(master=self, font=("Segoe UI", 24), fg_color = "grey32", text="Select User:", corner_radius=6))
        self.del_list[-1].place(relx = 0.355, rely = 0.285)

        for i in range(len_users):
            btn = customtkinter.CTkButton(master=self.frame_right, text="Config().users[i]", corner_radius=6, width=200, command = lambda l = i: self.loadUser(l+1)) #Do Keith stuff here
            btn.grid(row = i, column = 0, padx = 118, pady = 20)
            self.del_list.append(btn)

        self.del_list.append(customtkinter.CTkButton(master=self, text="New User", corner_radius=6, width=200, height = 40, command = self.new_user))
        self.del_list[-1].grid(row = 2, column = 1, padx = 8, pady = 1, sticky = "w")

        self.del_list.append(customtkinter.CTkButton(master=self, text="Delete User", corner_radius=6, width=200, height = 40, command = self.del_user))
        self.del_list[-1].grid(row = 2, column = 1, padx = 8, pady = 1, sticky = "e")

        self.del_list.append(self.frame_right)
        self.del_list.append(self.frame_left)

    def loadUser(self, user):
        self.frame_right.grid_forget()
        self.del_list = StateHandler().change_state(WindowState.HOME, self.del_list)

        self.password = ""
        self.ShowPass = customtkinter.StringVar(self, "off")

        self.frame_middle = customtkinter.CTkFrame(master = self)
        self.frame_middle.grid_columnconfigure(0, weight=1)
        self.frame_middle.grid(row = 0, column = 0, sticky="nswe", padx=7, pady=5)

        self.Label = customtkinter.CTkLabel(master=self.frame_middle, font=("Segoe UI", 50), text="Welcome!", corner_radius=6)
        self.Label.grid(row = 0, column = 0, padx = 5, pady = 20)

        self.userName = customtkinter.CTkLabel(master=self.frame_middle, font=("Segoe UI", 24), fg_color = "grey32", text=user, corner_radius=6)
        self.userName.grid(row = 1, column = 0, padx = 5, pady = 3)

        self.password = customtkinter.CTkEntry(master = self.frame_middle, font=("Segoe UI", 16), placeholder_text = "Password", width = 200, show = "*", textvariable = self.password)
        self.password.grid(row = 2, column = 0, padx = 5, pady = 30)

        self.showPassword = customtkinter.CTkCheckBox(master=self.frame_middle, font=("Segoe UI", 12), text = "Show password", variable = self.ShowPass, command = self.ShowPassword, onvalue = "on", offvalue = "off")
        self.showPassword.grid(row = 3, column = 0, padx = 5, pady = 0)

        self.LoginButton = customtkinter.CTkButton(master=self.frame_middle, text="Login", corner_radius=6, width=200, height = 40, command = self.UserLogin)
        self.LoginButton.grid(row = 5, column = 0, padx = 8, pady = 50, sticky = "e")

        self.BackButton = customtkinter.CTkButton(master=self.frame_middle, text="Back", corner_radius=6, width=200, height = 40, command = self.BackLogin)
        self.BackButton.grid(row = 5, column = 0, padx = 8, pady = 50, sticky = "w")

    def ShowPassword(self):
        if(self.ShowPass.get() == "on"):
            self.password.configure(show='')
        else:
            self.password.configure(show='*')

    def BackLogin(self):
        self.frame_middle.grid_forget()
        self.frame_middle.destroy()

        self.LoginWindow()

    def UserLogin(self):
        print(self.password.get()) #Do Keith stuff here
        if "password" == "WRONG": #Do Keith stuff here
            self.del_list.append(customtkinter.CTkLabel(master=self.frame_middle, font=("Segoe UI", 18), text="Wrong password", corner_radius=6))
            self.del_list[-1].grid(row = 4, column = 0, padx = 5, pady = 10)
        else:
            ()
            #Do Keith stuff here

    def new_user(self):
        self.frame_right.grid_forget()
        self.del_list = StateHandler().change_state(WindowState.HOME, self.del_list)

        self.frame_user = customtkinter.CTkFrame(master=self)
        self.frame_user.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)
        self.frame_user.grid_columnconfigure(0, weight=1)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_user, font=("Segoe UI", 50), text="New User", corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 0, pady = 30)

        self.username = customtkinter.CTkEntry(master=self.frame_user, corner_radius=6, width=200, placeholder_text="username")
        self.username.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Password = customtkinter.CTkEntry(master=self.frame_user, corner_radius=6, width=200, placeholder_text="password")
        self.Password.grid(row= 3, column = 0, padx = 150, pady = 20)

        self.Button_F = customtkinter.CTkButton(master=self.frame_user, text="Create", corner_radius=6, width=200, command=self.buttonC)
        self.Button_F.grid(row= 4, column = 0, padx = 150, pady = 20)

        self.Button_E = customtkinter.CTkButton(master=self.frame_user, text="Back", corner_radius=6, width=200, command=self.buttonB)
        self.Button_E.grid(row= 5, column = 0, padx = 150, pady = 20)

    def buttonC(self):
        self.username.get()#Do Keith stuff here
        self.Password.get()#Do Keith stuff here

        self.frame_user.grid_forget()
        self.frame_user.destroy()
        self.LoginWindow()

    def buttonB(self):
        self.frame_user.grid_forget()
        self.frame_user.destroy()
        self.LoginWindow()

    def del_user(self):
        print("Delete user pressed")
