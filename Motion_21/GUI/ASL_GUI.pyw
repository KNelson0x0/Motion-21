# copy and pasted from Jasons branch as github is being funky atm

from pickle import TRUE
import customtkinter
from enum import Enum
from ML.usertrain import UserTrain
from   Utils.constants import *
from .camera_window import CameraWindow
from PIL import Image, ImageTk
import os

#Can change this later for themes
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class CameraState(Enum):
    CAM_OFF = 0
    CAM_ON = 1
    CAM_REQUIRED = 2
    CAM_NOT_REQUIRED = 3

class WindowState(Enum):
    UNKNOWN  = [0, CameraState.CAM_NOT_REQUIRED] # for unstated windows, really only for debugging
    HOME     = [1, CameraState.CAM_NOT_REQUIRED]
    LESSONS  = [2, CameraState.CAM_REQUIRED]
    SETTINGS = [3, CameraState.CAM_NOT_REQUIRED]
    THEMES   = [4, CameraState.CAM_NOT_REQUIRED]
    CONFIG   = [5, CameraState.CAM_NOT_REQUIRED]
    TRAINING = [6, CameraState.CAM_REQUIRED]

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        #Size of window and title
        self.configure_guard = False;
        self.geometry("780x520")
        self.window_state = WindowState.HOME
        self.title("ASL Learning App")

        # Locks size of window
        self.resizable(False, False)

        #Handy closing function to stop all running processes even when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.home_window()

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
        print("testing user button")

    # Button that recreates window with the theme page
    def themes_button(self):
        self.window_state = WindowState.THEMES
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

    # Reconfigure the machine learnign on a letter for the user
    def configure_button(self): 
        self.window_state = WindowState.CONFIG
        # Destroyed old window
        self.frame_left.destroy()
        self.frame_right.destroy()

        # Creates left sub-window
        # ------------------------------------------------------------------------------------
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (1x8)
        self.frame_left.grid_rowconfigure(2, minsize=150)      # empty row as spacing
        self.frame_left.grid_rowconfigure(4, minsize=150)      # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=0)     # sets minimum size from bottom of screen to buttons

        # Creates label with the text "Configure Motion 21"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Configure Motion 21:", text_font=("Segoe UI", 14))
        self.label_1.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # Creates label with the description of the configure button menu
        self.label_3 = customtkinter.CTkLabel(master=self.frame_left, text="Is Motion 21 having trouble\n recognizing your signs?\n Reconfigure it to fit you \ninstead! Please click any of the\n letters from A to Z on the right \n and we will train our model\n based on your examples!\n", text_font=("Segoe UI", 11))
        self.label_3.grid(row=3, column=0, padx=1, pady=5, sticky="nswe")

        # Creates Return button
        self.button7 = customtkinter.CTkButton(master=self.frame_left, text = "Return", width = 150, height = 60, border_width = 1, corner_radius = 5, fg_color = "#292929", border_color="#101010", command=self.return_function)
        self.button7.grid(row=7, column=0, padx=0, pady=10, sticky="we")

        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self, fg_color = "#1A1A1A")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # configure grid layout (8x9)
        self.frame_right.grid_rowconfigure(1, minsize=50)      # empty row as spacing
        self.frame_right.grid_rowconfigure(8, minsize=0)       # sets minimum size from bottom of screen to buttons
        self.frame_right.grid_columnconfigure(0, minsize=25)   # empty column as spacing

        # Creates label with the text "Settings Page:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, text="Select a Letter to Change:", text_font=("Segoe UI", 20))
        self.label_1.grid(row=0, column=1, columnspan=7, padx=0, pady=0, sticky="we")

        #Button mapping and functionality
        # PLEASE ATTACH BUTTON FUNCTIONALITY FOR ALL THESE BUTTONS
        #

        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        row = 1 # 1 less than desired to account for modulo 0 op
        col = 0

        buttons = [] # ha, ha, ha, ha, keepinbuttonsalive, buttonsalive

        for i in range(26):
            if i % 6 == 0: row+=1
            if i == 24: col = 2 # align the last two in the middle
            col += 1
            
            new_button = customtkinter.CTkButton(master=self.frame_right, text = alpha[i], width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=lambda calling=alpha[i], : self.configure_button_handler(calling))
            new_button.grid(row=row, column=col,padx=15, pady=10, sticky="w")
            buttons.append(new_button)
            if col % 6 == 0: col=0
            
      
    def configure_button_handler(self, calling):
        print(calling)
        self.user_train(calling)



    def user_train(self, id):
        self.window_state = WindowState.TRAINING
        # Destroyed old window
        self.frame_left.destroy()
        self.frame_right.destroy()

        # Configures grid layout of 2x1
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creates left sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (9x1)
        self.frame_left.grid_rowconfigure(0, minsize=10)    # sets minimum size from top of screen to text
        self.frame_left.grid_rowconfigure(2, weight=1)      # creates empty row with weight 1
        self.frame_left.grid_rowconfigure(4, weight=0)      # creates empty row with weight 0
        self.frame_left.grid_rowconfigure(7, weight=1)      # creates empty row with weight 1
        self.frame_left.grid_rowconfigure(9, minsize=0)     # sets minimum size from bottom of screen to buttons

        # Creates user training label
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Training \nConfiguration:", text_font=("Segoe UI", 14))
        self.label_1.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # Previous training information for the user
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left, text='Please click "Begin"\nwhen ready to configure.\nPlease make sure your\n hand is in the frame.\nPlease move your\nhand around at different\nangles and lengths from\nthe camera. The camera\nwill record for a\nfew seconds and after\nyou should be good\n to go.', text_font=("Segoe UI", 11))
        self.label_2.grid(row=3, column=0, padx=1, pady=5, sticky="nswe")

        #Images for left side of window
        self.home_image = self.load_image("/images/home.png", 25, 25)
        self.home_example_image = self.load_image("/images/HomeExample.png", 700, 635)
        self.settings_image = self.load_image("/images/settings.png", 25, 25)
        self.exit_image = self.load_image("/images/exit.png", 25, 25)

        #Button mapping and functionality
        self.button3 = customtkinter.CTkButton(master=self.frame_left, image = self.home_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.button3.grid(row=8, column=0, padx=0, pady=0, sticky="sw")
        self.button4 = customtkinter.CTkButton(master=self.frame_left, image = self.settings_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.settings_button)
        self.button4.grid(row=8, column=0, padx=0, pady=0, sticky="s")
        self.button5 = customtkinter.CTkButton(master=self.frame_left, image = self.exit_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.exit_button)
        self.button5.grid(row=8, column=0, padx=0, pady=0, sticky="se")

        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.training = UserTrain("DEMO_USER", id, self.frame_right)

        # configure grid layout (5x3)
        self.frame_right.grid_rowconfigure((0, 1, 3), weight=1)        # sets weights of standard rows
        self.frame_right.grid_rowconfigure(5, weight=1)                # sets weight of last row
        self.frame_right.grid_columnconfigure((0, 1), weight=1)        # sets weights of standard columns
        self.frame_right.grid_columnconfigure(2, minsize=0)            # sets minimum size from right side of screen to cameras

        # Window for the main camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output
        if USE_CAMERA:
            self.config_cam_win1 = CameraWindow(master=self.frame_right, width = 290, height = 260, text = "", compound = "bottom",)
        else:
            self.config_cam_win1 = customtkinter.CTkLabel(master=self.frame_right, text = "[Debug] camera off")
        self.config_cam_win1.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Label that describes the main camera above
        self.label6 = customtkinter.CTkLabel(master=self.frame_right, text = "Main Camera")
        self.label6.grid(row=1, column=0, sticky="n", padx=10, pady=0)      

        # Creates instruction window for the application to communicate with the user
        self.label7 = customtkinter.CTkLabel(master=self.frame_right, text = 'Please sign the letter "{}" that you want \nMotion 21 to use as an example!'.format(id), text_font=("Segoe UI", 20), width = 450, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        self.label7.grid(row=3, column=0, columnspan=2, sticky="ns", padx=0, pady=0)

        self.button6 = customtkinter.CTkButton(master=self.frame_left, width = 160, height = 60, border_width = 1, corner_radius = 5, text = "Begin", compound = "bottom",  border_color="#101010", command=self.training_begin)
        self.button6.grid(row=7, column=0, columnspan=3, sticky="wse", padx=10, pady=10)

        # Window for the user hand camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output
        if USE_CAMERA:
            self.config_cam_win2 = CameraWindow(master=self.frame_right, width = 290, height = 260, text = "", compound = "bottom",)
        else:
            self.config_cam_win2 = customtkinter.CTkLabel(master=self.frame_right, width = 290, height = 260, text = "[Debug] camera off", cropped = True, compound = "bottom")
        self.config_cam_win2.grid(row=0, column=1, sticky="nw", padx=10, pady=10)

        # Label that describes the user hand camera above
        self.label9 = customtkinter.CTkLabel(master=self.frame_right, text = "Hand Camera")
        self.label9.grid(row=1, column=1, padx=0, pady=0, sticky="n")
        
        self.update()
        self.the_afterinator()
    # Button that recreates window with settings page

    def training_begin(self):
        self.training.on_begin()

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
        self.button7 = customtkinter.CTkButton(master=self.frame_left, text = "Configure Letter", width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = "#292929", border_color="#101010", command=self.configure_button)
        self.button7.grid(row=6, column=0, padx=0, pady=0)
    
        # Creates Return button
        self.button8 = customtkinter.CTkButton(master=self.frame_left, text = "Return", width = 150, height = 60, border_width = 1, corner_radius = 5, fg_color = "#292929", border_color="#101010", command=self.return_function)
        self.button8.grid(row=8, column=0, padx=0, pady=10, sticky="we")

        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self, fg_color = "#1A1A1A")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # Creates label with the text "Settings Page:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, text="Settings Page:", text_font=("Segoe UI", 20))
        self.label_1.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        # Creates label with the text describing button functionality
        self.label_2 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Home: Takes you back to the home page\n", text_font=("Segoe UI", 11))
        self.label_2.grid(row=1, column=0, padx=0, pady=0, sticky="w")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Home Settings: Customize your home page\n", text_font=("Segoe UI", 11))
        self.label_3.grid(row=2, column=0, padx=0, pady=0, sticky="w")
        self.label_4 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Users: Login to save your settings changes as well as lesson progression\n", text_font=("Segoe UI", 11))
        self.label_4.grid(row=3, column=0, padx=0, pady=0, sticky="w")
        self.label_5 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Themes: Change the theme and look of the application\n", text_font=("Segoe UI", 11))
        self.label_5.grid(row=4, column=0, padx=0, pady=0, sticky="w")
        self.label_6 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Volume: Change the audio volume of the application\n", text_font=("Segoe UI", 11))
        self.label_6.grid(row=5, column=0, padx=0, pady=0, sticky="w")
        self.label_7 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Notifications: Change notification options for the application\n", text_font=("Segoe UI", 11))
        self.label_7.grid(row=6, column=0, padx=0, pady=0, sticky="w")
        self.label_8 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Configure Letter: Lets you train Motion 21 to better suit your needs for letters\n", text_font=("Segoe UI", 11))
        self.label_8.grid(row=7, column=0, padx=0, pady=0, sticky="w")

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
    def previous_section_button(self):
        self.window_state = WindowState.UNKNOWN

        # Configures grid layout of 2x1
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creates left sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (1x9)
        self.frame_left.grid_rowconfigure(0, minsize=10)    # sets minimum size from top of screen to text
        self.frame_left.grid_rowconfigure(4, weight=20)      # creates empty row with weight 1
        self.frame_left.grid_rowconfigure(7, weight=1)      # creates empty row with weight 1
        self.frame_left.grid_rowconfigure(9, minsize=0)     # sets minimum size from bottom of screen to buttons

        # Creates lesson label
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Lesson 1-1:", text_font=("Segoe UI", 14))
        self.label_1.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # Space for the previous lesson data
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left, text="Alphabet Letters", text_font=("Segoe UI", 14))
        self.label_2.grid(row=2, column=0, padx=1, pady=1, sticky="we")

        # Previous lesson summary
        self.label_3 = customtkinter.CTkLabel(master=self.frame_left, text="\n\nThis lesson contains \ninformation on the \nalphabet letter \nsystem within ASL \nand will help you \nsign the letters A-E.", text_font=("Segoe UI", 11))
        self.label_3.grid(row=3, column=0, padx=1, pady=5, sticky="nswe")

        # Creates section label
        self.label_4 = customtkinter.CTkLabel(master=self.frame_left, text="Section 1 of 5", text_font=("Segoe UI", 10))
        self.label_4.grid(row=5, column=0, padx=1, pady=1, sticky="we")

        #Images for left side of window
        self.home_image = self.load_image("/images/home.png", 25, 25)
        self.home_example_image = self.load_image("/images/HomeExample.png", 700, 635)
        self.section_example_image = self.load_image("/images/SectionExample.png", 110, 50)
        self.settings_image = self.load_image("/images/settings.png", 25, 25)
        self.exit_image = self.load_image("/images/exit.png", 25, 25)

        # NEED TO FIX SIZING
        # Creates section image
        self.label5 = customtkinter.CTkLabel(master=self.frame_left, image = self.section_example_image)
        self.label5.grid(row=6, column=0, padx=0, pady=0, sticky="s")

        #Button mapping and functionality
        self.button3 = customtkinter.CTkButton(master=self.frame_left, image = self.home_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.button3.grid(row=8, column=0, padx=0, pady=0, sticky="sw")
        self.button4 = customtkinter.CTkButton(master=self.frame_left, image = self.settings_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.settings_button)
        self.button4.grid(row=8, column=0, padx=0, pady=0, sticky="s")
        self.button5 = customtkinter.CTkButton(master=self.frame_left, image = self.exit_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.exit_button)
        self.button5.grid(row=8, column=0, padx=0, pady=0, sticky="se")

        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # configure grid layout (2x5)
        self.frame_right.grid_rowconfigure((0, 1, 2, 3), weight=1)     # sets weights of standard rows
        self.frame_right.grid_rowconfigure(5, weight=1)               # sets weight of last row
        self.frame_right.grid_columnconfigure((0, 1), weight=1)        # sets weights of standard columns
        self.frame_right.grid_columnconfigure(2, weight=0)             # creates empty row with weight 0

        # Window for the main camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output
        self.label6 = customtkinter.CTkLabel(master=self.frame_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
        self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        # Label that describes the main camera above
        self.label7 = customtkinter.CTkLabel(master=self.frame_right, text = "Main Camera")
        self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)        

        # Creates instruction window for the application to communicate with the user
        self.label8 = customtkinter.CTkLabel(master=self.frame_right, text = "Please sign the letter \"A\" \nas provided in the example!", text_font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)

        # Window for the example camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output
        self.label9 = customtkinter.CTkLabel(master=self.frame_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)

        # Label that describes the example camera above
        self.label10 = customtkinter.CTkLabel(master=self.frame_right, text = "Example Camera")
        self.label10.grid(row=0, column=1, padx=0, pady=0) 

        # Window for the user hand camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output
        self.label11 = customtkinter.CTkLabel(master=self.frame_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)

        # Label that describes the user hand camera above
        self.label10 = customtkinter.CTkLabel(master=self.frame_right, text = "User Hand Camera")
        self.label10.grid(row=1, column=1, sticky="n", padx=0, pady=0) 

        # Label that describes the user's accuracy
        self.label11 = customtkinter.CTkLabel(master=self.frame_right, text = "Total Accuracy: 100%", text_font=("Segoe UI", 14))
        self.label11.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

    # Button that opens lesson select page
    def lesson_select_button(self):
        print("testing lesson select button")

    #Image processing function declarations
    # ------------------------------------------------------------------------------------    
    def load_image(self, path, image_size1, image_size2):
        return ImageTk.PhotoImage(Image.open("C:\\Users\\Resu\\Documents\\Dev\\Py\\Motion 21\\Motion_21\\GUI" + path).resize((image_size1, image_size2)))

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
        self.window_state = WindowState.HOME

        # Configures grid layout of 2x1
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creates left sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (1x9)
        self.frame_left.grid_rowconfigure(0, minsize=10)    # sets minimum size from top of screen to text
        self.frame_left.grid_rowconfigure(4, minsize=100)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(7, weight=1)      # empty row as spacing
        self.frame_left.grid_rowconfigure(9, minsize=0)     # sets minimum size from bottom of screen to buttons

        # Creates label with the text "Previous Lesson:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Previous Lesson:", text_font=("Segoe UI", 14))
        self.label_1.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # Space for the previous lesson data
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left, text="Lesson 1-1: \n\n Alphabet Letters", text_font=("Segoe UI", 13))
        self.label_2.grid(row=2, column=0, padx=1, pady=20, sticky="we")

        # Previous lesson summary
        self.label_3 = customtkinter.CTkLabel(master=self.frame_left, text="This lesson contains \ninformation on the \nalphabet letter \nsystem within ASL \nand will help you \nsign the letters A-E.", text_font=("Segoe UI", 11))
        self.label_3.grid(row=3, column=0, padx=1, pady=5, sticky="nswe")

        # Creates continue from previous section button
        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Continue from\n previous section?", width = 48, height = 20, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.previous_section_button)
        self.button1.grid(row=5, column=0, padx=10, pady=5, sticky="s")

        # Creates lesson select button
        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Move to lesson\n select?", width = 48, height = 20, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select_button)
        self.button2.grid(row=6, column=0, padx=10, pady=5, sticky="s")

        #Images for left side of window
        self.home_image = self.load_image("/images/home.png", 25, 25)
        self.home_example_image = self.load_image("/images/HomeExample.png", 700, 635)
        self.settings_image = self.load_image("/images/settings.png", 25, 25)
        self.exit_image = self.load_image("/images/exit.png", 25, 25)
        
        #Button mapping and functionality
        self.button3 = customtkinter.CTkButton(master=self.frame_left, image = self.home_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.button3.grid(row=8, column=0, padx=0, pady=0, sticky="sw")
        self.button4 = customtkinter.CTkButton(master=self.frame_left, image = self.settings_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.settings_button)
        self.button4.grid(row=8, column=0, padx=0, pady=0, sticky="s")
        self.button5 = customtkinter.CTkButton(master=self.frame_left, image = self.exit_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.exit_button)
        self.button5.grid(row=8, column=0, padx=0, pady=0, sticky="se")

        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        #Prints the home page help screen on the right window
        self.label4 = customtkinter.CTkLabel(master=self.frame_right, image = self.home_example_image, width = 550, height = 500)
        self.label4.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")

    def the_afterinator(self): # I can and will default to doofenshmirtz like naming conventions.
        # todo: change the afterinator to have more of a list of functions to execute or something instead of ifs statements.
        if self.window_state == WindowState.LESSONS and CameraState.CAM_REQUIRED in self.window_state: # find a better method of doing this later
            #self.cam_win1.cw_update();
            #self.cam_win2.cw_update();
            self.after(10, self.the_afterinator)
            return

        if self.window_state == WindowState.TRAINING: # find a better method of doing this later
            self.config_cam_win1.cw_update();
            self.config_cam_win2.cw_update();
            self.after(10, self.the_afterinator)

            #if DEBUG: cv2.imshow("Sanity Window.", Camera().get_cropped_frame()) 

    # Config functions for all the letters
    # ------------------------------------------------------------------------------------   
    

if __name__ == "__main__":
    app = App()
    app.start()
