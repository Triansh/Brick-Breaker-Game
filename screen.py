from colorama import Style
import numpy as np
import sys

from objects.gameObject import GameObject
from utils import util, config


class Screen:
    def __init__(self):
        """
        display: np.array : Contains the characters to display on screen
        width: Integer: Screen width
        height: Integer: Screen Height
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

        _x, _y = round(_x), round(_y)
        self.__display[_y:_y + _h, _x:_x + _w] = display

    def __get_top_bar(self, frames, lives, score, bricks):
        """
        Designing of Top Bar
        """
        _style = config.TEXT_STYLE

        single_x = "".join(config.BARRIER_STYLE) + 'X'
        single_sp = "".join(_style) + ' '
        item_1 = [
            "".join(_style) + f"  💕 Lives : {lives}",
            "".join(_style) + f"⏰ Time  : {util.frames_to_time(frames)}  "]
        item_2 = [
            "".join(_style) + f"  🌟 Score : {score}",
            "".join(_style) + f"🧱 Bricks: {bricks}  "]

        row = ['', '', '', '']
        row[0] = row[3] = single_x * (self.__width + 2)
        row[1] = single_x + item_1[0] + single_sp * (
                16 + self.__width - len(item_1[0]) - len(item_1[1])) + item_1[1] + single_x
        row[2] = single_x + item_2[0] + single_sp * (
                16 + self.__width - len(item_2[0]) - len(item_2[1])) + item_2[1] + single_x

        top_bar = "\n".join(x for x in row) + '\n'
        return top_bar

    def show(self, frames, lives, score, bricks):
        _w = self.__width
        for index, a in enumerate(self.__display):
            a = list(a)
            empty, space = a.count(''), a.count(' ')
            extra = _w - (empty * 2) - space
            if extra:
                try:
                    last_index = len(a) - 1 - a[::-1].index(' ')
                    self.__display[index, last_index] = ''
                except ValueError:
                    continue

        single_x = "".join(config.BARRIER_STYLE) + 'X'

        finalOutput = ""
        finalOutput += "".join(config.BACKGROUND_STYLE)

        finalOutput += self.__get_top_bar(frames, lives, score, bricks) + \
                       "\n".join((
                           (single_x + "".join(x) + single_x) for x in self.__display
                       )) + '\n'
        sys.stdout.write(finalOutput + Style.RESET_ALL)
