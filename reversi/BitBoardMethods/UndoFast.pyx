#cython: language_level=3
"""UndoFast
"""

import sys


def undo(board):
    """undo
    """
    _undo(board)


cdef inline _undo(board):
    """_undo
    """
    (board._black_bitboard, board._white_bitboard, board._black_score, board._white_score, _, _) = board.prev.pop()
