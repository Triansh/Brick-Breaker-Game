import config
from objects.gameObject import MovingObject
from objects.paddle import Paddle


class PowerUp(MovingObject):

    def __init__(self, id, position, emoji):
        self.__id = id
        shape = config.POWERUP_SHAPE
        direction = config.POWERUP_DIRECTION
        super().__init__(position, emoji, shape=shape, direction=direction)

    def activate(self, **kwargs):
        """
        This function will be overrided for each powerup for its activation
        """

    def move(self, **kwargs):
        self.add_position(self.get_direction())


# x = ['💥', '⚡⚡', '🥊', '⚜', '🔥', '💕', '⏪', '⏩', '💠', '🏈', '🌀', ]

class ExpandPaddle(PowerUp):
    def __init__(self, id, position):
        emoji = "⏩"
        super().__init__(id, position, emoji)

    def activate(self, **kwargs):
        _paddle: Paddle = kwargs['paddle']
        _paddle.update_shape_decider(1)


class ShrinkPaddle(PowerUp):
    def __init__(self, id, position):
        emoji = "⏪"
        super().__init__(id, position, emoji)

    def activate(self, **kwargs):
        _paddle: Paddle = kwargs['paddle']
        _paddle.update_shape_decider(-1)


class BallMultiplier(PowerUp):
    def __init__(self, id, position):
        emoji = "🌀"
        super().__init__(id, position, emoji)

    def activate(self, **kwargs):
        _paddle = kwargs['balls']


class ThruBall(PowerUp):  # TODO
    def __init__(self, id, position):
        emoji = "🥊"
        super().__init__(id, position, emoji)

    def activate(self, **kwargs):
        _paddle = kwargs['balls']


class FastBall(PowerUp):  # TODO
    def __init__(self, id, position):
        emoji = "⚡⚡"
        super().__init__(id, position, emoji=emoji)

    def activate(self, **kwargs):
        _paddle = kwargs['balls']


class PaddleGrab(PowerUp):  # TODO
    def __init__(self, id, position):
        emoji = "⚜"
        super().__init__(id, position, emoji)

    def activate(self, **kwargs):
        _paddle = kwargs['balls']
