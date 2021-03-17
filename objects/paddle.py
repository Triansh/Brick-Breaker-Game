import sys

import numpy as np

from utils import config
from objects.gameObject import MovingObject


class Paddle(MovingObject):

    def __init__(self, position, emoji, shape):
        """
        paddle_shapes: list(shape): Shapes of paddles
        grabber_mode: Boolean : True if Paddle Grab Power up is activated
        shape_decider: Integer -> {-1,0,1} : Which shape paddle must take
        """
        self.__grabber_mode = False
        self.__shooter_mode = False
        self.__shape_decider = 0
        self.__paddle_shapes = config.PADDLE_SHAPES
        _dir = config.PADDLE_VELOCITY
        super().__init__(position=position, emoji=emoji, shape=shape, direction=_dir)

    def move(self, **kwargs):
        _direction = self.get_direction()
        self.add_position(_direction if kwargs['ch'] == 'd' else -_direction)

    def get_extra_velocity(self, xb):
        """
        This function tells how much extra velocity must be added to ball when it hits the paddle
        """
        _pcx, _pcy = self.get_center()
        return int(8 * abs(int(_pcx) - xb) / self.get_shape()[1])

    def get_shape_decider(self):
        return self.__shape_decider

    def update_shape_decider(self, decider):
        self.__shape_decider = decider
        self.set_shape(self.__paddle_shapes[self.__shape_decider])
        self.set_emoji()

    def has_grabber_mode(self):
        return self.__grabber_mode

    def set_grabber_mode(self, mode: bool):
        self.__grabber_mode = mode
        self.set_emoji()

    def has_shooter_mode(self):
        return self.__shooter_mode

    def set_shooter_mode(self, mode: bool):
        self.__shooter_mode = mode
        self.set_emoji()

    def set_emoji(self, emoji="🧱"):
        if self.__shape_decider == -1:
            emoji = '😖'
        elif self.__shape_decider == 1:
            emoji = '🤓'
        super().set_emoji(emoji=emoji)

    def _make_rep(self):

        _shape = self.get_shape()
        _emoji = self.get_emoji()
        _block = np.full(_shape, ' ')

        for i in range(_shape[0]):
            for j in range(_shape[1]):
                _block[i, j] = _emoji if j % 2 == 0 else ''
            if self.__grabber_mode:
                _block[i, 0], _block[i, 1] = '🧲', ''
                _block[i, -2], _block[i, -1] = '🧲', ''

        if self.__shooter_mode:
            _block[0, 0], _block[0, 1] = _block[0, -2], _block[0, -1] = '💄', ''
        self.set_rep(_block)
