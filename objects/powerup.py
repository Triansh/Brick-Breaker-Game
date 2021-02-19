from utils import config
from objects.gameObject import MovingObject


class PowerUp(MovingObject):

    def __init__(self, id, position, emoji):
        self.__id = id
        shape = config.POWER_UP_SHAPE
        direction = config.POWER_UP_DIRECTION
        super().__init__(position, emoji, shape=shape, direction=direction)

    def move(self, **kwargs):
        self.add_position(self.get_direction())


class ExpandPaddle(PowerUp):
    def __init__(self, id, position):
        emoji = "⏩"
        super().__init__(id, position, emoji)


class ShrinkPaddle(PowerUp):
    def __init__(self, id, position):
        emoji = "⏪"
        super().__init__(id, position, emoji)


class BallMultiplier(PowerUp):
    def __init__(self, id, position):
        emoji = "🌀"
        super().__init__(id, position, emoji)


class ThruBall(PowerUp):  # TODO
    def __init__(self, id, position):
        emoji = "🥊"
        super().__init__(id, position, emoji)


class FastBall(PowerUp):  # TODO
    def __init__(self, id, position):
        emoji = "⚡⚡"
        super().__init__(id, position, emoji=emoji)


class PaddleGrab(PowerUp):  # TODO
    def __init__(self, id, position):
        emoji = "🔱"
        super().__init__(id, position, emoji)
