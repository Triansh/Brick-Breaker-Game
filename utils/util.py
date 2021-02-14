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


