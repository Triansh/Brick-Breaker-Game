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
        self.display: np.array
        self.color: np.array
        self.width = config.SCREEN_WIDTH
        self.height = config.SCREEN_HEIGHT
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
        _x, _y = obj.get_position()
        _h, _w = obj.get_shape()
        display = obj.get_rep()

        self.display[_y:_y + _h, _x:_x + _w] = display

    def show(self):
        """
        Displaying the screen.
        """
        _barrier_color = (Fore.LIGHTGREEN_EX, config.BG_COLOR, Style.NORMAL)

        finalOutput = ""
        for j in range(self.width + 2):
            finalOutput += "".join(_barrier_color) + 'X'
        finalOutput += "\n"

        for i in range(self.height):
            finalOutput += "".join(_barrier_color) + 'X'
            for j in range(self.width):
                finalOutput += "".join(self.color[i][j]) + self.display[i][j]
            finalOutput += "".join(_barrier_color) + 'X'
            finalOutput += "\n"

        sys.stdout.write(finalOutput + col.Style.RESET_ALL)

