import numpy as np
from colorama import Fore, Style, Back

import config
from utils import util
from objects.gameObject import MovingObject


class Paddle(MovingObject):

    def __init__(self, position, emoji, shape, direction=np.array([2, 0])):
        super().__init__(position=position, emoji=emoji, shape=shape, direction=direction)

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
