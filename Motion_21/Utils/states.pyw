import Utils.utils as utils
import Utils.utils as utils

from enum    import Enum
from .camera    import *
from .constants import DEBUG



class BorderColor(Enum):
    RED    = 1
    BLUE   = 2
    GREEN  = 3
    YELLOW = 4
    BLACK  = 5

class CameraState(Enum):
    CAM_OFF          = 0
    CAM_ON           = 1
    CAM_REQUIRED     = 2
    CAM_NOT_REQUIRED = 3
    CAM_CONTINOUS    = 4

class WindowState(Enum):
    UNKNOWN  = [0, CameraState.CAM_NOT_REQUIRED] # for unstated windows, really only for debugging
    HOME     = [1, CameraState.CAM_NOT_REQUIRED]
    LESSONS  = [2, CameraState.CAM_REQUIRED]
    SETTINGS = [3, CameraState.CAM_NOT_REQUIRED]
    THEMES   = [4, CameraState.CAM_NOT_REQUIRED]
    CONFIG   = [5, CameraState.CAM_NOT_REQUIRED]
    MOTION   = [6, CameraState.CAM_REQUIRED]

class LetterState():
    DESIRED_LETTER = ["_", CameraState.CAM_REQUIRED]
    def __init__(self, letter='_'):
        self.set_letter(letter)

    def set_letter(self, letter):
        self.DESIRED_LETTER = [letter,CameraState.CAM_REQUIRED]


class EventHandler(object):
    x = 0
    y = 0
  
    def __new__(self):
        if not USE_CAMERA: return 
        if not hasattr(self, 'instance'):
            self.instance = super(EventHandler, self).__new__(self)
        return self.instance

    # 420 | 320
    # top left -50, -50
    # top right 385, -50
    # bottom right 385, 225
    # bottom left -50, 225

    def arrow_key_up(self, _):
        if (self.y == -50): 
           Camera().q.put([self.x, self.y, BorderColor.RED])
           return
        self.y -= 5
        utils.debug_log("arrow up: {}".format(self.y))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_down(self, _):
        if (self.y == 225): 
           Camera().q.put([self.x, self.y, BorderColor.RED])
           return
        self.y += 5
        utils.debug_log("arrow down: {}".format(self.y))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_left(self, _):
        if (self.x == -50):
            Camera().q.put([self.x, self.y, BorderColor.RED])
            return
        self.x -= 5
        utils.debug_log("arrow left: {}".format(self.x))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_right(self, _):
        if (self.x == 385):
            Camera().q.put([self.x, self.y, BorderColor.RED])
            return
        self.x += 5
        utils.debug_log("arrow left: {}".format(self.x))
        Camera().q.put([self.x, self.y, None])

class StateHandler(object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance  = super(StateHandler, self).__new__(self)
            self.c_state   = WindowState.HOME
        return self.instance

    def change_state(self, state : WindowState, del_list : list = []):
        self.c_state = state

        if del_list == [] or del_list == None: return
        [i.destroy() for i in del_list]
        del_list = []
      
        return []


