#cython: language_level=3
"""PutDiscFast
"""


def put_disc(board, color, x, y):
    """put_disc
    """
    return _put_disc(board, color, x, y)


cdef inline _put_disc(board, color, x, y):
    """_put_disc
    """
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
