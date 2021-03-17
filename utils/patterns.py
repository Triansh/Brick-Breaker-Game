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
            '11111SSLLEEEEELLSS11111',
            '1P100SSSSSSSSSSSSS00111',
            # '1P100LLLLLLELLLLLL001P1',
            '1P100LLLLLLELLLLLL001P1',
            '1P100LLEEEEEEEEELL001P1',
            '1P100LLLLLLSLLLLLL001P1',
            '1P100LLLLLLSLLLLLL001P1',
            '11100SSSSSSSSSSSSS001P1',
            '11111SSSSSSSSSSSSS11111',
        ],
        np.array([config.SCREEN_WIDTH // 2 - 65, 4])
    ),

    (
        [
            '000000FFFF00000',
            '00000F0000F0000',
            '0000F00AA00F000',
            '0000F0AAAA0F000',
            '0000F000000F000',
            '000FFFFFFFFFF00',
            '00F0000000000F0',
            '0F00CC0000CC00F',
            'F00C00C00C00C00F',
            'F00000000000000F',
            '0FFFFFFFFFFFFFF0',
            '00000F0000F0000',
            '000000FFFF000',

            # '00000000UU0000000',
            # '0000000UUUU000000',
            # '000000UUUUUU000000',
            # '00000UUUUUUUU00000',
            # '0000UUUUUUUUUU0000',
            # '000UUUUU00UUUUU00',
            # '000UUUUU00UUUUU00',
            # '0000000U00U00000000',
            # '0000000U00U00000000',
        ],
        np.array([config.PADDLE_POSITION[0] - 14, 3])
    ),

]
