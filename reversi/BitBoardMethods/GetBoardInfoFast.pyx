#cython: language_level=3
"""GetBoardInfoFast
"""

import sys


MAXSIZE64 = 2**63 - 1


def get_board_info(size, b, w):
    """get_board_info
          return list of board information(black:1, white:-1, blank:0)
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_board_info_size8_64bit(b, w)

        return _get_board_info_size8(b, w)

    return _get_board_info(size, b, w)


cdef _get_board_info_size8_64bit(unsigned long long b, unsigned long long w):
    """_get_board_info_size8_64bit
    """
    cdef:
        unsigned int x, y
        unsigned long long mask = 0x8000000000000000
        signed int board_info[8][8]

    for y in range(8):
        for x in range(8):
            if b & mask:
                board_info[y][x] = 1
            elif w & mask:
                board_info[y][x] = -1
            else:
                board_info[y][x] = 0
            mask >>= 1

    return board_info


cdef _get_board_info_size8(b, w):
    """_get_board_info_size8
    """
    cdef:
        unsigned int x, y
        unsigned int b0 = ((0x10000000000000000 | b) >> 32) & 0xFFFFFFFF
        unsigned int b1 = b & 0xFFFFFFFF
        unsigned int w0 = ((0x10000000000000000 | w) >> 32) & 0xFFFFFFFF
        unsigned int w1 = w & 0x00000000FFFFFFFF
        unsigned int mask0 = 0x80000000
        unsigned int mask1 = 0x80000000

    board_info = []

    for y in range(8):
        tmp = []

        # ビットボード上位32bit
        if y < 4:
            for x in range(8):
                if b0 & mask0:
                    tmp += [1]
                elif w0 & mask0:
                    tmp += [-1]
                else:
                    tmp += [0]
                mask0 >>= 1
        # ビットボード下位32bit
        else:
            for x in range(8):
                if b1 & mask1:
                    tmp += [1]
                elif w1 & mask1:
                    tmp += [-1]
                else:
                    tmp += [0]
                mask1 >>= 1

        board_info += [tmp]

    return board_info


cdef _get_board_info(size, b, w):
    """_get_board_info
    """
    board_info = []
    mask = 1 << (size * size - 1)

    for y in range(size):
        tmp = []

        for x in range(size):
            if b & mask:
                tmp += [1]
            elif w & mask:
                tmp += [-1]
            else:
                tmp += [0]
            mask >>= 1

        board_info += [tmp]

    return board_info
