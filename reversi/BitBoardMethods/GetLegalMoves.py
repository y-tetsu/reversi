"""GetLegalMoves.py
"""


def get_legal_moves(color, size, b, w, mask):
    """
    石が置ける場所をすべて返す
    """
    # 前準備
    player, opponent = (b, w) if color == 'black' else (w, b)  # プレイヤーと相手を決定
    legal_moves = 0                                            # 石が置ける場所
    horizontal = opponent & mask.h                             # 水平方向のチェック値
    vertical = opponent & mask.v                               # 垂直方向のチェック値
    diagonal = opponent & mask.d                               # 斜め方向のチェック値
    blank = ~(player | opponent)                               # 空きマス位置

    # 置ける場所を探す
    legal_moves |= get_legal_moves_lshift(size, horizontal, player, blank, 1)     # 左方向
    legal_moves |= get_legal_moves_rshift(size, horizontal, player, blank, 1)     # 右方向
    legal_moves |= get_legal_moves_lshift(size, vertical, player, blank, size)    # 上方向
    legal_moves |= get_legal_moves_rshift(size, vertical, player, blank, size)    # 下方向
    legal_moves |= get_legal_moves_lshift(size, diagonal, player, blank, size+1)  # 左斜め上方向
    legal_moves |= get_legal_moves_lshift(size, diagonal, player, blank, size-1)  # 右斜め上方向
    legal_moves |= get_legal_moves_rshift(size, diagonal, player, blank, size-1)  # 左斜め下方向
    legal_moves |= get_legal_moves_rshift(size, diagonal, player, blank, size+1)  # 右斜め下方向

    # 石が置ける場所を格納
    ret = []
    check = 1 << (size * size - 1)
    for y in range(size):
        for x in range(size):
            # 石が置ける場合
            if legal_moves & check:
                ret.append((x, y))
            check >>= 1

    return ret


def get_legal_moves_lshift(size, mask, player, blank, shift_size):
    """
    左シフトで石が置ける場所を取得
    """
    tmp = mask & (player << shift_size)
    for _ in range(size-3):
        tmp |= mask & (tmp << shift_size)

    return blank & (tmp << shift_size)


def get_legal_moves_rshift(size, mask, player, blank, shift_size):
    """
    右シフトで石が置ける場所を取得
    """
    tmp = mask & (player >> shift_size)
    for _ in range(size-3):
        tmp |= mask & (tmp >> shift_size)

    return blank & (tmp >> shift_size)
