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
        unsigned int x, y, disc_num
        unsigned long long flippable_discs, put

    (color, x, y, flippable_discs, disc_num) = board.prev.pop()

    if color == 'black':
        put = <unsigned long long>1 << (63-(y*8+x))
        board._black_bitboard ^= put | flippable_discs
        board._white_bitboard ^= flippable_discs
        board.score['black'] -= 1 + disc_num
        board.score['white'] += disc_num
    elif color == 'white':
        put = <unsigned long long>1 << (63-(y*8+x))
        board._white_bitboard ^= put | flippable_discs
        board._black_bitboard ^= flippable_discs
        board.score['black'] += disc_num
        board.score['white'] -= 1 + disc_num

    return (color, x, y, flippable_discs, disc_num)


cdef inline _undo(size, board):
    """_undo
    """
    cdef:
        unsigned int disc_num
    (color, x, y, flippable_discs, disc_num) = board.prev.pop()

    if color:
        put = 1 << ((size*size-1)-(y*size+x))
        if color == 'black':
            board._black_bitboard ^= put | flippable_discs
            board._white_bitboard ^= flippable_discs
            board.score['black'] -= 1 + disc_num
            board.score['white'] += disc_num
        else:
            board._white_bitboard ^= put | flippable_discs
            board._black_bitboard ^= flippable_discs
            board.score['black'] += disc_num
            board.score['white'] -= 1 + disc_num

    return (color, x, y, flippable_discs, disc_num)
