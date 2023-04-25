from enum import Enum
from Utils.imports import *


class CameraState(Enum):
    CAM_OFF          = 0
    CAM_ON           = 1
    CAM_REQUIRED     = 2
    CAM_NOT_REQUIRED = 3
    CAM_CONTINOUS    = 4

class WindowState(Enum):
    UNKNOWN          = [0, CameraState.CAM_NOT_REQUIRED] # for unstated windows, really only for debugging
    HOME             = [1, CameraState.CAM_NOT_REQUIRED]
    LESSONS          = [2, CameraState.CAM_NOT_REQUIRED]
    IN_LESSON        = [2, CameraState.CAM_REQUIRED]
    SETTINGS         = [3, CameraState.CAM_NOT_REQUIRED]
    THEMES           = [4, CameraState.CAM_NOT_REQUIRED]
    CONFIG           = [5, CameraState.CAM_NOT_REQUIRED]
    MOTION           = [6, CameraState.CAM_CONTINOUS]
    IN_MOTION_LESSON = [7, CameraState.CAM_CONTINOUS]

class LetterState():
    DESIRED_LETTER = ["_", CameraState.CAM_REQUIRED]
    def __init__(self, letter='_'):
        self.set_letter(letter)

    def set_letter(self, letter):
        self.DESIRED_LETTER = [letter,CameraState.CAM_REQUIRED]

class StateHandler(object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance  = super(StateHandler, self).__new__(self)
            self.c_state   = WindowState.HOME
        return self.instance

    def change_state(self, state : WindowState, del_list : list = []):
        self.c_state = state

        if del_list == [] or del_list == None: return
        for i in del_list:
            try:
                i.destroy()
            except:
                pass
        del_list = []
      
        return del_list


