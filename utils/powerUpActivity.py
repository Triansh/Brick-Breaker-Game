from utils import util


class PowerUpActivity:

    def __init__(self):
        self.__time = 0
        self.__duration = util.time_to_frames(100)
        self.__active = False

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
        super().activate(**kwargs)


class FastBallActivity(PowerUpActivity):
    def __init__(self):
        super().__init__()

    def activate(self, **kwargs):
        balls = kwargs['balls']
        for ball in balls:
            ball.set_sp_factor(2)

    def deactivate(self, **kwargs):
        balls = kwargs['balls']
        for ball in balls:
            ball.set_sp_factor(1)


class BallCollisionActivity(PowerUpActivity):
    def __init__(self):
        super().__init__()

    def activate(self, **kwargs):
        balls = kwargs['balls']
        for ball in balls:
            ball.set_thru(True)

    def deactivate(self, **kwargs):
        balls = kwargs['balls']
        for ball in balls:
            ball.set_thru(False)
