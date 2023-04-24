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

from GUI.ASL_GUI   import App
from Utils.imports import *
from datetime      import datetime
from config        import *

if __name__ == "__main__":
    # Loading Window Here!
    cam = Camera() # init it.
    app = App()
    
    print("================= Config Read! ==================")
    try:
        ()
        Config("Stupendous", "Amazing")
        #Config("Beemer", "swag2")
        print(Config().c_cfg)
        #Config().save_var(datetime.today().timestamp(), "Last Login Time")
        #print(Config().c_cfg)
        #Archive().save_config("Stupendous")
        #Config().add_user("Stupendous", "Amazing")
        #print("Stop")
        print(Config()["Last Login Time"]["var"])
        #to_enc = {"M21ConfigName":"Beemer","c":2}
    
    except Exception as e:
        print("Except: {}".format(e))
        """
        print("Demo Day Error! This error should only ever appear if it is demo day and this error has been thoroughly checked and tested for.\n\
              There should be 0 reason this ever prints other than 'it broke because our professors were looking at it' and 'because ofc it would'.")
        """
        print("=================================================")

    app.start()
    