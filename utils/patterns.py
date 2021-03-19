import numpy as np

from utils import config

LAYOUTS = [

    (
        [
            '00LLLLLLLELLLL0000',
            '00LEEEEEEELLLLLLL00',
            '00LLLLLLLEEEEEEEL00',
            '000S00LLLLELLLLLLL0',
        ],
        np.array([config.SCREEN_WIDTH // 2 - 55, 4], dtype=float)
    ),

    (
        [
            '1111SSLLEEEEELLSS1111',
            '1P00SSSSSSSSSSSSS00P1',
            '1P00LLLLLLELLLLLL00P1',
            '1P00LLEEEEEEEEELL00P1',
            '1P00LLLLLLSLLLLLL00P1',
            '1P00LLLLLLSLLLLLL00P1',
            '1P00SSSSSSSSSSSSS00P1',
            '1111SSSSSSSSSSSSS1111',
        ],
        np.array([config.SCREEN_WIDTH // 2 - 55, 4], dtype=float)
    ),

    (
        [
            'BLLBLLLBLLLBLLLBLLLBLLBL',
        ],
        np.array([8, 18], dtype=float)
    ),

    (
        [
            '000000FFFF00000',
            '00000F0000F0000',
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
        ],
        config.UFO_POSITION
    ),

]
