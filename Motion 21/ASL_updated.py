import customtkinter
import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk
import os

dir_path = '%s\\ASL_Learning\\' %  os.environ['APPDATA'] 
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

# To-Do List:
# 1) Implement save file
# 2) Fix color on themes page as it is currently set to a grey on right side (implement along with save file)
# 3) Add functionality to other buttons
# 4) Add options for text resizing and button resizing

#Can change this later for themes
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Size of window and title
        self.geometry("780x520")
        self.title("ASL Learning App")

        #Handy closing function to stop all running processes even when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.home_window()


    # Button function declarations
    # ------------------------------------------------------------------------------------    
    
    # Button that recreates window with home page
    def home_button(self):
        # Destroyed old window
        self.frame_left.destroy()
        self.frame_middle.destroy()
        self.frame_right.destroy()

        self.home_window()

    # Button that recreates window with users page
    def users_button(self):
        self.frame_left.destroy()
        self.frame_middle.destroy()
        self.frame_right.destroy()

        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
        
        count = 0
        

        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Home", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.home_button)
        self.button1.grid(row=0, column=0, padx=20, pady=20)
        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Users", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", state="disabled")
        self.button2.grid(row=1, column=0, padx=20, pady=20)
        self.button3 = customtkinter.CTkButton(master=self.frame_left, text = "Themes", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.themes_button)
        self.button3.grid(row=2, column=0, padx=20, pady=20)
        self.button5 = customtkinter.CTkButton(master=self.frame_left, text = "Exit", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.exit_button)
        self.button5.grid(row=3, column=0, padx=20, pady=20)
    

        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Return", width = 200, height = 50, border_width = 0, corner_radius = 0, border_color="#000000", command=self.return_function)
        self.button2.grid(row=9, column=0, padx=20, pady=350, sticky="w")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Choose User", corner_radius=6)
        self.label_1.grid(row= 0, column = 0, padx = 150, pady = 30)

        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        self.users = os.listdir(dir_path)
        if count == 3:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, command=self.buttonu1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], corner_radius=6, width=200, command=self.buttonu2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_3 = customtkinter.CTkButton(master=self.frame_right, text= self.users[2], corner_radius=6, width=200, command=self.buttonu3)
            self.Button_3.grid(row= 3, column = 0, padx = 150, pady = 20)

            self.Button_D = customtkinter.CTkButton(master=self.frame_right, text="Delete User", corner_radius=6, width=100, command=self.deleteU)
            self.Button_D.grid(row= 4, column = 0, padx = 150, pady = 20)
        if count == 2:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, command=self.buttonu1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], corner_radius=6, width=200, command=self.buttonu2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_C = customtkinter.CTkButton(master=self.frame_right, text="Create User", corner_radius=6, width=100, command=self.createU)
            self.Button_C.grid(row= 3, column = 0, padx = 128, pady = 20, sticky = "w")

            self.Button_D = customtkinter.CTkButton(master=self.frame_right, text="Delete User", corner_radius=6, width=100, command=self.deleteU)
            self.Button_D.grid(row= 3, column = 0, padx = 128, pady = 20, sticky = "e")
        if count == 1:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, command=self.buttonu1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_C = customtkinter.CTkButton(master=self.frame_right, text="Create User", corner_radius=6, width=100, command=self.createU)
            self.Button_C.grid(row= 2, column = 0, padx = 128, pady = 20, sticky = "w")

            self.Button_D = customtkinter.CTkButton(master=self.frame_right, text="Delete User", corner_radius=6, width=100, command=self.deleteU)
            self.Button_D.grid(row= 2, column = 0, padx = 128, pady = 20, sticky = "e")

        if count == 0:
            self.Button_C = customtkinter.CTkButton(master=self.frame_right, text="Create User", corner_radius=6, width=150, height = 50, command=self.createU)
            self.Button_C.grid(row= 1, column = 0, padx = 150, pady = 20)


    def buttonu1(self):
        file_path = '%suser1' % dir_path

    def buttonu2(self):
        file_path = '%suser2' % dir_path

    def buttonu3(self):
        file_path = '%suser3' % dir_path

    def createU(self):
        self.frame_right.destroy()

        self.frame_user = customtkinter.CTkFrame(master=self)
        self.frame_user.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_user, width=200, height=60, fg_color=("gray70", "gray25"), text="User Creator", corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.entry_1 = customtkinter.CTkEntry(master=self.frame_user, corner_radius=6, width=200, placeholder_text="username")
        self.entry_1.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_F = customtkinter.CTkButton(master=self.frame_user, text="Create", corner_radius=6, width=200, command=self.buttonC)
        self.Button_F.grid(row= 3, column = 0, padx = 150, pady = 20)

        self.Button_E = customtkinter.CTkButton(master=self.frame_user, text="Back", corner_radius=6, width=200, command=self.buttonB)
        self.Button_E.grid(row= 4, column = 0, padx = 150, pady = 20)

    def buttonC(self):
        count = 0
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        if count >= 3:
            self.ewindow = customtkinter.CTkToplevel(self)
            self.ewindow.geometry("400x200")
            self.ewindow.title("Error: Too many users")

            self.label = customtkinter.CTkLabel(master=self.ewindow, width=200, height=60, fg_color=("gray70", "gray25"), text="Error: Too many users", corner_radius=6)
            self.label.place(relx=0.5, rely=0.22, anchor=tkinter.CENTER)

            self.Buttone = customtkinter.CTkButton(master=self.ewindow, text="Exit", corner_radius=6, width=200, command = self.cExit)
            self.Buttone.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
        else:
            UserName = self.entry_1.get()
            file_path = f'%s{UserName}' % dir_path
            f = open(file_path, 'x')
            f.close()
            self.users_button()

    def buttonB(self):
        self.users_button()

    def cExit(self):
        self.ewindow.destroy()
        self.users_button()

    def deleteU(self):
        self.frame_right.destroy()
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Choose User to delete", corner_radius=6)
        self.label_1.grid(row= 0, column = 0, padx = 150, pady = 30)

        count = 0

        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1

        self.users = os.listdir(dir_path)
        if count == 3:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, command=self.buttonud1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], corner_radius=6, width=200, command=self.buttonud2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_3 = customtkinter.CTkButton(master=self.frame_right, text= self.users[2], corner_radius=6, width=200, command=self.buttonud3)
            self.Button_3.grid(row= 3, column = 0, padx = 150, pady = 20)

            self.Button_E = customtkinter.CTkButton(master=self.frame_right, text="Back", corner_radius=6, width=200, command=self.buttonB)
            self.Button_E.grid(row= 4, column = 0, padx = 150, pady = 20)

        if count == 2:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, command=self.buttonud1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], corner_radius=6, width=200, command=self.buttonud2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_E = customtkinter.CTkButton(master=self.frame_right, text="Back", corner_radius=6, width=200, command=self.buttonB)
            self.Button_E.grid(row= 3, column = 0, padx = 150, pady = 20)

        if count == 1:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, command=self.buttonud1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_E = customtkinter.CTkButton(master=self.frame_right, text="Back", corner_radius=6, width=200, command=self.buttonB)
            self.Button_E.grid(row= 2, column = 0, padx = 150, pady = 20)

        if count == 0:
            self.users_button()

    def buttonud1(self):
        self.frame_right.destroy()

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Are you sure?", corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.Button_y = customtkinter.CTkButton(master=self.frame_right, text="Yes", corner_radius=6, width=200, command=self.verifyDel1)
        self.Button_y.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_n = customtkinter.CTkButton(master=self.frame_right, text="No", corner_radius=6, width=200, command=self.buttonBD)
        self.Button_n.grid(row= 3, column = 0, padx = 150, pady = 20)


    def buttonud2(self):
        self.frame_right.destroy()

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Are you sure?", corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.Button_y = customtkinter.CTkButton(master=self.frame_right, text="Yes", corner_radius=6, width=200, command=self.verifyDel2)
        self.Button_y.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_n = customtkinter.CTkButton(master=self.frame_right, text="No", corner_radius=6, width=200, command=self.buttonBD)
        self.Button_n.grid(row= 3, column = 0, padx = 150, pady = 20)

    def buttonud3(self):
        self.frame_right.destroy()

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Are you sure?", corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.Button_y = customtkinter.CTkButton(master=self.frame_right, text="Yes", corner_radius=6, width=200, command=self.verifyDel3)
        self.Button_y.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_n = customtkinter.CTkButton(master=self.frame_right, text="No", corner_radius=6, width=200, command=self.buttonBD)
        self.Button_n.grid(row= 3, column = 0, padx = 150, pady = 20)

    def buttonBD(self):
        self.deleteU()

    def verifyDel1(self):
        users = os.listdir(dir_path)
        file_path = f'%s{users[0]}' % dir_path
        os.remove(file_path)
        self.users_button()

    def verifyDel2(self):
        users = os.listdir(dir_path)
        file_path = f'%s{users[1]}' % dir_path
        os.remove(file_path)
        self.users_button()

    def verifyDel3(self):
        users = os.listdir(dir_path)
        file_path = f'%s{users[2]}' % dir_path
        os.remove(file_path)
        self.users_button()
    # Button that recreates window with the theme page
    def themes_button(self):

        # Destroyed old window
        self.frame_left.destroy()
        self.frame_middle.destroy()
        self.frame_right.destroy()

        # Creates theme left window
        # ------------------------------------------------------------------------------------
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
        
        # Creates labels for the left window
        # ------------------------------------------------------------------------------------
        
        # Creates label with the text "Users:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Users:")
        self.label_1.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        # Default user settings button to reset all changes
        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Default User Settings", width = 200, height = 50, border_width = 0, corner_radius = 0, border_color="#000000", command=self.defaultUser)
        self.button1.grid(row=1, column=0, padx=1, pady=1)

        # Creates Return button
        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Return", width = 200, height = 50, border_width = 0, corner_radius = 0, border_color="#000000", command=self.return_function)
        self.button2.grid(row=9, column=0, padx=20, pady=350, sticky="w")

        # Creates the right side of the theme wind
        # ------------------------------------------------------------------------------------
        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius = 0, fg_color = "#303030")
        self.frame_right.grid(row=0, column=1, sticky="nswe")

        # Creates labels for the right window
        # ------------------------------------------------------------------------------------

        # Creates label with the text "Theme Settings:" to describe what the drop down menu below it does
        self.label_2 = customtkinter.CTkLabel(master=self.frame_right, text="Overall Theme Settings:")
        self.label_2.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Creates theme drop down menu to change general theme details all at once
        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_right, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=0, column=1, padx=5, pady=10, sticky="w")

    # Button that recreates window with settings page
    def settings_button(self):

        # Destroyed old window
        self.frame_left.destroy()
        self.frame_middle.destroy()
        self.frame_right.destroy()

        # Creates theme left window
        # ------------------------------------------------------------------------------------
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
        
        # Creates labels for the left window
        # ------------------------------------------------------------------------------------        
        #Button mapping and functionality
        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Home", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.home_button)
        self.button1.grid(row=0, column=0, padx=20, pady=20)
        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Users", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.users_button)
        self.button2.grid(row=1, column=0, padx=20, pady=20)
        self.button3 = customtkinter.CTkButton(master=self.frame_left, text = "Themes", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.themes_button)
        self.button3.grid(row=2, column=0, padx=20, pady=20)
        self.button5 = customtkinter.CTkButton(master=self.frame_left, text = "Exit", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.exit_button)
        self.button5.grid(row=3, column=0, padx=20, pady=20)
    
        # Creates Return button
        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Return", width = 200, height = 50, border_width = 0, corner_radius = 0, border_color="#000000", command=self.return_function)
        self.button2.grid(row=9, column=0, padx=20, pady=350, sticky="w")


    # Button that destroys window and exits program
    def exit_button(self):
        self.destroy()

    #Image processing function declarations
    # ------------------------------------------------------------------------------------    
    def load_image(self, path, image_size):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

    # Miscellaneous function declarations
    # ------------------------------------------------------------------------------------    

    # Defines changing appearance mode
    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Defines user accounts
    def defaultUser(self):
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")

    # Deletes the old window and prints the home window
    def return_function(self):
        self.frame_left.destroy()
        self.frame_middle.destroy()
        self.frame_right.destroy()

        self.home_window()

    # Creates the home window
    def home_window(self):

        # Configures grid layout of 2x1
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Left side sub-window
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # Creates label with the text "Users:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Lesson Stuff Goes Here:")
        self.label_1.grid(row=0, column=0, padx=1, pady=1, sticky="we")

        #Button mapping and functionality
        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Home", width = 48, height = 20, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.button1.grid(row=1, column=0, padx=0, pady=468, sticky="sw")
        self.button4 = customtkinter.CTkButton(master=self.frame_left, text = "Settings", width = 48, height = 20, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.settings_button)
        self.button4.grid(row=1, column=0, padx=0, pady=468, sticky="s")
        self.button5 = customtkinter.CTkButton(master=self.frame_left, text = "Exit", width = 48, height = 20, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.exit_button)
        self.button5.grid(row=1, column=0, padx=0, pady=468, sticky="se")

        #Middle sub-window
        self.frame_middle = customtkinter.CTkFrame(master=self)
        self.frame_middle.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        #Right side sub-window (May not need)
        self.frame_right = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_right.grid(row=0, column=2, sticky="nswe")


if __name__ == "__main__":
    app = App()
    app.start()