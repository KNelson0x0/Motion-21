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

import json, base64, hashlib
from   cryptography.fernet import Fernet
from   GUI.ASL_GUI import App
from   Utils.constants import *
from   Utils.camera import Camera
from   config import *
import sys



if __name__ == "__main__":
    # Loading Window Here!
    # cam = Camera() # init it.
    app = App()

    # x = 1336.5

    Archive().parse_arch("swag")

    """
    cfg = Config("Beemer", "swag") 
    cfg.save(app, ['geometry','title'])
    cfg.save(app, ['geometry','title'], 'Test Name')
    cfg.save_var(x, 'x')
    cfg.load()
   
    
    """
    key = make_key("swag")
    crypt = Fernet(key)
    print(crypt.encrypt(bytes('{"M21ConfigName":"Beem","a":1,"b":2}','utf-8')))
    print("==========================================")
    print(key)
    #print(crypt.decrypt(bytes('gAAAAABkCXHAO04PhuDDAK0pOfA2QMYZVXW0ofHJCHoNy6EGrp07Sx7fy77zsikNcuxd0bfZ3GJSRWpx7E3CvCKnUeNfSILnFgES18xJyEfjYOBGidAyMGgZLK6sfuPa4m-gEQuOkaay','utf-8')).decode())
    Archive().parse_arch("swag")
    print(Archive().get_json(key.decode()))
    print("==========================================")
    protected = Archive().update_json('{"M21ConfigName":"Beem","a":1,"b":2}')
    print(crypt.decrypt(bytes(protected,'utf-8')).decode())
    print(Archive().get_json(key.decode()))
    # Passes are swag, Swag, swag
    #app.start()
   

    
    



