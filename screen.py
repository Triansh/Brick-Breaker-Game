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
        self.__display: np.array
        self.__width = config.SCREEN_WIDTH
        self.__height = config.SCREEN_HEIGHT
        self.clear()

    def clear(self):
        self.__display = np.full((self.__height, self.__width), " ")

    def draw(self, obj: GameObject):
        """
        This will print the given object on screen
        """
        _x, _y = obj.get_position()
        _h, _w = obj.get_shape()
        display = obj.get_rep()

        _x, _y = int(_x), int(_y)
        self.__display[_y:_y + _h, _x:_x + _w] = display

    def show(self, frames, lives, score, bricks):
        """
        Displaying the screen.
        """

        _w = self.__width
        for index, a in enumerate(self.__display):
            a = list(a)
            empty, space = a.count(''), a.count(' ')
            extra = _w - (empty * 2) - space
            if extra:
                try:
                    last_index = len(a) - 1 - a[::-1].index(' ')
                    self.__display[index, last_index] = ''
                except Exception:
                    continue

        _barrier_style = (Fore.LIGHTGREEN_EX, config.BG_COLOR, Style.BRIGHT)
        _style = (Fore.WHITE, Style.BRIGHT)

        single_x = "".join(_barrier_style) + 'X'
        single_sp = "".join(_style) + ' '
        item_1 = [
            "".join(_style) + f"  💕 Lives : {lives}",
            "".join(_style) + f"⏰ Time  : {util.frames_to_time(frames)}  "]
        item_2 = [
            "".join(_style) + f"  🌟 Score : {score}",
            "".join(_style) + f"🧱 Bricks: {bricks}  "]

        row = ['' for x in range(4)]
        row[0] = row[3] = single_x * (self.__width + 2)
        row[1] = single_x + item_1[0] + single_sp * (
                16 + self.__width - len(item_1[0]) - len(item_1[1])) + item_1[1] + single_x
        row[2] = single_x + item_2[0] + single_sp * (
                16 + self.__width - len(item_2[0]) - len(item_2[1])) + item_2[1] + single_x

        top_bar = "\n".join(x for x in row)

        finalOutput = ""
        finalOutput += "".join((config.BG_COLOR, config.STYLE))

        finalOutput += top_bar + "\n" + \
                       "\n".join((
                           ("".join(_barrier_style) + 'X' + "".join(x) + "".join(
                               _barrier_style) + 'X')
                           for x in self.__display
                       ))
        finalOutput += '\n'

        sys.stdout.write(finalOutput + col.Style.RESET_ALL)
