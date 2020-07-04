"""Undo
"""


def undo(board):
    """undo
    """
    prev = board.prev.pop()

    if prev:
        size = board.size
        flippable_discs, disc_num = prev['flippable_discs'], prev['disc_num']

        put = 1 << ((size*size-1)-(prev['y']*size+prev['x']))

        if prev['color'] == 'black':
            board._black_bitboard ^= put | flippable_discs
            board._white_bitboard ^= flippable_discs
            board.score['black'] -= 1 + disc_num
            board.score['white'] += disc_num
        else:
            board._white_bitboard ^= put | flippable_discs
            board._black_bitboard ^= flippable_discs
            board.score['black'] += disc_num
            board.score['white'] -= 1 + disc_num

    board._legal_moves_cache.clear()
