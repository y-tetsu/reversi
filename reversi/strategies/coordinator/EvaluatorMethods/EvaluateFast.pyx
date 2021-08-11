#cython: language_level=3
"""Evaluate
"""

import sys

EDGE_MASKVALUE = [
    0xC000000000000000,  # 上左2
    0xE000000000000000,  # 上左3
    0xF000000000000000,  # 上左4
    0xF800000000000000,  # 上左5
    0xFC00000000000000,  # 上左6
    0xFE00000000000000,  # 上左7
    0x0300000000000000,  # 上右2
    0x0700000000000000,  # 上右3
    0x0F00000000000000,  # 上右4
    0x1F00000000000000,  # 上右5
    0x3F00000000000000,  # 上右6
    0x7F00000000000000,  # 上右7
    0xFF00000000000000,  # 上8
    0x0101000000000000,  # 右上2
    0x0101010000000000,  # 右上3
    0x0101010100000000,  # 右上4
    0x0101010101000000,  # 右上5
    0x0101010101010000,  # 右上6
    0x0101010101010100,  # 右上7
    0x0000000000000101,  # 右下2
    0x0000000000010101,  # 右下3
    0x0000000001010101,  # 右下4
    0x0000000101010101,  # 右下5
    0x0000010101010101,  # 右下6
    0x0001010101010101,  # 右下7
    0x0101010101010101,  # 右8
    0x00000000000000C0,  # 下左2
    0x00000000000000E0,  # 下左3
    0x00000000000000F0,  # 下左4
    0x00000000000000F8,  # 下左5
    0x00000000000000FC,  # 下左6
    0x00000000000000FE,  # 下左7
    0x0000000000000003,  # 下右2
    0x0000000000000007,  # 下右3
    0x000000000000000F,  # 下右4
    0x000000000000001F,  # 下右5
    0x000000000000003F,  # 下右6
    0x000000000000007F,  # 下右7
    0x00000000000000FF,  # 下8
    0x8080000000000000,  # 左上2
    0x8080800000000000,  # 左上3
    0x8080808000000000,  # 左上4
    0x8080808080000000,  # 左上5
    0x8080808080800000,  # 左上6
    0x8080808080808000,  # 左上7
    0x0000000000008080,  # 左下2
    0x0000000000808080,  # 左下3
    0x0000000080808080,  # 左下4
    0x0000008080808080,  # 左下5
    0x0000808080808080,  # 左下6
    0x0080808080808080,  # 左下7
    0x8080808080808080,  # 左8
]

MAXSIZE64 = 2**63 - 1



def evaluate_tpw(t, params, color, board, possibility_b, possibility_w):
    return _evaluate_tpw(t, params, color, board, possibility_b, possibility_w)


cdef inline signed int _evaluate_tpw(t, params, color, board, possibility_b, possibility_w):
    if not possibility_b and not possibility_w:  # 勝敗が決まっている場合
        ret = board._black_score - board._white_score
        if ret > 0:    # 黒が勝った
            ret += params[1]
        elif ret < 0:  # 白が勝った
            ret -= params[1]
        return ret
    return t.get_score(board=board) + (possibility_b - possibility_w) * params[0]


def evaluate_tpwe(t, params, color, board, possibility_b, possibility_w):
    if sys.maxsize == MAXSIZE64:
        return _evaluate_tpwe_64bit(t, params, color, board, possibility_b, possibility_w)
    return _evaluate_tpwe(t, params, color, board, possibility_b, possibility_w)


cdef inline signed int _evaluate_tpwe_64bit(t, params, color, board, possibility_b, possibility_w):
    cdef:
        unsigned long long maskvalue = 0
        unsigned long long b_bitboard, w_bitboard
        unsigned long long edge_maskvalue[52]
        signed int ret = 0
        signed int score_t = 0
        signed int score_p = 0
        signed int score_e = 0
        signed int tmp_b, tmp_w
        signed int wp = params[0]
        signed int ww = params[1]
        signed int we = params[2]
    if not possibility_b and not possibility_w:  # 勝敗が決まっている場合
        ret = board._black_score - board._white_score
        if ret > <signed int>0:    # 黒が勝った
            ret += ww
        elif ret < <signed int>0:  # 白が勝った
            ret -= ww
        return ret
    edge_maskvalue[0] = <unsigned long long>0xC000000000000000  # 上左2
    edge_maskvalue[1] = <unsigned long long>0xE000000000000000  # 上左3
    edge_maskvalue[2] = <unsigned long long>0xF000000000000000  # 上左4
    edge_maskvalue[3] = <unsigned long long>0xF800000000000000  # 上左5
    edge_maskvalue[4] = <unsigned long long>0xFC00000000000000  # 上左6
    edge_maskvalue[5] = <unsigned long long>0xFE00000000000000  # 上左7
    edge_maskvalue[6] = <unsigned long long>0x0300000000000000  # 上右2
    edge_maskvalue[7] = <unsigned long long>0x0700000000000000  # 上右3
    edge_maskvalue[8] = <unsigned long long>0x0F00000000000000  # 上右4
    edge_maskvalue[9] = <unsigned long long>0x1F00000000000000  # 上右5
    edge_maskvalue[10] = <unsigned long long>0x3F00000000000000  # 上右6
    edge_maskvalue[11] = <unsigned long long>0x7F00000000000000  # 上右7
    edge_maskvalue[12] = <unsigned long long>0xFF00000000000000  # 上8
    edge_maskvalue[13] = <unsigned long long>0x0101000000000000  # 右上2
    edge_maskvalue[14] = <unsigned long long>0x0101010000000000  # 右上3
    edge_maskvalue[15] = <unsigned long long>0x0101010100000000  # 右上4
    edge_maskvalue[16] = <unsigned long long>0x0101010101000000  # 右上5
    edge_maskvalue[17] = <unsigned long long>0x0101010101010000  # 右上6
    edge_maskvalue[18] = <unsigned long long>0x0101010101010100  # 右上7
    edge_maskvalue[19] = <unsigned long long>0x0000000000000101  # 右下2
    edge_maskvalue[20] = <unsigned long long>0x0000000000010101  # 右下3
    edge_maskvalue[21] = <unsigned long long>0x0000000001010101  # 右下4
    edge_maskvalue[22] = <unsigned long long>0x0000000101010101  # 右下5
    edge_maskvalue[23] = <unsigned long long>0x0000010101010101  # 右下6
    edge_maskvalue[24] = <unsigned long long>0x0001010101010101  # 右下7
    edge_maskvalue[25] = <unsigned long long>0x0101010101010101  # 右8
    edge_maskvalue[26] = <unsigned long long>0x00000000000000C0  # 下左2
    edge_maskvalue[27] = <unsigned long long>0x00000000000000E0  # 下左3
    edge_maskvalue[28] = <unsigned long long>0x00000000000000F0  # 下左4
    edge_maskvalue[29] = <unsigned long long>0x00000000000000F8  # 下左5
    edge_maskvalue[30] = <unsigned long long>0x00000000000000FC  # 下左6
    edge_maskvalue[31] = <unsigned long long>0x00000000000000FE  # 下左7
    edge_maskvalue[32] = <unsigned long long>0x0000000000000003  # 下右2
    edge_maskvalue[33] = <unsigned long long>0x0000000000000007  # 下右3
    edge_maskvalue[34] = <unsigned long long>0x000000000000000F  # 下右4
    edge_maskvalue[35] = <unsigned long long>0x000000000000001F  # 下右5
    edge_maskvalue[36] = <unsigned long long>0x000000000000003F  # 下右6
    edge_maskvalue[37] = <unsigned long long>0x000000000000007F  # 下右7
    edge_maskvalue[38] = <unsigned long long>0x00000000000000FF  # 下8
    edge_maskvalue[39] = <unsigned long long>0x8080000000000000  # 左上2
    edge_maskvalue[40] = <unsigned long long>0x8080800000000000  # 左上3
    edge_maskvalue[41] = <unsigned long long>0x8080808000000000  # 左上4
    edge_maskvalue[42] = <unsigned long long>0x8080808080000000  # 左上5
    edge_maskvalue[43] = <unsigned long long>0x8080808080800000  # 左上6
    edge_maskvalue[44] = <unsigned long long>0x8080808080808000  # 左上7
    edge_maskvalue[45] = <unsigned long long>0x0000000000008080  # 左下2
    edge_maskvalue[46] = <unsigned long long>0x0000000000808080  # 左下3
    edge_maskvalue[47] = <unsigned long long>0x0000000080808080  # 左下4
    edge_maskvalue[48] = <unsigned long long>0x0000008080808080  # 左下5
    edge_maskvalue[49] = <unsigned long long>0x0000808080808080  # 左下6
    edge_maskvalue[50] = <unsigned long long>0x0080808080808080  # 左下7
    edge_maskvalue[51] = <unsigned long long>0x8080808080808080  # 左8
    score_t = t.get_score(board=board)
    score_p = (possibility_b - possibility_w) * wp
    if board.size != 8:
        return score_t + score_p
    b_bitboard, w_bitboard = board.get_bitboard_info()
    for maskvalue in edge_maskvalue:
        tmp_b = we if (b_bitboard & maskvalue) == maskvalue else <signed int>0
        tmp_w = we if (w_bitboard & maskvalue) == maskvalue else <signed int>0
        score_e += tmp_b - tmp_w
    return score_t + score_p + score_e


cdef inline signed int _evaluate_tpwe(t, params, color, board, possibility_b, possibility_w):
    if not possibility_b and not possibility_w:  # 勝敗が決まっている場合
        ret = board._black_score - board._white_score
        if ret > 0:    # 黒が勝った
            ret += params[1]
        elif ret < 0:  # 白が勝った
            ret -= params[1]
        return ret
    if board.size != 8:
        return t.get_score(board=board) + (possibility_b - possibility_w) * params[0]
    score = 0
    b_bitboard, w_bitboard = board.get_bitboard_info()
    for maskvalue in EDGE_MASKVALUE:
        score_b = params[2] if (b_bitboard & maskvalue) == maskvalue else 0
        score_w = params[2] if (w_bitboard & maskvalue) == maskvalue else 0
        score += score_b - score_w
    return t.get_score(board=board) + (possibility_b - possibility_w) * params[0] + score
