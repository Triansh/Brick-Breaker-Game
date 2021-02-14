"""
This file consists of global constants used in the code.
"""
import os

import numpy as np
from colorama import Fore, Back, Style

from utils import util

_sc_height, _sc_width = [int(x) for x in os.popen("stty size", "r").read().split()]

SCREEN_WIDTH = _sc_width - 2
SCREEN_HEIGHT = _sc_height - 3

BG_COLOR = Back.BLACK
FG_COLOR = Fore.GREEN
STYLE = Style.NORMAL

DELAY = 0.04

PADDLE_SHAPE = (2, 22)
PADDLE_POSITION = np.array(
    [(SCREEN_WIDTH - PADDLE_SHAPE[1]) // 2, SCREEN_HEIGHT - 1 - PADDLE_SHAPE[0]])
# PADDLE_VELOCITY = np.array([0, 2])

BALL_POSITION = np.array([100, 5])
# BALL_POSITION = PADDLE_POSITION + np.array([-1, _w // 2])
# BALL_VELOCITY = np.array([-1, 1])

# VELOCITY_INCREASE_FACTOR = 4 / _w  # every unit from center of paddle, velocity changes by this factor (change it to 6)
