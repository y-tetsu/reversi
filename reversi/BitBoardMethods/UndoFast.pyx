#cython: language_level=3
"""UndoFast
"""

import sys


MAXSIZE64 = 2**63 - 1


def undo(board):
    """undo
    """
    size = board.size
    if size == 8 and sys.maxsize == MAXSIZE64:
        return _undo_size8_64bit(board)

    return _undo(size, board)


cdef inline _undo_size8_64bit(board):
    """_undo_size8_64bit
    """
    cdef:
        unsigned long long black_bitboard, white_bitboard, flippable_discs_num
        unsigned int black_score, white_score

    (black_bitboard, white_bitboard, black_score, white_score, flippable_discs_num, color) = board.prev.pop()
    if black_bitboard is not None:
        board._black_bitboard = black_bitboard
        board._white_bitboard = white_bitboard
        board._black_score = black_score
        board._white_score = white_score

    return (black_bitboard, white_bitboard, black_score, white_score, flippable_discs_num, color)


cdef inline _undo(size, board):
    """_undo
    """
    (black_bitboard, white_bitboard, black_score, white_score, flippable_discs_num, color) = board.prev.pop()
    if black_bitboard is not None:
        board._black_bitboard = black_bitboard
        board._white_bitboard = white_bitboard
        board._black_score = black_score
        board._white_score = white_score

    return (black_bitboard, white_bitboard, black_score, white_score, flippable_discs_num, color)
