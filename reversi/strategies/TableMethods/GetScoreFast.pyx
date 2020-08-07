#cython: language_level=3
"""Get Score of Table strategy
"""

import sys


MAXSIZE64 = 2**63 - 1


def get_score(table, board):
    """get_score
    """
    if board.size == 8:
        if sys.maxsize == MAXSIZE64:
            if hasattr(board, '_black_bitboard'):
                return _get_score_size8_64bit(table, board)

    return _get_score(table, board)


cdef inline signed int _get_score_size8_64bit(table, board):
    """get_score
    """
    cdef:
        unsigned long long b, w
        unsigned long long mask = 0x8000000000000000
        unsigned int x, y
        signed int score = 0
    b = board._black_bitboard
    w = board._white_bitboard
    for y in range(8):
        for x in range(8):
            if b & mask:
                score += <signed int>table[y][x] * <signed int>1
            elif w & mask:
                score += <signed int>table[y][x] * <signed int>-1
            mask >>= 1

    return score


cdef inline signed int _get_score(table, board):
    """get_score
    """
    cdef:
        unsigned int x, y, size
        signed int score
    board_info = board.get_board_info()
    size = board.size
    score = 0
    for y in range(size):
        for x in range(size):
            score += table[y][x] * board_info[y][x]

    return score
