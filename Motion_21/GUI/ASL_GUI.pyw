import os
import cv2
import customtkinter
from   enum import Enum
from   Utils.utils import *
from   .camera_window import CameraWindow
from   Utils.camera import Camera
from   Utils.constants import DEBUG
from   PIL import Image, ImageTk

PATH = os.path.dirname(os.path.realpath(__file__)) # NOTE: move this to constants

# To-Do List:
# 1) Implement save file
# 2) Fix color on themes page as it is currently set to a grey on right side (implement along with save file)
# 3) Add functionality to other buttons
# 4) Add options for text resizing and button resizing

#Can change this later for themes
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")


class CameraState(Enum):
    CAM_OFF = 0
    CAM_ON = 1
    CAM_REQUIRED = 2
    CAM_NOT_REQUIRED = 3

class WindowState(Enum):
    HOME     = [1, CameraState.CAM_NOT_REQUIRED]
    LESSONS  = [1, CameraState.CAM_NOT_REQUIRED]
    SETTINGS = [1, CameraState.CAM_REQUIRED]
    THEMES   = [1, CameraState.CAM_NOT_REQUIRED]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

       
        #Size of window and title
        self.window_state = WindowState.HOME
        self.camera_state = CameraState.CAM_NOT_REQUIRED
        self.geometry("780x520")
        self.title("ASL Learning App")

        # Locks size of window
        #self.resizable(False, False)

        #Handy closing function to stop all running processes even when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.current_frame = None

        self.home_window()
        self.after(10, self.the_afterinator)



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
        print("Testing user")

    # Button that recreates window with the theme page
    def themes_button(self):
        self.window_state = WindowState.THEMES


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
        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Default User Settings", width = 200, height = 50, border_width = 0, corner_radius = 0, border_color="#000000", command=self.default_user)
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
        self.window_state = WindowState.SETTINGS
        if DEBUG: cv2.destroyAllWindows() # just to see if this works
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

    # Button that returns to previous lesson
    def previous_section_button(self):


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

        self.window_state = WindowState.LESSONS
        self.camera_state = CameraState.CAM_REQUIRED
        self.cam_win1 = CameraWindow(master = self.frame_right, width=450, height=350, compound = "bottom",text="")
        self.cam_win1.grid(row=0, column=0, sticky="n", padx=5, pady=10)
        #self.label6 = customtkinter.CTkLabel(master=self.frame_right, text = "No Camera Found", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
        #self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        # Label that describes the main camera above
        self.label7 = customtkinter.CTkLabel(master=self.frame_right, text = "Main Camera")
        self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)        

        # Creates instruction window for the application to communicate with the user
        self.label8 = customtkinter.CTkLabel(master=self.frame_right, text = "Please sign the letter \"A\" \nas provided in the example!", text_font=("Segoe UI", 20), width = 350, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)

        # Window for the example camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output
        self.label9 = customtkinter.CTkLabel(master=self.frame_right, text = "No Logo Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        self.label9.grid(row=0, column=1, sticky="n", padx=0, pady=10)

        # Label that describes the example camera above
        self.label10 = customtkinter.CTkLabel(master=self.frame_right, text = "Example")
        self.label10.grid(row=0, column=1, padx=0, pady=0) 

        # Window for the user hand camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output
        self.cam_win2 = CameraWindow(master = self.frame_right, width=150, height=150, text = "", cropped = True, corner_radius = 8, compound = "bottom")
        self.cam_win2.grid(row=0, column=1, sticky="s", padx=0, pady=0)
        #self.label11 = customtkinter.CTkLabel(master=self.frame_right, text = "No Camera Found", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        #self.label11.grid(row=0, column=1, sticky="s", padx=0, pady=10)

        # Label that describes the user hand camera above
        self.label10 = customtkinter.CTkLabel(master=self.frame_right, text = "User Hand Camera")
        self.label10.grid(row=1, column=1, sticky="n", padx=0, pady=0) 

        # Label that describes the user's accuracy
        self.label11 = customtkinter.CTkLabel(master=self.frame_right, text = "Total Accuracy: 100%", text_font=("Segoe UI", 14))
        self.label11.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 


        self.the_afterinator()

    # Button that opens lesson select page
    def lesson_select_button(self):
        print("testing lesson select button")

    #Image processing function declarations
    # ------------------------------------------------------------------------------------    
    def load_image(self, path, image_size):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def on_closing(self, event=0):
        self.destroy()

    def the_afterinator(self): # I can and will default to doofenshmirtz like naming conventions.
        # todo: change the afterinator to have more of a list of functions to execute or something instead of ifs statements.
        if self.window_state == WindowState.LESSONS and self.camera_state == CameraState.CAM_REQUIRED:
            self.cam_win1.cw_update();
            self.cam_win2.cw_update();
            self.after(10, self.the_afterinator)

            if DEBUG: cv2.imshow("Sanity Window.", Camera().get_cropped_frame()) 

    def start(self):
        self.mainloop()

    # Miscellaneous function declarations
    # ------------------------------------------------------------------------------------    

    # Defines changing appearance mode
    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Defines user accounts
    def default_user(self):
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
        self.window_state = WindowState.HOME
        
        # Configures grid layout of 2x1
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Left side sub-window
        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
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
        self.frame_middle       = CameraWindow(master=self)
        #self.frame_middle       = customtkinter.CTkFrame(master=self)
        self.frame_middle.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        #Right side sub-window (May not need)
        self.frame_right = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_right.grid(row=0, column=2, sticky="nswe")
        self.update()

