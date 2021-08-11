"""Evaluate
"""

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


def evaluate_tpw(t, params, color, board, possibility_b, possibility_w):
    if not possibility_b and not possibility_w:  # 勝敗が決まっている場合
        ret = board._black_score - board._white_score
        if ret > 0:    # 黒が勝った
            ret += params[1]
        elif ret < 0:  # 白が勝った
            ret -= params[1]
        return ret
    return t.get_score(board=board) + (possibility_b - possibility_w) * params[0]


def evaluate_tpwe(t, params, color, board, possibility_b, possibility_w):
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
