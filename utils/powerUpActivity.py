from random import randrange

from utils import util, config


class PowerUpActivity:

    def __init__(self):
        """
        duration: frames: The time for which the power up will be activated
        time: frames : Time left for deactivation
        active: Boolean : True if power up is active
        """
        self.__time = 0
        self.__duration = util.seconds_to_frames(10)
        self.__active = False

    def get_duration(self):
        return self.__time

    def is_active(self):
        return self.__active

    def activate(self, **kwargs):
        self.__time = self.__duration
        self.__active = True

    def deactivate(self, **kwargs):
        self.__active = False

    def update(self, **kwargs):
        if self.__active:
            self.__time -= 1
            if self.__time == 0:
                self.deactivate(**kwargs)


class PaddleSizeActivity(PowerUpActivity):

    def __init__(self):
        super().__init__()

    def activate(self, **kwargs):
        _paddle = kwargs['paddle']
        _expand = kwargs.get('expand', True)
        _paddle.update_shape_decider(1 if _expand else -1)
        super().activate(**kwargs)

    def deactivate(self, **kwargs):
        _paddle = kwargs['paddle']
        _paddle.update_shape_decider(0)
        super().deactivate(**kwargs)


class PaddleGrabActivity(PowerUpActivity):
    def __init__(self):
        super().__init__()

    def activate(self, **kwargs):
        _paddle = kwargs['paddle']
        _paddle.set_grabber_mode(True)
        super().activate(**kwargs)

    def deactivate(self, **kwargs):
        _paddle = kwargs['paddle']
        _paddle.set_grabber_mode(False)
        super().deactivate(**kwargs)


class FastBallActivity(PowerUpActivity):
    def __init__(self):
        super().__init__()

    def activate(self, **kwargs):
        balls = kwargs['balls']
        for ball in balls:
            ball.set_sp_factor(2)
        super().activate(**kwargs)

    def deactivate(self, **kwargs):
        balls = kwargs['balls']
        for ball in balls:
            ball.set_sp_factor(1)
        super().deactivate(**kwargs)


class ThruBallActivity(PowerUpActivity):
    def __init__(self):
        super().__init__()

    def activate(self, **kwargs):
        balls = kwargs['balls']
        for ball in balls:
            ball.set_thru(True)
            ball.set_emoji('🔥')
        super().activate(**kwargs)

    def deactivate(self, **kwargs):
        balls = kwargs['balls']
        for ball in balls:
            ball.set_thru(False)
            emoji = config.BALLS[randrange(len(config.BALLS))]
            ball.set_emoji(emoji)
        super().deactivate(**kwargs)


class ShootingActivity(PowerUpActivity):
    def __init__(self):
        super().__init__()

    def activate(self, **kwargs):
        _paddle = kwargs['paddle']
        _paddle.set_shooter_mode(True)
        super().activate(**kwargs)

    def deactivate(self, **kwargs):
        _paddle = kwargs['paddle']
        _paddle.set_shooter_mode(False)
        super().deactivate(**kwargs)
