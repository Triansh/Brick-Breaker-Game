import numpy as np
from colorama import Fore, Style

import config
from utils import util
from art import PADDLE
from objects.gameObject import MovingObject


class Paddle(MovingObject):

    def __init__(self):
        rep = util.str_to_array(PADDLE)
        _h, _w = rep.shape
        position = np.array([config.SCREEN_HEIGHT - _h - 3, (config.SCREEN_WIDTH - _w) // 2])
        color = util.form_color_array(rep.shape, (Fore.RED, Style.BRIGHT))
        velocity = config.PADDLE_VELOCITY
        super().__init__(position, rep, color, velocity)

    def move(self, **kwargs):
        _ch = kwargs['ch'].lower()
        _velocity = self.get_velocity()

        self.add_position(_velocity if _ch == 'd' else -_velocity)
