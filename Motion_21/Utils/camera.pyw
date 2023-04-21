import cv2
import threading
import mediapipe
import numpy as np

from time import sleep
from queue import Queue
from   Utils.utils import *
from   Utils.constants import *



class Camera(object): # singleton because every time the camera is initialized there is at least a five second freeze and I'd prefer not to hard global too much.
    stream             = cv2.VideoCapture(0)
    rgb_img            = np.zeros((5,5), np.float32) # honestly shouldnt be a problem anymore but just in case
    rgb_img_rect       = np.zeros((5,5), np.float32)
    rgb_img_crop       = np.zeros((5,5), np.float32)
    old_frame          = None
    frame              = None
    cropped_frame      = None
    cropped_frame_points      = None
    rect_frame         = None
    thread             = None
    previous_offsets   = [0,0]
    q                  = Queue()
    frame_q            = Queue()
    stop               = False
    drawingModule      = mediapipe.solutions.drawing_utils
    handsModule        = mediapipe.solutions.hands

    def __new__(self):
        if not USE_CAMERA: return
        if not hasattr(self, 'instance'):
            self.instance = super(Camera, self).__new__(self)
            self.thread   = threading.Thread(target=self.begin, args=(self,))
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

    def get_cropped_frame(self):
        if type(self.cropped_frame) != type(None):
            return self.cropped_frame
        return self.get_frame()

    def get_cropped_frame_points(self): # ground work. will use proper mutexs and things in the future.
        if type(self.cropped_frame_points) != type(None):
            return self.cropped_frame_points
        return self.get_cropped_frame()

    def draw_points(self, image):

        drawingModule = mediapipe.solutions.drawing_utils
        handsModule = mediapipe.solutions.hands

        with handsModule.Hands(static_image_mode=True) as hands: #True/False

            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            try:
                if results.multi_hand_landmarks != None:
                    for handLandmarks in results.multi_hand_landmarks:
                        for point in handsModule.HandLandmark:
        
                            drawingModule.draw_landmarks(image, handLandmarks, handsModule.HAND_CONNECTIONS)
                            #self.frame_q.put(image)

                #Camera().frame_q.put(image)

                return image
            except:
                print("No hand detected")

    def warmup(self): # camera seems to need a bit to warmup. not joking.

        try:
            for i in range(100):
                _, self.frame = self.stream.read() 

            roi = self.frame[52:252, 52:252]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi = cv2.resize(roi, (28, 28), interpolation = cv2.INTER_AREA)

            self.cropped_frame_points = roi
        except:
            sleep(10)

    def begin(self):
        i = 0
        
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
                    offsets = self.q.get(timeout=.01)
                    self.previous_offsets = offsets
                    if offsets[2] != None:
                        #cv2.rectangle(self.rect_frame, (50 + offsets[0], 50 + offsets[1]), (350 + offsets[0], 350 + offsets[1]), (1, 2,255), 3)
                        cv2.rectangle(self.rect_frame, (52 + offsets[0], 52 + offsets[1]), (252 + offsets[0], 252 + offsets[1]), (1, 2,255), 3)
                    else:
                        #cv2.rectangle(self.rect_frame, (50 + offsets[0], 50 + offsets[1]), (350 + offsets[0], 350 + offsets[1]), (255, 122,1), 3)
                        cv2.rectangle(self.rect_frame, (52 + offsets[0], 52 + offsets[1]), (252 + offsets[0], 252 + offsets[1]), (255, 122,1), 3)
                except:
                    offsets = self.previous_offsets
                    #cv2.rectangle(self.rect_frame, (50 + offsets[0], 50 + offsets[1]), (350 + offsets[0], 350 + offsets[1]), (255, 122,1), 3)
                    cv2.rectangle(self.rect_frame, (52 + offsets[0], 52 + offsets[1]), (252 + offsets[0], 252 + offsets[1]), (255, 122,1), 3)
                self.rgb_img_rect = cv2.cvtColor(self.rect_frame, cv2.COLOR_BGR2RGB)
                self.rgb_img_crop = cv2.cvtColor(self.rect_frame[52 + offsets[1] : 252 + offsets[1], 52 + offsets[0] : 252 + offsets[0]], cv2.COLOR_BGR2RGB)
                # self.rgb_img_crop = cv2.cvtColor(self.rect_frame[50 + offsets[1] : 350 + offsets[1], 50 + offsets[0] : 350 + offsets[0]], cv2.COLOR_BGR2RGB)
                self.rgb_img      = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
                
                #roi = self.rect_frame[50 + offsets[1] : 350 + offsets[1], 50 + offsets[0] : 350 + offsets[0]]
                roi = self.rect_frame[52 + offsets[1] : 252 + offsets[1], 52 + offsets[0] : 252 + offsets[0]]
                roi_points = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                roi_points = self.draw_points(self, roi_points)
                #roi_points = cv2.cvtColor(roi_points, cv2.COLOR_BGR2GRAY)

                self.cropped_frame = roi
                self.cropped_frame_points = roi_points # still an image


            except Exception as e:
                debug_log("Something Happened! [");
                debug_log(str(e))
                debug_log("]")

            
            #time.sleep(0.1)         # pErFoRmAnCe