"""PutDisc.py
"""


def put_disc(board, color, x, y):
    """put_disc
    """
    # 配置位置を整数に変換
    size = board.size
    shift_size = ((size*size-1)-(y*size+x))
    if shift_size < 0 or shift_size > size**2-1:
        return []

    # 反転位置を整数に変換
    flippable_discs = board.get_flippable_discs(color, x, y)
    flippable_discs_num = 0
    for tmp_x, tmp_y in flippable_discs:
        flippable_discs_num |= 1 << ((size*size-1)-(tmp_y*size+tmp_x))

    # 打つ前の状態を格納
    board.prev += [(board._black_bitboard, board._white_bitboard, board._black_score, board._white_score, flippable_discs_num, color)]

    # 自分の石を置いて相手の石をひっくり返す
    put = 1 << ((size*size-1)-(y*size+x))
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

    return flippable_discs
