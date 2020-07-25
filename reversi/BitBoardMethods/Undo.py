"""Undo
"""


def undo(board):
    """undo
    """
    (color, x, y, flippable_discs, disc_num) = board.prev.pop()

    if color:
        size = board.size

        put = 1 << ((size*size-1)-(y*size+x))

        if color == 'black':
            board._black_bitboard ^= put | flippable_discs
            board._white_bitboard ^= flippable_discs
            board._black_score -= 1 + disc_num
            board._white_score += disc_num
        else:
            board._white_bitboard ^= put | flippable_discs
            board._black_bitboard ^= flippable_discs
            board._black_score += disc_num
            board._white_score -= 1 + disc_num

    return (color, x, y, flippable_discs, disc_num)
