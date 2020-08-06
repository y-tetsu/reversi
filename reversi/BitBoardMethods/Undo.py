"""Undo
"""


def undo(board):
    """undo
    """
    (board._black_bitboard, board._white_bitboard, board._black_score, board._white_score, _, _) = board.prev.pop()
