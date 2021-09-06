#cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""Evaluate
"""

import sys

MAXSIZE64 = 2**63 - 1

cdef:
    signed int[256] edge_table8 = [
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 4,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 5,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 4,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 6,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 4,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 5,
        1, 1, 1, 2, 1, 1, 1, 3,
        1, 1, 1, 2, 1, 1, 1, 4,
        1, 1, 1, 2, 1, 1, 1, 3,
        1, 1, 1, 2, 1, 1, 1, 5,
        2, 2, 2, 3, 2, 2, 2, 4,
        2, 2, 2, 3, 2, 2, 2, 5,
        3, 3, 3, 4, 3, 3, 3, 5,
        4, 4, 4, 5, 5, 5, 6, 13
    ]

def evaluate_tpw(t, params, color, board, possibility_b, possibility_w):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _evaluate_tpw_size8_64bit(t.table.table, params, color, board, possibility_b, possibility_w)
    return _evaluate_tpw(t, params, color, board, possibility_b, possibility_w)


cdef inline signed int _evaluate_tpw_size8_64bit(table, params, color, board, possibility_b, possibility_w):
    cdef:
        signed int wp = params[0]
        signed int ww = params[1]
        signed int score_w = 0
        signed int score_t = 0
        signed int score_p = 0
        unsigned int x, y
        unsigned long long t_mask = 0x8000000000000000
        unsigned long long b_bitboard, w_bitboard, all_bitboard, bit_pos, lt, rt, lb, rb, b_t, w_t, b_b, w_b, b_l, w_l, b_r, w_r

    b_bitboard, w_bitboard = board.get_bitboard_info()

    # 勝敗が決まっている場合
    if not possibility_b and not possibility_w:
        score_w = board._black_score - board._white_score
        if score_w > 0:    # 黒が勝った
            score_w += ww
        elif score_w < 0:  # 白が勝った
            score_w -= ww
        return score_w

    # テーブルによるスコア
    for y in range(8):
        for x in range(8):
            if b_bitboard & t_mask:
                score_t += <signed int>table[y][x]
            elif w_bitboard & t_mask:
                score_t -= <signed int>table[y][x]
            t_mask >>= 1

    # 着手可能数によるスコア
    score_p = (possibility_b - possibility_w) * wp

    return score_t + score_p


cdef inline signed int _evaluate_tpw(t, params, color, board, possibility_b, possibility_w):
    if not possibility_b and not possibility_w:  # 勝敗が決まっている場合
        ret = board._black_score - board._white_score
        if ret > 0:    # 黒が勝った
            ret += params[1]
        elif ret < 0:  # 白が勝った
            ret -= params[1]
        return ret
    return t.get_score(None, board, None, None) + (possibility_b - possibility_w) * params[0]


def evaluate_tpwe(t, table, params, color, board, possibility_b, possibility_w):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _evaluate_tpwe_size8_64bit(table, params, color, board, possibility_b, possibility_w)
    return _evaluate_tpwe(t, params, color, board, possibility_b, possibility_w)


cdef inline signed int _evaluate_tpwe_size8_64bit(table, params, color, board, possibility_b, possibility_w):
    cdef:
        signed int wp = params[0]
        signed int ww = params[1]
        signed int we = params[2]
        signed int score_w = 0
        signed int score_t = 0
        signed int score_p = 0
        signed int score_e = 0
        signed int lt_sign, lb_sign, rt_sign, rb_sign
        unsigned int i, x, y
        unsigned long long t_mask = 0x8000000000000000
        unsigned long long b_bitboard, w_bitboard, all_bitboard, bit_pos, lt, rt, lb, rb, b_t, w_t, b_b, w_b, b_l, w_l, b_r, w_r

    b_bitboard, w_bitboard = board.get_bitboard_info()

    # 勝敗が決まっている場合
    if not possibility_b and not possibility_w:
        score_w = board._black_score - board._white_score
        if score_w > 0:    # 黒が勝った
            score_w += ww
        elif score_w < 0:  # 白が勝った
            score_w -= ww
        return score_w

    # テーブルによるスコア
    for y in range(8):
        for x in range(8):
            if b_bitboard & t_mask:
                score_t += <signed int>table[y][x]
            elif w_bitboard & t_mask:
                score_t -= <signed int>table[y][x]
            t_mask >>= 1

    # 着手可能数によるスコア
    score_p = (possibility_b - possibility_w) * wp

    # 辺のパターンによるスコア
    all_bitboard = b_bitboard | w_bitboard
    bit_pos = <unsigned long long>0x8000000000000000

    lt = <unsigned long long>0x8000000000000000
    rt = <unsigned long long>0x0100000000000000
    lb = <unsigned long long>0x0000000000000080
    rb = <unsigned long long>0x0000000000000001

    # 四隅のどこかに石がある場合
    if (lt | rt | lb | rb) & all_bitboard:
        # 上辺
        b_t, w_t = 0, 0
        if (lt | rt) & all_bitboard:
            b_t = (<unsigned long long>0xFF00000000000000 & b_bitboard) >> 56
            w_t = (<unsigned long long>0xFF00000000000000 & w_bitboard) >> 56
        # 下辺
        b_b = <unsigned long long>0x00000000000000FF & b_bitboard
        w_b = <unsigned long long>0x00000000000000FF & w_bitboard
        # 左辺
        b_l, w_l = 0, 0
        if (lt | lb) & b_bitboard:
            if b_bitboard & <unsigned long long>0x8000000000000000:
                b_l += <unsigned long long>0x0000000000000080
            if b_bitboard & <unsigned long long>0x0080000000000000:
                b_l += <unsigned long long>0x0000000000000040
            if b_bitboard & <unsigned long long>0x0000800000000000:
                b_l += <unsigned long long>0x0000000000000020
            if b_bitboard & <unsigned long long>0x0000008000000000:
                b_l += <unsigned long long>0x0000000000000010
            if b_bitboard & <unsigned long long>0x0000000080000000:
                b_l += <unsigned long long>0x0000000000000008
            if b_bitboard & <unsigned long long>0x0000000000800000:
                b_l += <unsigned long long>0x0000000000000004
            if b_bitboard & <unsigned long long>0x0000000000008000:
                b_l += <unsigned long long>0x0000000000000002
            if b_bitboard & <unsigned long long>0x0000000000000080:
                b_l += <unsigned long long>0x0000000000000001
        if (lt | lb) & w_bitboard:
            if w_bitboard & <unsigned long long>0x8000000000000000:
                w_l += <unsigned long long>0x0000000000000080
            if w_bitboard & <unsigned long long>0x0080000000000000:
                w_l += <unsigned long long>0x0000000000000040
            if w_bitboard & <unsigned long long>0x0000800000000000:
                w_l += <unsigned long long>0x0000000000000020
            if w_bitboard & <unsigned long long>0x0000008000000000:
                w_l += <unsigned long long>0x0000000000000010
            if w_bitboard & <unsigned long long>0x0000000080000000:
                w_l += <unsigned long long>0x0000000000000008
            if w_bitboard & <unsigned long long>0x0000000000800000:
                w_l += <unsigned long long>0x0000000000000004
            if w_bitboard & <unsigned long long>0x0000000000008000:
                w_l += <unsigned long long>0x0000000000000002
            if w_bitboard & <unsigned long long>0x0000000000000080:
                w_l += <unsigned long long>0x0000000000000001
        # 右辺
        b_r, w_r = 0, 0
        if (rt | rb) & b_bitboard:
            if b_bitboard & <unsigned long long>0x0100000000000000:
                b_r += <unsigned long long>0x0000000000000080
            if b_bitboard & <unsigned long long>0x0001000000000000:
                b_r += <unsigned long long>0x0000000000000040
            if b_bitboard & <unsigned long long>0x0000010000000000:
                b_r += <unsigned long long>0x0000000000000020
            if b_bitboard & <unsigned long long>0x0000000100000000:
                b_r += <unsigned long long>0x0000000000000010
            if b_bitboard & <unsigned long long>0x0000000001000000:
                b_r += <unsigned long long>0x0000000000000008
            if b_bitboard & <unsigned long long>0x0000000000010000:
                b_r += <unsigned long long>0x0000000000000004
            if b_bitboard & <unsigned long long>0x0000000000000100:
                b_r += <unsigned long long>0x0000000000000002
            if b_bitboard & <unsigned long long>0x0000000000000001:
                b_r += <unsigned long long>0x0000000000000001
        if (rt | rb) & w_bitboard:
            if w_bitboard & <unsigned long long>0x0100000000000000:
                w_r += <unsigned long long>0x0000000000000080
            if w_bitboard & <unsigned long long>0x0001000000000000:
                w_r += <unsigned long long>0x0000000000000040
            if w_bitboard & <unsigned long long>0x0000010000000000:
                w_r += <unsigned long long>0x0000000000000020
            if w_bitboard & <unsigned long long>0x0000000100000000:
                w_r += <unsigned long long>0x0000000000000010
            if w_bitboard & <unsigned long long>0x0000000001000000:
                w_r += <unsigned long long>0x0000000000000008
            if w_bitboard & <unsigned long long>0x0000000000010000:
                w_r += <unsigned long long>0x0000000000000004
            if w_bitboard & <unsigned long long>0x0000000000000100:
                w_r += <unsigned long long>0x0000000000000002
            if w_bitboard & <unsigned long long>0x0000000000000001:
                w_r += <unsigned long long>0x0000000000000001
        score_e = ((edge_table8[b_t] - edge_table8[w_t]) + (edge_table8[b_b] - edge_table8[w_b]) + (edge_table8[b_l] - edge_table8[w_l]) + (edge_table8[b_r] - edge_table8[w_r])) * we
    return score_t + score_p + score_e


cdef inline signed int _evaluate_tpwe(t, params, color, board, possibility_b, possibility_w):
    cdef:
        signed int wp = params[0]
        signed int ww = params[1]
        signed int we = params[2]
        signed int score_w = 0
        signed int score_t = 0
        signed int score_p = 0
        signed int score_e = 0
        signed int lt_sign, lb_sign, rt_sign, rb_sign
        unsigned int i

    # 勝敗が決まっている場合
    if not possibility_b and not possibility_w:
        score_w = board._black_score - board._white_score
        if score_w > 0:    # 黒が勝った
            score_w += ww
        elif score_w < 0:  # 白が勝った
            score_w -= ww
        return score_w
    score_t = t.get_score(None, board, None, None)  # テーブルによるスコア
    score_p = (possibility_b - possibility_w) * wp  # 着手可能数によるスコア
    # 辺のパターンによるスコア
    size = board.size
    b_bitboard, w_bitboard = board.get_bitboard_info()
    all_bitboard = b_bitboard | w_bitboard
    bit_pos = 1 << (size * size - 1)

    lt = bit_pos
    rt = bit_pos >> size-1
    lb = bit_pos >> size*(size-1)
    rb = bit_pos >> size*size-1

    # 四隅のどこかに石がある場合
    if (lt | rt | lb | rb) & all_bitboard:
        # 左上
        lt_board = b_bitboard
        lt_sign = 1
        if lt & w_bitboard:
            lt_board = w_bitboard
            lt_sign = -1
        lt_r, lt_b = lt & lt_board, lt & lt_board
        # 右上
        rt_board = b_bitboard
        rt_sign = 1
        if rt & w_bitboard:
            rt_board = w_bitboard
            rt_sign = -1
        rt_l, rt_b = rt & rt_board, rt & rt_board
        # 左下
        lb_board = b_bitboard
        lb_sign = 1
        if lb & w_bitboard:
            lb_board = w_bitboard
            lb_sign = -1
        lb_r, lb_t = lb & lb_board, lb & lb_board
        # 右下
        rb_board = b_bitboard
        rb_sign = 1
        if rb & w_bitboard:
            rb_board = w_bitboard
            rb_sign = -1
        rb_l, rb_t = rb & rb_board, rb & rb_board

        # 確定石の連続数(2個～7個まで)をカウント
        for i in range(<unsigned int>(size-2)):
            # 左上:右方向
            lt_r >>= 1
            lt_r &= lt_board
            if lt_r & lt_board:
                score_e += we * lt_sign
            # 左上:下方向
            lt_b >>= size
            lt_b &= lt_board
            if lt_b & lt_board:
                score_e += we * lt_sign
            # 右上:左方向
            rt_l <<= 1
            rt_l &= rt_board
            if rt_l & rt_board:
                score_e += we * rt_sign
            # 右上:下方向
            rt_b >>= size
            rt_b &= rt_board
            if rt_b & rt_board:
                score_e += we * rt_sign
            # 左下:右方向
            lb_r >>= 1
            lb_r &= lb_board
            if lb_r & lb_board:
                score_e += we * lb_sign
            # 左下:上方向
            lb_t <<= size
            lb_t &= lb_board
            if lb_t & lb_board:
                score_e += we * lb_sign
            # 右下:左方向
            rb_l <<= 1
            rb_l &= rb_board
            if rb_l & rb_board:
                score_e += we * rb_sign
            # 右下:上方向
            rb_t <<= size
            rb_t &= rb_board
            if rb_t & rb_board:
                score_e += we * rb_sign

        # 辺が同じ色で埋まっている場合はさらに加算
        top = int(''.join(['1'] * size + ['0'] * (size*(size-1))), 2)
        if lt_board & top == top:
            score_e += we * lt_sign
        left = int(''.join((['1'] + ['0'] * (size-1)) * size), 2)
        if lt_board & left == left:
            score_e += we * lt_sign
        right = int(''.join((['0'] * (size-1) + ['1']) * size), 2)
        if rb_board & right == right:
            score_e += we * rb_sign
        bottom = int(''.join(['0'] * (size*(size-1)) + ['1'] * size), 2)
        if rb_board & bottom == bottom:
            score_e += we * rb_sign

    return score_t + score_p + score_e
