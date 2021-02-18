import numpy as np

import config


class GameObject:

    def __init__(self, position, emoji, shape: np.array):
        """
        position: np.array -> [x, y]
        rep : Emoji -> in form of string
        shape : tuple -> (height, width) or (row, col)
        """
        self.__position = position
        self.__shape = shape
        self.__rep: np.array
        self.__emoji: str
        self.set_emoji(emoji=emoji)

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position
        self.fix_position()

    def add_position(self, position):
        self.__position += position
        self.fix_position()

    def fix_position(self):
        _x, _y = self.get_position()
        _h, _w = self.get_shape()
        _fix_x = min(max(0, _x), config.SCREEN_WIDTH - _w)
        _fix_y = min(max(0, _y), config.SCREEN_HEIGHT - _h)
        self.__position = np.array([_fix_x, _fix_y], dtype=float)

    def get_center(self):
        _h, _w = self.__shape
        return self.__position + np.array([_w - 1, _h - 1]) / 2

    def get_shape(self):
        return self.__shape

    def set_shape(self, shape):
        self.__shape = shape
        self.fix_position()
        self.make_rep()

    def get_emoji(self):
        return self.__emoji

    def set_emoji(self, emoji):
        self.__emoji = emoji
        self.make_rep()

    def make_rep(self):
        _block = np.full(self.__shape, ' ')
        for i in range(self.__shape[0]):
            for j in range(self.__shape[1]):
                _block[i, j] = self.__emoji if j % 2 == 0 else ''
        self.__rep = _block

    def get_rep(self):
        return self.__rep

    def set_rep(self, rep):
        self.__rep = rep


class MovingObject(GameObject):
    def __init__(self, position, emoji, shape, direction):
        """
        direction is the amount by which the ball moves in [x, y] direction
        """
        self.__direction = direction
        super().__init__(position=position, emoji=emoji, shape=shape)

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction
        self.fix_direction()

    def fix_direction(self):
        self.__direction[0] = max(min(self.__direction[0], config.MAX_VELOCITY),
                                  -config.MAX_VELOCITY)
        self.__direction[1] = max(min(self.__direction[1], config.MAX_VELOCITY),
                                  -config.MAX_VELOCITY)

    def move(self, **kwargs):
        """
        This is a general function for all objects which move.
        Can be override by next child classes accordingly
        """


class StaticObject(GameObject):
    pass
