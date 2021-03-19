import numpy as np

from utils import config


class GameObject:

    def __init__(self, position, emoji, shape: np.array):
        """
        position: np.array -> [x, y]
        emoji : Emoji -> in form of string
        shape : tuple -> (height, width) or (row, col)
        rep : How the object is represented in game using emojis
        """
        self._emoji = emoji
        self._position = position
        self._shape = shape
        self.__rep = np.full(self._shape, '')
        self.set_emoji(emoji=emoji)

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position
        self._fix_position()

    def add_position(self, position):
        self._position += position
        self._fix_position()
        # print(self._position,self.get_shape())

    def _fix_position(self):
        _x, _y = self._position
        _h, _w = self.get_shape()
        _fix_x = min(max(0, _x), config.SCREEN_WIDTH - _w)
        _fix_y = min(max(0, _y), config.SCREEN_HEIGHT - _h)
        # print(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self._position = np.array([_fix_x, _fix_y], dtype=float)

    def get_center(self):
        _h, _w = self._shape
        return self._position + np.array([_w - 1, _h - 1], dtype=float) / 2

    def get_shape(self):
        return self._shape

    def set_shape(self, shape):
        self._shape = shape
        self._fix_position()
        self._make_rep()

    def get_emoji(self):
        return self._emoji

    def set_emoji(self, emoji):
        self._emoji = emoji
        self._make_rep()

    def _make_rep(self):
        _block = np.full(self._shape, ' ')
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                _block[i, j] = self._emoji if j % 2 == 0 else ''
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
        self._direction = direction
        super().__init__(position=position, emoji=emoji, shape=shape)

    def get_direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction
        self._fix_direction()

    def _fix_direction(self):
        self._direction[0] = max(min(self._direction[0], config.MAX_VELOCITY),
                                 -config.MAX_VELOCITY)
        self._direction[1] = max(min(self._direction[1], config.MAX_VELOCITY),
                                 -config.MAX_VELOCITY)

    def _handle_wall_reflection(self):
        """
        This function accounts for all collisions of ball with walls
        """
        _x, _y = self._position
        _h, _w = self._shape
        _direction = self._direction

        if _y <= 0:
            _direction[1] *= -1
        if _x <= 0 or _x >= config.SCREEN_WIDTH - _w:
            _direction[0] *= -1

        self.set_direction(_direction)

    def move(self, **kwargs):
        """
        This is a general function for all objects which move.
        Can be override by next child classes accordingly
        """
