from random import randrange

import numpy as np

import config
from objects.gameObject import GameObject


class Brick(GameObject):

    def __init__(self, id, position, level, shape=(1, 2)):
        self.__bricks = config.BRICKS
        self.__id = id
        self.__level = level

        emoji = self.__bricks[self.__level - 1]  # TODO
        super().__init__(position=position, emoji=emoji, shape=shape)

    def get_id(self):
        return self.__id

    def get_level(self):
        return self.__level

    def set_level(self, level):
        self.__level = 0 if level < 0 else level
        self.set_emoji(self.__bricks[0 if self.__level - 1 < 0 else (self.__level - 1)])

    def reflect_obj(self, pos, direction):
        _x, _y = pos
        _dx, _dy = direction

        _bx, _by = self.get_position()
        _h, _w = self.get_shape()

        if _by <= _y <= _by + _h and (_x <= _bx or _x >= _bx + _w):
            _dx *= -1
        elif _bx <= _x <= _bx + _w and (_y <= _by or _y >= _by + _h):
            _dy *= -1
        else:
            _dx *= -1
            _dy *= -1

        self.set_level(self.__level - 1)

        return np.array([_dx, _dy])
