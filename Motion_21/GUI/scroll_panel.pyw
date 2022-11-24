import customtkinter as CT
from constants import *
import math
from utils import *
from enum import Enum


class ScrollPanel (CT.CTkFrame):

    class AnimationState(Enum):
        READY = 1
        IN_PROGRESS = 2
        COMPLETE = 3

    def __init__(self, *args, width: int = 100, height: int = 32, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.width         = width
        self.height        = height
        self.child_order   = {}
        self.timer         = Timer()
        self.counter       = Counter(0, 4)
        
    def as_destroy(self, el):
        el.destroy()
        self.child_order = {}
        self.update_child_order()

    def update_child_order(self):
        c_list  = self.winfo_children()

        if len(c_list) == 0:
            debug_log("No children in panel.")
            return

        for i in range(len(c_list)):
            elements = [i[1] for i in self.child_order.values()]
            if c_list[i] not in elements:
                if list(self.child_order.keys()) == []:
                    self.child_order[0] = [self.AnimationState.READY,c_list[i]] # if first entry, add.
                else:
                    self.child_order[max(self.child_order.keys())+1] = [self.AnimationState.READY,c_list[i]]  # if new entry, get next highest

    def check_children(self):
        old_keys = self.child_order.keys()
        self.update_child_order()
        new_keys = self.child_order.keys()

        if (len(old_keys) == len(new_keys)):
            return False
        else:
            return True

    def animate(self):
        count = self.counter.count
        total_height = 0
        #if not self.check_children() and self.anim_complete: # if no changes, dont bother animating
        #    return
        self.check_children()

        cvs = list(self.child_order.values())

        # move all of them
        for i in range(len(cvs)):
            animation_state = cvs[i][0]
            element = cvs[i][1]

            if animation_state != self.AnimationState.COMPLETE:
                element.place(x=self.winfo_width()/2 - element.winfo_width()/2, y = self.winfo_height() - element.winfo_height() + total_height - WEIRD_TKINTER_SPACE - count)
                total_height += element.winfo_height()

        
        self.counter.increment()
        count = self.counter.count

        
        if count >= self.winfo_height() - WEIRD_TKINTER_SPACE - cvs[-1][1].winfo_height():
            debug_log('inversion!')
            self.counter.set_increment((self.counter.inc)*-1)

        if len(cvs) > 1:
            if (count <= 0 + total_height - cvs[0][1].winfo_height()): # minus the initial elements height
                debug_log('inversion!2')
                self.counter.set_increment(-self.counter.inc)
        else:
            if (count <= 0):
                debug_log('inversion!2')
                self.counter.set_increment(-self.counter.inc)
       

