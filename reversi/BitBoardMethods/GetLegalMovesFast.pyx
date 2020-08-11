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

    return _get_legal_moves(color, size, b, w, mask)


def get_legal_moves_bits(color, size, b, w, mask):
    """get_legal_moves_bits
           return all legal moves bits
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_legal_moves_bits_size8_64bit(color, b, w)

    return _get_legal_moves_bits(color, size, b, w, mask)


def get_bit_count(size, bits):
    """get_bit_count
           return bit count
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_bit_count_size8_64bit(bits)

    return _get_bit_count(size, bits)


cdef inline _get_legal_moves_size8_64bit(color, unsigned long long b, unsigned long long w):
    """_get_legal_moves_size8_64bit
    """
    cdef:
        unsigned long long legal_moves
    legal_moves = _get_legal_moves_bits_size8_64bit(color, b, w)

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


cdef inline unsigned long long _get_legal_moves_bits_size8_64bit(color, unsigned long long b, unsigned long long w):
    """_get_legal_moves_bits_size8_64bit
    """
    cdef:
        unsigned long long player, opponent

    if color == 'black':
        player = b
        opponent = w
    else:
        player = w
        opponent = b

    cdef:
        unsigned long long blank = ~(player | opponent)
        unsigned long long horizontal = opponent & <unsigned long long>0x7E7E7E7E7E7E7E7E  # horizontal mask value
        unsigned long long vertical = opponent & <unsigned long long>0x00FFFFFFFFFFFF00    # vertical mask value
        unsigned long long diagonal = opponent & <unsigned long long>0x007E7E7E7E7E7E00    # diagonal mask value
        unsigned long long tmp_h, tmp_v, tmp_d1, tmp_d2

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

    return blank & ((tmp_h << 1) | (tmp_h >> 1) | (tmp_v << 8) | (tmp_v >> 8) | (tmp_d1 << 9) | (tmp_d1 >> 9) | (tmp_d2 << 7) | (tmp_d2 >> 7))


cdef inline unsigned long long _get_bit_count_size8_64bit(unsigned long long bits):
    """_get_bit_count_size8_64bit
    """
    bits = (bits & <unsigned long long>0x5555555555555555) + (bits >> <unsigned int>1 & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + (bits >> <unsigned int>2 & <unsigned long long>0x3333333333333333)
    bits = (bits & <unsigned long long>0x0F0F0F0F0F0F0F0F) + (bits >> <unsigned int>4 & <unsigned long long>0x0F0F0F0F0F0F0F0F)
    bits = (bits & <unsigned long long>0x00FF00FF00FF00FF) + (bits >> <unsigned int>8 & <unsigned long long>0x00FF00FF00FF00FF)
    bits = (bits & <unsigned long long>0x0000FFFF0000FFFF) + (bits >> <unsigned int>16 & <unsigned long long>0x0000FFFF0000FFFF)

    return (bits & <unsigned long long>0x00000000FFFFFFFF) + (bits >> <unsigned int>32 & <unsigned long long>0x00000000FFFFFFFF)


cdef _get_legal_moves(color, size, b, w, mask):
    """_get_legal_moves
    """
    legal_moves_bits = _get_legal_moves_bits(color, size, b, w, mask)

    # 石が置ける場所を格納
    ret = []
    check = 1 << (size * size - 1)
    for y in range(size):
        for x in range(size):
            # 石が置ける場合
            if legal_moves_bits & check:
                ret += [(x, y)]
            check >>= 1

    return ret


cdef _get_legal_moves_bits(color, size, b, w, mask):
    """_get_legal_moves_bits
    """
    # 前準備
    player, opponent = (b, w) if color == 'black' else (w, b)  # プレイヤーと相手を決定
    legal_moves_bits = 0                                       # 石が置ける場所
    horizontal = opponent & mask.h                             # 水平方向のチェック値
    vertical = opponent & mask.v                               # 垂直方向のチェック値
    diagonal = opponent & mask.d                               # 斜め方向のチェック値
    blank = ~(player | opponent)                               # 空きマス位置

    # 置ける場所を探す
    legal_moves_bits |= _get_legal_moves_lshift(size, horizontal, player, blank, 1)     # 左方向
    legal_moves_bits |= _get_legal_moves_rshift(size, horizontal, player, blank, 1)     # 右方向
    legal_moves_bits |= _get_legal_moves_lshift(size, vertical, player, blank, size)    # 上方向
    legal_moves_bits |= _get_legal_moves_rshift(size, vertical, player, blank, size)    # 下方向
    legal_moves_bits |= _get_legal_moves_lshift(size, diagonal, player, blank, size+1)  # 左斜め上方向
    legal_moves_bits |= _get_legal_moves_lshift(size, diagonal, player, blank, size-1)  # 右斜め上方向
    legal_moves_bits |= _get_legal_moves_rshift(size, diagonal, player, blank, size-1)  # 左斜め下方向
    legal_moves_bits |= _get_legal_moves_rshift(size, diagonal, player, blank, size+1)  # 右斜め下方向

    return legal_moves_bits


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


cdef _get_bit_count(size, bits):
    """_get_bit_count
    """
    count = 0
    mask = 1 << ((size**2)-1)
    for y in range(size):
        for x in range(size):
            if bits & mask:
                count += 1
            mask >>= 1

    return count


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
