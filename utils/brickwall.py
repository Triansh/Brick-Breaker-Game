from random import randrange
import numpy as np

from utils import config, patterns
from objects.brick import Brick, ExplosiveBrick, UnBreakableBrick


class BrickWall:

    def __init__(self, stage=0):
        """
        counter: Integer : Assigns id to each brick
        position: np.array -> [x, y] : Wall position
        bricks : list(Brick): All un-destroyed bricks
        next_explodes : list((Brick, frame)) : The brick must be destroyed in this frame
        matrix : list(String) : Design of brick wall
        """
        self._counter = self._time = 0
        self._stage = stage
        self._bricks = self.__next_explodes = []
        self._position = patterns.LAYOUTS[self._stage][1]
        self._matrix = patterns.LAYOUTS[self._stage][0]
        self._make_structure()

    def increment_stage(self):
        self._stage += 1
        self._position = patterns.LAYOUTS[self._stage][1]
        self._matrix = patterns.LAYOUTS[self._stage][0]
        self._make_structure()
        self._time = 0

    def get_stage(self):
        return self._stage

    def get_all_bricks(self):
        return self._bricks + [x[0] for x in self.__next_explodes]

    def get_count_bricks(self):
        return sum(
            [1 for x in self._bricks if
             x.__class__.__name__ not in ["UnBreakableBrick", "UFOBrick"]])

    @staticmethod
    def _is_neighbour(center, shape, brick):
        """
        Check whether a Brick b  is neighbour of another Brick brick
        """
        _cx, _cy = center
        _ch, _cw = shape
        for i, j in brick.get_coords():
            if (((_cx - i) / _cw) ** 2) + (((_cy - j) / _ch) ** 2) <= 1:
                return True
        return False

    def destroy_brick(self, brick: Brick, frames):
        if brick.__class__.__name__ == "ExplosiveBrick":
            return self._do_explosion(brick, frames)
        else:
            try:
                self._bricks.remove(brick)
            except ValueError:
                pass
            return 1

    def _do_explosion(self, brick, frames):
        to_remove = [brick]
        center, shape = brick.get_center(), brick.get_shape()
        for b in self._bricks:
            if b != brick and self._is_neighbour(center, shape, b):
                if b.__class__.__name__ == "ExplosiveBrick":
                    self.__next_explodes.append((b, frames + 2))
                else:
                    to_remove.append(b)
        count = len(self._bricks) - sum([1 for x in self._bricks if x not in to_remove])
        self._bricks = [x for x in self._bricks if x not in to_remove]
        self.__next_explodes = [x for x in self.__next_explodes if x[0] not in to_remove]
        return count

    def explode_bricks(self, frame):
        count = 0
        for brick, f in self.__next_explodes:
            if f == frame:
                count += self._do_explosion(brick, frame)
        return count

    def _make_structure(self):
        """
        Function to construct the design of wall
        """
        self._bricks = []
        y = 0
        for i in range(len(self._matrix)):
            x = 0
            for j in range(len(self._matrix[i])):
                x = self._set_character(self._matrix[i][j], x, y)
            y += 2
        return

    def _set_character(self, ch, x, y):
        """
        How the bricks are placed in layout
        """
        _shape = (2, 4)
        if ch == '0':
            x += 4
        elif ch == "S":
            x += 6
        else:
            if ch in ['L', 'E']:
                _shape = (2, 6)
            _pos = np.array([x, y]) + self._position

            if ch in ['E', 'P']:
                new_brick = ExplosiveBrick(id=self._counter, position=_pos, shape=_shape)
            else:

                if randrange(30) >= 2:
                    new_brick = Brick(id=self._counter, position=_pos, shape=_shape,
                                      level=randrange(1, config.BRICK_TYPES + 1),
                                      rainbow=True if randrange(25) < 2 else False)
                else:
                    new_brick = UnBreakableBrick(id=self._counter, position=_pos, shape=_shape)
            self._bricks.append(new_brick)
            self._counter += 1
            x += _shape[1]
        return x

    def fluctuate_bricks(self):
        for brick in self._bricks:
            brick.fluctuate()
        self._time += 1

    def shift_wall(self, val=1):
        if self._time > config.TIME_ATTACK and (not config.STAGES - 1 == self._stage):
            for brick in self._bricks:
                brick.add_position(np.array([0, val]))
