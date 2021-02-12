"""
This file consists of global constants used in the code.
"""

import os

import numpy as np
from colorama import Fore, Back, Style

SC_HEIGHT, SC_WIDTH = [int(x) for x in os.popen("stty size", "r").read().split()]

SCREEN_WIDTH = SC_WIDTH - 10
SCREEN_HEIGHT = SC_HEIGHT - 5

BG_COLOR = Back.BLACK
FG_COLOR = Fore.GREEN
STYLE = Style.NORMAL

DELAY = 0.04

INI_BALL_POSITION = np.array([5, 53])

BALL_VELOCITY = np.array([1, 1])
PADDLE_VELOCITY = np.array([0, 2])
