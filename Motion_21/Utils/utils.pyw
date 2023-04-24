import time
import json
import tkinter

from Utils.imports import *

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

def end_brace_index(string):
    brace_c = 1
    index = string.index('{') + 1
    
    while brace_c != 0:
        if string[index] == '{': brace_c += 1
        if string[index] == '}': brace_c -= 1
        index+=1

    return index-1

def get_header(config_str : str):
    header = config_str.strip().replace('\n','') # in case of formatting
    header = header[:end_brace_index(header)+1]

    return json.loads(header), header

def clean_json(js):
	out_str = ""
	searching = False
	for i in js:
		if i == '"': searching = not searching
		if searching and i == "'":
			out_str += 'M21_R3PL@C3_QUOTE'
			continue
		out_str += i
	return out_str

def get_json_size(self, j):
    return( len(str(j).replace('\n','').strip()) )

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

