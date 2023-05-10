# constants.pyw: collection of variables, functions, and objects that need to be constant and globally accessible

import os
from enum import Enum

# ====== Debug Options ======
DEBUG = 1
USE_CAMERA = 1
# ======================

WEIRD_TKINTER_SPACE = 114
PATH      = os.path.dirname(os.path.realpath(__file__)) + "/../"
THEME     = "#101010"
THEME_OPP = "#FFFFFF"
FONT      = "#101010"

def debug_log(x): # moved here as it resolves lots of circular conflicts
    if DEBUG:
        print(x)

class BorderColor(Enum):
    WHITE  = 0
    RED    = 1
    BLUE   = 2
    GREEN  = 3
    YELLOW = 4
    BLACK  = 5