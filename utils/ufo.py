import numpy as np

from objects.brick import UFOBrick
from objects.bullet import UFOBomb
from utils.brickwall import BrickWall
from utils import config
from utils.healthbar import HealthBar


class UFO(BrickWall):

    def __init__(self):
        self.__bombs = []
        self._health = HealthBar(config.UFO_POSITION - np.array([0, 1], dtype=float))
        self.__health_bar = ['']
        super().__init__(stage=config.STAGES)

    def dec_life(self):
        if self._health.get_lives() > 0:
            self._health.dec_lives()

    def get_lives(self):
        return self._health.get_lives()

    def _set_character(self, ch, x, y):
        _shape = (1, 2)
        if ch in ['A', 'F', 'C', 'G']:
            _pos = np.array([x, y], dtype=float) + self._position
            emoji = '🛸'
            if ch == 'F':
                emoji = '🛸'
            elif ch == 'A':
                emoji = '👽'
            elif ch == 'C':
                emoji = '🔵'
            elif ch == 'G':
                emoji = '🟩'
            self._bricks.append(
                UFOBrick(id=self._counter, position=_pos, shape=_shape, emoji=emoji))
            self._counter += 1
            x += 2
            return x
        else:
            x += 2
            return x

    def get_health(self):
        return self._health

    def make_structure(self):
        self._bricks = []
        y = 0
        for i in range(len(self._matrix)):
            x = 0
            for j in range(len(self._matrix[i])):
                x = self._set_character(self._matrix[i][j], x, y)
            y += 1
        return

    def shift_wall(self, val=1):
        _pos = np.array([val, 0], dtype=float)
        self._position += _pos
        for brick in self._bricks:
            brick.add_position(_pos)
        self._health.add_position(_pos)

    def get_bombs(self):
        return self.__bombs

    def set_bombs(self, bombs):
        self.__bombs = bombs

    def set_time(self, value=0):
        self._time = value

    def drop_bomb(self):
        self._time += 1
        if self._time % config.UFO_DROP_TIME == 0:
            _pos = config.UFO_CENTER + self._position
            new_bomb = UFOBomb(position=_pos, id=self._time)
            self.__bombs.append(new_bomb)
