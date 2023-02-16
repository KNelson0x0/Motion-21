import customtkinter
from   PIL import Image, ImageTk
from   Utils.camera import Camera



class CameraWindow(customtkinter.CTkLabel):
    def __init__(self, *args, width=None, height=None, cropped = False, **kwargs):
        self.width = width
        self.height = height
        self.cropped = cropped

        if width == None and height == None: super().__init__(*args, **kwargs)
        else:                                super().__init__(*args, width=self.width, height=self.height, **kwargs)
        
        self.cw_update();

    def cw_update(self):
        img         = Image.fromarray(Camera().rgb_img_rect if not self.cropped else Camera().rgb_img_crop)

        if self.width != None and self.height != None:
            img = img.resize((self.width, self.height))

        imgtk       = ImageTk.PhotoImage(image = img)

        self.imgtk = imgtk
        self.configure(image=imgtk)

    def pause(self):
        Camera().stop = True

    def resume(self):
        Camera().begin()

    def __del__(self):
        Camera().stop = True