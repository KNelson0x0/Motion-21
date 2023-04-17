import customtkinter
import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))
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
        self.geometry("740x520")
        self.title("ASL Learning App")

        #Handy closing function to stop all running processes even when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.home_window()


    # Button function declarations
    # ------------------------------------------------------------------------------------    
    def load_image(self, path, image_size1, image_size2):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size1, image_size2)))
    
    # Button that recreates window with home page
 

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


    # Creates the home window
    def home_window(self):
        self.grid_columnconfigure(1, weight=1)


        self.home_image = self.load_image("/images/MainBG.png", 740, 520)
        self.left_finger = self.load_image("/images/finger2.png", 80, 80)
        self.right_finger = self.load_image("/images/finger.png", 80, 80)

        self.background_image = tkinter.Label(master=self, image=self.home_image)
        self.background_image.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.frame_right = customtkinter.CTkFrame(master = self)
        self.frame_left = customtkinter.CTkFrame(master = self)

        #self.frame_right.grid(row = 0, column = 1, padx = 20, pady = 2)



        self.motion21_title = customtkinter.CTkLabel(master=self, text = "MOTION 21", corner_radius = 0, width = 20, height = 20, font = ("Segoe UI", 100, "bold"), fg_color=("black","black"))
        self.motion21_title.grid(row=0, column=1, padx=0, pady=5, sticky = "n")

        self.button1 = customtkinter.CTkButton(master=self, text = "Lesson Select", font = ("Seoue UI", 50, "bold"), width = 200, height = 50, border_width = 2, corner_radius = 8,  fg_color = "grey", border_color="#000000")
        self.button1.grid(row=1, column=1, padx=0, pady=5, sticky = "n")

        self.button2 = customtkinter.CTkButton(master=self, text = "Settings", font = ("Seoue UI", 50, "bold"), width = 200, height = 50, border_width = 2, corner_radius = 8,  fg_color = "grey", border_color="#000000")
        self.button2.grid(row=2, column=1, padx=0, pady=5, sticky = "n")

        self.button2 = customtkinter.CTkButton(master=self, text = "Exit", font = ("Seoue UI", 50, "bold"), width = 200, height = 50, border_width = 2, corner_radius = 8,  fg_color = "grey", border_color="#000000")
        self.button2.grid(row=3, column=1, padx=0, pady=5, sticky = "n")

        self.left_image = tkinter.Label(master = self, image = self.left_finger)
        self.left_image.grid(row = 0, column = 0)

        self.right_image = tkinter.Label(master = self, image = self.right_finger)
        self.right_image.grid(row = 0, column = 3)







if __name__ == "__main__":
    app = App()
    app.start()