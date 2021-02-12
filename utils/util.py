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


def str_to_array(obj_str):
    a = obj_str.split('\n')[1:-1]
    width = len(max(a, key=len))
    return np.array([list(x + (' ' * (width - len(x)))) for x in a])
    # return np.array([list(x)] for x in a)


def form_color_array(shape, color):
    """
    Args:
        shape: shape of np array
        color: tuple of colors to set at each entry of array
    """
    val = np.empty((), dtype=object)
    val[()] = color
    return np.full(shape, val, dtype=object)
