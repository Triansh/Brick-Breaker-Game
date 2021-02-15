import time

import numpy as np

import config
from objects.brick import Brick
from objects.brickwall import BrickWall
from utils import util
from utils.kBHit import KBHit
from objects.ball import Ball
from objects.paddle import Paddle
from screen import Screen


class Game:
    def __init__(self):
        self.__counter = 1
        self.__lives = 7
        self.__run = True
        self.__screen = Screen()
        self.__balls = [Ball(id=0, position=config.BALL_POSITION, emoji="🏐", shape=(1, 2),
                             direction=config.BALL_DIRECTION)]
        self.__paddle = Paddle(position=config.PADDLE_POSITION, emoji="🧱",
                               shape=config.PADDLE_SHAPE,
                               direction=np.array([2, 0]))
        self.__brickWall = BrickWall(position=config.WALL_POSITION, shape=config.WALL_SHAPE)
        self.__keys = KBHit()

        util.hide_cursor()
        # self.reset_ball_positions()

    def start(self):

        while self.__run:
            t = time.time()

            self.manage_key_hits()
            self.refresh()

            self.detect_collisions()

            self.move_objects()

            self.check_life_lost()
            t1 = time.time()

            self.draw_objects()

            self.__screen.show()

            t2 = time.time() - t1

            if len(self.__balls):
                print(f"position : {self.__balls[0].get_position()}")
                print(f"direction : {self.__balls[0].get_direction()}")
            print(f"time :  {t1 - t} , {t2}")
            print(f"lives : {self.__lives}")
            print(f"bricks : {len(self.__brickWall.get_all_bricks())}")

            time.sleep(max(config.DELAY - t, 0))

    def draw_objects(self):
        for brick in self.__brickWall.get_all_bricks():
            self.__screen.draw(brick)
        for ball in self.__balls:
            self.__screen.draw(ball)
        self.__screen.draw(self.__paddle)

        # self.__screen.draw(self.__brickWall)

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
                _pcx, _pcy = self.__paddle.get_center()
                _px, _py = self.__paddle.get_position()
                ball.set_position(np.array([int(_pcx), _py - 1]))

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

    def check_life_lost(self):
        _xp, _yp = self.__paddle.get_position()
        _hp, _wp = self.__paddle.get_shape()
        _pcx, _pcy = self.__paddle.get_center()

        to_remove = []
        for ball in self.__balls:
            _bx, _by = ball.get_position()
            _bh, _bw = ball.get_shape()
            if _by > _pcy and (_bx > _xp + _wp or _bx + _bw < _xp):
                to_remove.append(ball)

        for ball in to_remove:
            self.__balls.remove(ball)

        if len(self.__balls) == 0:
            self.__lives -= 1
            if self.__lives == 0:
                self.__run = False
                return
            self.__balls.append(
                Ball(id=self.__counter, position=config.BALL_POSITION, emoji="🏐", shape=(1, 2),
                     direction=config.BALL_DIRECTION))
            self.__counter += 1
            self.reset_ball_positions()

    def detect_collisions(self):

        for ball in self.__balls:
            if ball.is_released():
                self.detect_paddle_collisions(ball)
                self.detect_brick_collisions(ball)

    def detect_paddle_collisions(self, ball):
        _xb, _yb = ball.get_position()
        _hb, _wb = ball.get_shape()
        _vx, _vy = ball.get_direction()

        _xp, _yp = self.__paddle.get_position()
        _hp, _wp = self.__paddle.get_shape()
        _xc, _yc = self.__paddle.get_center()

        if _yp <= _yb <= _yp + _hp and _xp <= _xb + _wb and _xb <= _xp + _wp:
            _vy *= -1
            _vx += (-1 if _xc - _xb >= 0 else 1) * self.__paddle.get_extra_velocity(_xb)
            ball.set_direction(np.array([_vx, _vy]))

    def detect_brick_collisions(self, ball):

        _radius = 0.1

        _a, _b = ball.get_direction()
        f = int(abs(_a) + abs(_b) + 1)
        steps = (1000, 10)
        c_bricks = []

        for brick in self.__brickWall.get_all_bricks():

            curr_pos = ball.get_center()
            _x, _y = brick.get_position()
            _h, _w = brick.get_shape()

            for idx in range(f + 1):
                curr_pos += np.array([_a / f, _b / f])

                if ((_x <= curr_pos[0] <= _x + _w) or (_x <= curr_pos[0] + _radius <= _x + _w) or
                    (_x <= curr_pos[0] - _radius <= _x + _w)) and \
                        ((_y <= curr_pos[1] <= _y + _h) or (_y <= curr_pos[1] + _radius <= _y + _h)
                         or (_y <= curr_pos[1] - _radius <= _y + _h)):

                    if idx < steps[0]:
                        c_bricks = [brick]
                        steps = (idx, f)
                        break
                    elif idx == steps[0]:
                        c_bricks.append(brick)
                        break

        if not len(c_bricks):
            return

        _final_dir = np.zeros((len(c_bricks), 2))
        _xx, tot = steps[0] - 1, steps[1]

        for index, c_brick in enumerate(c_bricks):

            _dir = c_brick.reflect_obj(
                ball.get_center() + np.array([_xx * _a / tot, _xx * _b / tot]),
                ball.get_direction())

            _final_dir[index] = _dir
            # print(c_brick.get_id())
            if c_brick.get_level() == 0:
                self.__brickWall.destroy_brick(c_brick)
        ball.set_direction(_final_dir[0])

    def __del__(self):
        print("BYE")
        util.show_cursor()
