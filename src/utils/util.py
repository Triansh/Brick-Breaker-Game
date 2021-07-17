from utils import config


def position_cursor():
    """
    This positions the cursor back to (0,0)
    """
    print("\033[0;0H")


def hide_cursor():
    print("\x1b[?25l")


def show_cursor():
    print("\x1b[?25h")


def seconds_to_frames(sec):
    frame_rate = config.FPS
    return round(sec * frame_rate)


def format_num(num):
    return '{}'.format(num if num > 9 else ('0' + f'{num}'))


def frames_to_time(frames):
    s = int(frames * config.DELAY) % 60
    m = int((frames * config.DELAY) // 60) % 60
    h = int((frames * config.DELAY) // 3600) % 24
    return f"{format_num(h)}:{format_num(m)}:{format_num(s)}"
