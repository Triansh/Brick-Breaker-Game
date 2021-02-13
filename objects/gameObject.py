import numpy as np

import config


class GameObject:

    def __init__(self, position, rep: np.array, color):
        """
        Args:
            position (np.array) : [y, x]
            rep (np.array) :
            color (tuple) : (Fore, Back, Style)
        """
        self.__position = position
        self.__rep = rep
        self.__color = color

    def fix_position(self):
        _y, _x = self.get_position()
        _h, _w = self.get_shape()
        minx = min(max(0, _x), config.SCREEN_WIDTH - 1 - _w)
        miny = min(max(0, _y), config.SCREEN_HEIGHT - _h)
        self.__position = np.array([miny, minx])

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position
        self.fix_position()

    def add_position(self, position):
        self.__position += position
        self.fix_position()

    def get_shape(self):
        return self.__rep.shape

    def get_rep(self):
        return self.__rep, self.__color

    def set_color(self, color):
        self.__color = color


class MovingObject(GameObject):
    def __init__(self, position, rep, color, velocity):
        """
        Args:
            velocity (np.array): [y,x]
        """
        self.__velocity = velocity
        super().__init__(position=position, rep=rep, color=color)

    def get_velocity(self):
        return self.__velocity

    def set_velocity(self, velocity):
        self.__velocity = velocity

    def move(self, **kwargs):
        """
        This is a general function for all objects which move.
        Can be overrided by next child classes accordingly
        """


class StaticObject(GameObject):
    pass
