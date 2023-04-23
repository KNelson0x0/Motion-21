import os
import customtkinter
import cv2
import uuid
import time
from queue           import Queue
from PIL             import Image, ImageTk
from config          import *
from Utils.utils     import *
from Utils.constants import *
from Utils.camera    import *
from Utils.states    import *
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

            print("Counted[{}]: {}".format(letters, self.average))
            return (letters)
        
        except Exection as e:
            print(e)
            return last_average

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # states and events
        state_init        = StateHandler()
        self.letter_state = LetterState('_')

        if USE_CAMERA: 
            self.event_handler = EventHandler() # init eventhandler
            self.bind('<Left>',  EventHandler().arrow_key_left)
            self.bind('<Right>', EventHandler().arrow_key_right)
            self.bind('<Up>',    EventHandler().arrow_key_up)
            self.bind('<Down>',  EventHandler().arrow_key_down)

        #Size of window and title
        self.geometry("740x520")
        state_init = StateHandler()
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

    #Image processing function declarations
    # ------------------------------------------------------------------------------------    
    def load_image(self, path, image_size1, image_size2):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size1, image_size2)))


    # Button function declarations
    # ------------------------------------------------------------------------------------    
    
    # Button that recreates window with home page
    def home_button(self):
        # Destroyed old window
        #if StateHandler().c_state == WindowState.HOME:
        #    return

        StateHandler().change_state(WindowState.HOME, self.del_list)
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
    
    # Model Training front end, configuring letter (pulled from old and converting and dynamifying)
    def configure_button(self): 
        global THEME
        global THEME_OPP

        self.del_list = StateHandler().change_state(WindowState.SETTINGS, self.del_list)
        if self.after_id:     self.after_cancel(self.after_id)
        if self.cam_after_id: self.after_cancel(self.cam_after_id)

        self.usertrain_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        #trainlist_length = len(self.usertrain_letters)
        
        # Destroyed old window
        self.frame_left.destroy()
        self.frame_right.destroy()

        # Creates left sub-window
        # ------------------------------------------------------------------------------------
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0, fg_color = THEME)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (1x8)
        self.frame_left.grid_rowconfigure(2, minsize=150)      # empty row as spacing
        self.frame_left.grid_rowconfigure(4, minsize=150)      # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=0)     # sets minimum size from bottom of screen to buttons

        # Creates label with the text "Configure Motion 21"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Configure Motion 21:", text_color = THEME_OPP, font=("Segoe UI", 14))
        self.label_1.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # Creates label with the description of the configure button menu
        self.label_3 = customtkinter.CTkLabel(master=self.frame_left, text="Is Motion 21 having trouble\n recognizing your signs?\n Reconfigure it to fit you \ninstead! Please click any of the\n letters from A to Z on the right \n and we will train our model\n based on your examples!\n", text_color = THEME_OPP, font=("Segoe UI", 11))
        self.label_3.grid(row=3, column=0, padx=1, pady=5, sticky="nswe")

        # Creates Return button
        self.button7 = customtkinter.CTkButton(master=self.frame_left, text = "Return", text_color = THEME_OPP, width = 150, height = 60, border_width = 1, corner_radius = 5, fg_color = THEME, border_color=THEME, command=self.return_function)
        self.button7.grid(row=7, column=0, padx=0, pady=10, sticky="we")

        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self, fg_color = THEME)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # configure grid layout (8x9)
        self.frame_right.grid_rowconfigure(1, minsize=50)      # empty row as spacing
        self.frame_right.grid_rowconfigure(8, minsize=0)       # sets minimum size from bottom of screen to buttons
        self.frame_right.grid_columnconfigure(0, minsize=25)   # empty column as spacing

        # Creates label with the text "Settings Page:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, text="Select a Letter to Change:", text_color = THEME_OPP, font=("Segoe UI", 20))
        self.label_1.grid(row=0, column=0, columnspan=5, padx=0, pady=0, sticky="we")
        
        # attempting to make this dynamic, having issues
        '''
        for i in range(trainlist_length):
            if self.usertrain_letters[0:6]:
                letter_button = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[i], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color = THEME, command = self.config_letter(self.usertrain_letters[0:6]))
                #print(self.usertrain_letters[0:6])
                letter_button.grid(row = 2, column = i, padx = 15, pady = 10)
            
            if self.usertrain_letters[6:12]:
                print(self.usertrain_letters[6:12])
                letter_button.grid(row = 3, column = 1, columnspan = 6, padx = 15, pady = 10)
            if self.usertrain_letters[12:18]:
                print(self.usertrain_letters[12:18])
                letter_button.grid(row = 4, column = 1, columnspan = 6, padx = 15, pady = 10)
            if self.usertrain_letters[18:24]:
                print(self.usertrain_letters[18:24])                
                letter_button.grid(row = 5, column = 1, columnspan = 6, padx = 15, pady = 10)
            
            
            self.usertrain_letters.append(letter_button)    
        self.del_list = self.usertrain_letters
        '''

        self.buttonA = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[0], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[0]))
        self.buttonA.grid(row=2, column=1,padx=15, pady=10, sticky="w")
        self.buttonB = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[1], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[1]))
        self.buttonB.grid(row=2, column=2, padx=15, pady=10, sticky="w")
        self.buttonC = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[2], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[2]))
        self.buttonC.grid(row=2, column=3, padx=15, pady=10, sticky="w")
        self.buttonD = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[3], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[3]))
        self.buttonD.grid(row=2, column=4, padx=15, pady=10, sticky="w")
        self.buttonE = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[4], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[4]))
        self.buttonE.grid(row=2, column=5, padx=15, pady=10, sticky="w")
        self.buttonF = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[5], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[5]))
        self.buttonF.grid(row=2, column=6, padx=15, pady=10, sticky="w")
        self.buttonG = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[6], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[6]))
        self.buttonG.grid(row=3, column=1, padx=15, pady=10, sticky="w")
        self.buttonH = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[7], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[7]))
        self.buttonH.grid(row=3, column=2, padx=15, pady=10, sticky="w")
        self.buttonI = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[8], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[8]))
        self.buttonI.grid(row=3, column=3, padx=15, pady=10, sticky="w")
        self.buttonJ = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[9], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[9]))
        self.buttonJ.grid(row=3, column=4, padx=15, pady=10, sticky="w")
        self.buttonK = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[10], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[10]))
        self.buttonK.grid(row=3, column=5, padx=15, pady=10, sticky="w")
        self.buttonL = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[11], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[11]))
        self.buttonL.grid(row=3, column=6, padx=15, pady=10, sticky="w")
        self.buttonM = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[12], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[12]))
        self.buttonM.grid(row=4, column=1, padx=15, pady=10, sticky="w")
        self.buttonN = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[13], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[13]))
        self.buttonN.grid(row=4, column=2, padx=15, pady=10, sticky="w")
        self.buttonO = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[14], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[14]))
        self.buttonO.grid(row=4, column=3, padx=15, pady=10, sticky="w")
        self.buttonP = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[15], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[15]))
        self.buttonP.grid(row=4, column=4, padx=15, pady=10, sticky="w")
        self.buttonQ = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[16], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[16]))
        self.buttonQ.grid(row=4, column=5, padx=15, pady=10, sticky="w")
        self.buttonR = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[17], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[17]))
        self.buttonR.grid(row=4, column=6, padx=15, pady=10, sticky="w")
        self.buttonS = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[18], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[18]))
        self.buttonS.grid(row=5, column=1, padx=15, pady=10, sticky="w")
        self.buttonT = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[19], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[19]))
        self.buttonT.grid(row=5, column=2, padx=15, pady=10, sticky="w")
        self.buttonU = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[20], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[20]))
        self.buttonU.grid(row=5, column=3, padx=15, pady=10, sticky="w")
        self.buttonV = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[21], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[21]))
        self.buttonV.grid(row=5, column=4, padx=15, pady=10, sticky="w")
        self.buttonW = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[22], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[22]))
        self.buttonW.grid(row=5, column=5, padx=15, pady=10, sticky="w")
        self.buttonX = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[23], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[23]))
        self.buttonX.grid(row=5, column=6, padx=15, pady=10, sticky="w")
        self.buttonY = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[24], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[24]))
        self.buttonY.grid(row=6, column=3, padx=15, pady=10, sticky="w")
        self.buttonZ = customtkinter.CTkButton(master=self.frame_right, text = self.usertrain_letters[25], text_color = THEME_OPP, width = 55, height = 55, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=lambda:self.config_letter(self.usertrain_letters[25]))
        self.buttonZ.grid(row=6, column=4, padx=15, pady=10, sticky="w")

    def config_letter(self, letter):
        self.del_list = StateHandler().change_state(WindowState.TRAINING, self.del_list) # Change to TRAINING state
        # Destroyed old window
        self.frame_left.destroy()
        self.frame_right.destroy()

        # Configures grid layout of 2x1
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creates left sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (9x1)
        self.frame_left.grid_rowconfigure(0, minsize=10)    # sets minimum size from top of screen to text
        self.frame_left.grid_rowconfigure(2, weight=1)      # creates empty row with weight 1
        self.frame_left.grid_rowconfigure(4, weight=0)      # creates empty row with weight 0
        self.frame_left.grid_rowconfigure(7, weight=1)      # creates empty row with weight 1
        self.frame_left.grid_rowconfigure(9, minsize=0)     # sets minimum size from bottom of screen to buttons

        # Creates user training label
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Training \nConfiguration:", font=("Segoe UI", 14))
        self.label_1.grid(row=1, column=0, padx=1, pady=1, sticky="we")

        # Previous training information for the user
        self.label_2 = customtkinter.CTkLabel(master=self.frame_left, text='Please click "Begin"\nwhen ready to configure.\nPlease make sure your\n hand is in the frame.\nPlease move your\nhand around at different\nangles and lengths from\nthe camera. The camera\nwill record for a\nfew seconds and after\nyou should be good\n to go.', font=("Segoe UI", 11))
        self.label_2.grid(row=3, column=0, padx=1, pady=5, sticky="nswe")

        #Images for left side of window
        self.home_image = self.load_image("/images/home.png", 25, 25)
        self.home_example_image = self.load_image("/images/HomeExample.png", 700, 635)
        self.settings_image = self.load_image("/images/settings.png", 25, 25)
        self.exit_image = self.load_image("/images/exit.png", 25, 25)

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

        self.training = UserTrain("DEMO_USER", letter, self.frame_right)

        # configure grid layout (5x3)
        self.frame_right.grid_rowconfigure((0, 1, 3), weight=1)        # sets weights of standard rows
        self.frame_right.grid_rowconfigure(5, weight=1)                # sets weight of last row
        self.frame_right.grid_columnconfigure((0, 1), weight=1)        # sets weights of standard columns
        self.frame_right.grid_columnconfigure(2, minsize=0)            # sets minimum size from right side of screen to cameras

        # Window for the main camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output
        self.config_cam_win1 = CameraWindow(master=self.frame_right, width = 290, height = 260, text = "", compound = "bottom")
        self.config_cam_win1.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Label that describes the main camera above
        self.label6 = customtkinter.CTkLabel(master=self.frame_right, text = "Main Camera")
        self.label6.grid(row=1, column=0, sticky="n", padx=10, pady=0)      

        # Creates instruction window for the application to communicate with the user
        self.label7 = customtkinter.CTkLabel(master=self.frame_right, text = 'Please sign the letter "{}" that you want \nMotion 21 to use as an example!'.format(letter), font=("Segoe UI", 20), width = 450, height = 100, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        self.label7.grid(row=3, column=0, columnspan=2, sticky="ns", padx=0, pady=0)

        self.button6 = customtkinter.CTkButton(master=self.frame_left, width = 160, height = 60, border_width = 1, corner_radius = 5, text = "Begin", compound = "bottom",  border_color="#101010", command=self.training_begin)
        self.button6.grid(row=7, column=0, columnspan=3, sticky="wse", padx=10, pady=10)

        # Window for the user hand camera
        # For now this is just an error message of "No Camera Found"
        # Once a camera is linked we create the same size window but with the camera output
        self.config_cam_win2 = CameraWindow(master=self.frame_right, width = 290, height = 260, text = "", cropped = True, compound = "bottom")
        self.config_cam_win2.grid(row=0, column=1, sticky="nw", padx=10, pady=10)

        # Label that describes the user hand camera above
        self.label9 = customtkinter.CTkLabel(master=self.frame_right, text = "Hand Camera")
        self.label9.grid(row=1, column=1, padx=0, pady=0, sticky="n")
        

        self.average_list.reinit(letter)
        self.letter_state.set_letter(letter)
        self.update()
        self.the_afterinator()
        #self.camera_aftinerator()
    
    def training_begin(self):
        #self.training.on_begin()
        '''
        #letter = self.
        counter = 0
        while True:
            for letter in self.usertrain_letters:
                dir = os.path.dirname(__file__)
                path = dir + '\test_' + letter
            counter += 1
            cv2.imwrite(os.path.join(path, '{}.jpg'.format(uuid.uuid1())), #??? )

            time.sleep(2)
        '''
        ()



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
        self.button1 = customtkinter.CTkButton(master=self.frame_left, text = "Home", text_color = THEME_OPP,  width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color = THEME, command=self.home_button)
        self.button1.grid(row=0, column=0, padx=0, pady=0)
        self.button2 = customtkinter.CTkButton(master=self.frame_left, text = "Home Settings", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.home_settings_button)
        self.button2.grid(row=1, column=0, padx=0, pady=0)        
        self.button3 = customtkinter.CTkButton(master=self.frame_left, text = "Users", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.users_button)
        self.button3.grid(row=2, column=0, padx=0, pady=0)
        self.button4 = customtkinter.CTkButton(master=self.frame_left, text = "Themes", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.themes_button)
        self.button4.grid(row=3, column=0, padx=0, pady=0)
        #self.button5 = customtkinter.CTkButton(master=self.frame_left, text = "Volume", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.volume_button)
        #self.button5.grid(row=4, column=0, padx=0, pady=0)
        self.button6 = customtkinter.CTkButton(master=self.frame_left, text = "Notifications", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.notif_button)
        self.button6.grid(row=4, column=0, padx=0, pady=0)
        self.button7 = customtkinter.CTkButton(master=self.frame_left, text = "Configure Letter", text_color = THEME_OPP, width = 200, height = 60, border_width = 1, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color=THEME, command=self.configure_button)
        self.button7.grid(row=6, column=0, padx=0, pady=0)
    
        # Creates Return button
        self.button8 = customtkinter.CTkButton(master=self.frame_left, text = "Return", text_color = THEME_OPP, width = 150, height = 60, border_width = 1, corner_radius = 5, fg_color = THEME, border_color=THEME, command=self.return_function)
        self.button8.grid(row=8, column=0, padx=0, pady=10, sticky="we")

        # Creates right sub-window
        # ------------------------------------------------------------------------------------   
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # Creates label with the text "Settings Page:"
        self.label_1 = customtkinter.CTkLabel(master=self.frame_right, text="Settings Page:", text_color = THEME_OPP, font=("Segoe UI", 20))
        self.label_1.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        # Creates label with the text describing button functionality
        self.label_2 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Home: Takes you back to the home page\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        self.label_2.grid(row=1, column=0, padx=0, pady=0, sticky="w")
        self.label_3 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Home Settings: Customize your home page\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        self.label_3.grid(row=2, column=0, padx=0, pady=0, sticky="w")
        self.label_4 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Users: Login to save your settings changes as well as lesson progression\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        self.label_4.grid(row=3, column=0, padx=0, pady=0, sticky="w")
        self.label_5 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Themes: Change the theme and look of the application\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        self.label_5.grid(row=4, column=0, padx=0, pady=0, sticky="w")
        self.label_6 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Volume: Change the audio volume of the application\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        self.label_6.grid(row=5, column=0, padx=0, pady=0, sticky="w")
        self.label_7 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Notifications: Change notification options for the application\n", text_color = THEME_OPP, font=("Segoe UI", 12))
        self.label_7.grid(row=6, column=0, padx=0, pady=0, sticky="w")
        self.label_8 = customtkinter.CTkLabel(master=self.frame_right, text="\n   Configure Letter: Lets you train Motion 21 to better suit your needs for letters\n", font=("Segoe UI", 11))
        self.label_8.grid(row=7, column=0, padx=0, pady=0, sticky="w")

    # Button that allows the user to change notification options
    def notif_button(self):
        print("testing notification button")

    # Button that destroys window and exits program
    def exit_button(self):
        self.destroy()

    def lesson_select(self):
        self.del_list = StateHandler().change_state(WindowState.HOME, self.del_list)
        if self.after_id:     self.after_cancel(self.after_id)
        if self.cam_after_id: self.after_cancel(self.cam_after_id)

        self.static_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]
        self.movement_letters = ["J", "Z"]

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

        #self.button3 = customtkinter.CTkButton(master=self.frame_left, image = self.home_image, text = "", width = 48, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        #self.button3.grid(row=8, column=0, padx=0, pady=0, sticky="sw")
        self.lesson_home = customtkinter.CTkButton(master=self.frame_main_left, image = self.home_image, text = "", text_color = THEME_OPP, width = 120, height = 22, border_width = 2, corner_radius = 8, compound = "bottom", border_color="#000000", command=self.home_button)
        self.lesson_home.grid(row = 10,  column = 0, padx = 0, pady = 0, sticky = "s")
        

        # lessons
        self.lesson1 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 1:\n A, B, C, D", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(self.static_letters[0:4]))
        self.lesson1.grid(row = 0, column = 4, padx = 2, pady = 2)
        
        self.lesson2 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 2:\n E, F, G, H", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(self.static_letters[4:8]))
        self.lesson2.grid(row = 0, column = 5, padx = 2, pady = 2)

        self.lesson3 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 3:\n I, K, L, M", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(self.static_letters[8:12]))
        self.lesson3.grid(row = 1, column = 4, padx = 2, pady = 2)
        
        self.lesson4 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 4:\n N, O, P, Q", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(self.static_letters[12:16]))
        self.lesson4.grid(row = 1, column = 5, padx = 2, pady = 2)
        
        self.lesson5 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 5:\n R, S, T, U", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(self.static_letters[16:20]))
        self.lesson5.grid(row = 2, column = 4, padx = 2, pady = 2)

        self.lesson6 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 6:\n V, W, X, Y", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"), width = 200, height = 100, border_width = 2, corner_radius = 5, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_static(self.static_letters[20:24]))
        self.lesson6.grid(row = 2, column = 5, padx = 2, pady = 2)
        
        self.lesson7 = customtkinter.CTkButton(master = self.frame_main_right, text = "LESSON 7:\n J & Z", text_color = THEME_OPP, font = ("Segoe UI", 18, "bold"),  width = 200, height = 100, border_width = 2, corner_radius = 8, compound = "bottom", border_color = "#000000", command = lambda : self.lesson_letters_movement(self.movement_letters[0:2]))
        self.lesson7.grid(row = 3, column = 4, padx = 2, pady = 2)
    
        

    def lesson_letters_static(self, letters):
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

        # description label
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = f"Lesson 1: \nLetters {letters[0]}, {letters[1]}, {letters[2]}, and {letters[3]}\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language", text_color = THEME_OPP, font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")


        # letters A - D letters to select on screen
        self.A_image = self.load_image(f"/images/letters/{letters[0].lower()}.JPG", 150, 150) 
        self.buttonA = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.A_image, width = 200, height = 200, border_width = 2, corner_radius = 20, compound = "top", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters[0]))
        self.buttonA.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "nswe")

        self.B_image = self.load_image(f"/images/letters/{letters[1].lower()}.JPG", 150, 150)
        self.buttonB = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.B_image, width = 200, height = 200, border_width = 2, corner_radius = 20, compound = "top", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters[1]))
        self.buttonB.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "nswe")

        self.C_image = self.load_image(f"/images/letters/{letters[2].lower()}.JPG", 150, 150)
        self.buttonC = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.C_image, width = 200, height = 200, border_width = 2, corner_radius = 20, compound = "top", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters[2]))
        self.buttonC.grid(row = 2, column = 1, padx = 20, pady = 15, sticky = "nswe")

        self.D_image = self.load_image(f"/images/letters/{letters[3].lower()}.JPG", 150, 150)
        self.buttonD = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.D_image, width = 200, height = 200, border_width = 2, corner_radius = 20, compound = "top", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons(letters[3]))
        self.buttonD.grid(row = 2, column = 2, padx = 20, pady = 15, sticky = "nswe")


    def lesson_letters_movement(self, letters):
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
        self.lesson_description = customtkinter.CTkLabel(master=self.frame_main_left, text = f"Lesson 7: \nLetters {letters[0]} and {letters[1]}\n\n Goal:\n Learn the\n fundamentals of\n American Sign \n Language\n\n Begin learning the\n idea of hand\n movement", text_color = THEME_OPP, font = ("Segoue UI", 12))
        self.lesson_description.grid(row=1, column=0, padx=1, pady=1, sticky="we")
        
        # letters J and Z, which require a special case of teaching
        self.J_image = self.load_image(f"/images/letters/{letters[0].lower()}.JPG", 150, 150) 
        self.buttonJ = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.J_image, width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons("J"))
        self.buttonJ.grid(row = 1, column = 1, padx = 20, pady = 15, sticky = "we")

        self.Z_image = self.load_image(f"/images/letters/{letters[1].lower()}.JPG", 150, 150) 
        self.buttonZ = customtkinter.CTkButton(master = self.frame_main_right, text = "", font = ("Segoe UI", 50, "bold"), image = self.Z_image, width = 200, height = 200, border_width = 2, corner_radius = 5, compound = "bottom", fg_color = THEME, border_color = THEME, command=lambda : self.letter_lessons("Z"))
        self.buttonZ.grid(row = 1, column = 2, padx = 20, pady = 15, sticky = "we")



    # later we can alter this function to be just for "lesson 1" "lesson 2" and so on
    # for now it just has the entire alphabet, but later will call to each function for better organization
    def letter_lessons(self, letter):
        #static_arr = self.static_letters
        #currIndex = self.static_letters[letter]

        self.del_list = StateHandler().change_state(WindowState.LESSONS, self.del_list)
        self.frame_main_right.destroy()

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
        
        self.tabview = CustomTabview(master=self.frame_main_left, width=25)
        self.tabview.grid(row=4, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.tabview.add("Debug")

        
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
        self.label8 = customtkinter.CTkLabel(master=self.frame_main_right, text = f"Please sign the letter \"{letter}\" \nas provided in the example!", text_color = THEME_OPP, font=("Segoe UI", 20), width = 350, height = 100, fg_color=THEME, corner_radius = 8, compound = "bottom")
        self.label8.grid(row=3, column=0, sticky="ns", padx=10, pady=0)

        # Load the image from the /image/letters folder to use for this part and position it in the correct place
        # Place Imaage of example sign for user to use when signing in the main lesson window 
        self.A_image = self.load_image(f"/images/letters/{letter.lower()}.JPG", 150, 150)
        self.A_labelimage = customtkinter.CTkLabel(master=self.frame_main_right, text = "", image = self.A_image, width = 150, height = 150)
        self.A_labelimage.grid(row=0, column=1, sticky="n", padx=0, pady=10)

        # Label that describes the example camera above
        #self.label10 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Example Image", text_color = THEME_OPP)
        #self.label10.grid(row=0, column=1, padx=10, pady=10)  

        if USE_CAMERA:
            self.label_cam2 = CameraWindow(master=self.frame_main_right, width = 150, height = 150, text = "", cropped = True, compound = "bottom")
        else:
            self.label_cam2 = customtkinter.CTkLabel(master=self.frame_main_right, text = "[Debug] camera off", width = 150, height = 150, fg_color=("gray38"), corner_radius = 8, compound = "bottom")
        self.label_cam2.grid(row=0, column=1, sticky="s", padx=0, pady=10)

        # Label that describes the user's accuracy
        self.label12 = customtkinter.CTkLabel(master=self.frame_main_right, text = "Total Accuracy: {}%".format(self.curr_accuracy), text_color = THEME_OPP, font=("Segoe UI", 14))
        self.label12.grid(row=3, column=1, sticky="nsw", padx=0, pady=0) 

        # Move on to next letter, once the one you got is correct
        #self.buttonNext = customtkinter.CTkButton(master=self.frame_main_right, width = 160, height = 60, border_width = 1, corner_radius = 5, text = "Next Letter: {}".format(self.letter), compound = "bottom",  border_color="#101010", command=self.static_arr[currIndex+1])
        #self.buttonNext.grid(row=4, column=1, sticky="se", padx=10, pady=10)

        self.average_list.reinit(letter)
        self.letter_state.set_letter(letter)
        self.update()
        self.the_afterinator()
        self.camera_aftinerator()
    
    def back_button_lessons(self):
        self.del_list = StateHandler().change_state(WindowState.HOME, self.del_list)
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
        self.del_list = StateHandler().change_state(WindowState.HOME, self.del_list)
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
        if StateHandler().c_state == WindowState.LESSONS and USE_CAMERA == 1: # find a better method of doing this later
            if self.border_change == 1:
                self.label_cam.cw_update()
                self.after_id = self.after(10, self.the_afterinator)
            else:
                self.label_cam.cw_update()
                self.label_cam2.cw_update()

                

                self.after_id = self.after(10, self.the_afterinator)
        
        if StateHandler().c_state == WindowState.TRAINING:
            self.config_cam_win1.cw_update()
            self.config_cam_win2.cw_update()
            self.after_id = self.after(10, self.the_afterinator)

            return     

    def camera_aftinerator(self):
        if StateHandler().c_state == WindowState.LESSONS and USE_CAMERA == 1:
            self.border_change = 0  
            let = UserSign().run_comparison(self.letter_state.DESIRED_LETTER[0])

            border_color_change = make_color(self.color_dict[1])
            Camera().border_q.put(border_color_change)

            if let == None and self.border_change == 0: 
                self.cam_after_id = self.after(210, self.camera_aftinerator)
                return

            if let == self.letter_state.DESIRED_LETTER[0]:
                self.border_change = 1
                self.del_list = StateHandler().change_state(WindowState.HOME, self.del_list)
                print("FOUND!!!!!!!")

                # border color change
                border_color_change = make_color(self.color_dict[3])
                Camera().border_q.put(border_color_change)

                # weird error - sometimes when re-activating lesson, and getting the letter right AGAIN, this wont display the 2nd time
                self.label8.configure(text="Congrats! You have succesfully signed\n the letter: {}".format(self.letter_state.DESIRED_LETTER[0]))
                self.label8.update()

                #self.after_cancel(self.after_id)
                self.after_cancel(self.cam_after_id)

                if self.border_change == 1:
                    self.del_list = StateHandler().change_state(WindowState.LESSONS, self.del_list)
                    #self.label_cam.cw_update()
                    self.after_id = self.after(10, self.the_afterinator)
                
                let = None
                return

            try:
                if(let == None):
                    self.average_list.add(self.average_list.letter, 1)
                else:
                    self.average_list.add(let, 5)

                self.curr_accuracy = int(self.average_list.l_average())
                #print(self.average_list.let_list)
                #print("Curr Accurancy[{}]: {} - {}".format(let, self.curr_accuracy, int(self.average_list.l_average())))

                self.label12.configure(text = "Total Accuracy: {}%".format(self.curr_accuracy))
                self.label12.update()
            except Exception as e: 
                print(e)
            
            self.after_id = self.after(10, self.the_afterinator)
            self.cam_after_id = self.after(200, self.camera_aftinerator)



if __name__ == "__main__":
    app = App()
    app.start()
