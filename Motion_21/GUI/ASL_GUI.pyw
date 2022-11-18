import customtkinter
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))

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
        print("Testing user")

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
        self.frame_middle = customtkinter.CTkFrame(master=self)
        self.frame_middle.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        #Right side sub-window (May not need)
        self.frame_right = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_right.grid(row=0, column=2, sticky="nswe")


if __name__ == "__main__":
    app = App()
    app.start()