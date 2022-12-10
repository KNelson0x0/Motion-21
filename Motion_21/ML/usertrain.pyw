
import cv2
import customtkinter
import time
from   os.path  import exists
from   os       import mkdir
from   os       import remove
from   Utils.utils import *
from   Utils.camera import Camera
from   Utils.constants import DEBUG



class UserTrain:
    def __init__(self, username, symbol, main_window = None):
        self.user_path = "./UserData/{}/"
        self.user_name = username
        self.symbol = symbol
        self.main_window = main_window


        if self.main_window == None:
            self.main_window = customtkinter.CTk;
        if not exists("./UserData/{}/{}".format(self.user_name, symbol)):
            mkdir("./UserData/{}/{}".format(self.user_name, symbol))
        if not exists(self.user_path):
            open(self.user_path,'w').close()


    def open_window(self):
        train_window = customtkinter.CTkToplevel(self.main_window);
        train_window.title("Train Window: {}".format(self.symbol))
        train_window.geometry("200x400")
        train_window.grid_columnconfigure(1, weight=1)
        train_window.grid_rowconfigure(0, weight=1)
        train_window.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        train_window.frame_left.grid(row=0, column=0, sticky="nswe")

        frame_right = customtkinter.CTkFrame(master=self.main_window)
        frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
