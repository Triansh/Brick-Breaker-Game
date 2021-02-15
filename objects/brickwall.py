import sys
from random import randrange, shuffle

import numpy as np

import config
from objects.brick import Brick


class BrickWall:

    def __init__(self, position, shape=(10, 10)):
        self.__counter = 0

        self.__position = position
        self.__shape = shape
        self.__bricks = []
        # self.__rep = self.make_maze()
        self.create_maze()
        # print(self.__rep)

    def create_maze(self):
        _x, _y = self.__position
        _shape = (2, 6)
        _bricks = []
        for i in range(self.__shape[0]):
            for j in range(self.__shape[1]):
                pos = np.array([_x + j * _shape[1], _y + i * _shape[0]])
                _bricks.append(Brick(id=self.__counter, position=pos, level=randrange(1,4), shape=_shape))
                self.__counter += 1
        self.__bricks = _bricks

    def get_all_bricks(self):
        return self.__bricks

    def destroy_brick(self, brick):
        self.__bricks.remove(brick)

    def create_brick(self, y, x):
        _bricks = config.BRICKS
        _pos = np.array([x, y]) + self.__position
        level = randrange(1, len(_bricks) + 1)
        new_brick = Brick(self.__counter, _pos, level)
        self.__counter += 1
        self.__bricks.append(new_brick)
        return new_brick.get_emoji()

    # def make_maze(self):
    #
    #     _h, _w = self.__shape
    #
    #     vis = [[0] * _w + [1] for _ in range(_h)] + [[1] * (_w + 1)]
    #     ver = [["|  "] * _w + ['|'] for _ in range(_h)] + [[]]
    #     hor = [["+--"] * _w + ['+'] for _ in range(_h + 1)]
    #
    #     def walk(x, y):
    #         vis[y][x] = 1
    #
    #         d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    #         shuffle(d)
    #         for (xx, yy) in d:
    #             if vis[yy][xx]: continue
    #             if xx == x: hor[max(y, yy)][x] = "+  "
    #             if yy == y: ver[y][max(x, xx)] = "   "
    #             walk(xx, yy)
    #
    #     walk(randrange(_w), randrange(_h))
    #
    #     s = ""
    #     for (a, b) in zip(hor, ver):
    #         s += ''.join(a + ['\n'] + b + ['\n'])
    #
    #     x = [list(x) for x in s.split('\n')[1:-3]]
    #     size = (2 * _h - 1, 3 * _w + 1)
    #
    #     print(size)
    #     ar = []
    #     i = 0
    #     while i < size[0]:
    #         z = []
    #         j = 0
    #         while j < size[1]:
    #             if j == size[1] - 1:
    #                 z += [self.create_brick(i, 2 * j)] + ['']
    #             elif x[i][j] == '+' and x[i][j + 1] == '-':
    #                 z += [self.create_brick(i, 2 * j), '',
    #                       self.create_brick(i, 2 * j + 2), '',
    #                       self.create_brick(i, 2 * j + 4), '']
    #             elif x[i][j] == '+' or x[i][j] == '|':
    #                 z += [self.create_brick(i, 2 * j)] + [''] + ([' '] * 4)
    #             else:
    #                 z += [' '] * 6
    #             j += 3
    #         ar.append(z)
    #         i += 1
    #
    #     print("\n".join("".join(z) for z in ar))
    #
    #     return np.array(ar)

    def get_shape(self):
        _h, _w = self.__shape
        return 2 * _h - 1, 6 * _w + 2

    def get_position(self):
        return self.__position

    # def get_rep(self):
    #     return self.__rep




# [
#     "11111111111000011111111111110000000",
#     "11000000011000011000000000110000000",
#     "11000000011000011000000000110000000",
#     "11111111111000011111111111110000000",
#     "11000000000000011111100000000000000",
#     "11000000000000011001111100000000000",
#     "11000000000000011000001111000000000",
#     "11000000000000011000000011111000000"
# ]