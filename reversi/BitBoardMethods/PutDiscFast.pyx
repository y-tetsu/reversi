#cython: language_level=3
"""PutDiscFast
"""

import sys


MAXSIZE64 = 2**63 - 1


def put_disc(board, color, x, y):
    """put_disc
    """
    size = board.size

    if size == 8 and sys.maxsize == MAXSIZE64:
        return _put_disc_size8_64bit(board, color, x, y)

    return _put_disc(size, board, color, x, y)


cdef inline _put_disc_size8_64bit(board, color, unsigned int x, unsigned int y):
    """_put_disc_size8_64bit
    """
    cdef:
        unsigned long long put, flippable_discs_num
        unsigned int tmp_x, tmp_y
        signed int shift_size

    # 配置位置を整数に変換
    shift_size = (63-(y*8+x))
    if shift_size < 0 or shift_size > 63:
        return []

    put = <unsigned long long>1 << (63-(y*8+x))

    # 反転位置を整数に変換
    flippable_discs = board.get_flippable_discs(color, x, y)
    flippable_discs_num = 0
    for tmp_x, tmp_y in flippable_discs:
        flippable_discs_num |= <unsigned long long>1 << (63-(tmp_y*8+tmp_x))

    # 自分の石を置いて相手の石をひっくり返す
    if color == 'black':
        board._black_bitboard ^= put | flippable_discs_num
        board._white_bitboard ^= flippable_discs_num
        board._black_score += 1 + len(flippable_discs)
        board._white_score -= len(flippable_discs)
    else:
        board._white_bitboard ^= put | flippable_discs_num
        board._black_bitboard ^= flippable_discs_num
        board._black_score -= len(flippable_discs)
        board._white_score += 1 + len(flippable_discs)

    # 打った手の記録
    board.prev += [(color, x, y, flippable_discs_num, len(flippable_discs))]

    return flippable_discs


cdef inline _put_disc(size, board, color, unsigned int x, unsigned int y):
    """_put_disc
    """
    # 配置位置を整数に変換
    shift_size = ((size*size-1)-(y*size+x))
    if shift_size < 0 or shift_size > size**2-1:
        return []

    put = 1 << ((size*size-1)-(y*size+x))

    # 反転位置を整数に変換
    flippable_discs = board.get_flippable_discs(color, x, y)
    flippable_discs_num = 0
    cdef:
        unsigned int tmp_x, tmp_y
    for tmp_x, tmp_y in flippable_discs:
        flippable_discs_num |= 1 << ((size*size-1)-(tmp_y*size+tmp_x))

    # 自分の石を置いて相手の石をひっくり返す
    if color == 'black':
        board._black_bitboard ^= put | flippable_discs_num
        board._white_bitboard ^= flippable_discs_num
        board._black_score += 1 + len(flippable_discs)
        board._white_score -= len(flippable_discs)
    else:
        board._white_bitboard ^= put | flippable_discs_num
        board._black_bitboard ^= flippable_discs_num
        board._black_score -= len(flippable_discs)
        board._white_score += 1 + len(flippable_discs)

    # 打った手の記録
    board.prev += [(color, x, y, flippable_discs_num, len(flippable_discs))]

    return flippable_discs
