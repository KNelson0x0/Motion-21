import time
import tkinter

def debug_log(x):
    DEBUG = 1 # change to 0 for demo builds

    if DEBUG:
        print(x)

def find_element(root: tkinter.Frame, name: str, type=None): # okay the type doesnt really work
    lst = root.winfo_children()

    for i in lst:
        try:
            if i.text == name:
                if type != None:
                    if type(i) == type:
                        return i
                else:
                    return i
        except:
            debug_log('Probably comparing elements that arent of the same class')
            continue 
    debug_log ('Nothing found')
    return None

class Counter:
    def __init__(self, start = 0, increment = 1, ):
        self.count = start
        self.inc = increment
        
    def increment(self):
        self.count += self.inc
        
    def reset(self):
        self.count = 0

    def set_count(self, new_count):
        self.count = new_count

    def get_count(self):
        return self.count

    def set_increment(self, new_increment):
        self.inc = new_increment

class Timer:
    def __init__(self):
        self.last_time = time.time()

    def reset(self):
        self.lasttime = time.time()
    
    def peek(self):
        return time.time() - self.last_time

    def mark(self):
        self.last_time = time.time()    