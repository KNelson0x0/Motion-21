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

"""
# To Chad -  From Keith
# [+]: Fixed weird file structure
# [+]: Fixed SOME camera bugs
# [+]: Integrated updated UI
# [+]: Cleaned up a small part of algorithm.pyw
# [?]: Definitely changed the env from urs to mine so I could use it and I believe those settings change over.
#      You will need to find ur env and click Add Env -> Existing Env and choose the folder for yours. You will 
#      will also likely need to update your customtkinter.
# Note: Pushed to quickly save progress since now the cropped hand camera doesnt wanna work at all :/ (ofc 1 day b4)
#       demo.
"""

from GUI.ASL_GUI import App
from Utils.camera import Camera
from config import Config

if __name__ == "__main__":
    # Loading Window Here!
    cam = Camera() # init it.
    app = App()
    app.start()
    