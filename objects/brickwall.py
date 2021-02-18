import time
from random import randrange, shuffle

import numpy as np

import config
from objects.brick import Brick, ExplosiveBrick, UnBreakableBrick


class BrickWall:

    def __init__(self, position, shape=(10, 10)):
        self.__counter = 0
        self.__position = position
        self.__shape = shape
        self.__bricks = []

        self.matrix = [
            # [
            #     "00000011111",
            #     "000001100011",
            #     "0000110000011",
            #     "00011000000011",
            #     "001100000000011",
            #     "0110001000100011",
            #     "0100000010000001",
            #     "0100000000000001",
            #     "010001E000E10001",
            #     "011000*E00E*00011",
            #     "0011000EEE00011",
            #     "00011000000011",
            #     "0000110000011",
            #     "00000011111"
            #
            # ],
            # [
            #     "000000EEEEE",
            #     "00000E10001E",
            #     "0000E1000001E",
            #     "000E100000001E",
            #     "00E10000000001E",
            #     "0E1000100010001E",
            #     "0E0000001000000E",
            #     "0E0000000000000E",
            #     "0E0000011100000E",
            #     "0E100*110011*001E",
            #     "00E10000000001E",
            #     "000E100000001E",
            #     "0000E1000001E",
            #     "000000EEEEE"
            # ]
            [
                '00000011111SSSSSSSSSSSSS11111',
                '00000011100SSSSSSSSSSSSS00111',
                '00000011100LLLLLLLLLLLLL00111',
                '00000011100LLLLLLLLLLLLL00111',
                '00000011100LLLLLLLLLLLLL00111',
                '00000011100LLLLLLLLLLLLL00111',
                '00000011100LLLLLLLLLLLLL00111',
                '00000011100SSSSSSSSSSSSS00111',
                '00000011111SSSSSSSSSSSSS11111',
            ]
        ]
        self.make_structure()

    def get_all_bricks(self):
        return self.__bricks

    # def get_shape(self):
    #     _h, _w = self.__shape
    #     return 2 * _h - 1, 6 * _w + 2
    #
    # def get_position(self):
    #     return self.__position

    @staticmethod
    def get_coords(brick):
        _x, _y = brick.get_position()
        _h, _w = brick.get_shape()
        return [(_x, _y), (_x, _y + _h), (_x + _w, _y), (_x + _w, _y + _h)]

    def destroy_brick(self, brick: Brick):  # TODO should be a bfs with showing chain reaction
        # if brick.__class__.__name__ == "ExplosiveBrick":
        #
        #     ex_coord = self.get_coords(brick)
        #     self.__bricks.remove(brick)
        #     # time.sleep(.01)
        #     for br in self.__bricks:
        #         br_coord = self.get_coords(br)
        #         if any(cd in ex_coord for cd in br_coord):
        #             self.destroy_brick(br)
        # else:
        try:  # TODO check
            self.__bricks.remove(brick)
        except Exception:
            return
        return

    def make_structure(self):
        _shape = (2, 4)
        z = 0
        for k in range(len(self.matrix)):
            y = 0
            for i in range(len(self.matrix[k])):
                x = 0
                for j in range(len(self.matrix[k][i])):
                    x = self.set_character(self.matrix[k][i][j], x, y, z)
                y += _shape[0]
            z += 95

    def set_character(self, ch, x, y, z):
        _shape = (2, 4)
        if ch == '0':
            x += 4
        elif ch == '*':
            x += 2
        elif ch == "S":
            x += 6
        else:
            if ch == 'L':
                _shape = (2, 6)
            _pos = np.array([x + z, y]) + self.__position
            # if ch == 'E':
            #     self.__bricks.append(ExplosiveBrick(id=self.__counter, position=_pos))
            # else:
            p = randrange(10)
            if p >= 2:
                self.__bricks.append(Brick(id=self.__counter, position=_pos,
                                           level=randrange(1, config.BRICK_TYPES + 1),
                                           shape=_shape))
            else:
                self.__bricks.append(UnBreakableBrick(id=self.__counter, position=_pos,
                                                      shape=_shape))
            self.__counter += 1
            x += _shape[1]
        return x
