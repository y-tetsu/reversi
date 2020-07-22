#cython: language_level=3
"""GetFlippableDiscsFast
"""

import sys


MAXSIZE64 = 2**63 - 1


def get_flippable_discs(size, player, opponent, x, y, mask):
    """get_flippable_discs
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_flippable_discs_size8_64bit(player, opponent, x, y)

        return _get_flippable_discs_size8(player, opponent, x, y)

    return _get_flippable_discs(size, player, opponent, x, y, mask)


cdef _get_flippable_discs_size8_64bit(unsigned long long player, unsigned long long opponent, unsigned int x, unsigned int y):
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned int direction1, direction2
        unsigned long long buff, next_put
        unsigned long long move = 0
        unsigned long long flippable_discs = 0

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


cdef _get_flippable_discs_size8(unsigned long long player, unsigned long long opponent, unsigned int x, unsigned int y):
    """_get_flippable_discs_size8
    """
    cdef:
        unsigned int p0 = (player >> 32) & 0xFFFFFFFF    # プレイヤー石(上位)
        unsigned int p1 = player & 0xFFFFFFFF            # プレイヤー石(下位)
        unsigned int o0 = (opponent >> 32) & 0xFFFFFFFF  # 相手石(上位)
        unsigned int o1 = opponent & 0xFFFFFFFF          # 相手石(上位)
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
