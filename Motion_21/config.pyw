# config.pyw: File that houses all of the archive and config objects and functions
import json, base64, hashlib

from   Utils.imports import *
from   os       import mkdir
from   os       import remove
from   os.path  import exists
from   cryptography.fernet import Fernet


def make_key(passcode: str) -> bytes: # transforms a users plaintext key into a non-human-readable blob of characters and returns it in a fun base64 safe format for fernet.
    md5_obj = hashlib.md5()
    passcode = MemKey(passcode)
    md5_obj.update(bytes(passcode.get_key(),'utf-8'))
    del passcode
    return base64.urlsafe_b64encode(md5_obj.hexdigest().encode('utf-8'))

# key class, transforms a users plaintext key into something way worse to look at. If this we had compiled this into a bin (and python IR wasn't cringe) this would just deter reverse engineers and help combat mem scans for the plaintext key.
class MemKey(): # because we arent storing any of this on a server, the least we can do is make sure the plaintext key isn't just floating around in memory somewhere
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
    
        # XOR the shifted message with a super secret and very random key (could be randomized based on HWID)
        key = 'Motion21IsCool'
        xorred_msg = ''
        for i in range(len(shifted_msg)): # they are definitely gonna know this is the encrypt function lol
            key_char = key[i % len(key)]
            xorred_char = chr(ord(shifted_msg[i]) ^ ord(key_char))
            xorred_msg += xorred_char
    
        return xorred_msg
    
class Archive(object): # Class that reads, writes, encrypts, decrypts, and manages the config file (archive) | So python apparently does have circular imports but they are just really stupid and bad so heres another singleton
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance  = super(Archive, self).__new__(self)
            self.user_path = PATH + "UserData/m21_enc.cfg"
        
            if not exists(PATH + "UserData/"):
                mkdir    (PATH + "UserData/")
                f = open (PATH + "UserData/m21_enc.cfg", 'w').close()
            self.header_size                  = 0
            self.config_str                   = open(PATH + "UserData/m21_enc.cfg", 'r').read()
            self.header, self.header_str      = get_header(self.config_str) # small fix
            self.jsons                        = {}
            self.c_cfg                        = {} # add additional security later, this will require a similar protection to that of vm-based
            self.c_index                      = ''
            self.crypt                        = None
        return self.instance

    def set_password(self, key : str): # needs to be here for user switch
        self.crypt = Fernet(make_key(key))
        del key

    def parse_arch(self, key : str = ""): # parse the archive
        if key != "": 
            self.crypt  = Fernet(make_key(key))
            del key

        sizes       = [x[0] for x in list(self.header.values())]
        header_size = len(self.header_str)
      
        debug_log("[Header Str]: {}\n\n".format(self.header_str))
        config_str = self.config_str.strip().replace('\n','') # in case of formatting
        last_size  = header_size
        total_size = last_size
        debug_log(len(config_str))

        # we do some unpacking
        for k, value in list(self.header.items()):
            total_size += value[0]

            c_config = config_str[total_size - value[0]: total_size]

            self.jsons[value[1]] = c_config

        debug_log("\n\n\n".join([ "[{}]: \n\
Key: {}\n\
Value: {}\n".format(i, list(self.jsons.keys())[i], list(self.jsons.values())[i]) for i in range(len(self.jsons)) ]))
      
    def update_json(self, new_json): # update the json
        new_json_s = new_json 

        if type(new_json) == "<class 'config.Config'>":
            new_json_s = str(new_json.data).strip().replace("\n",'')
        if type(new_json) != str:
            new_json_s = str(new_json).strip().replace("\n",'')

        protected = self.crypt.encrypt(bytes(new_json_s, 'utf-8')).decode()
        
        debug_log("prot: " + protected)

        try:
            self.jsons[self.c_index] = protected
        except:
            debug_log("Config cannot be updated yet as it hasn't been added yet!")

        return protected

    def get_header(self):
        return self.header

    def get_json(self, user_name : str = "", key : bytes = ""): # get json based on username and pass | also up for name nomination, use_json
        crypt = Fernet(key)
        del key
        gate = ''

        if not user_name: return False # purely so I can have a key-value input without things being confusing

        for i, k in enumerate(self.jsons.keys()):
            try:
                keys = list(self.header.keys())
                if user_name == "" or user_name != keys[i]:
                   continue
                gate = self.crypt.decrypt(bytes(k, 'utf-8'))
                if gate == b"UserSuccess":
                    down_down    = crypt.decrypt(bytes(self.jsons[k],'utf-8')).decode()
                    down_down    = clean_json(down_down).replace('"',"'").replace("\'",'"').replace("M21_R3PL@C3_QUOTE",'\\"')
                    self.c_cfg   = json.loads(down_down)
                    self.c_index = k
                    self.crypt   = crypt
                    return self.c_cfg,
            except Exception as e:
                debug_log(e)
                debug_log("[Archive::get_json]: Idk do better or something.")
                continue
        return False

    def exists(self, name : str): # figures out whether a header exists or not
        for i in self.headers.keys():
            try:
                gate = self.crypt.decrypt(bytes(i[1], 'utf-8'))
                if gate == b"UserSuccess":
                   to_search = json.loads(self.crypt.decrypt(bytes(self.jsons[i[1]], 'utf-8')).decode())
                   return name in to_search.keys()
            except:
                pass
        return False

    def add_config(self, user_name : str, key : bytes): # adds the config the to db
        crypt = Fernet(key)
        payload = crypt.encrypt(bytes('{{"M21ConfigName" : "{}"}}'.format(user_name), 'utf-8')).decode()
        success = crypt.encrypt(b"UserSuccess").decode()
        self.c_cfg = '{{"M21ConfigName" : "{}"}}'.format(user_name)
        self.c_index = success
        self.header[user_name] = [len(payload), success]
        self.jsons[success] = payload
        self.save_config(user_name)
        self.crypt = crypt

    def del_config(self, user_name : str, key : bytes): # removes the config from the db
        self.crypt = Fernet(key)
        for i, k in enumerate(self.jsons.keys()):
            try:
                keys = list(self.header.keys())
                if user_name == "" or user_name != keys[i]:
                   continue
                gate = self.crypt.decrypt(bytes(k, 'utf-8'))
                if gate == b"UserSuccess":
                    del self.header[user_name]
                    del self.jsons[k]
                    self.c_cfg = {}
                    del self.crypt
                    
                    f = open(self.user_path,'w')
                    stang = json.dumps(self.header)

                    # write encrypted bits back
                    for k,v in self.jsons.items():
                        stang += v  

                    f.write(stang)
                    f.close()
                    return

            except Exception as e:
                debug_log("[Archive::del_config]: Nope!")
                continue


        return False

    def save_config(self, user_name): # saves the config
        f = open(self.user_path,'r')
        
        # add file header
        debug_log("[------]\n{}".format(self.c_cfg))
        crypted = self.crypt.encrypt(bytes(json.dumps(self.c_cfg), 'utf-8')).decode()

        self.jsons[self.c_index] = crypted
        self.header[user_name]   = [len(crypted), self.header[user_name][1]]
        bak = f.read()
        f.close()
        f = open(self.user_path,'w')

        stang = json.dumps(self.header)

        # write encrypted bits back
        for k,v in self.jsons.items():
            stang += v  

        debug_log("[------]")
        f.write(stang)
        f.close()

class Config(object): # Config class, more or less a wrap around archive to make usage easier and more understandable.
    def __new__(self, user_name : str = "", password : str = ""):
        if not hasattr(self, 'instance'):
            self.instance  = super(Config, self).__new__(self)
            self.user_name = user_name
            self.settings  = {'M21ConfigName' : user_name}
            self.data      = {}
            self.users     = []
            self.c_cfg     = False

            Archive().parse_arch(password) # password is swag.
                
            key   = make_key(password)
            del password

            self.users = list(Archive().get_header().keys())

            if user_name:
                self.c_cfg = Archive().get_json(user_name, key) # password is swag.      

            if self.c_cfg == False: 
                self.user_name = ""
                return self

            self.c_cfg = self.c_cfg[0] # dont get why its tupling, dc at this point, its getting selected

        return self.instance
  
    def __setitem__(self, key, new_val): # allows for Config()["key"] = x
        self.settings[key] = new_val # probably extremely shallow setting. I, may, add deeper searching sets. 

    def __getitem__(self, x): # allows for x = Config()["key"] 
        return self.c_cfg[x] # same as above with gets

    def save_var(self, var, name = ""): # saves an individual variable
        # var  - the variable you want values' saved.
        # name - the name of the variable you want it saved under. please use this though i've added support to do this without a name.

        f = Archive().c_cfg

        if name == "" or len(name) == 0: 
            self.data["CFG_VAR"] = var
        else:                            
            self.data["var"]  = var  # removed list as doing [x][var][the_value_you_were_looking_for] defeats the purpose
            self.data["type"] = str(type(var))
            self.data["both"] = [var, str(type(var))] # allow for weird syntax

        if name == "" or len(name) == 0: 
            tag  = "MVar_Unique0"
            keys = [i for i in list(self.settings.keys()) if "MVar_Unique" in i]
            keys.sort()

            if len(keys) >= 1:
                key = keys[-1] if len(keys) > 1 else keys[0]
                tag = "MVar_Unique" + str( int("".join(i for i in key if i.isdecimal()))+1 )
            self.settings[tag] = self.data
        else:                            
            self.settings[name] = self.data        

        self.c_cfg      = self.settings
        Archive().c_cfg = self.settings
        Archive().save_config(self.user_name)

    def save(self, object, name = "", attributes = []): # saves something from an object, ex: Animal.Legs
        # object     - the object you want the values saved from
        # attributes - if its an object you want values saved from, provide a list of the values youd like in string form
        # name       - provide a name for the object youd like saved (advised, otherwise it gets an autoname that you will have to find and deal with yourself https://pixy.org/src/455/4559042.png)

        for i in attributes:
            if i not in dir(object):
                debug_log("[Config.Save]> {} not in class {}. Stopping.".format(i), object.__name__)
                return False

        f = Archive().c_cfg

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
        
        self.c_cfg      = self.settings
        Archive().c_cfg = self.settings
        Archive().save_config(self.user_name)
    
    def add_user(self, user_name : str, password : str): # add a new user | plaintext user and pass
        key = make_key(password)
        del password
        Archive().add_config(user_name, key)

    def delete_user(self, user_name : str, password : str): # remove a user
        key = make_key(password)
        del password
        Archive().del_config(user_name, key)

    def reload(self, user_name : str = ""): # refresh Config
        if user_name != "":
            self.user_name = user_name
            self.settings  = {'M21ConfigName' : user_name}
            self.data      = {}
        self.users     = []

        Archive().parse_arch() # password is swag.

        self.users = list(Archive().get_header().keys())   

        return
    
    def set_password(self, password : str): # change the current stored password
        Archive().set_password(password)
        del password
        
    def load(self, user_name : str, password : str): # load a config from the Archive
        key = make_key(password)

        try: 
            Archive().parse_arch(password) # reparse
        except:
            return False

        del password

        cfg = Archive().get_json(user_name, key)
        
        if not cfg: return False

        self.user_name = user_name
        self.c_cfg = cfg[0]
        return True