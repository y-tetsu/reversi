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
            if hasattr(board, '_black_bitboard'):
                return _get_score_size8_64bit(color, table, board)

    return _get_score(color, table, board)


cdef inline signed int _get_score_size8_64bit(color, table, board):
    """get_score
    """
    cdef:
        unsigned long long b, w
        unsigned long long mask = 0x8000000000000000
        unsigned int x, y
        signed int sign = -1, score
        signed int board_info[8][8]

    if color == 'black':
        sign = 1

    # get board info
    b = board._black_bitboard
    w = board._white_bitboard
    for y in range(8):
        for x in range(8):
            if b & mask:
                board_info[y][x] = 1
            elif w & mask:
                board_info[y][x] = -1
            else:
                board_info[y][x] = 0
            mask >>= 1

    # calculate score
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
