import numpy as np
from colorama import Fore, Back, Style

import config
from utils import util

from objects.gameObject import MovingObject


class Ball(MovingObject):

    def __init__(self, id, position, emoji, shape, direction=config.BALL_DIRECTION, sp_factor=0):
        """
        sp_factor is the multiplying factor for direction to increase the velocity of ball
        """
        self.__id = id
        self.__sp_factor = sp_factor
        super().__init__(position=position, emoji=emoji, shape=shape, direction=direction)

    def get_sp_factor(self):
        return self.__sp_factor

    def set_sp_factor(self, sp_factor):
        self.__sp_factor = sp_factor

    def release(self):
        if self.__sp_factor == 0:
            self.__sp_factor = 1

    def is_released(self):
        return self.__sp_factor != 0

    def move(self, **kwargs):
        self.handle_wall_reflection()
        self.add_position(self.get_direction() * self.__sp_factor)

    def handle_wall_reflection(self):
        """
        This function accounts for all collisions with walls
        """
        _x, _y = self.get_position()
        _h, _w = self.get_shape()
        _direction = self.get_direction()

        if _y <= 0:
            _direction[1] *= -1
        if _x <= 0 or _x >= config.SCREEN_WIDTH - _w:
            _direction[0] *= -1

        self.set_direction(_direction)
