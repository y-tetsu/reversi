#cython: language_level=3
"""Get Score of Table strategy
"""

import sys


MAXSIZE64 = 2**63 - 1


def get_score(color, table, board):
    """get_score
    """
    if board.size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_score_size8_64bit(color, table, board)

    return _get_score(color, table, board)


cdef inline signed int _get_score_size8_64bit(color, table, board):
    """get_score
    """
    cdef:
        unsigned int x, y
        signed int sign = -1, score

    if color == 'black':
        sign = 1

    board_info = board.get_board_info()
    score = 0

    for y in range(8):
        for x in range(8):
            score += <signed int>table[y][x] * <signed int>board_info[y][x] * sign

    return score


cdef inline signed int _get_score(color, table, board):
    """get_score
    """
    cdef:
        unsigned int x, y, size
        signed int sign, score

    sign = 1 if color == 'black' else -1
    board_info = board.get_board_info()
    size = board.size
    score = 0

    for y in range(size):
        for x in range(size):
            score += table[y][x] * board_info[y][x] * sign

    return score
