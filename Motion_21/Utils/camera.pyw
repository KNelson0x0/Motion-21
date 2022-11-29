
import cv2
import threading
import time
import numpy as np
from   Utils.utils import *

class Camera(object): # singleton because every time the camera is initialized there is at least a five second freeze and I'd prefer not to hard global too much.
    stream             = cv2.VideoCapture(0)
    rgb_img            = np.zeros((5,5), np.float32) # honestly shouldnt be a problem anymore but just in case
    old_frame          = None
    frame              = None
    thread             = None
    stop               = False

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(Camera, self).__new__(self)
            self.thread   = threading.Thread(target=self.begin, args=(self,))

            self.warmup(self)
            self.thread.start()

        return self.instance
    
    def get_frame(self): # ground work. will use proper mutexs and things in the future.
        try:
            return self.frame
        except:
            debug_log("[You really need to be using thread locks.]")
            return self.old_frame


    def warmup(self): # camera seems to need a bit to warmup. not joking.
        for i in range(60):
            _, self.frame = self.stream.read() 

    def begin(self):
        i = 0
        
        self.warmup(self)

        while (not self.stop):
            if i % 5 == 0: 
                self.old_frame = self.frame
                i = 0

            _, self.frame = self.stream.read()

            try:
                self.rgb_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) # Tkinter is SINGLE THREADED and has so many issues if you do anything with tkinter outside of that thread
                                                                               # so for the time being this is the only operation i can do without recreating tkinters functions
                                                                               # to help better performance for this thing.
            except:
                debug_log("Something Happened!");
            
            time.sleep(0.1)         # pErFoRmAnCe


    

