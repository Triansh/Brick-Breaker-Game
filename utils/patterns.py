import numpy as np

from utils import config

LAYOUTS = [

    (
        [
            # '00LLLLLLLELLLLLLL00',
            '00LEEEEEEELLLLLLL00',
            '00LLLLLLLEEEEEEEL00',
            # '00LLLLLLLELLLLLLL00',
        ],
        np.array([config.SCREEN_WIDTH // 2 - 55, 4])
    ),

    (
        [
            '11111SSLLLEEEEELLLSS11111',
            '1P100SSSSSSSSSSSSSSS00111',
            '1P100LLLLLLLELLLLLLL001P1',
            '1P100LLLLLLLELLLLLLL001P1',
            '1P100LLEEEEEEEEEEELL001P1',
            '1P100LLLLLLLSLLLLLLL001P1',
            '1P100LLLLLLLSLLLLLLL001P1',
            '11100SSSSSSSSSSSSSSS001P1',
            '11111SSSSSSSSSSSSSSS11111',
        ],
        np.array([config.SCREEN_WIDTH // 2 - 65, 4])
    ),

    (
        [
            '00000000UU0000000',
            '0000000UUUU000000',
            '000000UUUUUU000000',
            '00000UUUUUUUU00000',
            '0000UUUUUUUUUU0000',
            '000UUUUU00UUUUU00',
            '000UUUUU00UUUUU00',
            '0000000U00U00000000',
            '0000000U00U00000000',

        ],
        np.array([config.PADDLE_POSITION[0] - 14, 3])
    ),

]
