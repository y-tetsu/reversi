#cython: language_level=3
"""UndoFast
"""

import sys


MAXSIZE64 = 2**63 - 1


def undo(board):
    """undo
    """
    if sys.maxsize == MAXSIZE64:
        return _undo_64bit(board)

    return _undo(board)


cdef inline _undo_64bit(board):
    """_undo_64bit
    """
    cdef:
        unsigned int size, disc_num
        unsigned long long flippable_discs, put

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

    return prev


cdef inline _undo(board):
    """_undo
    """
    cdef:
        unsigned int size, disc_num

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

    return prev
