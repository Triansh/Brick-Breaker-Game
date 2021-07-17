import numpy as np

from objects.gameObject import GameObject
from utils import patterns


class HealthBar(GameObject):
    def __init__(self, position):
        self._str = ['G'] * len(patterns.LAYOUTS[-1][0][0])
        self.__lives = len(self._str)
        super().__init__(position=position, emoji='🟩', shape=(1, len(self._str) * 2))

    def _make_rep(self):
        _block = np.full(self._shape, ' ')
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                emoji = '🟩' if self._str[j // 2] == 'G' else '🟥'
                _block[i, j] = emoji if j % 2 == 0 else ''
        self.set_rep(_block)

    def get_lives(self):
        return self.__lives

    def dec_lives(self):
        index = len(self._str) - 1 - self._str[::-1].index('G')
        self._str[index] = 'R'
        self.__lives -= 1
        self._make_rep()
