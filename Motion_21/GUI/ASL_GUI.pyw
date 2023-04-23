
import os
import threading
from tkinter.tix import COLUMN
import customtkinter
from queue           import Queue

from Utils.imports import *

from PIL             import Image, ImageTk
from config          import *
from ML.algorithm    import UserSign
from ML.usertrain    import UserTrain
from .camera_window  import CameraWindow
from .custom_tabview import CustomTabview

PATH = os.path.dirname(os.path.realpath(__file__))
main_cam_frame = []

dir_path = '%s\\ASL_Learning\\' %  os.environ['APPDATA'] 
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

#Can change this later for themes
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")
class AverageList:
    def __init__(self, letter = None):
        self.letter        = letter
        self.last_average  = 100
        self.count_limit   = 10
        self.current_count = 0
        self.let_list = [letter for i in range(100)]

    def reinit(self, letter):
        self.let_list = [letter for i in range(100)]
        for i in range(10): debug_log("REINITED")

    def add(self, value, override_count = 1):
        if value == None and self.current_count != self.count_limit:
            self.current_count += 1
            return

        for i in range(override_count):
            self.let_list.insert(0, value)
            del self.let_list[-1]

        current_count = 0
    
    def l_average(self):
        try:
            nones             = self.let_list.count(None)
            letters           = self.let_list.count(self.letter)

            self.average      = ( letters )
            self.last_average = self.average

            #print("Counted[{}]: {}".format(letters, self.average))
            return (letters)
        
        except Exection as e:
            print(e)
            return last_average

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Size of window and title
        self.geometry("740x520")
        self.title("ASL Learning App")

        # states and events
        state_init        = StateHandler()
        self.letter_state = LetterState('_')
        
        if USE_CAMERA: 
            self.event_handler = EventHandler() # init eventhandler
            self.bind('<Left>',  self.arrow_left)
            self.bind('<Right>', self.arrow_right)
            self.bind('<Up>',    self.arrow_up)
            self.bind('<Down>',  self.arrow_down)

        # helper attributes
        self.del_list            = []
        self.average_list        = AverageList()
        self.options_menu_open   = True
        self.curr_accuracy       = 100
        self.roi_size            = 50
        self.after_id            = ""
        self.cam_after_id        = ""
        self.motion_after_id     = ""
        self.motion_timer_count  = 0
        self.border_change       = 0 
        self.use_motion_afterinator  = False
        self.color_dict = { 0 : BorderColor.WHITE,
                            1 : BorderColor.RED,
                            2 : BorderColor.BLUE,
                            3 : BorderColor.GREEN,
                            4 : BorderColor.YELLOW,
                            5 : BorderColor.BLACK }

        # Locks size of window
        self.resizable(False, False)

        #Handy closing function to stop all running processes even when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.home_window()

    # Event Handler Stuff, was going to just pass a self instance to eventhandler but thats more messy than this is
    def arrow_left(self, _):
        if StateHandler().c_state == WindowState.IN_LESSON or StateHandler().c_state  == WindowState.IN_MOTION_LESSON:
            EventHandler().arrow_key_left(None)
            self.options_camera_x.configure(text="Cam X: {}".format(EventHandler().x+50))

    
    def arrow_right(self, _):
        if StateHandler().c_state == WindowState.IN_LESSON or StateHandler().c_state  == WindowState.IN_MOTION_LESSON:
            EventHandler().arrow_key_right(None)
            self.options_camera_x.configure(text="Cam X: {}".format(EventHandler().x+50))

    def arrow_up(self, _):
        if StateHandler().c_state == WindowState.IN_LESSON or StateHandler().c_state  == WindowState.IN_MOTION_LESSON:
            EventHandler().arrow_key_up(None)
            self.options_camera_y.configure(text="Cam Y: {}".format(EventHandler().y+50))

    def arrow_down(self, _):
        if StateHandler().c_state == WindowState.IN_LESSON or StateHandler().c_state  == WindowState.IN_MOTION_LESSON:
            EventHandler().arrow_key_down(None)
            self.options_camera_y.configure(text="Cam Y: {}".format(EventHandler().y+50))

    #Image processing function declarations
    # ------------------------------------------------------------------------------------    
    def load_image(self, path, image_size1, image_size2):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size1, image_size2)))


    # Button function declarations
    # ------------------------------------------------------------------------------------    
    
    def change_state(self, new_state : WindowState, dellist : list, motion_afterinator : bool = True, opts_menu : bool = True):
        if self.after_id:     self.after_cancel(self.after_id)
        if self.cam_after_id: self.after_cancel(self.cam_after_id)
        if self.motion_after_id: self.after_cancel(self.motion_after_id)
        self.use_motion_afterinator = motion_afterinator
        self.options_menu_open      = opts_menu
        self.del_list               = StateHandler().change_state(new_state, dellist)
        UserSign().reset_stage()

    # Button that recreates window with home page
    def home_button(self):
        # Destroyed old window

        if StateHandler().c_state == WindowState.HOME:
            return

        self.change_state(WindowState.HOME, self.del_list)

        self.frame_left.destroy()
        self.frame_right.destroy()

        self.home_window()

    # Button that allows user to change home page preferences
    def home_settings_button(self):
        print("testing home settings button")

    # Button that recreates window with users page
    def users_button(self):
        StateHandler().change_state(WindowState.SETTINGS, self.del_list)
        self.frame_right.destroy()
        btn_list = []

        len_users = len(Config().users)
        self.frame_right = customtkinter.CTkScrollableFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        for i in range(len_users):
            btn = customtkinter.CTkButton(master=self.frame_right, text=Config().users[i], text_color=THEME_OPP, corner_radius=6, width=200, fg_color=THEME, border_color=THEME, command = lambda l = i: self.testing(l+1))
            btn.grid(row = i, column = 0, padx = 150, pady = 20)
            btn_list.append(btn)

        self.del_list = btn_list
        
    def createU(self):
        self.frame_right.destroy()

        self.frame_user = customtkinter.CTkFrame(master=self)
        self.frame_user.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_user, width=200, height=60, font=("Segoe UI", 12), text="User Creator", text_color = THEME_OPP, corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.entry_1 = customtkinter.CTkEntry(master=self.frame_user, corner_radius=6, width=200, placeholder_text="username", text_color = THEME_OPP)
        self.entry_1.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_F = customtkinter.CTkButton(master=self.frame_user, text="Create", text_color = THEME_OPP, fg_color = THEME, border_color=THEME, corner_radius=6, width=200, command=self.buttonC)
        self.Button_F.grid(row= 3, column = 0, padx = 150, pady = 20)

        self.Button_E = customtkinter.CTkButton(master=self.frame_user, text="Back", text_color = THEME_OPP, fg_color = THEME, border_color=THEME, corner_radius=6, width=200, command=self.buttonBb)
        self.Button_E.grid(row= 4, column = 0, padx = 150, pady = 20)

    def buttonC(self):
        count = 0
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        if count >= 3:
            self.ewindow = customtkinter.CTkToplevel(self)
            self.ewindow.geometry("400x200")
            self.ewindow.title("Error: Too many users")

            self.label = customtkinter.CTkLabel(master=self.ewindow, width=200, height=60, fg_color=("gray70", "gray25"), text="Error: Too many users", text_color = THEME_OPP, corner_radius=6)
            self.label.place(relx=0.5, rely=0.22, anchor=tkinter.CENTER)

            self.Buttone = customtkinter.CTkButton(master=self.ewindow, text="Exit", text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command = self.cExit)
            self.Buttone.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
        else:
            UserName = self.entry_1.get()
            file_path = f'%s{UserName}' % dir_path
            f = open(file_path, 'x')
            f.close()
            self.users_button()

    def buttonBb(self):
        self.users_button()

    def cExit(self):
        self.ewindow.destroy()
        self.users_button()

    def deleteU(self):
        self.frame_right.destroy()
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Choose User to delete", text_color = THEME_OPP, corner_radius=6)
        self.label_1.grid(row= 0, column = 0, padx = 150, pady = 30)

        count = 0

        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1

        self.users = os.listdir(dir_path)
        if count == 3:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonud1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonud2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_3 = customtkinter.CTkButton(master=self.frame_right, text= self.users[2], text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonud3)
            self.Button_3.grid(row= 3, column = 0, padx = 150, pady = 20)

            self.Button_E = customtkinter.CTkButton(master=self.frame_right, text="Back", text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonBb)
            self.Button_E.grid(row= 4, column = 0, padx = 150, pady = 20)

        if count == 2:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonud1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_2 = customtkinter.CTkButton(master=self.frame_right, text= self.users[1], text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonud2)
            self.Button_2.grid(row= 2, column = 0, padx = 150, pady = 20)

            self.Button_E = customtkinter.CTkButton(master=self.frame_right, text="Back", text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonBb)
            self.Button_E.grid(row= 3, column = 0, padx = 150, pady = 20)

        if count == 1:

            self.Button_1 = customtkinter.CTkButton(master=self.frame_right, text= self.users[0], text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonud1)
            self.Button_1.grid(row= 1, column = 0, padx = 150, pady = 20)

            self.Button_E = customtkinter.CTkButton(master=self.frame_right, text="Back", text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonBb)
            self.Button_E.grid(row= 2, column = 0, padx = 150, pady = 20)

        if count == 0:
            self.users_button()

    def buttonud1(self):
        self.frame_right.destroy()

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Are you sure?", text_color = THEME_OPP, corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.Button_y = customtkinter.CTkButton(master=self.frame_right, text="Yes", text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.verifyDel1)
        self.Button_y.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_n = customtkinter.CTkButton(master=self.frame_right, text="No", text_color = THEME_OPP, corner_radius=6, width=200, fg_color = THEME, border_color=THEME, command=self.buttonBD)
        self.Button_n.grid(row= 3, column = 0, padx = 150, pady = 20)

    def buttonud2(self):
        self.frame_right.destroy()

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Are you sure?", text_color = THEME_OPP, corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.Button_y = customtkinter.CTkButton(master=self.frame_right, text="Yes", text_color = THEME_OPP, corner_radius=6, width=200, command=self.verifyDel2)
        self.Button_y.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_n = customtkinter.CTkButton(master=self.frame_right, text="No", text_color = THEME_OPP, corner_radius=6, width=200, command=self.buttonBD)
        self.Button_n.grid(row= 3, column = 0, padx = 150, pady = 20)

    def buttonud3(self):
        self.frame_right.destroy()

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, width=200, height=60, fg_color=("gray70", "gray25"), text="Are you sure?", text_color = THEME_OPP, corner_radius=6)
        self.label_1.grid(row= 1, column = 0, padx = 150, pady = 30)

        self.Button_y = customtkinter.CTkButton(master=self.frame_right, text="Yes", text_color = THEME_OPP, corner_radius=6, width=200, command=self.verifyDel3)
        self.Button_y.grid(row= 2, column = 0, padx = 150, pady = 20)

        self.Button_n = customtkinter.CTkButton(master=self.frame_right, text="No", text_color = THEME_OPP, corner_radius=6, width=200, command=self.buttonBD)
        self.Button_n.grid(row= 3, column = 0, padx = 150, pady = 20)

    def buttonBD(self):
        self.deleteU()

    def verifyDel1(self):
        users = os.listdir(dir_path)
        file_path = f'%s{users[0]}' % dir_path
        os.remove(file_path)
        self.users_button()

    def verifyDel2(self):
        users = os.listdir(dir_path)
        file_path = f'%s{users[1]}' % dir_path
        os.remove(file_path)
        self.users_button()

    def verifyDel3(self):
        users = os.listdir(dir_path)
        file_path = f'%s{users[2]}' % dir_path
        os.remove(file_path)
        self.users_button()

    # Button that recreates window with the theme page
    def themes_button(self):
        self.del_list = StateHandler().change_state(WindowState.SETTINGS, self.del_list)
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
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text = "Users:", text_color = THEME_OPP)
        self.label_1.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        # Default user settings button to reset all changes
        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Default User Settings", text_color = THEME_OPP, width = 200, height= 50, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.defaultUser)
        self.button1.grid(row=1, column=0, padx=1, pady=1)

        # Creates Return button
        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Return", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.return_function)
        self.button2.grid(row=9, column=0, padx=0, pady=350, sticky="we")

        # Creates the right side of the theme wind
        # ------------------------------------------------------------------------------------
        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius = 0)
        self.frame_right.grid(row=0, column=1, sticky="nswe")

        # Creates labels for the right window
        # ------------------------------------------------------------------------------------

        # Creates label with the text "Overall Theme Settings:" to describe what the drop down menu below it does
        self.label_2 = customtkinter.CTkLabel(master=self.frame_right, text="Overall Theme Settings:", text_color = THEME_OPP)
        self.label_2.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Creates theme drop down menu to change general theme details all at once
        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_right, values=["Dark", "Light"], text_color = THEME_OPP, fg_color = THEME, command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Creates label with the text "Font Size:" to describe what the slider below it does
        self.label_3 = customtkinter.CTkLabel(master=self.frame_right, text="Font Size:", text_color = THEME_OPP)
        self.label_3.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Creates font size progress bar to change font size of application
        self.progressbar = customtkinter.CTkProgressBar(master=self)

        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                                from_=0,
                                                to=1,
                                                number_of_steps=10,
                                                command=self.progressbar.set)
        self.slider_1.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="we")   

    # Button that recreates window with settings page
    def settings_button(self):
        global THEME
        self.del_list = StateHandler().change_state(WindowState.SETTINGS, self.del_list)

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
        #self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Home", text_color = THEME_OPP,  width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color = THEME, command=self.home_button)
        #self.button1.grid(row=0, column=0, padx=0, pady=0)
        #self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Home Settings", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.home_settings_button)
        #self.button2.grid(row=1, column=0, padx=0, pady=0)        
        self.button3 = customtkinter.CTkButton(master=self.frame_left, text = "Users", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", border_color=THEME, command=self.users_button)
        self.button3.grid(row=0, column=0, padx=0, pady=0)
        self.button4 = customtkinter.CTkButton(master=self.frame_left, text = "Themes", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", border_color=THEME, command=self.themes_button)
        self.button4.grid(row=1, column=0, padx=0, pady=0)
        self.button_logout = customtkinter.CTkButton(master=self.frame_left, text = "Logout", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", border_color=THEME, command=self.themes_button)
        self.button_logout.grid(row=2, column=0, padx=0, pady=0)
        #self.button6 = customtkinter.CTkButton(master=self.frame_left, text = "Notifications", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.notif_button)
        #self.button6.grid(row=3, column=0, padx=0, pady=0)
        #self.button7 = customtkinter.CTkButton(master=self.frame_left, text = "Configure Letter", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.configure_button)
        #self.button7.grid(row=6, column=0, padx=0, pady=0)
    
        # Creates Return button
        self.button8 = customtkinter.CTkButton(master=self.frame_left, text = "Return", text_color = THEME_OPP, width = 150, height = 60, border_width = 1, corner_radius = 5, border_color=THEME, command=self.return_function)
        self.button8.grid(row=8, column=0, padx=0, pady=0, sticky="we")

        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self, border_width= 3)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # Creates label with the text "Settings Page:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, text="Settings Page:", text_color = THEME_OPP, font=("Segoe UI", 20))
        self.label_1.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Creates label with the text describing button functionality
        #self.label_2 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Home: Takes you back to the home page\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        #self.label_2.grid(row=1, column=0, padx=0, pady=0, sticky="w")
        #self.label_3 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Home Settings: Customize your home page\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        #self.label_3.grid(row=2, column=0, padx=0, pady=0, sticky="w")
        self.label_4 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Users: Login to save your settings changes as well as lesson progression\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        self.label_4.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.label_5 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Themes: Change the theme and look of the application\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        self.label_5.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.label_logout = customtkinter.CTkLabel(master=self.frame_right, text="\n   Logout: Logout to leave current account or switch users\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        self.label_logout.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        #self.label_6 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Volume: Change the audio volume of the application\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        #self.label_6.grid(row=5, column=0, padx=0, pady=0, sticky="w")
        #self.label_7 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Notifications: Change notification options for the application\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        #self.label_7.grid(row=6, column=0, padx=0, pady=0, sticky="w")

    # Button that allows the user to change notification options
    def notif_button(self):
        print("testing notification button")

    def logout_button(self):
        print("Logout button")

    # Button that destroys window and exits program
    def exit_button(self):
        self.destroy()

    def lesson_select(self):
        self.change_state(WindowState.LESSONS, self.del_list)

        static_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]
        movement_letters = ["J", "Z"]

        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        # buttons
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", text_color = THEME_OPP, width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")
        

        # lessons
        self.lesson1 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 1:\n A, B, C, D", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(static_letters[0:4], 1))
        self.lesson1.grid(row = 0, column = 4, padx = 2, pady = 2)
        
        self.lesson2 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 2:\n E, F, G, H", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(static_letters[4:8], 2))
        self.lesson2.grid(row = 0, column = 5, padx = 2, pady = 2)

        self.lesson3 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 3:\n I, K, L, M", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(static_letters[8:12], 3))
        self.lesson3.grid(row = 1, column = 4, padx = 2, pady = 2)
        
        self.lesson4 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 4:\n N, O, P, Q", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(static_letters[12:16], 4))
        self.lesson4.grid(row = 1, column = 5, padx = 2, pady = 2)
        
        self.lesson5 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 5:\n R, S, T, U", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(static_letters[16:20], 5))
        self.lesson5.grid(row = 2, column = 4, padx = 2, pady = 2)

        self.lesson6 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 6:\n V, W, X, Y", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(static_letters[20:24], 6))
        self.lesson6.grid(row = 2, column = 5, padx = 2, pady = 2)
        
        self.lesson7 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 7:\n J & Z", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"),  width = 200, height = 100, border_width = 2, corner_radius = 8, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_motion(movement_letters[0:2], 7))
        self.lesson7.grid(row = 3, column = 4, padx = 2, pady = 2)
        
    def lesson_letters_static(self, letters, lesson_number):
        self.change_state(WindowState.LESSONS, self.del_list, False, True)

        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        # buttons *
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", text_color = THEME_OPP, width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", text_color = THEME_OPP, width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        # description label
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = f"Lesson {lesson_number}: \nLetters {letters[0]}, {letters[1]}, {letters[2]}, and {letters[3]}\n\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language", text_color = THEME_OPP, font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")


        # letters A - D letters to select on screen
        self.A_image = self.load_image(f"/images/letters/{letters[0].lower()}.JPG", 150, 150) 
        self.buttonA = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.A_image, width = 200, height = 200, border_width = 2, corner_radius = 20, compound = "top", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters, 0, lesson_number))
        self.buttonA.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "nswe")

        self.B_image = self.load_image(f"/images/letters/{letters[1].lower()}.JPG", 150, 150)
        self.buttonB = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.B_image, width = 200, height = 200, border_width = 2, corner_radius = 20, compound = "top", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters, 1, lesson_number))
        self.buttonB.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "nswe")

        self.C_image = self.load_image(f"/images/letters/{letters[2].lower()}.JPG", 150, 150)
        self.buttonC = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.C_image, width = 200, height = 200, border_width = 2, corner_radius = 20, compound = "top", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters, 2, lesson_number))
        self.buttonC.grid(row = 2, column = 1, padx = 20, pady = 15, sticky = "nswe")

        self.D_image = self.load_image(f"/images/letters/{letters[3].lower()}.JPG", 150, 150)
        self.buttonD = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.D_image, width = 200, height = 200, border_width = 2, corner_radius = 20, compound = "top", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters, 3, lesson_number))
        self.buttonD.grid(row = 2, column = 2, padx = 20, pady = 15, sticky = "nswe")
        self.use_motion_afterinator = False

    def lesson_letters_motion(self, letters, lesson_number):
        self.change_state(WindowState.MOTION, self.del_list, True, True)
        self.frame_left.destroy()
        self.frame_right.destroy()

        # left and right frame for window
        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)

        #buttons 
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Home", text_color = THEME_OPP, width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", text_color = THEME_OPP, width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.lesson_home.grid(row = 9,  column = 0, padx = 0, pady = 0, sticky = "s")

        # description labels
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = f"Lesson {lesson_number}: \nLetters {letters[0]} and {letters[1]}\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language\n\n Begin learning the\n idea of hand\n movement", text_color = THEME_OPP, font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")
        
        # letters J and Z, which require a special case of teaching
        self.J_image = self.load_image(f"/images/letters/{letters[0].lower()}.JPG", 150, 150)
        self.buttonJ = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.J_image, width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters, 0, lesson_number, True))
        self.buttonJ.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "we")

        self.Z_image = self.load_image(f"/images/letters/{letters[1].lower()}.JPG", 150, 150) 
        self.buttonZ = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.Z_image, width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters, 1, lesson_number, True))
        self.buttonZ.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "we")

        self.use_motion_afterinator = True

    def callback_test(self):
        print("Dripp!")
    # later we can alter this function to be just for "lesson 1" "lesson 2" and so on
    # for now it just has the entire alphabet, but later will call to each function for better organization
    def letter_lessons(self, letter, index, lesson_number, motion: bool = False):
        self.frame_main_right.destroy()
        self.frame_main_left.destroy()

        self.frame_main_left = customtkinter.CTkFrame(master = self, width = 200, height = 20, corner_radius = 0)
        self.frame_main_left.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_main_left.grid_rowconfigure(0, minsize=10)   
        self.frame_main_left.grid_rowconfigure(4, minsize=100)   
        self.frame_main_left.grid_rowconfigure(7, weight=1)      
        self.frame_main_left.grid_rowconfigure(9, minsize=0)

        if motion == True:
            self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = f"Lesson {lesson_number}: \nLetter {letter[index]}\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language\n\n Begin learning the\n idea of hand\n movement", text_color = THEME_OPP, font = ("Segoue UI", 12))
            self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        if motion == False:
            self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = f"Lesson {lesson_number}: \nLetter {letter[index]}\n\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language", text_color = THEME_OPP, font = ("Segoue UI", 12))
            self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        self.back_to_lesson = customtkinter.CTkButton(master=self.frame_main_left, text = "Lesson Select", text_color = THEME_OPP, width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.back_to_lesson.grid(row = 9, column = 0, padx = 0, pady = 0, sticky = "s")

        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, text = "Back", text_color = THEME_OPP, width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.back_button_lessons)
        self.lesson_home.grid(row = 9, column = 0, padx = 0, pady = 0, sticky = "s")
        
        self.frame_main_right = customtkinter.CTkFrame(master = self)
        self.frame_main_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_main_right.grid_rowconfigure(0, minsize=10)   
        self.frame_main_right.grid_rowconfigure(4, minsize=100)   
        self.frame_main_right.grid_rowconfigure(7, weight=1)      
        self.frame_main_right.grid_rowconfigure(9, minsize=0)
        
        self.tabview = CustomTabview(master=self.frame_main_left, width=25, height=100, command = self.options_button)
        self.tabview.grid(row=4, column=0, padx=(5, 0), pady=(50, 0), sticky="nsew")
        self.tabview.add("Options")
        self.options_frame = customtkinter.CTkFrame(master=self.frame_main_right, width = 10, height = 10) # remove warning
        
        self.options_camera_x    = customtkinter.CTkLabel(master = self.tabview.tab("Options"), text="Cam X: {}".format(EventHandler().x))
        self.options_camera_y    = customtkinter.CTkLabel(master = self.tabview.tab("Options"), text="Cam Y: {}".format(EventHandler().y))
        self.options_border_size = customtkinter.CTkLabel(master = self.tabview.tab("Options"), text="Box Size: {}".format(self.roi_size))

        self.options_camera_x.grid   (row=0, padx=(10,5), pady=(3,5), sticky="nsew")

        self.options_camera_y.grid   (row=1, padx=(10,5), pady=(5,5), sticky="nsew")

        self.options_border_size.grid(row=2, padx=(10,5), pady=(5,5), sticky="nsew")

        '''
        we can change these into lessons and call to lesssons "A-D" functions and etc and just call the function here
        add next and retry functionalities
        '''
        # This opens up the camera view for every sinlge letter, as the user chooses it
    
        self.label6 = customtkinter.CTkLabel(master=self.frame_main_right, text = "No Camera Found", text_color = THEME_OPP, width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
        self.label6.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        if USE_CAMERA:
            self.label_cam = CameraWindow(master=self.frame_main_right, width = 420, height = 320, text = "", compound = "bottom")
        else:
            self.label_cam = customtkinter.CTkLabel(master=self.frame_main_right, text = "[Debug] camera off", width = 420, height = 320, corner_radius = 8, compound = "bottom", fg_color=("white", "gray38"))
        self.label_cam.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        # Label that describes the main camera above
        self.label7 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Main Camera", text_color = THEME_OPP)
        self.label7.grid(row=1, column=0, sticky="n", padx=10, pady=0)        

        # Creates instruction window for the application to communicate with the user
        self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = f"Please sign the letter \"{letter[index]}\" \nas provided in the example!", text_color = THEME_OPP, font=("Segoe UI", 20), width = 350, height = 100, fg_color=THEME, corner_radius = 8, compound = "bottom")
        self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)

        # Load the image from the /image/letters folder to use for this part and position it in the correct place
        # Place Imaage of example sign for user to use when signing in the main lesson window 
        self.A_image = self.load_image(f"/images/letters/{letter[index].lower()}.JPG", 150, 150)
        #if not btns:
        self.A_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.A_image, width = 150, height = 150)
        #else:
            #self.A_labelimage = customtkinter.CTkButton(master=self.frame_main_right, text = "", image = self.A_image, width = 150, height = 150, command=lambda x=0 : print("YEAH!"))
        self.A_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)

        # Label that describes the example camera above
        self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Image", text_color = THEME_OPP)
        self.label10.grid(row=0, column=1, padx=0, pady=0) 

        # Window for the user hand camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output

        if USE_CAMERA:
            self.label_cam2 = CameraWindow(master=self.frame_main_right, width = 150, height = 150, text = "", cropped = True, compound = "bottom")
        else:
            self.label_cam2 = customtkinter.CTkLabel(master=self.frame_main_right, text = "[Debug] camera off", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        self.label_cam2.grid(row=0, column=1, sticky="s", padx=0, pady=10)

        # Label that describes the user's accuracy (Keep for now but move later)
        self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: {}%".format(self.curr_accuracy), text_color = THEME_OPP, font=("Segoe UI", 14))
        #self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 


        #Lesson next and previous (fix combining if statements later)

        if (index < 3 and motion == False) or (index < 1 and motion == True):
            self.next_button = customtkinter.CTkButton(master=self.frame_main_right, text = f"Next lesson: {letter[index+1]}", command = lambda : self.letter_lessons(letter, index+1, lesson_number, motion))
            self.next_button.grid(row=3, column = 1, sticky="n", padx=5, pady=10)

        if (index > 0 and motion == False) or (index > 0 and motion == True):
            self.previous_button = customtkinter.CTkButton(master=self.frame_main_right, text = f"Previous lesson: {letter[index-1]}", command = lambda : self.letter_lessons(letter, index-1, lesson_number, motion))
            self.previous_button.grid(row=3, column = 1, sticky="s", padx=0, pady=10)

        if not motion: self.change_state(WindowState.IN_LESSON, self.del_list)
        else:          self.change_state(WindowState.IN_MOTION_LESSON, self.del_list)
        self.average_list.reinit(letter[index])
        self.letter_state.set_letter(letter[index])
        
        self.tabview._segmented_button_callback("Options")
        self.update()

        self.border_change = 0
        if motion: self.motion_afterinator()
        self.camera_aftinerator()
        self.the_afterinator()

    def options_submit(self):
        self.options_menu_open = False
        try:
            self.roi_size = int(self.opts_roi_box.get())

            if self.roi_size > 330: self.roi_size = 330
            if self.roi_size < 50:   self.roi_rize = 50

            self.options_border_size.configure(text = "Box Size: {}".format(self.roi_size))
            EventHandler().set_boundary_range(self.roi_size)

            #for i in range(10): 
            Camera().box_size_q.put(self.roi_size) # I really wanna make sure it gets it since its called only once

        except:
            pass # for now, maybe change the box to red

        try:
            self.options_frame.destroy()
        except:
            pass

    def options_button(self):
        if self.options_menu_open == True:
            self.options_menu_open = False # not proper state usage but im not adding a third clause for a bool rn

            try:
                self.options_frame.destroy() 
            except:
                pass

        else:
            self.options_frame = customtkinter.CTkFrame(master=self.frame_main_right, width = 180, height = 180)
            self.options_frame.place(relx=.5, rely=.5, anchor="center")

            self.opts_roi_label = customtkinter.CTkLabel(master=self.options_frame, text = "Rectange Size: ", text_color = THEME_OPP, font=("Segoe UI", 14))
            self.opts_roi_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="ew")

            self.opts_roi_box = customtkinter.CTkEntry(master=self.options_frame, width=50, height=20, placeholder_text=self.roi_size)
            self.opts_roi_box.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="ew")

            self.opts_submit = customtkinter.CTkButton(master=self.options_frame, text = "Ok!", text_color = THEME_OPP, height = 42, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.options_submit)
            self.opts_submit.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), columnspan = 2)
            self.options_menu_open = True

    def back_button_lessons(self):
        self.change_state(WindowState.HOME, self.del_list)
        self.lesson_select()

    # Button that opens lesson select page
    def lesson_select_button(self, choice):
        print(f"testing lesson select button {choice}")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

    # Miscellaneous function declarations
    # ------------------------------------------------------------------------------------    
    # Defines changing appearance mode
    def change_appearance_mode(self, new_appearance_mode):
        global THEME 
        global THEME_OPP
        
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark":
            THEME     = "#101010"
            THEME_OPP = "#FFFFFF"
            print("Dark")
        elif new_appearance_mode == "Light":
            THEME     = "#FFFFFF"
            THEME_OPP = "#101010"
            print("Light")
        self.themes_button()
        
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
        # Configures grid layout of 2x1
        self.change_state(WindowState.HOME, self.del_list)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creates left sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (9x1)
        self.frame_left.grid_rowconfigure(0, minsize=10)    # sets minimum size from top of screen to text
        self.frame_left.grid_rowconfigure(4, minsize=100)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(7, weight=1)      # empty row as spacing
        self.frame_left.grid_rowconfigure(9, minsize=0)     # sets minimum size from bottom of screen to buttons

        
        self.frame_right = customtkinter.CTkFrame(master = self)
        self.frame_right.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")

        self.frame_right.grid_rowconfigure(0, minsize=10)   
        self.frame_right.grid_rowconfigure(4, minsize=100)   
        self.frame_right.grid_rowconfigure(7, weight=1)      
        self.frame_right.grid_rowconfigure(9, minsize=0)

        #Images for left side of window
        self.home_image = self.load_image("/images/home.png", 25, 25)
        self.home_example_image = self.load_image("/images/HomeExample.png", 700, 635)
        
        self.settings_image = self.load_image("/images/settings.png", 25, 25)
        self.exit_image = self.load_image("/images/exit.png", 25, 25)
        
        self.button3 = customtkinter.CTkButton(master=self.frame_left, image = self.home_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.button3.grid(row=8, column=0, padx=0, pady=0, sticky="sw")
        
        self.button4 = customtkinter.CTkButton(master=self.frame_left, image = self.settings_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.settings_button)
        self.button4.grid(row=8, column=1, padx=0, pady=0, sticky="s")
        
        self.button5 = customtkinter.CTkButton(master=self.frame_left, image = self.exit_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.exit_button)
        self.button5.grid(row=8, column=2, padx=0, pady=0, sticky="se")
        
        # Creates right sub-window
        # ------------------------------------------------------------------------------------   

        # Create a Label on the right of our Application Title
        self.motion21_title = customtkinter.CTkLabel(master=self.frame_right, text = "MOTION 21", text_color = THEME_OPP, width = 20, height = 20, font = ("Segoe UI", 100, "bold"), fg_color=("white","grey38"))
        self.motion21_title.grid(row=0, column=0, padx=0, pady=0, sticky = "we")

        # Creates continue from previous section button
        self.button1 = customtkinter.CTkButton(master=self.frame_right, text = "Lesson Select", text_color = THEME_OPP, font = ("Seoue UI", 50, "bold"), width = 200, height = 50, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.lesson_select)
        self.button1.grid(row=1, column=0, padx=0, pady=5, sticky="we")


        self.motion21_title = customtkinter.CTkLabel(master=self.frame_right, text = "Motion 21 is an American Sign Language Learning Application,\n using computer vision and machine learning to provide\n the user with live feedback on what gesture or character\n they are holding up on screen.", text_color = THEME_OPP, width = 20, height = 150, font = ("Segoe UI", 20), fg_color=("white", "gray20"))
        self.motion21_title.grid(row=2, column=0, padx=0, pady=50, sticky = "we")
    
    def the_afterinator(self): # I can and will default to doofenshmirtz like naming conventions.
        # todo: change the afterinator to have more of a list of functions to execute or something instead of ifs statements.
        if (StateHandler().c_state.value[1] == CameraState.CAM_CONTINOUS or StateHandler().c_state.value[1] == CameraState.CAM_REQUIRED) and USE_CAMERA == 1: # find a better method of doing this later
            if self.border_change == 1: # seb and keith pair programming line
                self.label_cam.cw_update()
                self.after_id = self.after(10, self.the_afterinator)
            else:
                self.label_cam.cw_update();
                self.label_cam2.cw_update();
                self.after_id = self.after(10, self.the_afterinator)

    def camera_aftinerator(self):
        if (StateHandler().c_state == WindowState.IN_LESSON or StateHandler().c_state == WindowState.IN_MOTION_LESSON) and USE_CAMERA == 1:


            let = UserSign().run_comparison(self.letter_state.DESIRED_LETTER[0])

            if let == None: 
                self.cam_after_id = self.after(210, self.camera_aftinerator)
                return

            if let == self.letter_state.DESIRED_LETTER[0]:
                #self.del_list = StateHandler().change_state(WindowState.LESSONS, self.del_list)
                self.border_change = 1

                self.label8.configure(text="Congrats! You have succesfully signed\n the letter: {}".format(self.letter_state.DESIRED_LETTER[0]))
                #self.label8.update()
                #self.after_cancel(self.after_id)
                #self.after_cancel(self.cam_after_id)
                return

            try:
                if(let == None):
                    self.average_list.add(self.average_list.letter, 1)
                else:
                    self.average_list.add(let, 5)

                self.curr_accuracy = int(self.average_list.l_average())

                self.label12.configure(text = "Total Accuracy: {}%".format(self.curr_accuracy))
                #self.label12.update()
            except Exception as e: 
                print(e)

            self.cam_after_id = self.after(200, self.camera_aftinerator)

    def motion_afterinator(self): # realistically, could throw this in the regular afterinator but its easier to read
        if StateHandler().c_state == WindowState.IN_MOTION_LESSON and USE_CAMERA == 1:

            if (self.motion_timer_count <= 3):
                self.motion_timer_count += 1
            else:
                self.motion_timer_count = 0

            #print("================================ Based! ================================")

            color_made = make_color(self.color_dict[self.motion_timer_count])
            Camera().border_q.put(color_made)
            #self.motion_after_id = self.after(1000, self.motion_afterinator)
            self.motion_after_id = self.after(1000, self.motion_afterinator)

if __name__ == "__main__":
    app = App()
    app.start()