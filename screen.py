import colorama as col
from colorama import Fore, Back, Style
import numpy as np
import sys

import config
from objects.gameObject import GameObject
from utils import util


class Screen:
    """
    This sets the layout of screen in terminal.
    """

    def __init__(self):
        """
        Constructor for the screen.
        """
        self.display: np.array
        self.width = config.SCREEN_WIDTH
        self.height = config.SCREEN_HEIGHT
        self.clear()

    def clear(self):
        self.display = np.full((self.height, self.width), " ")

    def draw(self, obj: GameObject):
        """
        This will print the given object on screen
        """
        # print(obj.__class__.__name__, obj.get_position())
        _x, _y = obj.get_position()
        _h, _w = obj.get_shape()
        display = obj.get_rep()

        _x = int(_x)
        _y = int(_y)

        self.display[_y:_y + _h, _x:_x + _w] = display

    def show(self, frames, lives, score):
        """
        Displaying the screen.
        """

        _w = self.width
        for index, a in enumerate(self.display):
            a = list(a)
            empty, space = a.count(''), a.count(' ')
            extra = _w - (empty * 2) - space
            if extra:
                try:
                    last_index = len(a) - 1 - a[::-1].index(' ')
                    self.display[index, last_index] = ''
                except Exception:
                    continue

        _barrier_style = "".join((Fore.LIGHTGREEN_EX, config.BG_COLOR, Style.BRIGHT))
        _style = "".join((Fore.WHITE, Style.BRIGHT))

        more_things = [
            (_barrier_style + 'X') * _w,
            _style + f"  ⏰ Time  : {util.frames_to_time(frames)}",
            _style + f"  💕 Lives : {lives}",
            _style + f"  🌟 Score : {score}",
        ]

        more_string = "\n".join(
            (_barrier_style + 'X' +
             x + ' ' * (_w - len(x)) +
             _barrier_style + 'X')
            for x in more_things)

        finalOutput = ""
        finalOutput += "".join((config.BG_COLOR, config.STYLE))

        finalOutput += more_string + "\n" + \
                       "\n".join((
                           (_barrier_style + 'X' + "".join(x) + _barrier_style + 'X')
                           for x in self.display
                       ))
        finalOutput += '\n'

        sys.stdout.write(finalOutput + col.Style.RESET_ALL)
