import customtkinter
from   enum import Enum
from   PIL import Image, ImageTk
from   Utils.camera import Camera


class WindowState(Enum):
    HOME = 1
    SETTINGS = 2
    THEMES = 3

class CameraWindow(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.camera_window      = customtkinter.CTkLabel(master = self);
        self.camera_window_crop = customtkinter.CTkLabel(master = self);
        self.camera_window.grid(row=1, column=0, padx=0, pady=0, sticky="w")
        self.cw_update();

    def cw_update(self):
        img         = Image.fromarray(Camera().rgb_img_rect)
        imgtk       = ImageTk.PhotoImage(image = img)
        self.camera_window.imgtk = imgtk
        self.camera_window.configure(image=imgtk)

    def pause(self):
        Camera().stop = True

    def resume(self):
        Camera().begin()

    def __del__(self):
        Camera().stop = True