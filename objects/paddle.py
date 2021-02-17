import numpy as np
from colorama import Fore, Style, Back

import config
from utils import util
from objects.gameObject import MovingObject


class Paddle(MovingObject):

    def __init__(self, position, emoji, shape):
        self.__shape_decider = 0
        self.__paddle_shapes = config.PADDLE_SHAPES
        _dir = config.PADDLE_VELOCITY
        super().__init__(position=position, emoji=emoji, shape=shape, direction=_dir)

    def move(self, **kwargs):
        _ch = kwargs['ch'].lower()
        _direction = self.get_direction()
        self.add_position(_direction if _ch == 'd' else -_direction)

    def get_extra_velocity(self, xb):
        """
        This function tells how much extra velocity must be added to ball when it hits the paddle
        """
        _pcx, _pcy = self.get_center()
        return int(8 * abs(int(_pcx) - xb) / self.get_shape()[1])

    def update_shape_decider(self, decider):
        _d = self.__shape_decider
        self.__shape_decider = decider
        self.set_shape(self.__paddle_shapes[self.__shape_decider])

    def get_shape_decider(self):  # TODO
        return self.__shape_decider
