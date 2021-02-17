import sys
from random import randrange

from objects.powerup import BallMultiplier, ThruBall, FastBall, PaddleGrab, ExpandPaddle, \
    ShrinkPaddle

from utils.powerUpActivity import PaddleSizeActivity, FastBallActivity, BallCollisionActivity, \
    PaddleGrabActivity, BallMultiplyActivity


class PowerUpHandler:

    def __init__(self):
        self.__counter = 0
        self.__power_ups_activity = [
            PaddleSizeActivity(),
            BallCollisionActivity(),
            FastBallActivity(),
            PaddleGrabActivity(),
            BallMultiplyActivity(),
        ]

    @staticmethod
    def map(name):

        if name in ["ExpandPaddle", "ShrinkPaddle"]:
            return 0
        elif name == "ThruBall ":
            return 1
        elif name == "FastBall":
            return 2
        elif name == "PaddleGrab":
            return 3
        elif name == "BallMultiplier":
            return 4

    def create_power_up(self, position):

        _type = randrange(3)
        # print(_type)
        # sys.exit()
        self.__counter += 1
        if _type == 5:
            return BallMultiplier(self.__counter, position)
        elif _type == 4:
            return ThruBall(self.__counter, position)
        elif _type == 2:
            return FastBall(self.__counter, position)
        elif _type == 3:
            return PaddleGrab(self.__counter, position)
        elif _type == 1:
            return ExpandPaddle(self.__counter, position)
        elif _type == 0:
            return ShrinkPaddle(self.__counter, position)

    def activate_power_ups(self, name, **kwargs):
        index = self.map(name)
        self.__power_ups_activity[index].activate(**kwargs)

    def update_power_ups(self, **kwargs):
        for activity in self.__power_ups_activity:
            activity.update(**kwargs)
