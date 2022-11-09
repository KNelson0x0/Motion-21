from cvzone.HandTrackingModule import HandDetector
from PIL import Image, ImageTk
from constants import *
from utils import *

import customtkinter as CT
import tkinter as TK
import scroll_panel
import cv2 
import os

PATH = os.path.dirname(os.path.realpath(__file__))

#Can changXthis later for themes
CT.set_appearance_mode("System")
CT.set_default_color_theme("dark-blue")
detector = HandDetector(maxHands = 1)
button_modal_x = 0
button_modal_y = 0

class App(CT.CTk):

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

        print('Inited')
        #Size of window and title
        self.geometry("780x520")
        self.title("ASL Learning App")

        #Handy closing function to stop all running processes even when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Left side sub-window
        self.frame_left = CT.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
        
        #Button mapping and functionality
        self.button1 = CT.CTkButton(master=self.frame_left,  text = "Home", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.button1_function)
        self.button1.grid(row=0, column=0, padx=20, pady=20)
        self.button2 = CT.CTkButton(master=self.frame_left,  text = "Users", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.button2_function)
        self.button2.grid(row=1, column=0, padx=20, pady=20)
        self.button3 = CT.CTkButton(master=self.frame_left,  text = "Themes", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.button3_function)
        self.button3.grid(row=2, column=0, padx=20, pady=20)
        self.button4 = CT.CTkButton(master=self.frame_left,  text = "Settings", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.button4_function)
        self.button4.grid(row=3, column=0, padx=20, pady=20)
        self.button5 = CT.CTkButton(master=self.frame_left,  text = "Exit", width = 130, height = 60, border_width = 2, corner_radius = 10, compound = "bottom", border_color="#000000", command=self.button5_function)
        self.button5.grid(row=4, column=0, padx=20, pady=20)

        #Middle sub-window
        self.frame_middle = CT.CTkFrame(master=self)
        self.frame_middle.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.label = TK.Label(self.frame_middle)
        self.label.grid(row=0,column=0, sticky = 'nsew')
        

        #Right side sub-window (May not need)
        self.frame_right = scroll_panel.ScrollPanel(master=self, width=180, corner_radius=0)
        self.frame_right.grid(row=0, column=2, sticky="nswe")

        self.update()
        self.show_frames()
    
    def show_frames(self):
        success, img = self.cap.read()
        hands, img_orig = detector.findHands(img)

        cv2image = cv2.cvtColor(img_orig,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)

        imgtk = ImageTk.PhotoImage(image = img.resize((self.frame_middle.winfo_width() - 69, self.frame_middle.winfo_height() - 69)))
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.after(2, self.show_frames)

    #Button functions
    def button1_function(self):
        global button_modal_x, button_modal_y
        new_button = CT.CTkButton(master=self.frame_right,  \
                                 text = "Down in ohio", width = 130, height = 60, \
                                 border_width = 2, corner_radius = 10, \
                                 compound = "bottom", border_color="#000000")

        new_button.grid(row=button_modal_x, column=button_modal_y, padx=20,pady=20)
        button_modal_x += 1
        print("Testing home")

    def button2_function(self):
        el = find_element(self.frame_right,'Down in ohio')
        if el != None:
            self.frame_right.as_destroy(el)

        print("Testing user")

    def button3_function(self):
        print("Testing themes")

    def button4_function(self):
        print("Testing settings")

    def button5_function(self):
        self.destroy()

    def animation_handler(self):
        self.frame_right.animate()
        app.after(10, app.animation_handler)

    #Image processing
    def load_image(self, path, image_size):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.after(10, app.animation_handler)
    app.start()


