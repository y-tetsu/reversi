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
        return _put_disc_size8_64bit(board, 1 if color == 'black' else 0, x, y)

    return _put_disc(size, board, color, x, y)


cdef inline unsigned long long _put_disc_size8_64bit(board, signed int color, unsigned int x, unsigned int y):
    """_put_disc_size8_64bit
    """
    cdef:
        unsigned long long put, black_bitboard, white_bitboard, flippable_discs_num, flippable_discs_count
        unsigned int black_score, white_score
        signed int shift_size

    # 配置位置を整数に変換
    shift_size = (63-(y*8+x))
    if shift_size < 0 or shift_size > 63:
        return <unsigned long long>0

    put = <unsigned long long>1 << (63-(y*8+x))

    # ひっくり返せる石を取得
    black_bitboard = board._black_bitboard
    white_bitboard = board._white_bitboard
    black_score = board._black_score
    white_score = board._white_score
    flippable_discs_num = _get_flippable_discs_num_size8_64bit(color, black_bitboard, white_bitboard, x, y)
    flippable_discs_count = _get_flippable_discs_count_size8_64bit(flippable_discs_num)

    # 打つ前の状態を格納
    board.prev += [(black_bitboard, white_bitboard, black_score, white_score)]

    # 自分の石を置いて相手の石をひっくり返す
    if color:
        black_bitboard ^= put | flippable_discs_num
        white_bitboard ^= flippable_discs_num
        black_score += <unsigned int>1 + <unsigned int>flippable_discs_count
        white_score -= <unsigned int>flippable_discs_count
    else:
        white_bitboard ^= put | flippable_discs_num
        black_bitboard ^= flippable_discs_num
        black_score -= <unsigned int>flippable_discs_count
        white_score += <unsigned int>1 + <unsigned int>flippable_discs_count

    board._black_bitboard = black_bitboard
    board._white_bitboard = white_bitboard
    board._black_score = black_score
    board._white_score = white_score
    board._flippable_discs_num = flippable_discs_num

    return flippable_discs_num


cdef inline unsigned long long _get_flippable_discs_num_size8_64bit(signed int color, unsigned long long black_bitboard, unsigned long long white_bitboard, unsigned int x, unsigned int y):
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned int direction1, direction2
        unsigned long long buff, next_put
        unsigned long long move = 0
        unsigned long long player, opponent, flippable_discs_num = 0

    if color:
        player = black_bitboard
        opponent = white_bitboard
    else:
        player = white_bitboard
        opponent = black_bitboard

    move = <unsigned long long>1 << (63-(y*8+x))

    for direction1 in range(8):
        buff = 0
        next_put = _get_next_put_size8_64bit(move, direction1)

        # get discs of consecutive opponents
        for direction2 in range(8):
            if next_put & opponent:
                buff |= next_put
                next_put = _get_next_put_size8_64bit(next_put, direction1)
            else:
                break

        # store result if surrounded by own disc
        if next_put & player:
            flippable_discs_num |= buff

    return flippable_discs_num


cdef inline unsigned long long _get_next_put_size8_64bit(unsigned long long put, unsigned int direction):
    """_get_next_put_size8_64bit
    """
    cdef:
        unsigned long long next_put

    if direction == 0:
        next_put = <unsigned long long>0xFFFFFFFFFFFFFF00 & (put << <unsigned int>8)  # top
    elif direction == 1:
        next_put = <unsigned long long>0x7F7F7F7F7F7F7F00 & (put << <unsigned int>7)  # right-top
    elif direction == 2:
        next_put = <unsigned long long>0x7F7F7F7F7F7F7F7F & (put >> <unsigned int>1)  # right
    elif direction == 3:
        next_put = <unsigned long long>0x007F7F7F7F7F7F7F & (put >> <unsigned int>9)  # right-bottom
    elif direction == 4:
        next_put = <unsigned long long>0x00FFFFFFFFFFFFFF & (put >> <unsigned int>8)  # bottom
    elif direction == 5:
        next_put = <unsigned long long>0x00FEFEFEFEFEFEFE & (put >> <unsigned int>7)  # left-bottom
    elif direction == 6:
        next_put = <unsigned long long>0xFEFEFEFEFEFEFEFE & (put << <unsigned int>1)  # left
    elif direction == 7:
        next_put = <unsigned long long>0xFEFEFEFEFEFEFE00 & (put << <unsigned int>9)  # left-top
    else:
        next_put = <unsigned long long>0                                              # unexpected

    return next_put


cdef inline unsigned long long _get_flippable_discs_count_size8_64bit(unsigned long long discs):
    """_get_flippable_discs_count_size8_64bit
    """
    discs = (discs & <unsigned long long>0x5555555555555555) + (discs >> <unsigned int>1 & <unsigned long long>0x5555555555555555)
    discs = (discs & <unsigned long long>0x3333333333333333) + (discs >> <unsigned int>2 & <unsigned long long>0x3333333333333333)
    discs = (discs & <unsigned long long>0x0F0F0F0F0F0F0F0F) + (discs >> <unsigned int>4 & <unsigned long long>0x0F0F0F0F0F0F0F0F)
    discs = (discs & <unsigned long long>0x00FF00FF00FF00FF) + (discs >> <unsigned int>8 & <unsigned long long>0x00FF00FF00FF00FF)
    discs = (discs & <unsigned long long>0x0000FFFF0000FFFF) + (discs >> <unsigned int>16 & <unsigned long long>0x0000FFFF0000FFFF)

    return (discs & <unsigned long long>0x00000000FFFFFFFF) + (discs >> <unsigned int>32 & <unsigned long long>0x00000000FFFFFFFF)


cdef inline _put_disc(size, board, color, unsigned int x, unsigned int y):
    """_put_disc
    """
    # 配置位置を整数に変換
    shift_size = ((size*size-1)-(y*size+x))
    if shift_size < 0 or shift_size > size**2-1:
        return 0

    put = 1 << ((size*size-1)-(y*size+x))

    # 反転位置を整数に変換
    flippable_discs = board.get_flippable_discs(color, x, y)
    flippable_discs_num = 0
    cdef:
        unsigned int tmp_x, tmp_y
    for tmp_x, tmp_y in flippable_discs:
        flippable_discs_num |= 1 << ((size*size-1)-(tmp_y*size+tmp_x))

    # 打つ前の状態を格納
    board.prev += [(board._black_bitboard, board._white_bitboard, board._black_score, board._white_score)]

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

    board._flippable_discs_num = flippable_discs_num

    return flippable_discs_num
