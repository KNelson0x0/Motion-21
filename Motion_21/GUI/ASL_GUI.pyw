import customtkinter
import tkinter
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))

dir_path = '%s\\ASL_Learning\\' %  os.environ['APPDATA'] 
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

#Can change this later for themes
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Size of window and title
        self.geometry("740x520")
        self.title("ASL Learning App")

        # Locks size of window
        self.resizable(False, False)

        #Handy closing function to stop all running processes even when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.home_window()

    #Image processing function declarations
    # ------------------------------------------------------------------------------------    
    def load_image(self, path, image_size1, image_size2):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size1, image_size2)))


    # Button function declarations
    # ------------------------------------------------------------------------------------    
    
    # Button that recreates window with home page
    def home_button(self):
        # Destroyed old window
        self.frame_left.destroy()
        self.frame_right.destroy()

        self.home_window()

    # Button that allows user to change home page preferences
    def home_settings_button(self):
        print("testing home settings button")

    # Button that recreates window with users page
    def users_button(self):
        self.frame_right.destroy()
        
        count = 0

        self.frame_right = customtkinter.CTkFrame(master=self, fg_color = "#1A1A1A")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Choose User", corner_radius=6)
        self.label_1.grid(row= 0, column = 0, padx = 150, pady = 30)

        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        self.users = os.listdir(dir_path)
        if count == 3:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonu1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonu2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_3 = customtkinter.CTkButton(master=self.frame_right, text= self.users[2], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonu3)
            self.Button_3.grid(row= 3, column = 0, padx = 150, pady = 20)

            self.Button_D = customtkinter.CTkButton(master=self.frame_right, text="Delete User", corner_radius=6, width=100, fg_color = "#292929", border_color="#101010", command=self.deleteU)
            self.Button_D.grid(row= 4, column = 0, padx = 150, pady = 20)
            
        if count == 2:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonu1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonu2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_C = customtkinter.CTkButton(master=self.frame_right, text="Create User", corner_radius=6, width=100, fg_color = "#292929", border_color="#101010", command=self.createU)
            self.Button_C.grid(row= 3, column = 0, padx = 128, pady = 20, sticky = "w")

            self.Button_D = customtkinter.CTkButton(master=self.frame_right, text="Delete User", corner_radius=6, width=100, fg_color = "#292929", border_color="#101010", command=self.deleteU)
            self.Button_D.grid(row= 3, column = 0, padx = 128, pady = 20, sticky = "e")

        if count == 1:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonu1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_C = customtkinter.CTkButton(master=self.frame_right, text="Create User", corner_radius=6, width=100, fg_color = "#292929", border_color="#101010", command=self.createU)
            self.Button_C.grid(row= 2, column = 0, padx = 128, pady = 20, sticky = "w")

            self.Button_D = customtkinter.CTkButton(master=self.frame_right, text="Delete User", corner_radius=6, width=100, fg_color = "#292929", border_color="#101010", command=self.deleteU)
            self.Button_D.grid(row= 2, column = 0, padx = 128, pady = 20, sticky = "e")

        if count == 0:
            self.Button_C = customtkinter.CTkButton(master=self.frame_right, text="Create User", corner_radius=6, width=150, height = 50, fg_color = "#292929", border_color="#101010", command=self.createU)
            self.Button_C.grid(row= 1, column = 0, padx = 150, pady = 20)


    def buttonu1(self):
        file_path = '%suser1' % dir_path

    def buttonu2(self):
        file_path = '%suser2' % dir_path

    def buttonu3(self):
        file_path = '%suser3' % dir_path

    def createU(self):
        self.frame_right.destroy()

        self.frame_user = customtkinter.CTkFrame(master=self, fg_color = "#1A1A1A")
        self.frame_user.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_user, width=200, height=60, font=("Segoe UI", 12), text="User Creator", corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.entry_1 = customtkinter.CTkEntry(master=self.frame_user, corner_radius=6, width=200, placeholder_text="username")
        self.entry_1.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_F = customtkinter.CTkButton(master=self.frame_user, text="Create", fg_color = "#292929", border_color="#101010", corner_radius=6, width=200, command=self.buttonC)
        self.Button_F.grid(row= 3, column = 0, padx = 150, pady = 20)

        self.Button_E = customtkinter.CTkButton(master=self.frame_user, text="Back", fg_color = "#292929", border_color="#101010", corner_radius=6, width=200, command=self.buttonBb)
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

            self.Buttone = customtkinter.CTkButton(master=self.ewindow, text="Exit", corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command = self.cExit)
            self.Buttone.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
        else:
            UserName = self.entry_1.get()
            file_path = f'%s{UserName}' % dir_path
            f = open(file_path, 'x')
            f.close()
            self.users_button()

    def buttonBb(self):
        self.users_button()

    def cExit(self):
        self.ewindow.destroy()
        self.users_button()

    def deleteU(self):
        self.frame_right.destroy()
        self.frame_right = customtkinter.CTkFrame(master=self, fg_color = "#1A1A1A")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Choose User to delete", corner_radius=6)
        self.label_1.grid(row= 0, column = 0, padx = 150, pady = 30)

        count = 0

        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1

        self.users = os.listdir(dir_path)
        if count == 3:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonud1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonud2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_3 = customtkinter.CTkButton(master=self.frame_right, text= self.users[2], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonud3)
            self.Button_3.grid(row= 3, column = 0, padx = 150, pady = 20)

            self.Button_E = customtkinter.CTkButton(master=self.frame_right, text="Back", corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonBb)
            self.Button_E.grid(row= 4, column = 0, padx = 150, pady = 20)

        if count == 2:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonud1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonud2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_E = customtkinter.CTkButton(master=self.frame_right, text="Back", corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonBb)
            self.Button_E.grid(row= 3, column = 0, padx = 150, pady = 20)

        if count == 1:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonud1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_E = customtkinter.CTkButton(master=self.frame_right, text="Back", corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonBb)
            self.Button_E.grid(row= 2, column = 0, padx = 150, pady = 20)

        if count == 0:
            self.users_button()

    def buttonud1(self):
        self.frame_right.destroy()

        self.frame_right = customtkinter.CTkFrame(master=self, fg_color = "#1A1A1A")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Are you sure?", corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.Button_y = customtkinter.CTkButton(master=self.frame_right, text="Yes", corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.verifyDel1)
        self.Button_y.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_n = customtkinter.CTkButton(master=self.frame_right, text="No", corner_radius=6, width=200, fg_color = "#292929", border_color="#101010", command=self.buttonBD)
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
        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Default User Settings", width = 200, height= 50, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.defaultUser)
        self.button1.grid(row=1, column=0, padx=1, pady=1)

        # Creates Return button
        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Return", width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.return_function)
        self.button2.grid(row=9, column=0, padx=0, pady=350, sticky="we")

        # Creates the right side of the theme wind
        # ------------------------------------------------------------------------------------
        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius = 0, fg_color = "#303030")
        self.frame_right.grid(row=0, column=1, sticky="nswe")

        # Creates labels for the right window
        # ------------------------------------------------------------------------------------

        # Creates label with the text "Overall Theme Settings:" to describe what the drop down menu below it does
        self.label_2 = customtkinter.CTkLabel(master=self.frame_right, text="Overall Theme Settings:")
        self.label_2.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Creates theme drop down menu to change general theme details all at once
        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_right, values=["System", "Light", "Dark"], fg_color = "#292929", command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Creates label with the text "Font Size:" to describe what the slider below it does
        self.label_3 = customtkinter.CTkLabel(master=self.frame_right, text="Font Size:")
        self.label_3.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Creates font size progress bar to change font size of application
        self.progressbar = customtkinter.CTkProgressBar(master=self)

        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                                from_=0,
                                                to=1,
                                                number_of_steps=10,
                                                command=self.progressbar.set)
        self.slider_1.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="we")   

        # Creates label with the text "Button Size:" to describe what the slider below it does
        self.label_3 = customtkinter.CTkLabel(master=self.frame_right, text="Button Size:")
        self.label_3.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Creates font size progress bar to change font size of application
        self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
                                                from_=0,
                                                to=1,
                                                number_of_steps=10,
                                                command=self.progressbar.set)
        self.slider_2.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")   


    # Button that recreates window with settings page
    def settings_button(self):

        # Destroyed old window
        self.frame_left.destroy()
        self.frame_right.destroy()

        # Creates left sub-window
        # ------------------------------------------------------------------------------------
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (1x8)
        self.frame_left.grid_rowconfigure(7, weight=1)      # empty row as spacing
        self.frame_left.grid_rowconfigure(9, minsize=0)     # sets minimum size from bottom of screen to buttons
        
        # Creates labels for the left window
        # ------------------------------------------------------------------------------------        
        #Button mapping and functionality
        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Home", width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.home_button)
        self.button1.grid(row=0, column=0, padx=0, pady=0)
        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Home Settings", width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.home_settings_button)
        self.button2.grid(row=1, column=0, padx=0, pady=0)        
        self.button3 = customtkinter.CTkButton(master=self.frame_left, text = "Users", width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.users_button)
        self.button3.grid(row=2, column=0, padx=0, pady=0)
        self.button4 = customtkinter.CTkButton(master=self.frame_left, text = "Themes", width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.themes_button)
        self.button4.grid(row=3, column=0, padx=0, pady=0)
        self.button5 = customtkinter.CTkButton(master=self.frame_left, text = "Volume", width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.volume_button)
        self.button5.grid(row=4, column=0, padx=0, pady=0)
        self.button6 = customtkinter.CTkButton(master=self.frame_left, text = "Notifications", width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.notif_button)
        self.button6.grid(row=5, column=0, padx=0, pady=0)
        #self.button7 = customtkinter.CTkButton(master=self.frame_left, text = "Configure Letter", width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.configure_button)
        #self.button7.grid(row=6, column=0, padx=0, pady=0)
    
        # Creates Return button
        self.button8 = customtkinter.CTkButton(master=self.frame_left, text = "Return", width = 150, height = 60, border_width = 1, corner_radius = 5, fg_color = "#292929", border_color="#101010", command=self.return_function)
        self.button8.grid(row=8, column=0, padx=0, pady=10, sticky="we")

        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self, fg_color = "#1A1A1A")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # Creates label with the text "Settings Page:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, text="Settings Page:", font=("Segoe UI", 20))
        self.label_1.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        # Creates label with the text describing button functionality
        self.label_2 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Home: Takes you back to the home page\n", font=("Segoe UI", 12))
        self.label_2.grid(row=1, column=0, padx=0, pady=0, sticky="w")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Home Settings: Customize your home page\n", font=("Segoe UI", 12))
        self.label_3.grid(row=2, column=0, padx=0, pady=0, sticky="w")
        self.label_4 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Users: Login to save your settings changes as well as lesson progression\n", font=("Segoe UI", 12))
        self.label_4.grid(row=3, column=0, padx=0, pady=0, sticky="w")
        self.label_5 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Themes: Change the theme and look of the application\n", font=("Segoe UI", 12))
        self.label_5.grid(row=4, column=0, padx=0, pady=0, sticky="w")
        self.label_6 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Volume: Change the audio volume of the application\n", font=("Segoe UI", 12))
        self.label_6.grid(row=5, column=0, padx=0, pady=0, sticky="w")
        self.label_7 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Notifications: Change notification options for the application\n", font=("Segoe UI", 12))
        self.label_7.grid(row=6, column=0, padx=0, pady=0, sticky="w")
        #self.label_8 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Configure Letter: Lets you train Motion 21 to better suit your needs for letters\n", font=("Segoe UI", 12))
        #self.label_8.grid(row=7, column=0, padx=0, pady=0, sticky="w")

    # Button that allows the user to change volume options
    def volume_button(self):
        print("testing volume button")

    # Button that allows the user to change notification options
    def notif_button(self):
        print("testing notification button")

    # Button that destroys window and exits program
    def exit_button(self):
        self.destroy()

    # Button that returns to previous lesson
    '''
    def start_lesson(self):
    
        self.button1.destroy()
        self.label_1.destroy()
        self.label_2.destroy()
        self.label_3.destroy()

        self.combobox1 = customtkinter.CTkComboBox(master=self.frame_left, values=["Lesson 1-1", "Lesson 1-2", "Lesson 1-3"], command=self.lesson_select_button)
        self.combobox1.grid(row=2, column=0, padx=5, pady=5, sticky="n")

        self.combobox2 = customtkinter.CTkComboBox(master=self.frame_left, values=["Lesson 2-1", "Lesson 2-2", "Lesson 2-3"], command=self.lesson_select_button)
        self.combobox2.grid(row=3, column=0, padx=5, pady=5, sticky="n")

        self.combobox2 = customtkinter.CTkComboBox(master=self.frame_left, values=["Lesson 3-1", "Lesson 3-2", "Lesson 3-3"], command=self.lesson_select_button)
        self.combobox2.grid(row=4, column=0, padx=5, pady=5, sticky="n")

        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # configure grid layout (5x2)
        self.frame_right.grid_rowconfigure((0, 1, 2, 3), weight=1)     # sets weights of standard rows
        self.frame_right.grid_rowconfigure(5, weight=1)               # sets weight of last row
        self.frame_right.grid_columnconfigure((0, 1), weight=1)        # sets weights of standard columns
        self.frame_right.grid_columnconfigure(2, weight=0)             # creates empty row with weight 0
'''

    def lesson_select(self):
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        # buttons
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")
        

        # lessons
        self.lesson1 = customtkinter.CTkButton(master = self.frame_main_right, text = "Lesson 1: A, B, C, D", font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = self.lesson1_letters)
        self.lesson1.grid(row = 1, column = 1, padx = 2, pady = 2)
        
        self.lesson2 = customtkinter.CTkButton(master = self.frame_main_right, text = "Lesson 2: E, F, G, H", font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = self.lesson2_letters)
        self.lesson2.grid(row = 1, column = 2, padx = 2, pady = 2)

        self.lesson3 = customtkinter.CTkButton(master = self.frame_main_right, text = "Lesson 3: I, K, L, M", font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = self.lesson3_letters)
        self.lesson3.grid(row = 1, column = 3, padx = 2, pady = 2)
        
        self.lesson4 = customtkinter.CTkButton(master = self.frame_main_right, text = "Lesson 4: N, O, P, Q", font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = self.lesson4_letters)
        self.lesson4.grid(row = 3, column = 1, padx = 2, pady = 2)
        
        self.lesson5 = customtkinter.CTkButton(master = self.frame_main_right, text = "Lesson 5: R, S, T, U", font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = self.lesson5_letters)
        self.lesson5.grid(row = 3, column = 2, padx = 2, pady = 2)

        self.lesson6 = customtkinter.CTkButton(master = self.frame_main_right, text = "Lesson 6: V, W, X, Y", font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = self.lesson6_letters)
        self.lesson6.grid(row = 3, column = 3, padx = 2, pady = 2)
        
        self.lesson7 = customtkinter.CTkButton(master = self.frame_main_right, text = "Lesson 7: J & Z", font = ("Segoe UI", 18, "bold"),  width = 200, height = 100, border_width = 2, corner_radius = 8, compound = "bottom", border_color = "#000000", command = self.lesson7_letters)
        self.lesson7.grid(row = 4, column = 2, padx = 2, pady = 2)
        
    def lesson1_letters(self):
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        #buttons
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        # description label
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = "Lesson 1: \nLetters A, B, C, and D\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language", font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")


        # letters A - D letters to select on screen
        self.buttonA = customtkinter.CTkButton(master = self.frame_main_right, text = "A", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("A"))
        self.buttonA.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonB = customtkinter.CTkButton(master = self.frame_main_right, text = "B", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("B"))
        self.buttonB.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "we")

        self.buttonC = customtkinter.CTkButton(master = self.frame_main_right, text = "C", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("C"))
        self.buttonC.grid(row = 2, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonD = customtkinter.CTkButton(master = self.frame_main_right, text = "D", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("D"))
        self.buttonD.grid(row = 2, column = 2, padx = 20, pady = 15, sticky = "we")

    def lesson2_letters(self):
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        #buttons
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        # description label
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = "Lesson 2: \nLetters E, F, G, and H\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language", font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # letters E,F,G,H to select on screen
        self.buttonE = customtkinter.CTkButton(master = self.frame_main_right, text = "E", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("E"))
        self.buttonE.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonF = customtkinter.CTkButton(master = self.frame_main_right, text = "F", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("F"))
        self.buttonF.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "we")

        self.buttonG = customtkinter.CTkButton(master = self.frame_main_right, text = "G", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("G"))
        self.buttonG.grid(row = 2, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonH = customtkinter.CTkButton(master = self.frame_main_right, text = "H", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("H"))
        self.buttonH.grid(row = 2, column = 2, padx = 20, pady = 15, sticky = "we")

    def lesson3_letters(self):
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        #buttons 
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        # description label
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = "Lesson 3: \nLetters I, K, L, and M\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language", font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = "\n\nLater on, the\n letter 'J' will\n be shown, since\n it is more\n complicated.", font = ("Segoue UI", 12))
        self.lesson_description.grid(row=2, column=0, padx=1, pady=1, sticky="we")

        # letters I, K, L, M to select on screen
        # skip J here and later Z because of movement
        self.buttonE = customtkinter.CTkButton(master = self.frame_main_right, text = "I", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("I"))
        self.buttonE.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonF = customtkinter.CTkButton(master = self.frame_main_right, text = "K", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("K"))
        self.buttonF.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "we")

        self.buttonG = customtkinter.CTkButton(master = self.frame_main_right, text = "L", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("L"))
        self.buttonG.grid(row = 2, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonH = customtkinter.CTkButton(master = self.frame_main_right, text = "M", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("M"))
        self.buttonH.grid(row = 2, column = 2, padx = 20, pady = 15, sticky = "we")

    def lesson4_letters(self):
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        #buttons 
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        # description labels
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = "Lesson 4: \nLetters N, O, P, and Q\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language", font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # letters N,O,P,Q to select on screen
        self.buttonE = customtkinter.CTkButton(master = self.frame_main_right, text = "N", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("N"))
        self.buttonE.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonF = customtkinter.CTkButton(master = self.frame_main_right, text = "O", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("O"))
        self.buttonF.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "we")

        self.buttonG = customtkinter.CTkButton(master = self.frame_main_right, text = "P", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("P"))
        self.buttonG.grid(row = 2, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonH = customtkinter.CTkButton(master = self.frame_main_right, text = "Q", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("Q"))
        self.buttonH.grid(row = 2, column = 2, padx = 20, pady = 15, sticky = "we")

    def lesson5_letters(self):
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        #buttons 
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        # description labels
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = "Lesson 5: \nLetters R, S, T, and U\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language", font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # Letters R,S,T,U to show on screen
        self.buttonE = customtkinter.CTkButton(master = self.frame_main_right, text = "R", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("R"))
        self.buttonE.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonF = customtkinter.CTkButton(master = self.frame_main_right, text = "S", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("S"))
        self.buttonF.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "we")

        self.buttonG = customtkinter.CTkButton(master = self.frame_main_right, text = "T", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("T"))
        self.buttonG.grid(row = 2, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonH = customtkinter.CTkButton(master = self.frame_main_right, text = "U", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("U"))
        self.buttonH.grid(row = 2, column = 2, padx = 20, pady = 15, sticky = "we")

    def lesson6_letters(self):
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        #buttons 
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        # description labels
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = "Lesson 6: \nLetters V, W, X, and Y\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language", font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # letters V, W, X, Y to show on screen
        self.buttonE = customtkinter.CTkButton(master = self.frame_main_right, text = "V", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("V"))
        self.buttonE.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonF = customtkinter.CTkButton(master = self.frame_main_right, text = "W", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("W"))
        self.buttonF.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "we")

        self.buttonG = customtkinter.CTkButton(master = self.frame_main_right, text = "X", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("X"))
        self.buttonG.grid(row = 2, column = 1, padx = 20, pady = 15, sticky = "we")

        self.buttonH = customtkinter.CTkButton(master = self.frame_main_right, text = "Y", font = ("Segoe UI", 50, "bold"), width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("Y"))
        self.buttonH.grid(row = 2, column = 2, padx = 20, pady = 15, sticky = "we")

    def lesson7_letters(self):
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        #buttons 
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        # letters J and Z, which require a special case of teaching
        self.buttonE = customtkinter.CTkButton(master = self.frame_main_right, text = "J", font = ("Segoe UI", 50, "bold"), width = 300, height = 300, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("J"))
        self.buttonE.grid(row = 1, column = 1, padx = 10, pady = 15, sticky = "we")

        self.buttonF = customtkinter.CTkButton(master = self.frame_main_right, text = "Z", font = ("Segoe UI", 50, "bold"), width = 300, height = 300, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color = "#101010", command=lambda : self.letter_lessons("Z"))
        self.buttonF.grid(row = 1, column = 2, padx = 10, pady = 15, sticky = "we")
    
    '''
    def letter_select(self):
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        #buttons
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        
        To Make This Dynamic!!!!:
        for statement for lessons, create those amount of buttons
        increase row and column with incrementing
        change text each increment
        '''
        
        

    # later we can alter this function to be just for "lesson 1" "lesson 2" and so on
    # for now it just has the entire alphabet, but later will call to each function for better organization
    def letter_lessons(self, letter):
        self.frame_main_right.destroy()

        self.back_to_lesson = customtkinter.CTkButton(master=self.frame_main_left, text = "Lesson Select", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.back_to_lesson.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")
        
        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)
        
        '''
        we can change these into lessons and call to lesssons "A-D" functions and etc and just call the function here
        add next and retry functionalities
        '''
        # This opens up the camera view for every sinlge letter, as the user chooses it
    
        match letter:
            case "A":
                # Window for the main camera
                # For now this is just an error message of "No Camera Found"
                # Once a camera is linked we create the same size window but with the camera output
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)

                # Label that describes the main camera above
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)        

                # Creates instruction window for the application to communicate with the user
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"A\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)

                # Window for the example camera
                # For now this is just an error message of "No Camera Found"
                # Once a camera is linked we create the same size window but with the camera output
                
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)

                # Load the image from the /image/letters folder to use for this part and position it in the correct place
                # Place Imaage of example sign for user to use when signing in the main lesson window 
                self.A_image = self.load_image("/images/letters/a.JPG", 150, 150)
                self.A_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.A_image, width = 150, height = 150)
                self.A_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)

                # Label that describes the example camera above
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Image")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 

                # Window for the user hand camera
                # For now this is just an error message of "No Camera Found"
                # Once a camera is linked we create the same size window but with the camera output
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)

                # Label that describes the user hand camera above
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 

                # Label that describes the user's accuracy
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "B":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"B\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.B_image = self.load_image("/images/letters/b.JPG", 150, 150)
                self.B_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.B_image, width = 150, height = 150)
                self.B_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "C":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"C\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.C_image = self.load_image("/images/letters/c.JPG", 150, 150)
                self.C_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.C_image, width = 150, height = 150)
                self.C_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "D":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"D\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.D_image = self.load_image("/images/letters/d.JPG", 150, 150)
                self.D_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.D_image, width = 150, height = 150)
                self.D_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "E":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"E\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.E_image = self.load_image("/images/letters/e.JPG", 150, 150)
                self.E_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.E_image, width = 150, height = 150)
                self.E_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "F":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"F\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.F_image = self.load_image("/images/letters/f.JPG", 150, 150)
                self.F_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.F_image, width = 150, height = 150)
                self.F_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "G":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"G\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.G_image = self.load_image("/images/letters/g.JPG", 150, 150)
                self.G_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.G_image, width = 150, height = 150)
                self.G_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "H":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"H\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.H_image = self.load_image("/images/letters/h.JPG", 150, 150)
                self.H_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.H_image, width = 150, height = 150)
                self.H_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "I":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"I\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.I_image = self.load_image("/images/letters/i.JPG", 150, 150)
                self.I_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.I_image, width = 150, height = 150)
                self.I_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "K":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"K\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.K_image = self.load_image("/images/letters/k.JPG", 150, 150)
                self.K_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.K_image, width = 150, height = 150)
                self.K_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "L":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"L\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.L_image = self.load_image("/images/letters/l.JPG", 150, 150)
                self.L_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.L_image, width = 150, height = 150)
                self.L_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "M":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"M\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                #self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                #self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.M_image = self.load_image("/images/letters/m.JPG", 150, 150)
                self.M_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.M_image, width = 150, height = 150)
                self.M_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "N":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"N\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "O":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"O\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "P":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"P\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "Q":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"Q\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "R":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"R\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "S":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"S\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "T":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"T\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "U":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"U\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "V":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"V\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "W":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"W\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "X":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"X\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "Y":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"Y\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
            
            case "J":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"J\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

            case "Z":
                self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
                self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)
                self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera")
                self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)
                self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Please sign the letter \"Z\" \nas provided in the example!", font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)
                self.label9 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)
                self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Camera")
                self.label10.grid(row=0, column=1, padx=0, pady=0) 
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
                self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)
                self.label11 = customtkinter.CTkLabel(master=self.frame_main_right, text = "User Hand Camera")
                self.label11.grid(row=1, column=1, sticky="n", padx=0, pady=0) 
                self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: 100%", font=("Segoe UI", 14))
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 
                self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

    # Button that opens lesson select page
    def lesson_select_button(self, choice):
        print(f"testing lesson select button {choice}")

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
        self.frame_right.destroy()

        self.home_window()

    # Creates the home window
    def home_window(self):

        # Configures grid layout of 2x1
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creates left sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (9x1)
        self.frame_left.grid_rowconfigure(0, minsize=10)    # sets minimum size from top of screen to text
        self.frame_left.grid_rowconfigure(4, minsize=100)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(7, weight=1)      # empty row as spacing
        self.frame_left.grid_rowconfigure(9, minsize=0)     # sets minimum size from bottom of screen to buttons

        
        self.frame_right = customtkinter.CTkFrame(master = self)
        self.frame_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_right.grid_rowconfigure(0, minsize=10)   
        self.frame_right.grid_rowconfigure(4, minsize=100)   
        self.frame_right.grid_rowconfigure(7, weight=1)      
        self.frame_right.grid_rowconfigure(9, minsize=0)
        

        '''
        # Creates label with the text "Previous Lesson:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Previous Lesson:", font=("Segoe UI", 14))
        self.label_1.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # Space for the previous lesson data
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left, text="Lesson 1-1: \n\n Alphabet Letters", font=("Segoe UI", 13))
        self.label_2.grid(row=2, column=0, padx=1, pady=20, sticky="we")

        # Previous lesson summary
        self.label_3 = customtkinter.CTkLabel(master=self.frame_left, text="This lesson contains \ninformation on the \nalphabet letter \nsystem within ASL \nand will help you \nsign the letters A-E.", font=("Segoe UI", 12))
        self.label_3.grid(row=3, column=0, padx=1, pady=5, sticky="nswe")
        '''

        #Images for left side of window
        self.home_image = self.load_image("/images/home.png", 25, 25)
        self.home_example_image = self.load_image("/images/HomeExample.png", 700, 635)
        self.home_description = self.load_image("/images/home2.png", 600, 250)
        self.settings_image = self.load_image("/images/settings.png", 25, 25)
        self.exit_image = self.load_image("/images/exit.png", 25, 25)
        
        #Button mapping and functionality
        self.button3 = customtkinter.CTkButton(master=self.frame_left, image = self.home_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.button3.grid(row=8, column=0, padx=0, pady=0, sticky="sw")
        
        self.button4 = customtkinter.CTkButton(master=self.frame_left, image = self.settings_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.settings_button)
        self.button4.grid(row=8, column=1, padx=0, pady=0, sticky="s")
        
        self.button5 = customtkinter.CTkButton(master=self.frame_left, image = self.exit_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.exit_button)
        self.button5.grid(row=8, column=2, padx=0, pady=0, sticky="se")


        
        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        #self.frame_right = customtkinter.CTkFrame(master=self)
        #self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        #Prints the home page help screen on the right window
        #self.label4 = customtkinter.CTkLabel(master=self.frame_right, text = "", width = 550, height = 500)
        #self.label4.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")

        # Create a Label on the right of our Application Title
        self.motion21_title = customtkinter.CTkLabel(master=self.frame_right, text = "MOTION 21", width = 20, height = 20, font = ("Segoe UI", 100, "bold"), fg_color=("white", "gray38"))
        self.motion21_title.grid(row=0, column=0, padx=0, pady=0, sticky = "we")

        # Creates continue from previous section button
        self.button1 = customtkinter.CTkButton(master=self.frame_right, text = "Lesson Select", font = ("Seoue UI", 50, "bold"), width = 200, height = 50, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.button1.grid(row=1, column=0, padx=0, pady=5, sticky="we")

        # Create a label based on the image of the home description
        #self.motion21_description = customtkinter.CTkLabel(master=self.frame_right, text = "", image = self.home_description, width = 20, height = 20, fg_color=("white", "gray38"))
        #self.motion21_description.grid(row=2, column=0, padx=0, pady=5)

        self.motion21_title = customtkinter.CTkLabel(master=self.frame_right, text = "Motion 21 is an American Sign Language Learning Application,\n using computer vision and machine learning to provide\n the user with live feedback on what gesture or character\n they are holding up on screen.", width = 20, height = 150, font = ("Segoe UI", 20), fg_color=("white", "gray20"))
        self.motion21_title.grid(row=2, column=0, padx=0, pady=50, sticky = "we")

    # Config functions for all the letters
    # ------------------------------------------------------------------------------------   
    '''
    def config_A(self):
        
        id = 'A'

        self.user_train(id)

    def config_B(self):
        print("testing config B")

    def config_C(self):
        print("testing config C")

    def config_D(self):
        print("testing config D")

    def config_E(self):
        print("testing config E")

    def config_F(self):
        print("testing config F")

    def config_G(self):
        print("testing config G")

    def config_H(self):
        print("testing config H")

    def config_I(self):
        print("testing config I")

    def config_J(self):
        print("testing config J")

    def config_K(self):
        print("testing config K")

    def config_L(self):
        print("testing config L")

    def config_M(self):
        print("testing config M")

    def config_N(self):
        print("testing config N")

    def config_O(self):
        print("testing config O")

    def config_P(self):
        print("testing config P")

    def config_Q(self):
        print("testing config Q")

    def config_R(self):
        print("testing config R")

    def config_S(self):
        print("testing config S")

    def config_T(self):
        print("testing config T")

    def config_U(self):
        print("testing config U")

    def config_V(self):
        print("testing config V")

    def config_W(self):
        print("testing config W")

    def config_X(self):
        print("testing config X")

    def config_Y(self):
        print("testing config Y")

    def config_Z(self):
        print("testing config Z")
    '''


if __name__ == "__main__":
    app = App()
    app.start()
