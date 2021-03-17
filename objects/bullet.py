import numpy as np

from objects.gameObject import MovingObject


class Bullet(MovingObject):

    def __init__(self, id, position):
        self.__id = id
        emoji = '🗼'
        shape = (1, 2)
        direction = np.array([0, -1])
        super().__init__(position=position, emoji=emoji, shape=shape, direction=direction)

    def move(self, **kwargs):
        self._position += self._direction
