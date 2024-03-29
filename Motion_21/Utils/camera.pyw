import cv2
import threading
import mediapipe
import numpy as np

from time  import sleep
from queue import Queue

from Utils.imports import *

def make_color(color : BorderColor): # Helper function to correlate enum to color | BGR 
    return {
            BorderColor.WHITE  : (255,255,255),
            BorderColor.RED    : (1,1,255),
            BorderColor.BLUE   : (255,122,1),
            BorderColor.GREEN  : (1,255,1) ,
            BorderColor.YELLOW : (1,255,255),
            BorderColor.BLACK  : (1,1,1),
        }[color]

class EventHandler(object): # Event handler for the camera
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(EventHandler, self).__new__(self)
            self.x = 345
            self.y = 0
            self.boundary_range = 0

        return self.instance

    # 420 | 320
    # top left -50, -50
    # top right 385, -50
    # bottom right 385, 225
    # bottom left -50, 225

    def set_boundary_range(self, new_range): # change the bounding box boundary range
        try:
            self.boundary_range = 50-new_range
            print("set!")
        except:
            debug_log("[EventHandler]::set_boundary_range> HOW?")

    def arrow_key_up(self, _):
        if (self.y == -50): 
           Camera().q.put([self.x, self.y, BorderColor.RED])
           return
        self.y -= 5
        debug_log("arrow up: {}".format(self.y))
        Camera().q.put([self.x, self.y, None])

    def arrow_key_down(self, _):
        if (self.y == 230 + self.boundary_range): 
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
        if (self.x == 385 + self.boundary_range):
            Camera().q.put([self.x, self.y, BorderColor.RED])
            return
        self.x += 5
        debug_log("arrow left: {}".format(self.x))
        Camera().q.put([self.x, self.y, None])


class Camera(object): # Camera class for the entire program | singleton because every time the camera is initialized there is at least a five second freeze and I'd prefer not to hard global too much.
    stream               = cv2.VideoCapture(0)
    rgb_img              = np.zeros((5,5), np.float32) # honestly shouldnt be a problem anymore but just in case
    rgb_img_rect         = np.zeros((5,5), np.float32)
    rgb_img_crop         = np.zeros((5,5), np.float32)
    old_frame            = None
    frame                = None
    cropped_frame        = None
    cropped_frame_points = None
    rect_frame           = None
    thread               = None
    offsets              = [EventHandler().x, EventHandler().y, None]
    previous_offsets     = offsets
    q                    = Queue()
    border_q             = Queue()
    box_size_q           = Queue()
    pause_q              = Queue()
    pause                = True
    box_size             = 50
    last_box_size        = 50
    last_border_color    = make_color(BorderColor.BLUE)
    border_color         = last_border_color
    drawingModule        = mediapipe.solutions.drawing_utils
    handsModule          = mediapipe.solutions.hands

    def __new__(self):
        if not USE_CAMERA: return
        if not hasattr(self, 'instance'):
            self.instance   = super(Camera, self).__new__(self)
            self.thread     = threading.Thread(target=self.start_cam, args=(self,))
            self.lock       = ""
            self.start(self)

        return self.instance
    
    def start(self): # this is here so I don't have to include the warmup on the thread at all.
        self.warmup(self)
        self.thread.start()

    def get_frame(self): # get the current frame
        try:
            return self.frame
        except:
            debug_log("[You really need to be using thread locks.]")
            return self.old_frame

    def get_rect_frame(self): # get the frame with the rect drawn on
        try:
            return self.rect_frame
        except:
            debug_log("[You really need to be using thread locks.]")
            return self.old_frame

    def get_cropped_frame(self): # get the cropped frame
        if type(self.cropped_frame) != type(None):
            return self.cropped_frame
        return self.get_frame()

    def get_cropped_frame_points(self): # get the cropped frame with the mediapipe points drawn on 
        if type(self.cropped_frame_points) != type(None):
            return self.cropped_frame_points
        return self.get_cropped_frame()

    def draw_points(self, image): # add the points to the image | From Chad
        drawingModule = mediapipe.solutions.drawing_utils
        handsModule = mediapipe.solutions.hands

        with handsModule.Hands(static_image_mode=True) as hands: 

            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            try:
                if results.multi_hand_landmarks != None:
                    for handLandmarks in results.multi_hand_landmarks:
                        for point in handsModule.HandLandmark:
        
                            drawingModule.draw_landmarks(image, handLandmarks, handsModule.HAND_CONNECTIONS)
                return image
            except:
                debug_log("No hand detected")

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
    
    def start_cam(self): # starts or stops the program from reading from the camera. This was added in order to help better runtime
        while (True):
            try:
                self.pause = self.pause_q.get(timeout=0.01)
            except:
                pass
            if self.pause: 
                sleep(.5)
            else:
                debug_log("Starting Run Cam!")
                self.run_cam(self)
                debug_log("Back from Run Cam!")

    def run_cam(self): # updates the camera's attributes based on whether or not we are currently paused oir not.
        i = 1
        go = True

        while (go):
            # this is so it only writes the last frame every five frames, counts count 0 so 5.
            if i == 4: # every 5 frames
                self.old_frame = self.frame
                try:
                    self.pause = self.pause_q.get(timeout=0.01)
                    go = not self.pause # not because if we want it to pause we'd set pause to true, so if we want cam to pause we set it to false
                    if go == False:
                        return
                except:
                    pass
                i = -1
            i += 1

            _, self.frame = self.stream.read()

            try:
                # Tkinter is SINGLE THREADED and has so many issues if you do anything with tkinter outside of that thread
                # so for the time being these are the only operation i can do without recreating tkinters functions
                # to help better performance for this thing.
                
                self.rect_frame = self.frame.copy()
                self.rect_frame = cv2.flip(self.rect_frame, 1) # flips image horizontally, might need to change later

                # this entire chunk slows down the thread by .03 seconds. this is because this chunk is responsible for receiving communication sent to it from the tkinter thread.
                try:
                    self.border_color = self.border_q.get(timeout=.01)
                    self.last_border_color = self.border_color
                except:
                    self.border_color = self.last_border_color

                try:
                    self.offsets = self.q.get(timeout=.01)
                    self.previous_offsets = self.offsets
                except:
                    self.offsets  = self.previous_offsets

                try:
                    self.box_size = self.box_size_q.get(timeout=0.01)
                    self.last_box_size = self.box_size
                except:
                    self.box_size = self.last_box_size

                if self.offsets[2] == None:
                    color = self.border_color
                else:
                    color = make_color(self.offsets[2])

                #cv2.rectangle(self.rect_frame, (52 + offsets[0], 52 + offsets[1]), (252 + offsets[0], 252 + offsets[1]), color, 3)
                cv2.rectangle(self.rect_frame, (50 + self.offsets[0], 50 + self.offsets[1]), (200 + self.box_size + self.offsets[0], 200 + self.box_size + self.offsets[1]), color, 3)

                self.rgb_img_rect = cv2.cvtColor(self.rect_frame, cv2.COLOR_BGR2RGB)
                self.rgb_img_crop = cv2.cvtColor(self.rect_frame[50 + self.offsets[1] : 200 + self.box_size + self.offsets[1], 50 + self.offsets[0] : 200 + self.box_size + self.offsets[0]], cv2.COLOR_BGR2RGB)
                self.rgb_img      = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 

                # [y1:y2, x1:x2]
                # - 55 x
                roi = self.rect_frame[50 + self.offsets[1] : 200 + self.box_size + self.offsets[1], 
                                      50 + self.offsets[0] : 200 + self.box_size + self.offsets[0]]
                roi_points = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                roi_points = self.draw_points(self, roi_points)

                self.cropped_frame = roi # still an image
                self.cropped_frame_points = roi_points # still an image
            except Exception as e:
                debug_log("Something Happened! [");
                debug_log(str(e))
                debug_log("]")

        debug_log("Exiting Run Cam!")