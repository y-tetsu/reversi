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


cdef _get_legal_moves_size8_64bit(color, unsigned long long b, unsigned long long w):
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
        unsigned long long tmp, legal_moves = 0

    # left
    tmp = horizontal & (player << 1)
    tmp |= horizontal & (tmp << 1)
    tmp |= horizontal & (tmp << 1)
    tmp |= horizontal & (tmp << 1)
    tmp |= horizontal & (tmp << 1)
    tmp |= horizontal & (tmp << 1)
    legal_moves |= blank & (tmp << 1)

    # right
    tmp = horizontal & (player >> 1)
    tmp |= horizontal & (tmp >> 1)
    tmp |= horizontal & (tmp >> 1)
    tmp |= horizontal & (tmp >> 1)
    tmp |= horizontal & (tmp >> 1)
    tmp |= horizontal & (tmp >> 1)
    legal_moves |= blank & (tmp >> 1)

    # top
    tmp = vertical & (player << 8)
    tmp |= vertical & (tmp << 8)
    tmp |= vertical & (tmp << 8)
    tmp |= vertical & (tmp << 8)
    tmp |= vertical & (tmp << 8)
    tmp |= vertical & (tmp << 8)
    legal_moves |= blank & (tmp << 8)

    # bottom
    tmp = vertical & (player >> 8)
    tmp |= vertical & (tmp >> 8)
    tmp |= vertical & (tmp >> 8)
    tmp |= vertical & (tmp >> 8)
    tmp |= vertical & (tmp >> 8)
    tmp |= vertical & (tmp >> 8)
    legal_moves |= blank & (tmp >> 8)

    # left-top
    tmp = diagonal & (player << 9)
    tmp |= diagonal & (tmp << 9)
    tmp |= diagonal & (tmp << 9)
    tmp |= diagonal & (tmp << 9)
    tmp |= diagonal & (tmp << 9)
    tmp |= diagonal & (tmp << 9)
    legal_moves |= blank & (tmp << 9)

    # left-bottom
    tmp = diagonal & (player >> 7)
    tmp |= diagonal & (tmp >> 7)
    tmp |= diagonal & (tmp >> 7)
    tmp |= diagonal & (tmp >> 7)
    tmp |= diagonal & (tmp >> 7)
    tmp |= diagonal & (tmp >> 7)
    legal_moves |= blank & (tmp >> 7)

    # right-top
    tmp = diagonal & (player << 7)
    tmp |= diagonal & (tmp << 7)
    tmp |= diagonal & (tmp << 7)
    tmp |= diagonal & (tmp << 7)
    tmp |= diagonal & (tmp << 7)
    tmp |= diagonal & (tmp << 7)
    legal_moves |= blank & (tmp << 7)

    # right-bottom
    tmp = diagonal & (player >> 9)
    tmp |= diagonal & (tmp >> 9)
    tmp |= diagonal & (tmp >> 9)
    tmp |= diagonal & (tmp >> 9)
    tmp |= diagonal & (tmp >> 9)
    tmp |= diagonal & (tmp >> 9)
    legal_moves |= blank & (tmp >> 9)

    # prepare result
    cdef:
        unsigned int x, y
        unsigned long long mask = 0x8000000000000000
    ret = {}
    for y in range(8):
        for x in range(8):
            if legal_moves & mask:
                ret[(x, y)] = _get_flippable_discs_size8_64bit(player, opponent, x, y)
            mask >>= 1

    return ret


cdef _get_flippable_discs_size8_64bit(unsigned long long player, unsigned long long opponent, unsigned int x, unsigned int y):
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned int direction
        unsigned long long buff, next_put
        unsigned long long move = 0
        unsigned long long flippable_discs = 0

    move = <unsigned long long>1 << (63-(y*8+x))

    for direction in range(8):
        buff = 0
        next_put = _get_next_put_size8_64bit(move, direction)

        # get discs of consecutive opponents
        while next_put & opponent:
            buff |= next_put
            next_put = _get_next_put_size8_64bit(next_put, direction)

        # store result if surrounded by own disc
        if next_put & player:
            flippable_discs |= buff

    # prepare result
    cdef:
        unsigned long long mask = 0x8000000000000000
    ret = []
    for y in range(8):
        for x in range(8):
            if flippable_discs & mask:
                ret += [(x, y)]
            mask >>= 1

    return ret


cdef inline unsigned long long _get_next_put_size8_64bit(unsigned long long put, unsigned int direction):
    """_get_next_put_size8_64bit
    """
    cdef:
        unsigned long long next_put

    if direction == 0:
        next_put = 0xFFFFFFFFFFFFFF00 & (put << 8)  # top
    elif direction == 1:
        next_put = 0x7F7F7F7F7F7F7F00 & (put << 7)  # right-top
    elif direction == 2:
        next_put = 0x7F7F7F7F7F7F7F7F & (put >> 1)  # right
    elif direction == 3:
        next_put = 0x007F7F7F7F7F7F7F & (put >> 9)  # right-bottom
    elif direction == 4:
        next_put = 0x00FFFFFFFFFFFFFF & (put >> 8)  # bottom
    elif direction == 5:
        next_put = 0x00FEFEFEFEFEFEFE & (put >> 7)  # left-bottom
    elif direction == 6:
        next_put = 0xFEFEFEFEFEFEFEFE & (put << 1)  # left
    elif direction == 7:
        next_put = 0xFEFEFEFEFEFEFE00 & (put << 9)  # left-top
    else:
        next_put = 0                                # unexpected

    return next_put


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
    ret = {}

    cdef:
        unsigned int mask0 = 0x80000000
        unsigned int mask1 = 0x80000000

    for y in range(8):
        # ビットボード上位32bit
        if y < 4:
            for x in range(8):
                if legal_moves0 & mask0:
                    ret[(x, y)] = _get_flippable_discs_size8(p0, p1, o0, o1, x, y)
                mask0 >>= 1
        # ビットボード下位32bit
        else:
            for x in range(8):
                if legal_moves1 & mask1:
                    ret[(x, y)] = _get_flippable_discs_size8(p0, p1, o0, o1, x, y)
                mask1 >>= 1

    return ret


cdef _get_flippable_discs_size8(unsigned int p0, unsigned int p1, unsigned int o0, unsigned int o1, unsigned int x, unsigned int y):
    """_get_flippable_discs_size8
    """
    cdef:
        unsigned int direction, next0, next1, buff0, buff1
        unsigned int put0 = 0              # 石を置く場所(上位)
        unsigned int put1 = 0              # 石を置く場所(下位)
        unsigned int flippable_discs0 = 0  # ひっくり返せる場所(上位)
        unsigned int flippable_discs1 = 0  # ひっくり返せる場所(下位)

    # 石を置く場所
    if y < 4:
        put0 = 1 << (31-(y*8+x))
    else:
        put1 = 1 << (31-((y-4)*8+x))

    # 8方向を順番にチェック
    for direction in range(8):
        buff0, buff1 = 0, 0
        next0, next1 = _get_next_put_size8(put0, put1, direction)

        # 相手の石が存在する限り位置を記憶
        while (next0 & o0) or (next1 & o1):
            buff0 |= next0
            buff1 |= next1
            next0, next1 = _get_next_put_size8(next0, next1, direction)

        # 自分の石で囲まれている場合は結果を格納する
        if (next0 & p0) or (next1 & p1):
            flippable_discs0 |= buff0
            flippable_discs1 |= buff1

    # 配列に変換
    ret = []

    cdef:
        unsigned int mask0 = 0x80000000
        unsigned int mask1 = 0x80000000

    for y in range(8):
        # ビットボード上位32bit
        if y < 4:
            for x in range(8):
                if flippable_discs0 & mask0:
                    ret += [(x, y)]
                mask0 >>= 1
        # ビットボード下位32bit
        else:
            for x in range(8):
                if flippable_discs1 & mask1:
                    ret += [(x, y)]
                mask1 >>= 1

    return ret


cdef _get_next_put_size8(unsigned int put0, unsigned int put1, unsigned int direction):
    """_get_next_put_size8
           指定位置から指定方向に1マス分移動した場所を返す(ボードサイズ8限定)
    """
    cdef:
        unsigned int upper, lower

    if direction == 0:     # 上
        upper = 0xFFFFFFFF & ((put0 << 8) | (put1 >> 24))
        lower = 0xFFFFFF00 & (put1 << 8)
    elif direction == 1:  # 右上
        upper = 0x7F7F7F7F & ((put0 << 7) | (put1 >> 25))
        lower = 0x7F7F7F00 & (put1 << 7)
    elif direction == 2:   # 右
        upper = 0x7F7F7F7F & (put0 >> 1)
        lower = 0x7F7F7F7F & (put1 >> 1)
    elif direction == 3:  # 右下
        upper = 0x007F7F7F & (put0 >> 9)
        lower = 0x7F7F7F7F & ((put1 >> 9) | (put0 << 23))
    elif direction == 4:   # 下
        upper = 0x00FFFFFF & (put0 >> 8)
        lower = 0xFFFFFFFF & ((put1 >> 8) | (put0 << 24))
    elif direction == 5:  # 左下
        upper = 0x00FEFEFE & (put0 >> 7)
        lower = 0xFEFEFEFE & ((put1 >> 7) | (put0 << 25))
    elif direction == 6:   # 左
        upper = 0xFEFEFEFE & (put0 << 1)
        lower = 0xFEFEFEFE & (put1 << 1)
    elif direction == 7:  # 左上
        upper = 0xFEFEFEFE & ((put0 << 9) | (put1 >> 23))
        lower = 0xFEFEFE00 & (put1 << 9)
    else:
        upper, lower = 0, 0

    return upper, lower


cdef _get_legal_moves(color, size, b, w, mask):
    """_get_legal_moves
    """
    ret = {}

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
    check = 1 << (size * size - 1)
    for y in range(size):
        for x in range(size):
            # 石が置ける場合
            if legal_moves & check:
                ret[(x, y)] = _get_flippable_discs(size, player, opponent, x, y, mask)
            check >>= 1

    return ret


cdef _get_flippable_discs(size, player, opponent, x, y, mask):
    """_get_flippable_discs
    """
    ret = []
    flippable_discs = 0

    # 石を置く場所
    put = 1 << ((size*size-1)-(y*size+x))

    # 8方向を順番にチェック
    for direction in ('U', 'UR', 'R', 'BR', 'B', 'BL', 'L', 'UL'):
        tmp = 0
        check = _get_next_put(size, put, direction, mask)

        # 相手の石が存在する限り位置を記憶
        while check & opponent:
            tmp |= check
            check = _get_next_put(size, check, direction, mask)

        # 自分の石で囲まれている場合は結果を格納する
        if check & player:
            flippable_discs |= tmp

    # 配列に変換
    check = 1 << (size*size-1)
    for y in range(size):
        for x in range(size):
            if flippable_discs & check:
                ret += [(x, y)]
            check >>= 1

    return ret


cdef _get_next_put(size, put, direction, mask):
    """_get_next_put
           指定位置から指定方向に1マス分移動した場所を返す(ボードサイズ8以外)
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
