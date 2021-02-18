import numpy as np
from colorama import Fore, Style, Back

import config
from utils import util
from objects.gameObject import MovingObject


class Paddle(MovingObject):

    def __init__(self, position, emoji, shape):
        self.__grabber_mode = False
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

    def update_shape_decider(self, decider):
        self.__shape_decider = decider
        self.set_shape(self.__paddle_shapes[self.__shape_decider])
        self.set_emoji()

    def get_shape_decider(self):  # TODO
        return self.__shape_decider

    def has_grabber_mode(self):
        return self.__grabber_mode

    def set_grabber_mode(self, mode: bool):
        self.__grabber_mode = mode
        self.set_emoji()

    def set_emoji(self, emoji="🧱"):
        if self.__shape_decider == -1:
            emoji = '😖'
        elif self.__shape_decider == 1:
            emoji = '🤓'
        super().set_emoji(emoji=emoji)

    def make_rep(self):
        if not self.__grabber_mode:
            super().make_rep()
            return

        _shape = self.get_shape()
        _emoji = self.get_emoji()
        _block = np.full(_shape, ' ')
        for i in range(_shape[0]):
            _block[i, 0], _block[i, 1] = '🧲', ''
            for j in range(2, _shape[1] - 2):
                _block[i, j] = _emoji if j % 2 == 0 else ''
            _block[i, -2], _block[i, -1] = '🧲', ''
        self.set_rep(_block)
