import json
from   Utils.constants import *
from   Utils.utils import *
from   os.path  import exists
from   os       import mkdir
from   os       import remove

# custom file format to put all the configs in so they werent just laying around in random folders.
# This is the manager for it.
class Archive():
    def __init__(self): # TODO: fix later
        self.header    = {}
        self.user_path = PATH + "UserData/m21.cfg"
        
        if not exists(PATH + "UserData/"):
            mkdir    (PATH + "UserData/")
            f = open (PATH + "UserData/m21.cfg", 'w').close()

        self.config_str = open(PATH + "UserData/m21.cfg", 'r').read()
        self.header     = self.get_header()

    def parse_arch(self):
        sizes       = list(self.header.values())
        data_size   = sum(sizes)
        header_size = len(str(self.header))
      
        header    = self.config_str.strip().replace('\n','') # in case of formatting
        blob      = header[header_size-1:]
        last_size = header_size
        jsons     = []

        c_config = header[last_size + (-1) : self.end_brace_index(blob)+last_size]
        if (len(sizes) == 1): return [json.loads(c_config)]

        for i in range(len(sizes)):
            last_size += len(c_config)

        print(jsons)
      
    def load_json(self):
        pass

    def update_json(self):
        pass

    def add_json(self):
        pass

    def get_json(self):
        pass

    def remove_json(self):
        pass
    # helpers
    def end_brace_index(self, string):
        brace_c = 1
        index = string.index('{') + 1
    
        while brace_c != 0:
            if string[index] == '{': brace_c += 1
            if string[index] == '}': brace_c -= 1
            index+=1

        return index-1

    def get_header(self):
        header = self.config_str.strip().replace('\n','') # in case of formatting
        return json.loads(header[:self.end_brace_index(header)+1])

    def get_json_size(self, j):
        return( len(str(j).replace('\n','').strip()) )

class Config(): # singleton me later
    def __init__(self, user_name = '', pass_hash = ''): # TODO: fix later
        self.user_name = user_name
        self.pass_hash = pass_hash
        self.settings  = {}
        self.user_path = "./UserData/{}/m21.cfg".format(self.user_name)

        if not exists(PATH + "/UserData/m21.cfg"):
            mkdir(PATH + "/UserData/m21.cfg")
        if not exists(PATH + "/UserData/m21.cfg"):
            open(self.user_path,'w').close()

    def login(self):
        # check user_name v pass_hash
        # if good load copy of user data into mem and decrypt as needed
        # for now decrypted stuff for testing
        pass

    def __setitem__(self, key, new_val):
        self.settings[key] = new_val # probably extremely shallow setting. I, may, add deeper searching sets. 

    def __getitem__(self, x):
        return self.settings[x] # same as above with gets

    def load(self):
        f = open(self.user_path,'r').read()
        self.settings = json.loads(f)

    def save_var(self, var, name = ""):
        # var  - the variable you want values' saved.
        # name - the name of the variable you want it saved under. please use this though i've added support to do this without a name.

        f = open(self.user_path,'r').read() # breaks my peace of mind but python will close this file for me
        if len(f) != 0: f = json.loads(f)
        data = {}

        if name == "" or len(name) == 0: 
            data["CFG_VAR"] = var
        else:                            
            data["var"]  = var  # removed list as doing [x][var][the_value_you_were_looking_for] defeats the purpose
            data["type"] = str(type(var))
            data["both"] = [var, str(type(var))] # allow for weird syntax

        if name == "" or len(name) == 0: 
            tag = "MVar_Unique0"
            keys = [i for i in list(self.settings.keys()) if "MVar_Unique" in i]
            keys.sort()

            if len(keys) >= 1:
                key = keys[-1] if len(keys) > 1 else keys[0]
                tag = "MVar_Unique" + str( int("".join(i for i in key if i.isdecimal()))+1 )
            self.settings[tag] = data
        else:                            
            self.settings[name] = data        

        f = open(self.user_path,'w').write(json.dumps(self.settings))


    def save(self, object, attributes = [], name = ""):
        # object     - the object you want the values saved from
        # attributes - if its an object you want values saved from, provide a list of the values youd like in string form
        # name       - provide a name for the object youd like saved (advised, otherwise it gets an autoname that you will have to find and deal with yourself https://pixy.org/src/455/4559042.png)

        for i in attributes:
            if i not in dir(object):
                debug_log("[Config.Save]> {} not in class {}. Stopping.".format(i), object.__name__)
                return False

        f = open(self.user_path,'r').read()
        if len(f) != 0: f = json.loads(f)
        data = {}

        obj = type(object)
        if type(object) != str: obj = str(obj)

        if name == "" or len(name) == 0: data["CFG_OBJ"] = obj
        else: data["Type"] = obj

        for i in attributes: # new data entered
            att = getattr(object, i)
            x = i # att copy so I dont have to worry about modifying att when I use 'type'

            if type(i)   != str: x = str(i)

            sub_data = {}
            sub_data["var"]  = str(att)  # removed list as doing [x][var][the_value_you_were_looking_for] defeats the purpose
            sub_data["type"] = str(type(att))
            sub_data["both"] = [str(att), str(type(att))] # allows for weird syntax

            data[x] = sub_data

        if name == "" or len(name) == 0: # Auto Namer. for some reason name '' was a problem for a bit.
            tag = "M_Unique0"
            keys = [i for i in list(self.settings.keys()) if "M_Unique" in i]
            keys.sort() # keys[-1] wont work if the largest key isnt there.

            if len(keys) >= 1: # make sure theres something in there
                key = keys[-1] if len(keys) > 1 else keys[0]
                tag = "M_Unique" + str( int("".join(i for i in key if i.isdecimal()))+1 ) # only get numbers, convert to number, add, convert back to str

            self.settings[tag] = data
        else:                            
            self.settings[name] = data
        
        f = open(self.user_path,'w').write(json.dumps(self.settings))

    def delete(self):
       self.settings = {}
       if exists(self.user_path): remove(self.user_path)
