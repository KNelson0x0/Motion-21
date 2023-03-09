import json, base64, hashlib
from   cryptography.fernet import Fernet
from   Utils.constants import *
from   Utils.utils import *
from   os.path  import exists
from   os       import mkdir
from   os       import remove


#
# UNFINISHED COMMIT (almost done, i do gotta be making sure everything works), Moving to other git to help fix git issues.
#


def make_key(passcode: str) -> str:
    md5_obj = hashlib.md5()
    passcode = MemKey(passcode)
    md5_obj.update(bytes(passcode.get_key(),'utf-8'))
    del passcode
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

class MemKey(): # because we arent storing any of this on a server, the least we can do is make sure the key isn't just floating around in memory somewhere
    """
       [NEVER USE THE ASSIGNMENT OPERATOR WITH THIS CLASS!]
       In order for the entire point of this class to work the key has to 
       be in memory for as little time as possible. If you do:

       mem_key = MemKey("password")

       and later do:
       
       mem_key = "password"

       mem_key is now a string obj and the key is once again in plaintext.
       Dont do that. Use .set_key.
    """
    def __init__(self, key):
        self.key = self.key_encrypt(key)
        del key

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = self.key_encrypt(key)
        del key

    def key_encrypt(self, msg):
        substitution_map = {
            'a': 'Q', 'b': 'W', 'c': 'E', 'd': 'R', 'e': 'T', 'f': 'Y', 'g': 'U', 'h': 'I', 'i': 'O', 'j': 'P', 'k': 'A', 'l': 'S', 'm': 'D', 'n': 'F', 'o': 'G', 'p': 'H', 'q': 'J', 'r': 'K', 's': 'L', 't': 'Z', 'u': 'X', 'v': 'C', 'w': 'V', 'x': 'B', 'y': 'N', 'z': 'M', 
            'Q': 'a', 'W': 'b', 'E': 'c', 'R': 'd', 'T': 'e', 'Y': 'f', 'U': 'g', 'I': 'h', 'O': 'i', 'P': 'j', 'A': 'k', 'S': 'l', 'D': 'm', 'F': 'n', 'G': 'o', 'H': 'p', 'J': 'q', 'K': 'r', 'L': 's', 'Z': 't', 'X': 'u', 'C': 'v', 'V': 'w', 'B': 'x', 'N': 'y', 'M': 'z'
        }
    
        # Apply the substitution cipher - basic but decently annoying to reverse
        encrypted_msg = ''
        for c in msg:
            if c in substitution_map:
                encrypted_msg += substitution_map[c]
            else:
                try:
                    encrypted_msg += c
                except:
                    encrypted_msg += chr(c)
    
        # bit shift every character
        shifted_msg = ''
        for c in encrypted_msg: # potentially annoying to reverse
            shifted_ascii = ord(c) << (1 << 3 << 3 << 7 & (255))  # Shift the ASCII value one by a really cool amount and then make sure it stays within valid ascii range
            shifted_msg += chr(shifted_ascii)
    
        # XOR the shifted message with a super secret and very random key (can be randomized, do this later)
        key = 'Motion21IsCool'
        xorred_msg = ''
        for i in range(len(shifted_msg)): # they are definitely gonna know this is the encrypt function lol
            key_char = key[i % len(key)]
            xorred_char = chr(ord(shifted_msg[i]) ^ ord(key_char))
            xorred_msg += xorred_char
    
        return xorred_msg
    
class Archive(object): # So python apparently does have circular imports but they are just really stupid and bad so heres another singleton
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(Archive, self).__new__(self)
            self.user_path = PATH + "UserData/m21_enc.cfg"
        
            if not exists(PATH + "UserData/"):
                mkdir    (PATH + "UserData/")
                f = open (PATH + "UserData/m21_enc.cfg", 'w').close()
            self.header_size                  = 0
            self.config_str                   = open(PATH + "UserData/m21_enc.cfg", 'r').read()
            self.header, self.header_str      = get_header(self.config_str) # small fix
            self.jsons                        = {}
            self.c_cfg                        = {} # add additional security later
            self.c_index                      = ''
            self.crypt                        = None
        return self.instance

    def parse_arch(self, key):
        self.crypt  = Fernet(make_key(key))
        sizes       = [x[0] for x in list(self.header.values())]
        header_size = len(self.header_str)
      
        debug_log("[Header Str]: {}\n\n".format(self.header_str))
        config_str = self.config_str.strip().replace('\n','') # in case of formatting
        last_size  = header_size
        total_size = last_size
        self.jsons = {}
        debug_log(len(config_str))

        # we do some unpacking
        for k, value in list(self.header.items()):
            key = None
            try:
                key = self.crypt.decrypt(bytes(value[1], 'utf-8'))
            except:
                pass

            total_size += value[0]

            c_config = config_str[total_size - value[0]: total_size]

            self.jsons[value[1]] = c_config

        debug_log("\n\n\n".join([ "[{}]: \n\
Key: {}\n\
Value: {}\n".format(i, list(self.jsons.keys())[i], list(self.jsons.values())[i]) for i in range(len(self.jsons)) ]))
      

    def commit_json(self, new_json):
        new_json_s = new_json 

        if type(new_json) == "<class 'config.Config'>":
            new_json_s = str(new_json.data).strip().replace("\n",'')
        if type(new_json) != str:
            new_json_s = str(new_json).strip().replace("\n",'')

        protected = self.crypt.encrypt(bytes(new_json_s, 'utf-8')).decode()
        
        debug_log("prot: " + protected)

        self.jsons[self.c_index] = protected
        print(self.jsons)
        return protected

    def commit_json(self, new_json):
        new_json_s = new_json 

        if type(new_json) == "<class 'config.Config'>":
            new_json_s = str(new_json.data).strip().replace("\n",'')
        if type(new_json) != str:
            new_json_s = str(new_json).strip().replace("\n",'')

        protected = self.crypt.encrypt(bytes(new_json_s, 'utf-8')).decode()
        
        debug_log("prot: " + protected)

        self.jsons[self.c_index] = protected
        print(self.jsons)
        return protected


    def get_json(self, key : str): # also up for name nomination, use_json
        crypt = Fernet(bytes(key, 'utf-8'))
        gate = ''
        for i in self.jsons.keys():
            try:
                gate = self.crypt.decrypt(bytes(i, 'utf-8'))
                if gate == b"UserSuccess":
                    print(self.jsons[i])
                    self.c_cfg = json.loads(crypt.decrypt(bytes(self.jsons[i],'utf-8')).decode())
                    self.c_index = i
                    return self.c_cfg
            except Exception as e:
                debug_log("[Archive::get_json]: Idk do better or something.")
                continue

    def save(self, name):
        f = open(self.user_path,'w')
        
        # add file header
        f.write(json.dumps(self.jsons))


        # write encrypted bits back
        for k,v in self.jsons:
            f.write(v)

        f.close()

 


class Config(): # singleton me later
    def __init__(self, user_name = '', password = ''): # TODO: fix later
        self.user_name = user_name
        self.password = password
        self.settings  = {'M21ConfigName' : user_name}
        self.data = {}
        self.user_path = "./UserData/m21_enc.cfg".format(self.user_name)

        if not exists(PATH + "/UserData/m21.cfg"):
            mkdir(PATH + "/UserData/m21.cfg")
        if not exists(PATH + "/UserData/m21.cfg"):
            open(self.user_path,'w').close()

    def __setitem__(self, key, new_val):
        self.settings[key] = new_val # probably extremely shallow setting. I, may, add deeper searching sets. 

    def __getitem__(self, x):
        return self.settings[x] # same as above with gets

    def save_var(self, var, name = ""):
        # var  - the variable you want values' saved.
        # name - the name of the variable you want it saved under. please use this though i've added support to do this without a name.

        # HERE
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
        self.settings = Archive().get_json(key)

    def delete(self):
       self.settings = {} 
