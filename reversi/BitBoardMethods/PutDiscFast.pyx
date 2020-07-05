#cython: language_level=3
"""PutDiscFast
"""

import sys


MAXSIZE64 = 2**63 - 1


def put_disc(board, color, x, y):
    """put_disc
    """
    if sys.maxsize == MAXSIZE64:
        return _put_disc_64bit(board, color, x, y)

    return _put_disc(board, color, x, y)


cdef inline _put_disc_64bit(board, color, unsigned int x, unsigned int y):
    """_put_disc_64bit
    """
    cdef:
        unsigned long long put, flippable_discs
        unsigned int size, tmp_x, tmp_y

    legal_moves = board.get_legal_moves(color)

    if (x, y) in legal_moves:
        # 配置位置を整数に変換
        size = board.size
        put = <unsigned long long>1 << ((size*size-1)-(y*size+x))

        # 反転位置を整数に変換
        reversibles_list = legal_moves[(x, y)]
        flippable_discs = 0
        for tmp_x, tmp_y in reversibles_list:
            flippable_discs |= <unsigned long long>1 << ((size*size-1)-(tmp_y*size+tmp_x))

        # 自分の石を置いて相手の石をひっくり返す
        if color == 'black':
            board._black_bitboard ^= put | flippable_discs
            board._white_bitboard ^= flippable_discs
            board.score['black'] += 1 + len(reversibles_list)
            board.score['white'] -= len(reversibles_list)
        else:
            board._white_bitboard ^= put | flippable_discs
            board._black_bitboard ^= flippable_discs
            board.score['black'] -= len(reversibles_list)
            board.score['white'] += 1 + len(reversibles_list)

        # 打った手の記録
        board.prev.append({'color': color, 'x': x, 'y': y, 'flippable_discs': flippable_discs, 'disc_num': len(reversibles_list)})

        return reversibles_list

    return []


cdef inline _put_disc(board, color, unsigned int x, unsigned int y):
    """_put_disc
    """
    cdef:
        unsigned int tmp_x, tmp_y

    legal_moves = board.get_legal_moves(color)

    if (x, y) in legal_moves:
        # 配置位置を整数に変換
        size = board.size
        put = 1 << ((size*size-1)-(y*size+x))

        # 反転位置を整数に変換
        reversibles_list = legal_moves[(x, y)]
        flippable_discs = 0
        for tmp_x, tmp_y in reversibles_list:
            flippable_discs |= 1 << ((size*size-1)-(tmp_y*size+tmp_x))

        # 自分の石を置いて相手の石をひっくり返す
        if color == 'black':
            board._black_bitboard ^= put | flippable_discs
            board._white_bitboard ^= flippable_discs
            board.score['black'] += 1 + len(reversibles_list)
            board.score['white'] -= len(reversibles_list)
        else:
            board._white_bitboard ^= put | flippable_discs
            board._black_bitboard ^= flippable_discs
            board.score['black'] -= len(reversibles_list)
            board.score['white'] += 1 + len(reversibles_list)

        # 打った手の記録
        board.prev.append({'color': color, 'x': x, 'y': y, 'flippable_discs': flippable_discs, 'disc_num': len(reversibles_list)})

        return reversibles_list

    return []
