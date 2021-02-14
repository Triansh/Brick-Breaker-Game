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
        self.__run = True
        self.__screen = Screen()
        self.__balls = [Ball(config.BALL_POSITION, "🏐", (1, 2))]
        self.__paddle = Paddle(config.PADDLE_POSITION, "🧱", config.PADDLE_SHAPE,
                               direction=np.array([2, 0]))
        self.__keys = KBHit()

        util.hide_cursor()
        self.reset_ball_positions()

    def start(self):

        while self.__run:
            time.sleep(config.DELAY)
            self.manage_key_hits()
            self.refresh()

            self.check_for_collisions()
            self.move_objects()
            self.draw_objects()

            self.__screen.show()

    def draw_objects(self):
        for ball in self.__balls:
            self.__screen.draw(ball)
        self.__screen.draw(self.__paddle)

    def move_objects(self):
        for ball in self.__balls:
            ball.move()


    def refresh(self):
        self.__screen.clear()
        util.position_cursor()

    def move_paddle(self, ch):
        self.__paddle.move(ch=ch)
        self.reset_ball_positions()

    def reset_ball_positions(self):
        for ball in self.__balls:
            if not ball.is_released():
                ball.set_position(self.__paddle.get_center() + np.array([0, -1]))

    def manage_key_hits(self):

        if self.__keys.kb_hit() is True:
            _ch = self.__keys.get_ch()
            self.__keys.clear()
            if _ch == 'q':
                self.__run = False
            elif _ch == 'a' or _ch == 'd':
                self.move_paddle(_ch)
            elif _ch == ' ':
                for ball in self.__balls:
                    ball.release()
        else:
            self.__keys.clear()

    def check_for_collisions(self):
        for ball in self.__balls:
            _xb, _yb = ball.get_position()
            _hb, _wb = ball.get_shape()
            _vx, _vy = ball.get_direction()

            _xp, _yp = self.__paddle.get_position()
            _hp, _wp = self.__paddle.get_shape()
            _xc, _yc = self.__paddle.get_center()

            if _yb == _yp and _xb + _wb >= _xp and _xb <= _xp + _wp:
                _vy *= -1
                _vx += (-1 if _xc - _xb >= 0 else 1) * self.__paddle.get_extra_velocity(_xb)
                ball.set_direction(np.array([_vx, _vy]))

    def __del__(self):
        print("BYE")
        util.show_cursor()
