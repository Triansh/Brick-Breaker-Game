import sys
import time
from random import randrange

import numpy as np

import config
from objects.brick import Brick
from objects.brickwall import BrickWall
from utils import util
from utils.kBHit import KBHit
from objects.ball import Ball
from objects.paddle import Paddle
from screen import Screen
from utils.powerupHandler import PowerUpHandler


class Game:
    def __init__(self):
        self.__counter = 1
        self.__run = True
        self.__screen = Screen()
        self.__balls = [Ball(id=0, position=config.BALL_POSITION)]
        self.__paddle = Paddle(position=config.PADDLE_POSITION, emoji="🧱",
                               shape=config.PADDLE_SHAPE)
        self.__brick_wall = BrickWall(position=config.WALL_POSITION, shape=config.WALL_SHAPE)
        self.__total_bricks = len(self.__brick_wall.get_all_bricks())
        self.__power_ups = []
        self.__powerup_handler = PowerUpHandler()
        self.__keys = KBHit()

        self.__lives = 7
        self.__frames_count = 0
        self.__score = 0

        util.hide_cursor()
        self.reset_ball_positions()

    def start(self):

        while self.__run:
            t = time.time()

            self.refresh()
            self.manage_key_hits()

            self.detect_collisions()

            self.check_life_lost()

            self.update_powerup_time()
            self.reset_ball_positions()

            self.update_score()

            self.draw_objects()
            t3 = time.time() - t

            self.__screen.show(self.__frames_count, self.__lives, self.__score,
                               len(self.__brick_wall.get_all_bricks()))

            t4 = time.time() - t - t3

            if len(self.__balls):
                pass
                # print( f"position : {self.__balls[0].get_position()}, direction : {self.__balls[0].get_direction()}")
                # print(f"power ups : {self.__powerups_list}")
            print(f"time :  {t3}, {t4}, {t3 + t4}")
            print(f"bricks : {len(self.__brick_wall.get_all_bricks())}")
            self.__frames_count += 1
            time.sleep(max(config.DELAY - (time.time() - t), 0))

    def update_score(self):
        self.__score = (self.__total_bricks - len(
            self.__brick_wall.get_all_bricks())) * config.SCORE_FACTOR

    def draw_objects(self):
        for brick in self.__brick_wall.get_all_bricks():
            self.__screen.draw(brick)
        for ball in self.__balls:
            self.__screen.draw(ball)
        self.__screen.draw(self.__paddle)
        for power_up in self.__power_ups:
            self.__screen.draw(power_up)

    def refresh(self):
        self.__screen.clear()
        util.position_cursor()

    def move_paddle(self, ch):
        self.__paddle.move(ch=ch)
        _ph, _pw = self.__paddle.get_shape()
        _px, _py = self.__paddle.get_position()
        for ball in self.__balls:
            _bx, _by = ball.get_position()
            _bw, _bh = ball.get_shape()
            if (not ball.is_released()) and (
                    _px <= _bx + _bw and _bx <= _px + _px and _by + 1 == _py):
                ball.add_position(self.__paddle.get_direction() * (1 if ch == 'd' else -1))

    def reset_ball_positions(self):  # TODO
        _ph, _pw = self.__paddle.get_shape()
        _px, _py = self.__paddle.get_position()
        for ball in self.__balls:
            _bx, _by = ball.get_position()
            _bw, _bh = ball.get_shape()
            if not (ball.is_released() or (
                    _px <= _bx + _bw and _bx <= _px + _pw and _by + 1 == _py)):
                _new_pos = self.__paddle.get_position() + np.array([randrange(1, _pw - 1), - 1])
                ball.set_position(_new_pos)

    def manage_key_hits(self):

        if self.__keys.kb_hit() is True:
            _ch = self.__keys.get_ch()
            if _ch == 'q':
                self.__run = False
            elif _ch == 'a' or _ch == 'd':
                self.move_paddle(_ch)
            elif _ch == ' ':
                for ball in self.__balls:
                    ball.set_release(True)
        self.__keys.clear()

    def remove_objects_after_missing_paddle(self, objs):
        _xp, _yp = self.__paddle.get_position()
        _hp, _wp = self.__paddle.get_shape()
        _pcx, _pcy = self.__paddle.get_center()

        to_remove = []
        for obj in objs:
            _x, _y = obj.get_position()
            _h, _w = obj.get_shape()
            if _y > _pcy and (_x > _xp + _wp or _x + _w < _xp):
                to_remove.append(obj)
        return [b for b in objs if b not in to_remove]

    def check_life_lost(self):

        self.__balls = self.remove_objects_after_missing_paddle(self.__balls)
        self.__power_ups = self.remove_objects_after_missing_paddle(self.__power_ups)

        if len(self.__balls) == 0:
            self.__lives -= 1
            if self.__lives == 0:
                self.__run = False
                return
            self.__balls.append(Ball(id=self.__counter, position=config.BALL_POSITION))
            self.__counter += 1
            self.reset_ball_positions()

    def detect_collisions(self):

        self.detect_power_up_paddle_collisions()
        for power_up in self.__power_ups:
            power_up.move()

        for ball in self.__balls:
            if ball.is_released():
                self.detect_ball_paddle_collisions(ball)
            if ball.is_released():
                if not self.detect_brick_collisions(ball):  # TODO
                    ball.move()

    def check_paddle_collisions(self, obj):
        _xb, _yb = obj.get_position()
        _hb, _wb = obj.get_shape()

        _xp, _yp = self.__paddle.get_position()
        _hp, _wp = self.__paddle.get_shape()

        return _yp <= _yb and _xp <= _xb + _wb and _xb <= _xp + _wp

    def detect_ball_paddle_collisions(self, ball):

        if not ball.is_released():
            return

        if not self.check_paddle_collisions(ball):
            return

        _xb, _yb = ball.get_position()
        _vx, _vy = ball.get_direction()
        _xc, _yc = self.__paddle.get_center()

        _vy *= -1
        _vx += (-1 if _xc - _xb >= 0 else 1) * self.__paddle.get_extra_velocity(_xb)
        ball.set_direction(np.array([_vx, _vy]))

        if self.__paddle.has_grabber_mode():
            ball.set_release(False)
            _xp, _yp = self.__paddle.get_position()
            _hp, _wp = self.__paddle.get_shape()
            _hb, _wb = ball.get_shape()
            ball.set_position(np.array([min(max(_xp, _xb), _xp + _wp - _wb), _yp - 1]))

    def detect_power_up_paddle_collisions(self):
        pass
        to_remove = []
        for power_up in self.__power_ups:
            if self.check_paddle_collisions(power_up):
                name = power_up.__class__.__name__
                if name == "BallMultiplier":
                    self.multiply_balls()
                elif name == "ShrinkPaddle":
                    self.__powerup_handler.activate_power_ups(name, paddle=self.__paddle,
                                                              expand=False)
                else:
                    self.__powerup_handler.activate_power_ups(name, paddle=self.__paddle,
                                                              balls=self.__balls)  # TODO
                to_remove.append(power_up)

        self.__power_ups = [p for p in self.__power_ups if p not in to_remove]

    def multiply_balls(self):
        to_add = []
        for ball in self.__balls:
            if ball.is_released():
                if len(self.__balls) + len(to_add) < config.MAXIMUM_BALLS:
                    to_add.append(
                        Ball(self.__counter, ball.get_position(), direction=-ball.get_direction(),
                             release=True, sp_factor=1))
                    self.__counter += 1
                else:
                    break
        self.__balls = self.__balls + to_add

    def update_powerup_time(self):
        pass
        self.__powerup_handler.update_power_ups(balls=self.__balls, paddle=self.__paddle)

    def detect_brick_collisions(self, ball):
        _dir = ball.get_direction()
        _bc = ball.get_center()
        _radius = ball.get_shape()  # minor axis(h) , major axis(w)
        _radius = [_radius[0] / 2, _radius[1] / 2]

        f = int(abs(_dir[0]) + abs(_dir[1]) + 1)

        c_bricks = []
        for idx in range(f + 1):

            curr_pos = _bc + (_dir * idx / f)

            for brick in self.__brick_wall.get_all_bricks():
                _x, _y = brick.get_position()
                _h, _w = brick.get_shape()

                if ((_x <= curr_pos[0] <= _x + _w) or (_x <= curr_pos[0] + _radius[1] <= _x + _w) or
                    (_x <= curr_pos[0] - _radius[1] <= _x + _w)) and \
                        ((_y <= curr_pos[1] <= _y + _h) or (
                                _y <= curr_pos[1] + _radius[0] <= _y + _h)
                         or (_y <= curr_pos[1] - _radius[0] <= _y + _h)):
                    c_bricks.append(brick)

            if (size := len(c_bricks)) > 0 and not ball.is_thru():
                _final_dir = np.zeros((size, 2))

                _prev_pos = curr_pos - (_dir / f)

                for index, brick in enumerate(c_bricks):

                    _next_dir = brick.reflect_obj(_prev_pos, _dir)
                    _final_dir[index] = _next_dir
                    brick.set_level(brick.get_level() - 1)
                    if brick.get_level() == 0:
                        self.destroy_and_check_for_powerup(brick)

                ball.set_direction(_final_dir[0])
                # ball.set_direction(np.mean(_final_dir, axis=0))
                # ball.set_position(_prev_pos.astype(int))  # TODO
                return False

        for brick in c_bricks:
            self.destroy_and_check_for_powerup(brick)

        return False

    def destroy_and_check_for_powerup(self, brick):
        _pos = brick.get_position()
        self.__brick_wall.destroy_brick(brick)
        new_power_up = self.__powerup_handler.create_power_up(_pos)
        if new_power_up is not None:
            self.__power_ups.append(new_power_up)

    def __del__(self):
        print("BYE")
        util.show_cursor()
