from .camera         import *
from .utils          import *
from enum            import Enum

class CameraState(Enum):
    CAM_OFF = 0
    CAM_ON = 1
    CAM_REQUIRED = 2
    CAM_NOT_REQUIRED = 3

class WindowState(Enum):
    UNKNOWN  = [0, CameraState.CAM_NOT_REQUIRED] # for unstated windows, really only for debugging
    HOME     = [1, CameraState.CAM_NOT_REQUIRED]
    LESSONS  = [2, CameraState.CAM_REQUIRED]
    SETTINGS = [3, CameraState.CAM_NOT_REQUIRED]
    THEMES   = [4, CameraState.CAM_NOT_REQUIRED]
    CONFIG   = [5, CameraState.CAM_NOT_REQUIRED]
    TRAINING = [6, CameraState.CAM_REQUIRED]

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
           Camera().q.put([self.x, self.y, 1])
           return
        self.y -= 5
        debug_log("arrow up: {}".format(self.y))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_down(self, _):
        if (self.y == 225): 
           Camera().q.put([self.x, self.y, 1])
           return
        self.y += 5
        debug_log("arrow down: {}".format(self.y))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_left(self, _):
        if (self.x == -50):
            Camera().q.put([self.x, self.y, 1])
            return
        self.x -= 5
        debug_log("arrow left: {}".format(self.x))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_right(self, _):
        if (self.x == 385):
            Camera().q.put([self.x, self.y, 1])
            return
        self.x += 5
        debug_log("arrow left: {}".format(self.x))
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
