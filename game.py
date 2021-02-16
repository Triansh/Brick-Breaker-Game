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


class Game:
    def __init__(self):
        self.__counter = 1
        self.__lives = 7
        self.__run = True
        self.__screen = Screen()
        self.__balls = [Ball(id=0, position=config.BALL_POSITION, emoji="🏐", shape=(1, 2),
                             direction=config.BALL_DIRECTION)]
        self.__paddle = Paddle(position=config.PADDLE_POSITION, emoji="🧱",
                               shape=config.PADDLE_SHAPE)
        self.__brick_wall = BrickWall(position=config.WALL_POSITION, shape=config.WALL_SHAPE)
        self.__power_ups = []
        self.__powerups_list = config.POWER_UP_LIST
        self.__keys = KBHit()

        util.hide_cursor()
        self.reset_ball_positions()

    def start(self):

        while self.__run:
            t = time.time()

            self.reset_ball_positions()
            self.manage_key_hits()
            self.refresh()

            self.detect_collisions()

            self.check_life_lost()
            self.update_powerup_time()

            self.draw_objects()

            self.__screen.show()

            t = time.time() - t

            if len(self.__balls):
                print(
                    f"position : {self.__balls[0].get_position()}, direction : {self.__balls[0].get_direction()}")
                print(f"power ups : {self.__powerups_list}")
            print(f"time : {t}, lives : {self.__lives}")
            print(f"decider : {self.__paddle.get_shape_decider()}")
            print(f"bricks : {len(self.__brick_wall.get_all_bricks())}")

            time.sleep(max(config.DELAY - t, 0))

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

    def update_powerup_time(self):
        for power_up_name, value in self.__powerups_list.items():

            if value['time'] - 1 == 0:
                self.deactivate_powerups(power_up_name)
            value['time'] = max(0, value['time'] - 1)

    def deactivate_powerups(self, name):
        if name == "ExpandPaddle":
            # sys.exit()
            self.__paddle.update_shape_decider(-1)
        elif name == "ShrinkPaddle":
            self.__paddle.update_shape_decider(1)

        elif name == "BallMultiplier":
            pass

        elif name == "ThruBall ":
            pass

        elif name == "FastBall":
            pass

        elif name == "PaddleGrab":
            pass

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
            self.__balls.append(
                Ball(id=self.__counter, position=config.BALL_POSITION, emoji="🏐", shape=(1, 2),
                     direction=config.BALL_DIRECTION))
            self.__counter += 1
            self.reset_ball_positions()

    def detect_collisions(self):

        for ball in self.__balls:
            if ball.is_released():
                self.detect_ball_paddle_collisions(ball)
                if not self.detect_brick_collisions(ball): #TODO
                    ball.move()

        self.detect_power_up_paddle_collisions()
        for power_up in self.__power_ups:
            power_up.move()

    def check_paddle_collisions(self, obj):
        _xb, _yb = obj.get_position()
        _hb, _wb = obj.get_shape()

        _xp, _yp = self.__paddle.get_position()
        _hp, _wp = self.__paddle.get_shape()

        return _yp <= _yb <= _yp + _hp and _xp <= _xb + _wb and _xb <= _xp + _wp

    def detect_ball_paddle_collisions(self, ball):

        if not self.check_paddle_collisions(ball):
            return

        _xb, _yb = ball.get_position()
        _vx, _vy = ball.get_direction()
        _xc, _yc = self.__paddle.get_center()

        _vy *= -1
        _vx += (-1 if _xc - _xb >= 0 else 1) * self.__paddle.get_extra_velocity(_xb)
        ball.set_direction(np.array([_vx, _vy]))

    def detect_power_up_paddle_collisions(self):
        to_remove = []
        for power_up in self.__power_ups:
            if self.check_paddle_collisions(power_up):
                power_up.activate(paddle=self.__paddle)
                name = power_up.__class__.__name__
                dic = self.__powerups_list
                dic[name]['time'] += dic[name]['duration']
                to_remove.append(power_up)

        self.__power_ups = [p for p in self.__power_ups if p not in to_remove]

    def detect_brick_collisions(self, ball):
        _dir = ball.get_direction()
        _bc = ball.get_center()
        _radius = ball.get_shape()  # minor axis(h) , major axis(w)
        _radius = [_radius[0] / 2, _radius[1] / 2]

        f = int(abs(_dir[0]) + abs(_dir[1]) + 1)

        for idx in range(f + 1):

            curr_pos = _bc + (_dir * idx / f)
            c_bricks = []

            for brick in self.__brick_wall.get_all_bricks():
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
                        _pos = brick.get_position()
                        self.__brick_wall.destroy_brick(brick)
                        new_power_up = util.get_power_up(self.__counter, _pos)
                        self.__power_ups.append(new_power_up)

                ball.set_direction(_final_dir[0])
                # ball.set_direction(np.mean(_final_dir, axis=0))
                # ball.set_position(_prev_pos.astype(int))  # TODO
                return False
        return False

    def __del__(self):
        print("BYE")
        util.show_cursor()
