"""
This file consists of global constants used in the code.
"""
import os
import numpy as np
from colorama import Fore, Back, Style

# SCREEN SIZES
_sc_height, _sc_width = [int(x) for x in os.popen("stty size", "r").read().split()]
SCREEN_WIDTH = _sc_width - 10
SCREEN_HEIGHT = _sc_height - 7

# COLOR STYLES
BARRIER_STYLE = (Fore.WHITE, Back.BLACK, Style.BRIGHT)
TEXT_STYLE = (Fore.LIGHTCYAN_EX, Style.BRIGHT)
BACKGROUND_STYLE = (Back.BLACK, Style.NORMAL)

# MISCELLANEOUS
SCORE_FACTOR = 50
FPS = 30
DELAY = 1 / FPS
LIVES = 15
STAGES = 3
TIME_ATTACK = 60 * FPS
PADDLE_LIVES = 3

# PADDLE
PADDLE_SHAPE = (2, 32)
EXPAND_PADDLE_SHAPE = (2, PADDLE_SHAPE[1] + 10)
SHRINK_PADDLE_SHAPE = (2, PADDLE_SHAPE[1] - 10)
PADDLE_POSITION = np.array(
    [(SCREEN_WIDTH - PADDLE_SHAPE[1]) // 2, SCREEN_HEIGHT - PADDLE_SHAPE[0] - 1], dtype=float)
PADDLE_VELOCITY = np.array([4, 0], dtype=float)
PADDLE_SHAPES = [PADDLE_SHAPE, EXPAND_PADDLE_SHAPE, SHRINK_PADDLE_SHAPE]
SHOOT_BULLET_TIME = FPS // 1

# BALLS
BALL_POSITION = np.array([20, 20], dtype=float)
BALL_DIRECTION = np.array([0, -1], dtype=float)
MAXIMUM_BALLS = 4
MAX_VELOCITY = 3
BALLS = ['🏐', '🏉', '🥎', '⚾', '🏈']

# BRICKS
BRICK_TYPES = 4

# POWER UPS
POWER_UP_DIRECTION = np.array([0, 1], dtype=float)
POWER_UP_SHAPE = (1, 2)
POWER_UP_CHANCE = 10
GRAVITY = np.array([0, .025], dtype=float)

# UFO BOSS
UFO_SHAPE = (13, 32)
UFO_POSITION = np.array([(SCREEN_WIDTH - UFO_SHAPE[1]) // 2, 1], dtype=float)
UFO_CENTER = np.array([UFO_SHAPE[1] // 2, UFO_SHAPE[0] + 1], dtype=float)
UFO_DROP_TIME = FPS * 4
