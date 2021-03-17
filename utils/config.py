"""
This file consists of global constants used in the code.
"""
import os
import numpy as np
from colorama import Fore, Back, Style

# SCREEN SIZES
_sc_height, _sc_width = [int(x) for x in os.popen("stty size", "r").read().split()]
SCREEN_WIDTH = _sc_width - 24
SCREEN_HEIGHT = _sc_height - 10

# COLOR STYLES
BARRIER_STYLE = (Fore.LIGHTGREEN_EX, Back.BLACK, Style.BRIGHT)
TEXT_STYLE = (Fore.WHITE, Style.BRIGHT)
BACKGROUND_STYLE = (Back.BLACK, Style.NORMAL)

# MISCELLANEOUS
SCORE_FACTOR = 50
FPS = 30
DELAY = 1 / FPS
LIVES = 7+100
STAGES = 3

# PADDLE
EXPAND_PADDLE_SHAPE = (2, 50)
PADDLE_SHAPE = (2, 40)
SHRINK_PADDLE_SHAPE = (2, 30)
PADDLE_POSITION = np.array(
    [(SCREEN_WIDTH - PADDLE_SHAPE[1]) // 2, SCREEN_HEIGHT - PADDLE_SHAPE[0] - 1])
PADDLE_VELOCITY = np.array([4, 0])
PADDLE_SHAPES = [PADDLE_SHAPE, EXPAND_PADDLE_SHAPE, SHRINK_PADDLE_SHAPE]

# BALLS
BALL_POSITION = np.array([20, 20])
BALL_DIRECTION = np.array([0, -1])
MAXIMUM_BALLS = 4
MAX_VELOCITY = 3
BALLS = ['🏐', '🏉', '🥎', '⚾', '🏈']


# BRICKS
BRICK_TYPES = 4

# POWER UPS
POWER_UP_DIRECTION = np.array([0, 1])
POWER_UP_SHAPE = (1, 2)
POWER_UP_CHANCE = 100
