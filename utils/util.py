from random import randrange

import numpy as np

import config
from objects.powerup import ExpandPaddle, ShrinkPaddle


def position_cursor():
    """
    This positions the cursor back to (0,0)
    """
    print("\033[0;0H")


def hide_cursor():
    print("\x1b[?25l")


def show_cursor():
    print("\x1b[?25h")


def seconds_to_frames(sec):
    frame_rate = 1 / config.DELAY
    return round(sec * frame_rate)


def get_power_up(id, position):
    return ExpandPaddle(id=id, position=position) if randrange(2) == 1 else ShrinkPaddle(id=id,
                                                                                         position=position)
