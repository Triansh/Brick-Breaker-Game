import numpy as np


def position_cursor():
    """
    This positions the cursor back to (0,0)
    """
    print("\033[0;0H")


def hide_cursor():
    print("\x1b[?25l")


def show_cursor():
    print("\x1b[?25h")


def get_theta(base, perp):
    pi = np.pi
    theta = pi/2 if base == 0 else abs(np.arctan(perp / base))
    return theta
    # if perp >= 0 and base >= 0:
    #     return theta
    # elif perp > 0 and base < 0:
    #     return pi - theta
    # elif perp < 0 and base > 0:
    #     return - theta
    # elif perp <= 0 and base <= 0:
    #     return pi + theta
