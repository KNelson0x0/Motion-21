#▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
#         |                                                                                      |                                                
#    ╔════■══════════════════════════════════════════════════════════════════════════════════════■════╗  
#    ║                                      P R O J E C T                                             ║
#    ╠════════════════════════════════════════════════════════════════════════════════════════════════╣ 
#    ║  ____    ____             _      _                          |¯\               _______          ║
#    ║ |_   \  /   _|           / |_   (_)                      ---'  |________  ---'   ____)_______  ║
#    ║   |   \/   |     .--.   `| |-'  __     .--.    _ .--.    |        ______) |            ______) ║
#    ║   | |\  /| |   / .'`\ \  | |   [  |  / .'`\ \ [ `.-. |   |       /(|_)    |        /(|_)       ║
#    ║  _| |_\/_| |_  | \__. |  | |,   | |  | \__. |  | | | |   |       /(|_)    |        /(|_)       ║
#    ║ |_____||_____|  '.__.'   \__/  [___]  '.__.'  [___||__]  ---'___/(|_)     ---'___/(|_)         ║  
#    ╚═══════════════════════■═══════════════════════════════════════════■════════════════════════════╝   
#                            |                                           |
#                            ■══╦═════════════════════════════════════╦══■
#                               ║            Contributers             ║
#                               ╠═════════════════╦═══════════════════╣
#                               ║  Chad Josim     ║        ML         ║
#                               ║  Jason Liang    ║      UI, ML       ║
#                               ║  Keegan Graf    ║      UI, ML       ║
#                               ║  Keith Nelson   ║         *         ║
#                               ║ Sebastian Reel  ║      ML, MGR      ║
#                               ╚═════════════════╩═══════════════════╝ 
#
#▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

from GUI.ASL_GUI import App
from Utils.constants import *
from Utils.camera import Camera

# -- del
import json, base64, hashlib
from   cryptography.fernet import Fernet
# -- del
from config import *

if __name__ == "__main__":
    # Loading Window Here!
    cam = Camera() # init it.
    app = App()
    
    print("================= Config Read! ==================")
    try:
        #Archive().parse_arch("swag") # password is swag.
        #key = make_key("swag")
        #print(Archive().get_json(key.decode()))

        Config("Beemer", "swag2")
        print(Config().c_cfg)
        Archive().save_config()
        print("Stop")

        """
        key    = make_key("swag2")
        cipher = Fernet(key)

        ciphertext = cipher.encrypt(bytes('{"M21ConfigName":"Beemer","c":2}', 'utf-8'))
        usertext   = cipher.encrypt(bytes('UserSuccess', 'utf-8'))
        print("Text:\n{}".format(ciphertext))
        print("UserSuccess: {}".format(usertext))
        print("Pass out: {}".format(cipher.decrypt(ciphertext)))
        #to_enc = {"M21ConfigName":"Beemer","c":2}
        """
    except:
        print("Demo Day Error! This error should only ever appear if it is demo day and this error has been thoroughly checked and tested for.\n\
              There should be 0 reason this ever prints other than 'it broke because our professors were looking at it' and 'because ofc it would'.")
    print("=================================================")

    app.start()
