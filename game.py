import time
from random import randrange
import numpy as np
import sys
import copy

from objects.ball import Ball
from objects.bullet import Bullet
from objects.paddle import Paddle
from screen import Screen

from utils.powerupHandler import PowerUpHandler
from utils.brickwall import BrickWall
from utils.kBHit import KBHit
from utils.ufo import UFO
from utils import util, config


class Game:
    def __init__(self):
        self.__counter = 1
        self.__run = True
        self.__screen = Screen()
        self.__balls = [Ball(id=0, position=config.BALL_POSITION)]
        self.__paddle = Paddle(position=config.PADDLE_POSITION, emoji="🧱",
                               shape=config.PADDLE_SHAPE)
        self.__power_ups = []
        self.__bullets = []

        self.__brick_wall = BrickWall()
        self.__ufo = UFO()

        self.__power_up_handler = PowerUpHandler()
        self.__keys = KBHit()

        self.__boss_mode = False

        self.__lives = config.LIVES
        self.__plives = config.PADDLE_LIVES
        self.__frames_count = 0
        self.__score = 0

        util.hide_cursor()
        self._reset_ball_positions()

    def start(self):
        print(config.DELAY)
        z = 0
        while self.__run:
            t = time.time()

            self._refresh()

            self.__score += config.SCORE_FACTOR * self.__brick_wall.explode_bricks(
                self.__frames_count)

            self.handle_ufo()

            self.__brick_wall.fluctuate_bricks()

            self._update_power_up_time()

            self._detect_collisions()
            self.shoot_bullets()
            self.move_objects()

            self._reset_ball_positions()

            self.draw_objects()
            self.__screen.show(self.__frames_count, self.__lives, self.__score,
                               self.__brick_wall.get_count_bricks(), self.__plives,
                               self.__power_up_handler.get_power_up_duration("ShootingPaddle"))

            self.__frames_count += 1

            self._check_life_lost()
            self._manage_key_hits()

            z += 0 if (config.DELAY - (time.time() - t) >= 0) else 1
            print(f"{z} {config.DELAY - (time.time() - t)} {self.__ufo._time}")
            time.sleep(max(config.DELAY - (time.time() - t), 0))

    def handle_ufo(self):
        if self.__boss_mode:
            self.__ufo.drop_bomb()
            self.detect_bomb_paddle_collisions()

    def detect_bomb_paddle_collisions(self):
        to_remove = []
        for bomb in self.__ufo.get_bombs():
            if self._check_collisions(self.__paddle, bomb):
                self.__plives -= 1
                to_remove.append(bomb)
        self.__ufo.set_bombs([x for x in self.__ufo.get_bombs() if x not in to_remove])

    def shoot_bullets(self):
        if self.__power_up_handler.is_power_up_active("ShootingPaddle"):
            if (self.__frames_count % config.SHOOT_BULLET_TIME) == 0:
                _px, _py = self.__paddle.get_position()
                _ph, _pw = self.__paddle.get_shape()
                coords = [np.array([_px, _py - 1]), np.array([_px + _pw - 1, _py - 1])]
                for cd in coords:
                    self.__bullets.append(Bullet(id=self.__counter, position=cd))

    def draw_objects(self):
        for brick in self.__brick_wall.get_all_bricks():
            self.__screen.draw(brick)
        for ball in self.__balls:
            self.__screen.draw(ball)
        self.__screen.draw(self.__paddle)
        for power_up in self.__power_ups:
            self.__screen.draw(power_up)
        for bullet in self.__bullets:
            self.__screen.draw(bullet)

        if self.__boss_mode:
            for ufo in self.__ufo.get_all_bricks():
                self.__screen.draw(ufo)
            for bomb in self.__ufo.get_bombs():
                self.__screen.draw(bomb)
            self.__screen.draw(self.__ufo.get_health())

    def _move_paddle(self, ch):
        old_pos = copy.copy(self.__paddle.get_position())
        self.__paddle.move(ch=ch)
        new_pos = self.__paddle.get_position()
        for ball in self.__balls:
            if not ball.is_released():
                ball.add_position(new_pos - old_pos)

        if self.__boss_mode:
            self.__ufo.shift_wall(int((new_pos - old_pos)[0]))

    def _reset_ball_positions(self):  # TODO
        _ph, _pw = self.__paddle.get_shape()
        _px, _py = self.__paddle.get_position()
        for ball in self.__balls:
            _bx, _by = ball.get_position()
            _bw, _bh = ball.get_shape()
            if not (ball.is_released() or self._check_collisions(self.__paddle, ball, True)):
                _new_pos = self.__paddle.get_position() + np.array([randrange(1, _pw - 1), - 1])
                ball.set_position(_new_pos)

    def _manage_key_hits(self):

        if self.__keys.kb_hit() is True:
            _ch = self.__keys.get_ch().lower()
            if _ch == 'q':
                self.__run = False
            elif _ch == 'a' or _ch == 'd':
                self._move_paddle(_ch)
            elif _ch == ' ':
                for ball in self.__balls:
                    ball.set_release(True)
            elif _ch == 's':
                if self.__brick_wall.get_stage() == config.STAGES - 1:
                    self.__run = False
                else:
                    self.change_stage()
        self.__keys.clear()

    def _remove_objects_after_missing_paddle(self, objs):
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

    @staticmethod
    def _check_collisions(collider, obj, on_top=False):
        _xb, _yb = obj.get_position()
        _hb, _wb = obj.get_shape()

        _xp, _yp = collider.get_position()
        _hp, _wp = collider.get_shape()

        if on_top:
            return _xp < _xb + _wb and _xb < _xp + _wp and _yb + _hb - 1 == _yp - 1
        return _yp < _yb + _hb and _yb < _yp + _hp and _xp < _xb + _wb and _xb < _xp + _wp

    def _detect_collisions(self):
        self._detect_power_up_paddle_collisions()
        self.detect_bullet_wall_collisions()

        for ball in self.__balls:
            if ball.is_released():
                self._detect_ball_paddle_collisions(ball)  # Ball Paddle Collisions
            if ball.is_released():
                if not self._detect_brick_collisions(ball):  # Brick Ball Collisions
                    ball.move()  # Move balls

        to_remove = []
        for bullet in self.__bullets:
            for brick in self.__brick_wall.get_all_bricks():
                if self._check_collisions(brick, bullet):  # Brick bullet Collisions
                    to_remove.append(bullet)
                    self.dec_strength_of_brick(brick)
                    break
        self.__bullets = [x for x in self.__bullets if x not in to_remove]

    def move_objects(self):
        for power_up in self.__power_ups:
            power_up.move()
        for bullet in self.__bullets:
            bullet.move()

        if self.__boss_mode:
            for bomb in self.__ufo.get_bombs():
                bomb.move()

    def detect_bullet_wall_collisions(self):
        to_remove = []
        for bullet in self.__bullets:
            if bullet.get_position()[0] <= 0:
                to_remove.append(bullet)
        self.__bullets = [x for x in self.__bullets if x not in to_remove]

    def _update_power_up_time(self):
        self.__power_up_handler.update_power_ups(balls=self.__balls, paddle=self.__paddle)

    def _detect_ball_paddle_collisions(self, ball):

        if not (ball.is_released() and self._check_collisions(self.__paddle, ball)):
            return

        self.__brick_wall.shift_wall()

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

    def _detect_power_up_paddle_collisions(self):
        to_remove = []
        for power_up in self.__power_ups:
            if self._check_collisions(self.__paddle, power_up):
                name = power_up.__class__.__name__
                if name == "BallMultiplier":
                    self._multiply_balls()
                elif name == "ShrinkPaddle":
                    self.__power_up_handler.activate_power_ups(name, paddle=self.__paddle,
                                                               expand=False)
                else:
                    self.__power_up_handler.activate_power_ups(name, paddle=self.__paddle,
                                                               balls=self.__balls)  # TODO
                to_remove.append(power_up)

        self.__power_ups = [p for p in self.__power_ups if p not in to_remove]

    def _multiply_balls(self):
        to_add = []
        for ball in self.__balls:
            if ball.is_released():
                if len(self.__balls) + len(to_add) < config.MAXIMUM_BALLS:
                    to_add.append(
                        Ball(self.__counter, ball.get_position(), direction=-ball.get_direction(),
                             release=True, sp_factor=ball.get_sp_factor()))
                    self.__counter += 1
                else:
                    break
        self.__balls = self.__balls + to_add

    def _refresh(self):
        self.__screen.clear()
        util.position_cursor()

    def _detect_brick_collisions(self, ball):
        _dir = copy.copy(ball.get_direction())
        _bc = ball.get_center()
        _radius = ball.get_shape()  # minor axis(h) , major axis(w)
        _radius = [_radius[0] / 2, _radius[1] / 2]

        f = int(abs(_dir[0]) + abs(_dir[1]) + 1)

        c_bricks = []

        is_ball_thru = ball.is_thru()
        hit_ufo = False

        for idx in range(f + 1):

            curr_pos = _bc + (_dir * idx / f)
            tot_bricks = self.__brick_wall.get_all_bricks()
            if self.__boss_mode:
                tot_bricks = tot_bricks + self.__ufo.get_all_bricks()
            for brick in tot_bricks:
                _x, _y = brick.get_position()
                _h, _w = brick.get_shape()

                if ((_x <= curr_pos[0] <= _x + _w) or (_x <= curr_pos[0] + _radius[1] <= _x + _w) or
                    (_x <= curr_pos[0] - _radius[1] <= _x + _w)) and \
                        ((_y <= curr_pos[1] <= _y + _h) or (
                                _y <= curr_pos[1] + _radius[0] <= _y + _h)
                         or (_y <= curr_pos[1] - _radius[0] <= _y + _h)):
                    c_bricks.append(brick)
                    if brick.__class__.__name__ == "UFOBrick":
                        hit_ufo = True
                        is_ball_thru = False

            if (size := len(c_bricks)) > 0 and not is_ball_thru:

                if hit_ufo:
                    self.__ufo.dec_life()
                    if self.__ufo.get_lives() == 8 or self.__ufo.get_lives() == 4:
                        self.__brick_wall.set_enable()
                        self.__brick_wall.make_structure()

                _final_dir = np.zeros((size, 2))

                _prev_pos = curr_pos - (_dir / f)

                for index, brick in enumerate(c_bricks):
                    _next_dir = brick.reflect_obj(_prev_pos, _dir)
                    _final_dir[index] = _next_dir
                    self.dec_strength_of_brick(brick, _dir)
                ball.set_direction(_final_dir[0])
                return False

        if hit_ufo:
            self.__ufo.dec_life()

        for brick in c_bricks:
            self._destroy_and_check_for_power_up(brick, _dir)

        return False

    def dec_strength_of_brick(self, brick, direction):
        brick.set_rainbow()
        brick.set_level(brick.get_level() - 1)
        if brick.get_level() == 0:
            self._destroy_and_check_for_power_up(brick, direction)

    def _destroy_and_check_for_power_up(self, brick, direction):
        if brick.__class__.__name__ == "UFOBrick":
            return
        _pos = brick.get_position()
        self.__score += config.SCORE_FACTOR * self.__brick_wall.destroy_brick(brick,
                                                                              self.__frames_count)

        if not self.__boss_mode:
            new_power_up = self.__power_up_handler.create_power_up(_pos, direction)
            if new_power_up is not None:
                self.__power_ups.append(new_power_up)

    def change_stage(self):
        time.sleep(1)
        self.reset_all()
        self.__paddle.set_position(config.PADDLE_POSITION)
        if self.__brick_wall.get_stage() == config.STAGES - 1:
            self.__run = False
            return True
        self.__brick_wall.increment_stage()
        if self.__brick_wall.get_stage() == config.STAGES - 1:
            self.__boss_mode = True
            self.__ufo.set_time(0)
        return False

    def reset_all(self):
        self.__power_up_handler.deactivate_power_ups(paddle=self.__paddle, balls=self.__balls)
        self.__balls = [Ball(id=self.__counter, position=config.BALL_POSITION)]
        self.__power_ups = []
        self.__counter += 1
        self._reset_ball_positions()

    def _check_life_lost(self):
        self.__balls = self._remove_objects_after_missing_paddle(self.__balls)
        self.__power_ups = self._remove_objects_after_missing_paddle(self.__power_ups)
        if self.__boss_mode:
            self.__ufo.set_bombs(self._remove_objects_after_missing_paddle(self.__ufo.get_bombs()))

        if ((not self.__boss_mode) and self.__brick_wall.get_count_bricks() == 0) \
                or (self.__boss_mode and self.__ufo.get_lives() == 0):
            if self.change_stage():
                self.__run = False
                print('YOU WIN! 🥳🥳')

        if len(self.__balls) == 0:
            self.reset_all()
            self.__lives -= 1
            if self.__lives == 0:
                self.game_over()
                return
        if self.__plives == 0:
            self.game_over()
            return

        _py = self.__paddle.get_position()[1]
        for brick in self.__brick_wall.get_all_bricks():
            if _py <= brick.get_position()[1] + brick.get_shape()[0]:
                self.game_over()
                return

    def game_over(self):
        self.__run = False
        print('GAME OVER 😈 !!')

    def __del__(self):
        print("BYE")
        util.show_cursor()
