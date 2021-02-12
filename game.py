import time

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

    def refresh(self):

        self.__screen.clear()
        util.position_cursor()

    def draw_ball(self):
        self.ball.move()
        self.__screen.draw(self.ball)

    def manage_keyhits(self, kb_inp):

        _ch = kb_inp.get_ch()
        kb_inp.clear()
        if _ch == 'q':
            return True
        elif _ch == 'a' or _ch == 'd':
            self.paddle.move(ch=_ch)
        return False

    def start(self):
        kb_inp = KBHit()

        while True:
            time.sleep(config.DELAY)

            if kb_inp.kb_hit() is True:
                # kb_inp.clear()
                if self.manage_keyhits(kb_inp):
                    break
            else:
                kb_inp.clear()

            self.refresh()

            self.draw_ball()
            self.__screen.draw(self.paddle)

            self.__screen.show()

    def __del__(self):
        print("BYE")
        util.show_cursor()
