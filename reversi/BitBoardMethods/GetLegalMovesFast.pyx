#cython: language_level=3
"""GetLegalMovesFast
"""

import sys


MAXSIZE64 = 2**63 - 1


def get_legal_moves(color, size, b, w, mask):
    """get_legal_moves
           return all legal moves
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_legal_moves_size8_64bit(color, b, w)

        return _get_legal_moves_size8(color, b, w)

    return _get_legal_moves(color, size, b, w, mask)


cdef inline _get_legal_moves_size8_64bit(color, unsigned long long b, unsigned long long w):
    """_get_legal_moves_size8_64bit
    """
    cdef:
        unsigned long long player, opponent

    player, opponent = (b, w) if color == 'black' else (w, b)

    cdef:
        unsigned long long blank = ~(player | opponent)
        unsigned long long horizontal = opponent & 0x7E7E7E7E7E7E7E7E  # horizontal mask value
        unsigned long long vertical = opponent & 0x00FFFFFFFFFFFF00    # vertical mask value
        unsigned long long diagonal = opponent & 0x007E7E7E7E7E7E00    # diagonal mask value
        unsigned long long tmp_h, tmp_v, tmp_d1, tmp_d2, legal_moves = 0

    # left/right
    tmp_h = horizontal & ((player << 1) | (player >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))

    # top/bottom
    tmp_v = vertical & ((player << 8) | (player >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))

    # left-top/right-bottom
    tmp_d1 = diagonal & ((player << 9) | (player >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))

    # right-top/left-bottom
    tmp_d2 = diagonal & ((player << 7) | (player >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))

    legal_moves = blank & ((tmp_h << 1) | (tmp_h >> 1) | (tmp_v << 8) | (tmp_v >> 8) | (tmp_d1 << 9) | (tmp_d1 >> 9) | (tmp_d2 << 7) | (tmp_d2 >> 7))

    # prepare result
    ret = []
    cdef:
        unsigned int x, y
        unsigned long long mask = 0x8000000000000000
    for y in range(8):
        for x in range(8):
            if legal_moves & mask:
                ret += [(x, y)]
            mask >>= 1

    return ret


cdef _get_legal_moves_size8(color, b, w):
    """_get_legal_moves_size8
    """
    # 前準備
    player, opponent = (b, w) if color == 'black' else (w, b)  # プレイヤーと相手を決定

    """
     a b c d e f g h
    1■■■■■■■■ … 上位(0)
    2■■■■■■■■
    3■■■■■■■■
    4■■■■■■■■
    5□□□□□□□□ … 下位(1)
    6□□□□□□□□
    7□□□□□□□□
    8□□□□□□□□
    """
    player |= 0x10000000000000000    # 32bit以下でもシフトできるよう対策
    opponent |= 0x10000000000000000

    cdef:
        unsigned int x, y, tmp0, tmp1
        unsigned int p0 = (player >> 32) & 0xFFFFFFFF    # プレイヤー石(上位)
        unsigned int p1 = player & 0xFFFFFFFF            # プレイヤー石(下位)
        unsigned int o0 = (opponent >> 32) & 0xFFFFFFFF  # 相手石(上位)
        unsigned int o1 = opponent & 0xFFFFFFFF          # 相手石(上位)
        unsigned int blank0 = ~(p0 | o0)                 # 空き(上位)
        unsigned int blank1 = ~(p1 | o1)                 # 空き(下位)
        unsigned int horizontal0 = o0 & 0x7E7E7E7E       # 水平方向のマスク値(上位)
        unsigned int horizontal1 = o1 & 0x7E7E7E7E       # 水平方向のマスク値(下位)
        unsigned int vertical0 = o0 & 0x00FFFFFF         # 垂直方向のマスク値(上位)
        unsigned int vertical1 = o1 & 0xFFFFFF00         # 垂直方向のマスク値(下位)
        unsigned int diagonal0 = o0 & 0x007E7E7E         # 斜め方向のマスク値(上位)
        unsigned int diagonal1 = o1 & 0x7E7E7E00         # 斜め方向のマスク値(下位)
        unsigned int legal_moves0 = 0                    # 石を置ける場所(上位)
        unsigned int legal_moves1 = 0                    # 石を置ける場所(下位)

    # 左方向に石を置ける場所を探す
    tmp0 = horizontal0 & (p0 << 1)
    tmp0 |= horizontal0 & (tmp0 << 1)
    tmp0 |= horizontal0 & (tmp0 << 1)
    tmp0 |= horizontal0 & (tmp0 << 1)
    tmp0 |= horizontal0 & (tmp0 << 1)
    tmp0 |= horizontal0 & (tmp0 << 1)
    legal_moves0 |= blank0 & (tmp0 << 1)

    tmp1 = horizontal1 & (p1 << 1)
    tmp1 |= horizontal1 & (tmp1 << 1)
    tmp1 |= horizontal1 & (tmp1 << 1)
    tmp1 |= horizontal1 & (tmp1 << 1)
    tmp1 |= horizontal1 & (tmp1 << 1)
    tmp1 |= horizontal1 & (tmp1 << 1)
    legal_moves1 |= blank1 & (tmp1 << 1)

    # 右方向に石を置ける場所を探す
    tmp0 = horizontal0 & (p0 >> 1)
    tmp0 |= horizontal0 & (tmp0 >> 1)
    tmp0 |= horizontal0 & (tmp0 >> 1)
    tmp0 |= horizontal0 & (tmp0 >> 1)
    tmp0 |= horizontal0 & (tmp0 >> 1)
    tmp0 |= horizontal0 & (tmp0 >> 1)
    legal_moves0 |= blank0 & (tmp0 >> 1)

    tmp1 = horizontal1 & (p1 >> 1)
    tmp1 |= horizontal1 & (tmp1 >> 1)
    tmp1 |= horizontal1 & (tmp1 >> 1)
    tmp1 |= horizontal1 & (tmp1 >> 1)
    tmp1 |= horizontal1 & (tmp1 >> 1)
    tmp1 |= horizontal1 & (tmp1 >> 1)
    legal_moves1 |= blank1 & (tmp1 >> 1)

    # 上方向に石を置ける場所を探す
    tmp1 = vertical1 & (p1 << 8)  # 下位のシフト
    tmp1 |= vertical1 & (tmp1 << 8)
    tmp1 |= vertical1 & (tmp1 << 8)
    legal_moves1 |= blank1 & (tmp1 << 8)

    tmp0 = vertical0 & ((p0 << 8) | ((tmp1 | p1) >> 24))   # 上位のシフト+下位続き+上位直下にプレイヤー
    tmp0 |= vertical0 & (tmp0 << 8)
    tmp0 |= vertical0 & (tmp0 << 8)
    legal_moves0 |= blank0 & ((tmp0 << 8) | (tmp1 >> 24))  # 上位のシフト+下位直上で置く場合

    # 下方向に石を置ける場所を探す
    tmp0 = vertical0 & (p0 >> 8)  # 上位のシフト
    tmp0 |= vertical0 & (tmp0 >> 8)
    tmp0 |= vertical0 & (tmp0 >> 8)
    legal_moves0 |= blank0 & (tmp0 >> 8)

    tmp1 = vertical1 & ((p1 >> 8) | ((tmp0 | p0) << 24))   # 下位のシフト+上位続き+下位直上にプレイヤー
    tmp1 |= vertical1 & (tmp1 >> 8)
    tmp1 |= vertical1 & (tmp1 >> 8)
    legal_moves1 |= blank1 & ((tmp1 >> 8) | (tmp0 << 24))  # 下位のシフト+上位直下で置く場合

    # 左斜め上方向に石を置ける場所を探す
    tmp1 = diagonal1 & (p1 << 9)  # 下位のシフト
    tmp1 |= diagonal1 & (tmp1 << 9)
    tmp1 |= diagonal1 & (tmp1 << 9)
    legal_moves1 |= blank1 & (tmp1 << 9)

    tmp0 = diagonal0 & ((p0 << 9) | ((tmp1 | p1) >> 23))   # 上位のシフト+下位続き+上位直下にプレイヤー
    tmp0 |= diagonal0 & (tmp0 << 9)
    tmp0 |= diagonal0 & (tmp0 << 9)
    legal_moves0 |= blank0 & ((tmp0 << 9) | (tmp1 >> 23))  # 上位のシフト+下位直上で置く場合

    # 左斜め下方向に石を置ける場所を探す
    tmp0 = diagonal0 & (p0 >> 7)  # 上位のシフト
    tmp0 |= diagonal0 & (tmp0 >> 7)
    tmp0 |= diagonal0 & (tmp0 >> 7)
    legal_moves0 |= blank0 & (tmp0 >> 7)

    tmp1 = diagonal1 & ((p1 >> 7) | ((tmp0 | p0) << 25))   # 下位のシフト+上位続き+下位直上にプレイヤー
    tmp1 |= diagonal1 & (tmp1 >> 7)
    tmp1 |= diagonal1 & (tmp1 >> 7)
    legal_moves1 |= blank1 & ((tmp1 >> 7) | (tmp0 << 25))  # 下位のシフト+上位直下で置く場合

    # 右斜め上方向に石を置ける場所を探す
    tmp1 = diagonal1 & (p1 << 7)  # 下位のシフト
    tmp1 |= diagonal1 & (tmp1 << 7)
    tmp1 |= diagonal1 & (tmp1 << 7)
    legal_moves1 |= blank1 & (tmp1 << 7)

    tmp0 = diagonal0 & ((p0 << 7) | ((tmp1 | p1) >> 25))   # 上位のシフト+下位続き+上位直下にプレイヤー
    tmp0 |= diagonal0 & (tmp0 << 7)
    tmp0 |= diagonal0 & (tmp0 << 7)
    legal_moves0 |= blank0 & ((tmp0 << 7) | (tmp1 >> 25))  # 上位のシフト+下位直上で置く場合

    # 右斜め下方向に石を置ける場所を探す
    tmp0 = diagonal0 & (p0 >> 9)  # 上位のシフト
    tmp0 |= diagonal0 & (tmp0 >> 9)
    tmp0 |= diagonal0 & (tmp0 >> 9)
    legal_moves0 |= blank0 & (tmp0 >> 9)

    tmp1 = diagonal1 & ((p1 >> 9) | ((tmp0 | p0) << 23))   # 下位のシフト+上位続き+下位直上にプレイヤー
    tmp1 |= diagonal1 & (tmp1 >> 9)
    tmp1 |= diagonal1 & (tmp1 >> 9)
    legal_moves1 |= blank1 & ((tmp1 >> 9) | (tmp0 << 23))  # 下位のシフト+上位直下で置く場合

    # 石が置ける場所を格納
    ret = []
    cdef:
        unsigned int mask0 = 0x80000000
        unsigned int mask1 = 0x80000000
    for y in range(8):
        # ビットボード上位32bit
        if y < 4:
            for x in range(8):
                if legal_moves0 & mask0:
                    ret += [(x, y)]
                mask0 >>= 1
        # ビットボード下位32bit
        else:
            for x in range(8):
                if legal_moves1 & mask1:
                    ret += [(x, y)]
                mask1 >>= 1

    return ret


cdef _get_legal_moves(color, size, b, w, mask):
    """_get_legal_moves
    """
    # 前準備
    player, opponent = (b, w) if color == 'black' else (w, b)  # プレイヤーと相手を決定
    legal_moves = 0                                            # 石が置ける場所
    horizontal = opponent & mask.h                             # 水平方向のチェック値
    vertical = opponent & mask.v                               # 垂直方向のチェック値
    diagonal = opponent & mask.d                               # 斜め方向のチェック値
    blank = ~(player | opponent)                               # 空きマス位置

    # 置ける場所を探す
    legal_moves |= _get_legal_moves_lshift(size, horizontal, player, blank, 1)     # 左方向
    legal_moves |= _get_legal_moves_rshift(size, horizontal, player, blank, 1)     # 右方向
    legal_moves |= _get_legal_moves_lshift(size, vertical, player, blank, size)    # 上方向
    legal_moves |= _get_legal_moves_rshift(size, vertical, player, blank, size)    # 下方向
    legal_moves |= _get_legal_moves_lshift(size, diagonal, player, blank, size+1)  # 左斜め上方向
    legal_moves |= _get_legal_moves_lshift(size, diagonal, player, blank, size-1)  # 右斜め上方向
    legal_moves |= _get_legal_moves_rshift(size, diagonal, player, blank, size-1)  # 左斜め下方向
    legal_moves |= _get_legal_moves_rshift(size, diagonal, player, blank, size+1)  # 右斜め下方向

    # 石が置ける場所を格納
    ret = []
    check = 1 << (size * size - 1)
    for y in range(size):
        for x in range(size):
            # 石が置ける場合
            if legal_moves & check:
                ret += [(x, y)]
            check >>= 1

    return ret


cdef _get_legal_moves_lshift(size, mask, player, blank, shift_size):
    """_get_legal_moves_lshift
           左シフトで石が置ける場所を取得
    """
    tmp = mask & (player << shift_size)
    for _ in range(size-3):
        tmp |= mask & (tmp << shift_size)
    return blank & (tmp << shift_size)


cdef _get_legal_moves_rshift(size, mask, player, blank, shift_size):
    """_get_legal_moves_rshift
           右シフトで石が置ける場所を取得
    """
    tmp = mask & (player >> shift_size)
    for _ in range(size-3):
        tmp |= mask & (tmp >> shift_size)
    return blank & (tmp >> shift_size)


cdef _print_bitboard(bitboard):
    """_print_bitboard
           ビットボード表示用
    """
    mask = 0x8000000000000000
    for y in range(8):
        for x in range(8):
            if bitboard & mask:
                print("●", end='')
            else:
                print("□", end='')
            mask >>= 1
        print()


cdef _print_bitboard_half(bitboard):
    """_print_bitboard_half
           ビットボード表示用
    """
    mask = 0x80000000
    for y in range(4):
        for x in range(8):
            if bitboard & mask:
                print("●", end='')
            else:
                print("□", end='')
            mask >>= 1
        print()
