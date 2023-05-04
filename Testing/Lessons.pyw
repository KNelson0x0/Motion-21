import customtkinter
import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk
import os

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

    def lesson_select(self):
        self.grid_columnconfigure(1, weight=1)

        self.frame_middle = customtkinter.CTkFrame(master = self, border_width= 3)

        self.frame_middle.grid(row = 0, column = 1, padx = 5, pady = 120)

        self.lesson_title = customtkinter.CTkLabel(master=self, text = "Lesson Select", corner_radius = 10, width = 20, height = 20, font = ("Segoe UI", 50, "bold"))
        self.lesson_title.place(relx=0.28, rely=0.04)

        self.lesson1 = customtkinter.CTkButton(master=self.frame_middle, text = "LESSON 1:\n A, B, C, D", font = ("Seoue UI", 22, "bold"), width = 150, height = 60, border_width = 3, corner_radius = 10, border_color="#000000")
        self.lesson1.grid(row=1, column=0, padx=30, pady=12)

        self.lesson2 = customtkinter.CTkButton(master=self.frame_middle, text = "LESSON 2:\n E, F, G, H", font = ("Seoue UI", 22, "bold"), width = 150, height = 60, border_width = 3, corner_radius = 10, border_color="#000000")
        self.lesson2.grid(row=1, column=1, padx=30, pady=12)

        self.lesson3 = customtkinter.CTkButton(master=self.frame_middle, text = "LESSON 3:\n I, K, L, M", font = ("Seoue UI", 22, "bold"), width = 150, height = 60, border_width = 3, corner_radius = 10, border_color="#000000")
        self.lesson3.grid(row=1, column=2, padx=30, pady=12)

        self.lesson4 = customtkinter.CTkButton(master=self.frame_middle, text = "LESSON 4:\n N, O, P, Q", font = ("Seoue UI", 22, "bold"), width = 150, height = 60, border_width = 3, corner_radius = 10, border_color="#000000")
        self.lesson4.grid(row=2, column=0, padx=30, pady=12)

        self.lesson5 = customtkinter.CTkButton(master=self.frame_middle, text = "LESSON 5:\n R, S, T, U", font = ("Seoue UI", 22, "bold"), width = 150, height = 60, border_width = 3, corner_radius = 10, border_color="#000000")
        self.lesson5.grid(row=2, column=1, padx=30, pady=12)

        self.lesson6 = customtkinter.CTkButton(master=self.frame_middle, text = "LESSON 6:\n V, W, X, Y", font = ("Seoue UI", 22, "bold"), width = 150, height = 60, border_width = 3, corner_radius = 10, border_color="#000000")
        self.lesson6.grid(row=2, column=2, padx=30, pady=12)

        self.lesson7 = customtkinter.CTkButton(master=self.frame_middle, text = "LESSON 7:\nJ & Z", font = ("Seoue UI", 22, "bold"), width = 150, height = 60, border_width = 3, corner_radius = 10, border_color="#000000")
        self.lesson7.grid(row=3, column=1, padx=30, pady=12)

        self.home_button = customtkinter.CTkButton(master=self, text = "Home", font = ("Seoue UI", 30, "bold"), width = 240, height = 60, border_width = 3, corner_radius = 10, border_color="#000000")
        self.home_button.place(relx = .33, rely = 0.8)


if __name__ == "__main__":
    app = App()
    app.start()