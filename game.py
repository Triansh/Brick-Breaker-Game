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
        self.reset_ball_positions()

    def start(self):

        while self.__run:
            t = time.time()

            self.manage_key_hits()
            self.refresh()

            self.detect_collisions()

            # self.move_objects()

            self.check_life_lost()

            self.draw_objects()

            self.__screen.show()

            t = time.time() - t

            if len(self.__balls):
                print(f"position : {self.__balls[0].get_position()}")
                print(f"direction : {self.__balls[0].get_direction()}")
            print(f"time :   {t}")
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

    # def move_objects(self):
    #     for ball in self.__balls:

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
                if not self.detect_brick_collisions(ball):
                    ball.move()

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

        _dir = ball.get_direction()
        _bc = ball.get_center()
        _radius = ball.get_shape()  # minor axis(h) , major axis(w)
        _radius = [_radius[0] / 2, _radius[1] / 2]

        f = int(abs(_dir[0]) + abs(_dir[1]) + 1)

        for idx in range(f + 1):

            curr_pos = _bc + (_dir * idx / f)
            c_bricks = []

            for brick in self.__brickWall.get_all_bricks():
                _x, _y = brick.get_position()
                _h, _w = brick.get_shape()

                if ((_x <= curr_pos[0] <= _x + _w) or (_x <= curr_pos[0] + _radius[1] <= _x + _w) or
                    (_x <= curr_pos[0] - _radius[1] <= _x + _w)) and \
                        ((_y <= curr_pos[1] <= _y + _h) or (
                                _y <= curr_pos[1] + _radius[0] <= _y + _h)
                         or (_y <= curr_pos[1] - _radius[0] <= _y + _h)):
                    c_bricks.append(brick)

            if (size := len(c_bricks)) > 0:
                _final_dir = np.zeros((size, 2))

                _prev_pos = curr_pos - (_dir / f)

                for index, brick in enumerate(c_bricks):

                    _next_dir = brick.reflect_obj(_prev_pos, _dir)

                    _final_dir[index] = _next_dir
                    brick.set_level(brick.get_level() - 1)
                    if brick.get_level() == 0:
                        self.__brickWall.destroy_brick(brick)

                ball.set_direction(_final_dir[0])
                # ball.set_direction(np.mean(_final_dir, axis=0))
                # ball.set_position(_prev_pos.astype(int))  # TODO
                return False
        return False

    def __del__(self):
        print("BYE")
        util.show_cursor()
