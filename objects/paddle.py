import numpy as np
from colorama import Fore, Style, Back

import config
from utils import util
from art import PADDLE
from objects.gameObject import MovingObject


class Paddle(MovingObject):

    def __init__(self):
        position = config.PADDLE_POSITION
        rep = util.str_to_array(PADDLE)
        color = util.form_color_array(rep.shape, (Fore.LIGHTRED_EX, Style.BRIGHT))
        velocity = config.PADDLE_VELOCITY
        super().__init__(position, rep, color, velocity)

    def get_center(self):
        _pos = self.get_position()
        _shape = self.get_shape()
        return _pos + np.array([0, _shape[1] // 2])

    def move(self, **kwargs):
        _ch = kwargs['ch'].lower()
        _velocity = self.get_velocity()

        self.add_position(_velocity if _ch == 'd' else -_velocity)
