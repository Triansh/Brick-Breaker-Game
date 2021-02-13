import time

import numpy as np

import config
from utils import util
from utils.kBHit import KBHit
from objects.ball import Ball
from objects.paddle import Paddle
from screen import Screen


class Game:
    def __init__(self):
        self.__screen = Screen()
        self.ball = Ball()
        self.paddle = Paddle()

        util.hide_cursor()

    def start(self):
        kb_inp = KBHit()

        while True:
            time.sleep(config.DELAY)

            if kb_inp.kb_hit() is True:
                if self.manage_key_hits(kb_inp):
                    break
            else:
                kb_inp.clear()

            self.refresh()

            self.check_for_collisions()
            self.ball.move()
            self.__screen.draw(self.ball)
            self.__screen.draw(self.paddle)

            self.__screen.show()

    def refresh(self):
        self.__screen.clear()
        util.position_cursor()

    def move_paddle(self, ch):
        self.paddle.move(ch=ch)
        if not self.ball.is_active():
            self.ball.set_position(self.paddle.get_center() + np.array([-1, 0]))

    def manage_key_hits(self, kb_inp):

        _ch = kb_inp.get_ch()
        kb_inp.clear()
        if _ch == 'q':
            return True
        elif _ch == 'a' or _ch == 'd':
            self.move_paddle(_ch)
        elif _ch == ' ':
            self.ball.activate()
        return False

    def check_for_collisions(self):
        _yb, _xb = self.ball.get_position()
        _yp, _xp = self.paddle.get_position()
        _yc, _xc = self.paddle.get_center()

        _hb, _wb = self.paddle.get_shape()
        _hp, _wp = self.paddle.get_shape()

        _vy, _vx = self.ball.get_velocity()

        if _yb  == _yp and _xb + _wb >= _xp and _xb <= _xp + _wp:
            _vy *= -1
            extra_vel = int(abs(_xc - _xb) * config.VELOCITY_INCREASE_FACTOR)
            _vx += (-1 if _xc - _xb >= 0 else 1) * extra_vel
            self.ball.set_velocity(np.array([_vy, _vx]))

    def __del__(self):
        print("BYE")
        util.show_cursor()
