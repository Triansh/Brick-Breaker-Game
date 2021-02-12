from colorama import Fore, Back, Style

import config
from utils import util
from art import BALL

from objects.gameObject import MovingObject


class Ball(MovingObject):

    def __init__(self):
        self.__released = False

        pos = config.INI_BALL_POSITION
        rep = util.str_to_array(BALL)
        rep[0, 1] = ''
        color = util.form_color_array(rep.shape, (Fore.RED, Back.LIGHTBLACK_EX, Style.BRIGHT))
        velocity = config.BALL_VELOCITY

        super().__init__(position=pos, rep=rep, color=color, velocity=velocity)

    def move(self, **kwargs):
        self.reflect_from_wall()
        self.add_position(self.get_velocity())

    def reflect_from_wall(self):
        """
        This function account for all collisions with walls
        """
        _y, _x = self.get_position()
        _h, _w = self.get_shape()
        _velocity = self.get_velocity()
        _max_width = config.SCREEN_WIDTH

        if _y == 0:
            _velocity[0] *= -1
        if _x == 0 or _x == _max_width - _w:
            _velocity[1] *= -1

        self.set_velocity(_velocity)
