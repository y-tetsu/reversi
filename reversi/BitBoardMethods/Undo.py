"""Undo
"""


def undo(board):
    """undo
    """
    (black_bitboard, white_bitboard, black_score, white_score) = board.prev.pop()
    if black_bitboard is not None:
        board._black_bitboard = black_bitboard
        board._white_bitboard = white_bitboard
        board._black_score = black_score
        board._white_score = white_score

    return (black_bitboard, white_bitboard, black_score, white_score)
