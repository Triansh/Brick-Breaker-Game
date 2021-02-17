"""
This file consists of global constants used in the code.
"""
import os

import numpy as np
from colorama import Fore, Back, Style

DEBUG = False

_sc_height, _sc_width = [int(x) for x in os.popen("stty size", "r").read().split()]

SCREEN_WIDTH = _sc_width - 7
SCREEN_HEIGHT = _sc_height - 10

BG_COLOR = Back.BLACK
FG_COLOR = Fore.GREEN
STYLE = Style.NORMAL

DELAY = 1 / 20

if DEBUG:
    EXPAND_PADDLE_SHAPE = SHRINK_PADDLE_SHAPE = PADDLE_SHAPE = (2, (SCREEN_WIDTH - 1))
    PADDLE_POSITION = np.array([1, SCREEN_HEIGHT - 2 - PADDLE_SHAPE[0]])
else:
    EXPAND_PADDLE_SHAPE = (2, 36)
    PADDLE_SHAPE = (2, 16)
    SHRINK_PADDLE_SHAPE = (2, 8)
    PADDLE_POSITION = np.array(
        [(SCREEN_WIDTH - PADDLE_SHAPE[1]) // 2, SCREEN_HEIGHT - 1 - PADDLE_SHAPE[0]])

PADDLE_VELOCITY = np.array([3, 0])
PADDLE_SHAPES = [PADDLE_SHAPE, EXPAND_PADDLE_SHAPE, SHRINK_PADDLE_SHAPE]

BALL_POSITION = np.array([20, 20])
# BALL_POSITION = PADDLE_POSITION + np.array([-1, _w // 2])
BALL_DIRECTION = np.array([0, -1])

WALL_POSITION = np.array([4, 5])
WALL_SHAPE = (11, SCREEN_WIDTH // 8)

MAX_VELOCITY = 3

# BRICKS
POWERUP_DIRECTION = np.array([0, 1])
POWERUP_SHAPE = (1, 2)

BRICK_TYPES = 3

# x = ['💥', '⚡⚡', '🥊', '⚜', '🔥', '💕', '⏪', '⏩', '💠', '🏈', '🌀', ]