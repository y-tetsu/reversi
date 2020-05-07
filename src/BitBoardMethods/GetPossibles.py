#!/usr/bin/env python
"""
ビットボードの配置可能位置取得処理
"""

def get_possibles(color, size, b, w, mask):
    """
    石が置ける場所をすべて返す
    """
    ret = {}

    # 前準備
    player, opponent = (b, w) if color == 'black' else (w, b)  # プレイヤーと相手を決定
    possibles = 0                                              # 石が置ける場所
    horizontal = opponent & mask.h                             # 水平方向のチェック値
    vertical = opponent & mask.v                               # 垂直方向のチェック値
    diagonal = opponent & mask.d                               # 斜め方向のチェック値
    blank = ~(player | opponent)                               # 空きマス位置

    # 置ける場所を探す
    possibles |= get_possibles_lshift(size, horizontal, player, blank, 1)     # 左方向
    possibles |= get_possibles_rshift(size, horizontal, player, blank, 1)     # 右方向
    possibles |= get_possibles_lshift(size, vertical, player, blank, size)    # 上方向
    possibles |= get_possibles_rshift(size, vertical, player, blank, size)    # 下方向
    possibles |= get_possibles_lshift(size, diagonal, player, blank, size+1)  # 左斜め上方向
    possibles |= get_possibles_lshift(size, diagonal, player, blank, size-1)  # 右斜め上方向
    possibles |= get_possibles_rshift(size, diagonal, player, blank, size-1)  # 左斜め下方向
    possibles |= get_possibles_rshift(size, diagonal, player, blank, size+1)  # 右斜め下方向

    # 石が置ける場所を格納
    check = 1 << (size * size - 1)
    for y in range(size):
        for x in range(size):
            # 石が置ける場合
            if possibles & check:
                ret[(x, y)] = get_flippable_discs(size, player, opponent, x, y, mask)
            check >>= 1

    return ret

def get_flippable_discs(size, player, opponent, x, y, mask):
    """
    指定座標のひっくり返せる石の場所をすべて返す
    """
    ret = []
    reversibles = 0

    # 石を置く場所
    put = 1 << ((size*size-1)-(y*size+x))

    # 8方向を順番にチェック
    for direction in ('U', 'UR', 'R', 'BR', 'B', 'BL', 'L', 'UL'):
        tmp = 0
        check = get_next_put(size, put, direction, mask)

        # 相手の石が存在する限り位置を記憶
        while check & opponent:
            tmp |= check
            check = get_next_put(size, check, direction, mask)

        # 自分の石で囲まれている場合は結果を格納する
        if check & player:
            reversibles |= tmp

    # 配列に変換
    check = 1 << (size*size-1)
    for y in range(size):
        for x in range(size):
            if reversibles & check:
                ret += [(x, y)]
            check >>= 1

    return ret

def get_next_put(size, put, direction, mask):
    """
    指定位置から指定方向に1マス分移動した場所を返す
    """
    if direction == 'U':     # 上
        return (put << size) & mask.u
    elif direction == 'UR':  # 右上
        return (put << (size-1)) & mask.ur
    elif direction == 'R':   # 右
        return (put >> 1) & mask.r
    elif direction == 'BR':  # 右下
        return (put >> (size+1)) & mask.br
    elif direction == 'B':   # 下
        return (put >> size) & mask.b
    elif direction == 'BL':  # 左下
        return (put >> (size-1)) & mask.bl
    elif direction == 'L':   # 左
        return (put << 1) & mask.l
    elif direction == 'UL':  # 左上
        return (put << (size+1)) & mask.ul
    else:
        return 0

def get_possibles_lshift(size, mask, player, blank, shift_size):
    """
    左シフトで石が置ける場所を取得
    """
    tmp = mask & (player << shift_size)
    for _ in range(size-3):
        tmp |= mask & (tmp << shift_size)
    return blank & (tmp << shift_size)

def get_possibles_rshift(size, mask, player, blank, shift_size):
    """
    右シフトで石が置ける場所を取得
    """
    tmp = mask & (player >> shift_size)
    for _ in range(size-3):
        tmp |= mask & (tmp >> shift_size)
    return blank & (tmp >> shift_size)
