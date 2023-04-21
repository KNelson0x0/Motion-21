import cv2
import threading
import mediapipe
import numpy as np

from time  import sleep
from queue import Queue

from Utils.imports import *

def make_color(color : BorderColor): # BGR
    return {
            BorderColor.WHITE  : (255,255,255),
            BorderColor.RED    : (1,1,255),
            BorderColor.BLUE   : (255,122,1),
            BorderColor.GREEN  : (1,255,1) ,
            BorderColor.YELLOW : (1,255,255),
            BorderColor.BLACK  : (1,1,1),
        }[color]

class EventHandler(object):
    x = 0
    y = 0
  
    def __new__(self):
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
           Camera().q.put([self.x, self.y, BorderColor.YELLOW])
           return
        self.y -= 5
        debug_log("arrow up: {}".format(self.y))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_down(self, _):
        if (self.y == 225): 
           Camera().q.put([self.x, self.y, BorderColor.RED])
           return
        self.y += 5
        debug_log("arrow down: {}".format(self.y))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_left(self, _):
        if (self.x == -50):
            Camera().q.put([self.x, self.y, BorderColor.RED])
            return
        self.x -= 5
        debug_log("arrow left: {}".format(self.x))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_right(self, _):
        if (self.x == 385):
            Camera().q.put([self.x, self.y, BorderColor.RED])
            return
        self.x += 5
        debug_log("arrow left: {}".format(self.x))
        Camera().q.put([self.x, self.y, None])


class Camera(object): # singleton because every time the camera is initialized there is at least a five second freeze and I'd prefer not to hard global too much.
    stream             = cv2.VideoCapture(0)
    rgb_img            = np.zeros((5,5), np.float32) # honestly shouldnt be a problem anymore but just in case
    rgb_img_rect       = np.zeros((5,5), np.float32)
    rgb_img_crop       = np.zeros((5,5), np.float32)
    old_frame          = None
    frame              = None
    cropped_frame      = None
    rect_frame         = None
    thread             = None
    previous_offsets   = [0,0,None]
    q                  = Queue()
    border_q           = Queue()
    stop               = False
    last_border_color  = make_color(BorderColor.BLUE)
    border_color       = last_border_color
    drawingModule      = mediapipe.solutions.drawing_utils
    handsModule        = mediapipe.solutions.hands

    def __new__(self):
        if not USE_CAMERA: return
        if not hasattr(self, 'instance'):
            self.instance   = super(Camera, self).__new__(self)
            self.thread     = threading.Thread(target=self.begin, args=(self,))
            self.lock       = ""
            self.start(self)

        return self.instance
    
    def start(self):
        self.warmup(self)
        self.thread.start()

    def get_frame(self): # ground work. will use proper mutexs and things in the future.
        try:
            return self.frame
        except:
            debug_log("[You really need to be using thread locks.]")
            return self.old_frame

    def get_rect_frame(self): # ground work. will use proper mutexs and things in the future.
        try:
            return self.rect_frame
        except:
            debug_log("[You really need to be using thread locks.]")
            return self.old_frame

    def get_cropped_frame(self): # ground work. will use proper mutexs and things in the future.
        if type(self.cropped_frame) != None:
            return self.cropped_frame
        return self.get_frame()

    def warmup(self): # camera seems to need a bit to warmup. not joking.
        try:
            for i in range(100):
                _, self.frame = self.stream.read() 

            roi = self.frame[52:252, 52:252]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi = cv2.resize(roi, (28, 28), interpolation = cv2.INTER_AREA)

            self.cropped_frame = roi
        except:
            sleep(10)

    def change_border_color(self):
        debug_log("make sure you put something in the q!")
        try:
            self.border_color = make_color(self.border_q.get(timeout=1))
        except:
            debug_log("you didn't put something in the q.")

    def begin(self):
        i = 0
        self.border_color
        self.warmup(self)

        while (not self.stop):
            if i % 5 == 0: 
                self.old_frame = self.frame
                i = 0

            _, self.frame = self.stream.read()

            try:
                # Tkinter is SINGLE THREADED and has so many issues if you do anything with tkinter outside of that thread
                # so for the time being these are the only operation i can do without recreating tkinters functions
                # to help better performance for this thing ... right now.
                
                self.rect_frame = self.frame.copy()

                try:
                    self.border_color = self.border_q.get(timeout=.01)
                    self.last_border_color = self.border_color
                except:
                    self.border_color = self.last_border_color

                try:
                    offsets = self.q.get(timeout=.01)
                    self.previous_offsets = offsets
                except:
                    offsets = self.previous_offsets

                if offsets[2] == None:
                   color = self.border_color
                else:
                   color = make_color(offsets[2])

                cv2.rectangle(self.rect_frame, (52 + offsets[0], 52 + offsets[1]), (252 + offsets[0], 252 + offsets[1]), color, 3)

                self.rgb_img_rect = cv2.cvtColor(self.rect_frame, cv2.COLOR_BGR2RGB)
                self.rgb_img_crop = cv2.cvtColor(self.rect_frame[52 + offsets[1] : 252 + offsets[1], 52 + offsets[0] : 252 + offsets[0]], cv2.COLOR_BGR2RGB)
                self.rgb_img      = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 

                roi = self.rect_frame[52 + offsets[1] : 252 + offsets[1], 52 + offsets[0] : 252 + offsets[0]]

                self.cropped_frame = roi # still an image
            except Exception as e:
                debug_log("Something Happened! [");
                debug_log(str(e))
                debug_log("]")