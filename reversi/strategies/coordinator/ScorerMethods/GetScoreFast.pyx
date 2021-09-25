#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""GetScore
"""

import sys

MAXSIZE64 = 2**63 - 1


def get_blank_score(board, w1, w2, w3):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _get_blank_score_size8_64bit(board, w1, w2, w3)
    return _get_blank_score(board, w1, w2, w3)


cdef:
    signed int[8] directions_x = [-1, 0, 1, -1, 1, -1, 0, 1]
    signed int[8] directions_y = [-1, -1, -1, 0, 0, 1, 1, 1]


cdef inline signed int _get_blank_score_size8_64bit(board, signed int w1, signed int w2, signed int w3):
    cdef:
        signed int score = 0
        unsigned long long black, white, blackwhite, not_blackwhite
        unsigned long long horizontal, vertical, diagonal
        unsigned long long l_blank, r_blank, t_blank, b_blank, lt_blank, rt_blank, lb_blank, rb_blank
        unsigned long long lt_x, rt_x, lb_x, rb_x
        unsigned long long lt_r, lt_b, rt_l, rt_b, lb_t, lb_r, rb_t, rb_l
        signed int lt_r_sign = 1, lt_b_sign = 1, rt_l_sign = 1, rt_b_sign = 1, lb_t_sign = 1, lb_r_sign = 1, rb_t_sign = 1, rb_l_sign = 1

    black, white = board.get_bitboard_info()
    blackwhite = black | white

    horizontal = blackwhite & <unsigned long long>0x7E7E7E7E7E7E7E7E  # 左右チェック用マスク
    vertical = blackwhite & <unsigned long long>0x00FFFFFFFFFFFF00    # 上下チェック用マスク
    diagonal = blackwhite & <unsigned long long>0x007E7E7E7E7E7E00    # 斜めチェック用マスク

    not_blackwhite = ~blackwhite

    # 左方向に空がある(右方向が盤面の範囲内)
    l_blank = horizontal & ((horizontal << 1) & not_blackwhite) >> 1

    # 右方向に空がある(左方向が盤面の範囲内)
    r_blank = horizontal & ((horizontal >> 1) & not_blackwhite) << 1

    # 上方向に空がある(下方向が盤面の範囲内)
    t_blank = vertical & ((vertical << 8) & not_blackwhite) >> 8

    # 下方向に空がある(上方向が盤面の範囲内)
    b_blank = vertical & ((vertical >> 8) & not_blackwhite) << 8

    # 左上方向に空がある(右下方向が盤面の範囲内)
    lt_blank = diagonal & ((diagonal << 9) & not_blackwhite) >> 9

    # 右上方向に空がある(左下方向が盤面の範囲内)
    rt_blank = diagonal & ((diagonal << 7) & not_blackwhite) >> 7

    # 左下方向に空がある(右上方向が盤面の範囲内)
    lb_blank = diagonal & ((diagonal >> 7) & not_blackwhite) << 7

    # 右下方向に空がある(左上方向が盤面の範囲内)
    rb_blank = diagonal & ((diagonal >> 9) & not_blackwhite) << 9

    # w1の計算
    score += w1 * (_popcount(l_blank & black) - _popcount(l_blank & white))
    score += w1 * (_popcount(r_blank & black) - _popcount(r_blank & white))
    score += w1 * (_popcount(t_blank & black) - _popcount(t_blank & white))
    score += w1 * (_popcount(b_blank & black) - _popcount(b_blank & white))
    score += w1 * (_popcount(lt_blank & black) - _popcount(lt_blank & white))
    score += w1 * (_popcount(rt_blank & black) - _popcount(rt_blank & white))
    score += w1 * (_popcount(lb_blank & black) - _popcount(lb_blank & white))
    score += w1 * (_popcount(rb_blank & black) - _popcount(rb_blank & white))

    # w2の計算
    lt_x = lt_blank & <unsigned long long>0x0040000000000000  # 左上のX打ち
    if lt_x:
        if lt_x & black:
            score += w2
        else:
            score -= w2
    rt_x = rt_blank & <unsigned long long>0x0002000000000000  # 右上のX打ち
    if rt_x:
        if rt_x & black:
            score += w2
        else:
            score -= w2
    lb_x = lb_blank & <unsigned long long>0x0000000000004000  # 左下のX打ち
    if lb_x:
        if lb_x & black:
            score += w2
        else:
            score -= w2
    rb_x = rb_blank & <unsigned long long>0x0000000000000200  # 右下のX打ち
    if rb_x:
        if rb_x & black:
            score += w2
        else:
            score -= w2

    # w3の計算
    lt_r = l_blank & <unsigned long long>0x4000000000000000
    lt_b = t_blank & <unsigned long long>0x0080000000000000
    rt_l = r_blank & <unsigned long long>0x0200000000000000
    rt_b = t_blank & <unsigned long long>0x0001000000000000
    lb_t = b_blank & <unsigned long long>0x0000000000008000
    lb_r = l_blank & <unsigned long long>0x0000000000000040
    rb_t = b_blank & <unsigned long long>0x0000000000000100
    rb_l = r_blank & <unsigned long long>0x0000000000000002
    if lt_r & white:
        lt_r_sign = -1
    if lt_b & white:
        lt_b_sign = -1
    if rt_l & white:
        rt_l_sign = -1
    if rt_b & white:
        rt_b_sign = -1
    if lb_t & white:
        lb_t_sign = -1
    if lb_r & white:
        lb_r_sign = -1
    if rb_t & white:
        rb_t_sign = -1
    if rb_l & white:
        rb_l_sign = -1
    for i in range(1, 5):
        lt_r >>= 1
        if lt_r & not_blackwhite:
            score += w3 * lt_r_sign
        lt_b >>= 8
        if lt_b & not_blackwhite:
            score += w3 * lt_b_sign
        rt_l <<= 1
        if rt_l & not_blackwhite:
            score += w3 * rt_l_sign
        rt_b >>= 8
        if rt_b & not_blackwhite:
            score += w3 * rt_b_sign
        lb_t <<= 8
        if lb_t & not_blackwhite:
            score += w3 * lb_t_sign
        lb_r >>= 1
        if lb_r & not_blackwhite:
            score += w3 * lb_r_sign
        rb_t <<= 8
        if rb_t & not_blackwhite:
            score += w3 * rb_t_sign
        rb_l <<= 1
        if rb_l & not_blackwhite:
            score += w3 * rb_l_sign
    return score


cdef inline signed int _popcount(unsigned long long bits):
    """_popcount
    """
    bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
    bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
    bits = bits + (bits >> <unsigned int>8)
    bits = bits + (bits >> <unsigned int>16)
    return (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F


cdef inline signed int _get_blank_score(board, signed int w1, signed int w2, signed int w3):
    cdef:
        signed int size = board.size
        signed int size_x_size = size * size
        signed int i, x, y, value, j, dx, dy, next_x1, next_y1, next_x2, next_y2, d, dx_abs, dy_abs, k, next_x3, next_y3
        signed int score = 0
        signed int board_info[26][26]

    board_info_tmp = board.get_board_info()
    for y in range(size):
        for x in range(size):
            board_info[x][y] = board_info_tmp[x][y]

    for y in range(size):
        for x in range(size):
            i = y * size + x
            # 自分または相手の石が存在する
            if board_info[x][y]:
                value = 0
                for j in range(8):
                    dx, dy = directions_x[j], directions_y[j]
                    next_x1, next_y1 = x + dx, y + dy
                    next_x2, next_y2 = x - dx, y - dy
                    if 0 <= next_x1 < size and 0 <= next_y1 < size and 0 <= next_x2 < size and 0 <= next_y2 < size:
                        # 空きマスに面している(ただし反対側が盤面の範囲内)
                        if not board_info[next_x1][next_y1]:
                            value += w1
                            # 隅に接している場合
                            d = dy * size + dx
                            if i+d == 0 or i+d == size-1 or i+d == size_x_size-8 or i+d == size_x_size-1:
                                if abs(dx) + abs(dy) == 2:
                                    value += w2  # X打ち(チェック方向が斜め)の場合
                                else:
                                    for k in range(1, 5):
                                        next_x3, next_y3 = x - k * dx, y - k * dy
                                        if not board_info[next_x3][next_y3]:
                                            value += w3  # 隅の反対の縦横方向に空きマスがある場合
                score += value * board_info[x][y]
    return score
