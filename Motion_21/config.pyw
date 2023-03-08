import json, base64, hashlib
from   cryptography.fernet import Fernet
from   Utils.constants import *
from   Utils.utils import *
from   os.path  import exists
from   os       import mkdir
from   os       import remove

# {Header: [size_here, "UserSuccess"]}



# helpers
def make_key(passcode: str) -> str:
    md5_obj = hashlib.md5()
    md5_obj.update(bytes(passcode,'utf-8'))
    return base64.urlsafe_b64encode(md5_obj.hexdigest().encode('utf-8'))

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


def get_json_size(self, j):
    return( len(str(j).replace('\n','').strip()) )


class Archive():
    def __init__(self): # TODO: fix later
        self.user_path = PATH + "UserData/m21.cfg"
        
        if not exists(PATH + "UserData/"):
            mkdir    (PATH + "UserData/")
            f = open (PATH + "UserData/m21.cfg", 'w').close()
        self.header_size                  = 0
        self.config_str                   = open(PATH + "UserData/m21.cfg", 'r').read()
        self.header, self.header_str      = self.get_header() # small fix
        self.jsons                        = []

    def parse_arch(self):
        sizes       = list(self.header.values())
        header_size = len(self.header_str)
      
        config_str = self.config_str.strip().replace('\n','') # in case of formatting
        last_size  = header_size
        self.jsons = []

        for _, value in list(self.header.items()):
            end_brace = self.end_brace_index(config_str[last_size:])
            c_config = config_str[last_size : end_brace + last_size + 1]
            last_size += value[0]  # one for EOS and one for th?te original len returning human sizings. There should be no size loss as long as the header reports the correct values.

            self.jsons.append(c_config)

        print("\n\n\n".join( [ "[{}]: {}".format(i, self.jsons[i]) for i in range(len(self.jsons)) ]))
      
    def commit_json(self, name):
        assert len(self.jsons) == len(self.header) # yw guys.
        to_commit = str(self.header) + "\n\n\n".join(self.jsons).strip()

        print(to_commit)

    def add_json(self, new_json):
        new_json_d = new_json # d for dict, cause thats what it is, a dictionary.

        if type(new_json) == "<class 'config.Config'>":
            new_json_d = new_json.data
        if type(new_json) == "<class 'str'>":
            new_json_d = json.loads(new_json)

        self.header[new_json_m["M21ConfigName"]] = len(str(new_json_m))

    def get_json(self, name):
        for i in self.jsons:
            pass

    def remove_json(self, name):
        pass


class Config(): # singleton me later
    def __init__(self, user_name = '', pass_hash = ''): # TODO: fix later
        self.user_name = user_name
        self.pass_hash = pass_hash
        self.settings  = {}
        self.data = {}
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

    def save_var(self, var, name = ""):
        # var  - the variable you want values' saved.
        # name - the name of the variable you want it saved under. please use this though i've added support to do this without a name.

        f = open(self.user_path,'r').read() # breaks my peace of mind but python will close this file for me
        if len(f) != 0: f = json.loads(f)

        if name == "" or len(name) == 0: 
            self.data["CFG_VAR"] = var
        else:                            
            self.data["var"]  = var  # removed list as doing [x][var][the_value_you_were_looking_for] defeats the purpose
            self.data["type"] = str(type(var))
            self.data["both"] = [var, str(type(var))] # allow for weird syntax

        if name == "" or len(name) == 0: 
            tag = "MVar_Unique0"
            keys = [i for i in list(self.settings.keys()) if "MVar_Unique" in i]
            keys.sort()

            if len(keys) >= 1:
                key = keys[-1] if len(keys) > 1 else keys[0]
                tag = "MVar_Unique" + str( int("".join(i for i in key if i.isdecimal()))+1 )
            self.settings[tag] = self.data
        else:                            
            self.settings[name] = self.data        

        f = open(self.user_path,'w').write(json.dumps(self.settings))

    def save(self, object, name = "", attributes = []):
        # object     - the object you want the values saved from
        # attributes - if its an object you want values saved from, provide a list of the values youd like in string form
        # name       - provide a name for the object youd like saved (advised, otherwise it gets an autoname that you will have to find and deal with yourself https://pixy.org/src/455/4559042.png)

        for i in attributes:
            if i not in dir(object):
                debug_log("[Config.Save]> {} not in class {}. Stopping.".format(i), object.__name__)
                return False

        f = open(self.user_path,'r').read()
        if len(f) != 0: f = json.loads(f)

        obj = type(object)
        if type(object) != str: obj = str(obj)

        if name == "" or len(name) == 0: self.data["CFG_OBJ"] = obj
        else: self.data["Type"] = obj

        for i in attributes: # new data entered
            att = getattr(object, i)
            x = i # att copy so I dont have to worry about modifying att when I use 'type'

            if type(i)   != str: x = str(i)

            sub_data = {}
            sub_data["var"]  = str(att)  # removed list as doing [x][var][the_value_you_were_looking_for] defeats the purpose
            sub_data["type"] = str(type(att))
            sub_data["both"] = [str(att), str(type(att))] # allows for weird syntax

            self.data[x] = sub_data

        if name == "" or len(name) == 0: # Auto Namer. for some reason name '' was a problem for a bit.
            tag = "M_Unique0"
            keys = [i for i in list(self.settings.keys()) if "M_Unique" in i]
            keys.sort() # keys[-1] wont work if the largest key isnt there.

            if len(keys) >= 1: # make sure theres something in there
                key = keys[-1] if len(keys) > 1 else keys[0]
                tag = "M_Unique" + str( int("".join(i for i in key if i.isdecimal()))+1 ) # only get numbers, convert to number, add, convert back to str

            self.settings[tag] = self.data
        else:                            
            self.settings[name] = self.data
        
        f = open(self.user_path,'w').write(json.dumps(self.settings))
    
    def load(self, key):
        f = open(self.user_path,'r').read()

        self.settings = json.loads(f)

    def delete(self):
       self.settings = {}
       if exists(self.user_path): remove(self.user_path)
