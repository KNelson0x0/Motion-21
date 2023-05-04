import customtkinter
import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk
import os
from datetime import date

PATH = os.path.dirname(os.path.realpath(__file__))
dir_path = '%s\\ASL_Learning\\' %  os.environ['APPDATA'] 
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

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

        self.lesson_select()

 
    def load_image(self, path, image_size1, image_size2):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size1, image_size2)))

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


    # Creates the home window
    def lesson_select(self):
        #self.grid_columnconfigure(1, weight=1)
        #self.grid_rowconfigure(0, weight=1)


        #self.bg_image = customtkinter.CTkImage(Image.open(PATH + "/images/blackbg.png"), size=(740, 520))
        #self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image, text = "")
        #self.bg_image_label.place(relx= 0, rely = 0)
        today = date.today()
        dateTime = today.strftime("%m/%d/%y")

        self.frame_middle = customtkinter.CTkFrame(master = self, border_width= 3)
        self.frame_left = customtkinter.CTkFrame(master = self, height = 40, border_width= 3)
        self.frame_right = customtkinter.CTkFrame(master = self, height = 40, border_width= 3)

        self.frame_middle.grid(row = 1, column = 0, padx = 30, pady = 60)
        self.frame_left.place(relx = 0.08, rely = .85)
        self.frame_right.grid(row = 1, column = 1, padx = 30, pady = 60)




        self.motion21_title = customtkinter.CTkLabel(master=self.frame_middle, text = "MOTION 21", corner_radius = 10, width = 20, height = 20, font = ("Segoe UI", 70, "bold"))
        self.motion21_title.grid(row=0, column=0, padx=5, pady=5, sticky = "n")

        self.button1 = customtkinter.CTkButton(master=self.frame_middle, text = "Lesson Select", font = ("Seoue UI", 50, "bold"), width = 100, height = 50, border_width = 3, corner_radius = 10, border_color="#000000")
        self.button1.grid(row=1, column=0, padx=0, pady=10, sticky = "n")

        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Settings", font = ("Seoue UI", 12, "bold"), width = 200, height = 50, border_width = 3, corner_radius = 10, border_color="#000000")
        self.button2.grid(row=0, column=0, padx=2, pady=5, sticky = "n")

        self.button3 = customtkinter.CTkButton(master=self.frame_left, text = "Logout", font = ("Seoue UI", 12, "bold"), width = 200, height = 50, border_width = 3, corner_radius = 10, border_color="#000000")
        self.button3.grid(row=0, column=1, padx=2, pady=5, sticky = "n")

        self.button4 = customtkinter.CTkButton(master=self.frame_left, text = "Exit", font = ("Seoue UI", 12, "bold"), width = 200, height = 50, border_width = 3, corner_radius = 10, border_color="#000000")
        self.button4.grid(row=0, column=2, padx=2, pady=5, sticky = "n")

        self.label = customtkinter.CTkLabel(master = self.frame_right, text = "\nWelcome back", corner_radius = 10, width = 20, height = 20, font = ("Segoe UI", 15, "bold"))
        self.label.grid(row = 0, column = 0, padx =0, pady = 5)

        self.label1 = customtkinter.CTkLabel(master = self.frame_right, text = "Jason!", corner_radius = 10, width = 20, height = 20, font = ("Segoe UI", 22, "bold"))
        self.label1.grid(row = 1, column = 0, padx =5)

        self.label2 = customtkinter.CTkLabel(master = self.frame_right, text = f"\nDate: {dateTime}\n", corner_radius = 10, width = 20, height = 20, font = ("Segoe UI", 15, "bold"))
        self.label2.grid(row = 2, column = 0, padx =5, pady = 5)

        self.label3 = customtkinter.CTkLabel(master = self.frame_right, text = "Fun Fact: ASL is considered\n as a foreign language!\n\n", corner_radius = 10, width = 20, height = 20, font = ("Segoe UI", 12, "bold"))
        self.label3.grid(row = 3, column = 0, padx =5, pady = 5)



if __name__ == "__main__":
    app = App()
    app.start()