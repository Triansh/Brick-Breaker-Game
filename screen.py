import colorama as col
from colorama import Fore, Back, Style
import numpy as np
import sys

import config
from objects.gameObject import GameObject


class Screen:
    """
    This sets the layout of screen in terminal.
    """

    def __init__(self):
        """
        Constructor for the screen.
        """
        self.width, self.height = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        self.clear()

    def clear(self):
        self.display = np.full((self.height, self.width), " ")
        val = np.empty((), dtype=object)
        val[()] = (config.FG_COLOR, config.BG_COLOR, config.STYLE)

        self.color = np.full((self.height, self.width), val, dtype=object)

    def draw(self, obj: GameObject):
        """
        This will print the given object on screen
        """
        _y, _x = obj.get_position()
        _h, _w = obj.get_shape()

        display, color = obj.get_rep()

        minx = min(max(0, _x), self.width - 1 - _w)
        miny = min(max(0, _y), self.height - _h)

        # print(minx, miny, obj.__class__.__name__, obj.get_position(), obj.get_shape())

        self.display[miny:miny + _h, minx:minx + _w] = display
        self.color[miny:miny + _h, minx:minx + _w] = color

    def show(self):
        """
        Displaying the screen.
        """
        finalOutput = ""
        for j in range(self.width + 1):
            finalOutput += "".join((Fore.LIGHTGREEN_EX, config.BG_COLOR, Style.NORMAL)) + 'X'
        finalOutput += "\n"

        for i in range(self.height):
            finalOutput += "".join((Fore.LIGHTGREEN_EX, config.BG_COLOR, Style.BRIGHT)) + 'X'
            for j in range(self.width - 1):
                finalOutput += "".join(self.color[i][j]) + self.display[i][j]
            finalOutput += "".join((Fore.LIGHTGREEN_EX, config.BG_COLOR, Style.BRIGHT)) + 'X'
            finalOutput += "\n"

        sys.stdout.write(finalOutput + col.Style.RESET_ALL)
