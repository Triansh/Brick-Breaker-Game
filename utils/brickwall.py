import sys
from random import randrange
import numpy as np

from utils import config, patterns
from objects.brick import Brick, ExplosiveBrick, UnBreakableBrick


class BrickWall:

    def __init__(self):
        """
        counter: Integer : Assigns id to each brick
        position: np.array -> [x, y] : Wall position
        bricks : list(Brick): All un-destroyed bricks
        next_explodes : list((Brick, frame)) : The brick must be destroyed in this frame
        matrix : list(String) : Design of brick wall
        """
        self.__counter = self.__total_bricks = 0
        self.__stage = 0
        self.__bricks = self.__next_explodes = []
        self.__position = patterns.LAYOUTS[self.__stage][1]
        self.__matrix = patterns.LAYOUTS[self.__stage][0]
        self.__make_structure()

    def increment_stage(self):
        self.__stage += 1
        self.__position = patterns.LAYOUTS[self.__stage][1]
        self.__matrix = patterns.LAYOUTS[self.__stage][0]
        # if self.__stage == 2:
        #     sys.exit()
        self.__make_structure()

    def get_stage(self):
        return self.__stage

    def get_max_bricks(self):
        return self.__total_bricks

    def get_all_bricks(self):
        return self.__bricks + [x[0] for x in self.__next_explodes]

    def get_destroyed_bricks(self):
        return self.get_max_bricks() - self.get_count_bricks()

    def get_count_bricks(self):
        return sum([1 for x in self.__bricks if x.__class__.__name__ != "UnBreakableBrick"])

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
                self.__bricks.remove(brick)
            except ValueError:
                pass
            return 1

    def _do_explosion(self, brick, frames):
        to_remove = [brick]
        center, shape = brick.get_center(), brick.get_shape()
        for b in self.__bricks:
            if b != brick and self._is_neighbour(center, shape, b):
                if b.__class__.__name__ == "ExplosiveBrick":
                    self.__next_explodes.append((b, frames + 2))
                else:
                    to_remove.append(b)
        count = len(self.__bricks) - sum([1 for x in self.__bricks if x not in to_remove])
        self.__bricks = [x for x in self.__bricks if x not in to_remove]
        self.__next_explodes = [x for x in self.__next_explodes if x[0] not in to_remove]
        return count

    def explode_bricks(self, frame):
        count = 0
        for brick, f in self.__next_explodes:
            if f == frame:
                count += self._do_explosion(brick, frame)
        return count

    def __make_structure(self):
        """
        Function to construct the design of wall
        """
        self.__bricks = []
        _shape = (1, 4) if self.__stage == config.STAGES else (2, 4)
        y = 0
        for i in range(len(self.__matrix)):
            x = 0
            for j in range(len(self.__matrix[i])):
                x = self.__set_character(self.__matrix[i][j], x, y)
            y += _shape[0]
        self.__total_bricks += len(self.__bricks)

    def __set_character(self, ch, x, y):
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
            _pos = np.array([x, y]) + self.__position

            if ch in ['E', 'P']:
                new_brick = ExplosiveBrick(id=self.__counter, position=_pos, shape=_shape)
            elif ch == 'U':
                # _shape = (1, 3)
                new_brick = UnBreakableBrick(id=self.__counter, position=_pos, shape=_shape,
                                             ufo=True)
            else:
                if randrange(15) >= 2:
                    new_brick = Brick(id=self.__counter, position=_pos, shape=_shape,
                                      level=randrange(1, config.BRICK_TYPES + 1),
                                      rainbow=randrange(15) < 2)
                else:
                    new_brick = UnBreakableBrick(id=self.__counter, position=_pos, shape=_shape)
            self.__bricks.append(new_brick)
            self.__counter += 1
            x += _shape[1]
        return x

    def update_bricks(self):
        for brick in self.__bricks:
            brick.update()
