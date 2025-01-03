#cython: language_level=3, profile=False, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
# Cython Coordinator Methods

import sys


DEF MAXSIZE64 = 2**63 - 1


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


# =========================================== #
# EvaluatorMethods
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
    b_bitboard, w_bitboard, h_bitboard = board.get_bitboard_info()
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
    b_bitboard, w_bitboard, h_bitboard = board.get_bitboard_info()
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
    b_bitboard, w_bitboard, h_bitboard = board.get_bitboard_info()
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


# =========================================== #
# ScorerMethods
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
        unsigned long long black, white, hole, blackwhite, not_blackwhite
        unsigned long long horizontal, vertical, diagonal
        unsigned long long l_blank, r_blank, t_blank, b_blank, lt_blank, rt_blank, lb_blank, rb_blank
        unsigned long long lt_x, rt_x, lb_x, rb_x
        unsigned long long lt_r, lt_b, rt_l, rt_b, lb_t, lb_r, rb_t, rb_l
        signed int lt_r_sign = 1, lt_b_sign = 1, rt_l_sign = 1, rt_b_sign = 1, lb_t_sign = 1, lb_r_sign = 1, rb_t_sign = 1, rb_l_sign = 1
    black, white, hole = board.get_bitboard_info()
    blackwhite = (black | white) & ~hole
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
