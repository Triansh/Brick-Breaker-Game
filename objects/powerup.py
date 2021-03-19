from utils import config
from objects.gameObject import MovingObject


class PowerUp(MovingObject):

    def __init__(self, id, position, emoji, direction):
        self.__id = id
        shape = config.POWER_UP_SHAPE
        super().__init__(position, emoji, shape=shape, direction=direction)

    def move(self, **kwargs):
        self._handle_wall_reflection()
        self._direction += config.GRAVITY
        self.add_position(self._direction)


class ExpandPaddle(PowerUp):
    def __init__(self, id, position, direction):
        emoji = "⏩"
        super().__init__(id, position, emoji, direction)


class ShrinkPaddle(PowerUp):
    def __init__(self, id, position, direction):
        emoji = "⏪"
        super().__init__(id, position, emoji, direction)


class BallMultiplier(PowerUp):
    def __init__(self, id, position, direction):
        emoji = "🌀"
        super().__init__(id, position, emoji, direction)


class ThruBall(PowerUp):  # TODO
    def __init__(self, id, position, direction):
        emoji = "🥊"
        super().__init__(id, position, emoji, direction)


class FastBall(PowerUp):  # TODO
    def __init__(self, id, position, direction):
        emoji = "⚡⚡"
        super().__init__(id, position, emoji, direction)


class PaddleGrab(PowerUp):  # TODO
    def __init__(self, id, position, direction):
        emoji = "🔱"
        super().__init__(id, position, emoji, direction)


class ShootingPaddle(PowerUp):  # TODO
    def __init__(self, id, position, direction):
        emoji = "🔫"
        super().__init__(id, position, emoji, direction)
