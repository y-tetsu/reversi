#cython: language_level=3, profile=False, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""Cython BitBoardMethods
"""

import sys
from collections import namedtuple


MAXSIZE64 = 2**63 - 1

MIN_BOARD_SIZE = 4
MAX_BOARD_SIZE = 26


def get_legal_moves(color, size, b, w, h, mask):
    """get_legal_moves
           return all legal moves
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_legal_moves_size8_64bit(color, b, w, h)

    return _get_legal_moves(color, size, b, w, h, mask)


def get_legal_moves_bits(color, size, b, w, h, mask):
    """get_legal_moves_bits
           return all legal moves bits
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_legal_moves_bits_size8_64bit(color, b, w, h)

    return _get_legal_moves_bits(color, size, b, w, h, mask)


def get_bit_count(size, bits):
    """get_bit_count
           return bit count
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _popcount_size8_64bit(bits)

    return _get_bit_count(size, bits)


def get_flippable_discs(color, size, black_bitboard, white_bitboard, x, y, mask):
    """get_flippable_discs
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_flippable_discs_size8_64bit(color == 'black', black_bitboard, white_bitboard, x, y)

        return _get_flippable_discs_size8(color, black_bitboard, white_bitboard, x, y)

    return _get_flippable_discs(color, size, black_bitboard, white_bitboard, x, y, mask)


def put_disc(board, color, x, y):
    """put_disc
    """
    size = board.size

    if size == 8 and sys.maxsize == MAXSIZE64:
        return _put_disc_size8_64bit(board, color == 'black', x, y)

    return _put_disc(size, board, color, x, y)


def get_board_info(size, b, w):
    """get_board_info
          return list of board information(black:1, white:-1, blank:0)
    """
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_board_info_size8_64bit(b, w)

        return _get_board_info_size8(b, w)

    return _get_board_info(size, b, w)


def undo(board):
    """undo
    """
    _undo(board)


cdef class CythonBitBoard():
    """Cython BitBoard
    """
    cdef readonly size
    cdef public _black_score, _white_score, prev, _green_bitboard, _black_bitboard, _white_bitboard, _hole_bitboard, _ini_green, _ini_black, _ini_white, _mask, _flippable_discs_num

    def __init__(self, hole=0x0, ini_black=None, ini_white=None):
        self.size = 8
        self.prev = []
        self._green_bitboard = 0
        self._black_bitboard = 0
        self._white_bitboard = 0

        # 初期配置
        size = self.size
        center = size // 2
        self._ini_black = 1 << ((size*size-1)-(size*(center-1)+center))
        self._ini_black |= 1 << ((size*size-1)-(size*center+(center-1)))
        self._ini_white = 1 << ((size*size-1)-(size*(center-1)+(center-1)))
        self._ini_white |= 1 << ((size*size-1)-(size*center+center))
        if ini_black is not None:
            self._ini_black = ini_black
        if ini_white is not None:
            self._ini_white = ini_white

        self._ini_green = self._ini_black & self._ini_white
        self._ini_black &= ~self._ini_green
        self._ini_white &= ~self._ini_green
        self._green_bitboard |= self._ini_green
        self._black_bitboard |= self._ini_black
        self._white_bitboard |= self._ini_white
        self._hole_bitboard = hole

        # 置ける場所の検出用マスク
        BitMask = namedtuple('BitMask', 'h v d u ur r br b bl l ul')
        self._mask = BitMask(
            int(''.join((['0'] + ['1'] * (size-2) + ['0']) * size), 2),                                      # 水平方向のマスク値
            int(''.join(['0'] * size + ['1'] * size * (size-2) + ['0'] * size), 2),                          # 垂直方向のマスク値
            int(''.join(['0'] * size + (['0'] + (['1'] * (size-2)) + ['0']) * (size-2) + ['0'] * size), 2),  # 斜め方向のマスク値
            int(''.join(['1'] * size * (size-1) + ['0'] * size), 2),                                         # 上方向のマスク値
            int(''.join((['0'] + ['1'] * (size-1)) * (size-1) + ['0'] * size), 2),                           # 右上方向のマスク値
            int(''.join((['0'] + ['1'] * (size-1)) * size), 2),                                              # 右方向のマスク値
            int(''.join(['0'] * size + (['0'] + ['1'] * (size-1)) * (size-1)), 2),                           # 右下方向のマスク値
            int(''.join(['0'] * size + ['1'] * size * (size-1)), 2),                                         # 下方向のマスク値
            int(''.join(['0'] * size + (['1'] * (size-1) + ['0']) * (size-1)), 2),                           # 左下方向のマスク値
            int(''.join((['1'] * (size-1) + ['0']) * size), 2),                                              # 左方向のマスク値
            int(''.join((['1'] * (size-1) + ['0']) * (size-1) + ['0'] * size), 2)                            # 左上方向のマスク値
        )

        # 穴をあける
        self._green_bitboard &= ~self._hole_bitboard
        self._black_bitboard &= ~self._hole_bitboard
        self._white_bitboard &= ~self._hole_bitboard
        self.update_score()

    def _is_invalid_size(self, size):
        return not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0)

    def __str__(self):
        header = '   ' + ' '.join([chr(97 + i) for i in range(8)]) + '\n'
        board = [['□' for _ in range(8)] for _ in range(8)]
        mask = 1 << 63
        for y in range(8):
            for x in range(8):
                if self._hole_bitboard & mask:
                    board[y][x] = '　'
                elif self._black_bitboard & mask:
                    board[y][x] = '〇'
                elif self._white_bitboard & mask:
                    board[y][x] = '●'
                elif self._green_bitboard & mask:
                    board[y][x] = '◎'
                mask >>= 1

        body = ''
        for num, row in enumerate(board, 1):
            body += f'{num:2d}' + ''.join([value for value in row]) + '\n'

        return header + body

    def get_legal_moves(self, str color):
        return _get_legal_moves_size8_64bit(color, self._black_bitboard, self._white_bitboard, self._hole_bitboard)

    def get_legal_moves_bits(self, str color):
        return _get_legal_moves_bits_size8_64bit(color, self._black_bitboard, self._white_bitboard, self._hole_bitboard)

    def get_flippable_discs(self, str color, x, y):
        return _get_flippable_discs_size8_64bit(color == 'black', self._black_bitboard, self._white_bitboard, x, y)

    def put_disc(self, str color, x, y):
        return _put_disc_size8_64bit(self, color == 'black', x, y)

    def update_score(self):
        self._black_score, self._white_score = 0, 0
        mask = 1 << 63
        for y in range(8):
            for x in range(8):
                if self._black_bitboard & mask:
                    self._black_score += 1
                elif self._white_bitboard & mask:
                    self._white_score += 1
                mask >>= 1

    def get_board_info(self):
        return _get_board_info_size8_64bit(self._black_bitboard, self._white_bitboard)

    def get_board_line_info(self, player, black='*', white='O', hole='_', empty='-'):
        board_line_info = ''
        # board
        size = self.size
        mask = 1 << (size * size - 1)
        for y in range(size):
            for x in range(size):
                if self._black_bitboard & mask:
                    board_line_info += black
                elif self._white_bitboard & mask:
                    board_line_info += white
                elif self._hole_bitboard & mask:
                    board_line_info += hole
                else:
                    board_line_info += empty
                mask >>= 1
        # player
        if player == 'black':
            board_line_info += black
        elif player == 'white':
            board_line_info += white
        else:
            board_line_info += empty
        return board_line_info

    def get_bit_count(self, bits):
        return _popcount_size8_64bit(bits)

    def get_bitboard_info(self):
        return self._black_bitboard, self._white_bitboard, self._hole_bitboard

    def undo(self):
        (self._black_bitboard, self._white_bitboard, self._black_score, self._white_score) = self.prev.pop()

    def get_remain(self):
        size = self.size
        mask = 1 << (size * size - 1)
        remain = size * size
        hole = self._hole_bitboard
        green = self._green_bitboard
        black = self._black_bitboard
        white = self._white_bitboard
        not_blank = hole | green | black | white
        return remain - self.get_bit_count(not_blank)


# -------------------------------------------------- #
# _get_legal_moves
cdef inline _get_legal_moves_size8_64bit(str color, unsigned long long b, unsigned long long w, unsigned long long h):
    """_get_legal_moves_size8_64bit
    """
    cdef:
        unsigned long long legal_moves
    legal_moves = _get_legal_moves_bits_size8_64bit(color, b, w, h)

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


cdef _get_legal_moves(color, size, b, w, h, mask):
    """_get_legal_moves
    """
    legal_moves_bits = _get_legal_moves_bits(color, size, b, w, h, mask)

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


cdef inline unsigned long long _get_legal_moves_bits_size8_64bit(str color, unsigned long long b, unsigned long long w, unsigned long long h):
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
        unsigned long long blank = ~(player | opponent | h)
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


cdef _get_legal_moves_bits(color, size, b, w, h, mask):
    """_get_legal_moves_bits
    """
    # 前準備
    player, opponent = (b, w) if color == 'black' else (w, b)  # プレイヤーと相手を決定
    legal_moves_bits = 0                                       # 石が置ける場所
    horizontal = opponent & mask.h                             # 水平方向のチェック値
    vertical = opponent & mask.v                               # 垂直方向のチェック値
    diagonal = opponent & mask.d                               # 斜め方向のチェック値
    blank = ~(player | opponent | h)                           # 空きマス位置

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


cdef inline unsigned long long _popcount_size8_64bit(unsigned long long bits):
    """_popcount_size8_64bit
    """
    bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
    bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
    bits = bits + (bits >> <unsigned int>8)
    bits = bits + (bits >> <unsigned int>16)
    return (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F


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


# -------------------------------------------------- #
# _get_flippable_discs
cdef inline _get_flippable_discs_size8_64bit(unsigned int color, unsigned long long black_bitboard, unsigned long long white_bitboard, unsigned int x, unsigned int y):
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned long long move = <unsigned long long>1 << (63-(y*8+x))
        unsigned long long flippable_discs = 0
        unsigned long long mask = 0x8000000000000000
    ret = []
    flippable_discs = _get_flippable_discs_num_size8_64bit(color, black_bitboard, white_bitboard, move)
    for y in range(8):
        for x in range(8):
            if flippable_discs & mask:
                ret += [(x, y)]
            mask >>= 1
    return ret


cdef _get_flippable_discs_size8(color, black_bitboard, white_bitboard, unsigned int x, unsigned int y):
    """_get_flippable_discs_size8
    """
    player, opponent = (black_bitboard, white_bitboard) if color == 'black' else (white_bitboard, black_bitboard)
    player |= 0x10000000000000000    # 32bit以下でもシフトできるよう対策
    opponent |= 0x10000000000000000

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


cdef _get_flippable_discs(color, size, black_bitboard, white_bitboard, x, y, mask):
    """_get_flippable_discs
    """
    ret = []
    flippable_discs = 0
    player, opponent = (black_bitboard, white_bitboard) if color == 'black' else (white_bitboard, black_bitboard)

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


cdef inline unsigned long long _get_flippable_discs_num_size8_64bit(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long move):
    """_get_flippable_discs_num_size8_64bit
    """
    cdef:
        unsigned long long t_, rt, r_, rb, b_, lb, l_, lt
        unsigned long long m_t_, m_rt, m_r_, m_rb, m_b_, m_lb, m_l_, m_lt
        unsigned long long player = w, opponent = b, flippable_discs_num = 0
        unsigned int x, other = 0
    if int_color:
        player = b
        opponent = w
    # x座標を取得
    x = <unsigned int>(move % <unsigned int>0xFF)
    # ひっくり返せるディスクを求める
    if x >= <unsigned int>0x40:
        # (1)a1, b1, a2, b2
        if move >= <unsigned long long>0x0001000000000000:
            # 右、右下、下
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            m_rb = <unsigned long long>0x007F7F7F7F7F7F7F & opponent
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            rb = m_rb & (move >> <unsigned int>9)  # right-bottom
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            for _ in range(5):
                r_ |= m_r_ & (r_ >> <unsigned int>1)
                rb |= m_rb & (rb >> <unsigned int>9)
                b_ |= m_b_ & (b_ >> <unsigned int>8)
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
            if (<unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)) & player:
                flippable_discs_num |= rb
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
        # (4)a7, b7, a8, b8
        elif move <= <unsigned long long>0x0000000000008000:
            # 上、右上、右
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            m_rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & opponent
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            t_ = m_t_ & (move << <unsigned int>8)  # top
            rt = m_rt & (move << <unsigned int>7)  # right-top
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            for _ in range(5):
                t_ |= m_t_ & (t_ << <unsigned int>8)
                rt |= m_rt & (rt << <unsigned int>7)
                r_ |= m_r_ & (r_ >> <unsigned int>1)
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
            if (<unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)) & player:
                flippable_discs_num |= rt
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
        # (8)a3-b3, a4-b4, a5-b5, a6-b6
        elif move <= <unsigned long long>0x0000800000000000 and move >= <unsigned long long>0x0000000000400000:
            # 上、右上、右、右下、下
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            m_rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & opponent
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            m_rb = <unsigned long long>0x007F7F7F7F7F7F7F & opponent
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            t_ = m_t_ & (move << <unsigned int>8)  # top
            rt = m_rt & (move << <unsigned int>7)  # right-top
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            rb = m_rb & (move >> <unsigned int>9)  # right-bottom
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            for _ in range(5):
                r_ |= m_r_ & (r_ >> <unsigned int>1)
            for _ in range(3):
                t_ |= m_t_ & (t_ << <unsigned int>8)
                rt |= m_rt & (rt << <unsigned int>7)
                rb |= m_rb & (rb >> <unsigned int>9)
                b_ |= m_b_ & (b_ >> <unsigned int>8)
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
            if (<unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)) & player:
                flippable_discs_num |= rt
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
            if (<unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)) & player:
                flippable_discs_num |= rb
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
        else:
            other = 1;
    elif x <= <unsigned int>0x02:
        # (2)g1, h1, g2, h2
        if move >= <unsigned long long>0x0001000000000000:
            # 下、左下、左
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            m_lb = <unsigned long long>0x00FEFEFEFEFEFEFE & opponent
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            lb = m_lb & (move >> <unsigned int>7)  # left-bottom
            l_ = m_l_ & (move << <unsigned int>1)  # left
            for _ in range(5):
                b_ |= m_b_ & (b_ >> <unsigned int>8)
                lb |= m_lb & (lb >> <unsigned int>7)
                l_ |= m_l_ & (l_ << <unsigned int>1)
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
            if (<unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)) & player:
                flippable_discs_num |= lb
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
        # (3)g7, h7, g8, h8
        elif move <= <unsigned long long>0x0000000000008000:
            # 左、左上、上
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            m_lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & opponent
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            l_ = m_l_ & (move << <unsigned int>1)  # left
            lt = m_lt & (move << <unsigned int>9)  # left-top
            t_ = m_t_ & (move << <unsigned int>8)  # top
            for _ in range(5):
                l_ |= m_l_ & (l_ << <unsigned int>1)
                lt |= m_lt & (lt << <unsigned int>9)
                t_ |= m_t_ & (t_ << <unsigned int>8)
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
            if (<unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)) & player:
                flippable_discs_num |= lt
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
        # (6)g3-h3, g4-h4, g5-h5, g6-h6
        elif move <= <unsigned long long>0x00000200000000000 and move >= <unsigned long long>0x0000000000010000:
            # 下、左下、左、左上、上
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            m_lb = <unsigned long long>0x00FEFEFEFEFEFEFE & opponent
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            m_lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & opponent
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            lb = m_lb & (move >> <unsigned int>7)  # left-bottom
            l_ = m_l_ & (move << <unsigned int>1)  # left
            lt = m_lt & (move << <unsigned int>9)  # left-top
            t_ = m_t_ & (move << <unsigned int>8)  # top
            for _ in range(5):
                l_ |= m_l_ & (l_ << <unsigned int>1)
            for _ in range(3):
                b_ |= m_b_ & (b_ >> <unsigned int>8)
                lb |= m_lb & (lb >> <unsigned int>7)
                lt |= m_lt & (lt << <unsigned int>9)
                t_ |= m_t_ & (t_ << <unsigned int>8)
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
            if (<unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)) & player:
                flippable_discs_num |= lb
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
            if (<unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)) & player:
                flippable_discs_num |= lt
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
        else:
            other = 1;
    elif x <= <unsigned int>0x20 and x >= <unsigned int>0x04:
        # (5)c1-f1, c2-f2
        if move >= <unsigned long long>0x0004000000000000:
            # 右、右下、下、左下、左
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            m_rb = <unsigned long long>0x007F7F7F7F7F7F7F & opponent
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            m_lb = <unsigned long long>0x00FEFEFEFEFEFEFE & opponent
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            rb = m_rb & (move >> <unsigned int>9)  # right-bottom
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            lb = m_lb & (move >> <unsigned int>7)  # left-bottom
            l_ = m_l_ & (move << <unsigned int>1)  # left
            for _ in range(5):
                b_ |= m_b_ & (b_ >> <unsigned int>8)
            for _ in range(3):
                r_ |= m_r_ & (r_ >> <unsigned int>1)
                rb |= m_rb & (rb >> <unsigned int>9)
                lb |= m_lb & (lb >> <unsigned int>7)
                l_ |= m_l_ & (l_ << <unsigned int>1)
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
            if (<unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)) & player:
                flippable_discs_num |= rb
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
            if (<unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)) & player:
                flippable_discs_num |= lb
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
        # (7)c7-f7, c8-f8
        elif move <= <unsigned long long>0x0000000000002000:
            # 左、左上、上、右上、右
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            m_lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & opponent
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            m_rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & opponent
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            l_ = m_l_ & (move << <unsigned int>1)  # left
            lt = m_lt & (move << <unsigned int>9)  # left-top
            t_ = m_t_ & (move << <unsigned int>8)  # top
            rt = m_rt & (move << <unsigned int>7)  # right-top
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            for _ in range(5):
                t_ |= m_t_ & (t_ << <unsigned int>8)
            for _ in range(3):
                l_ |= m_l_ & (l_ << <unsigned int>1)
                lt |= m_lt & (lt << <unsigned int>9)
                rt |= m_rt & (rt << <unsigned int>7)
                r_ |= m_r_ & (r_ >> <unsigned int>1)
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
            if (<unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)) & player:
                flippable_discs_num |= lt
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
            if (<unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)) & player:
                flippable_discs_num |= rt
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
        else:
            other = 1;
    else:
        other = 1

    if other:
        m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
        m_rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & opponent
        m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
        m_rb = <unsigned long long>0x007F7F7F7F7F7F7F & opponent
        m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
        m_lb = <unsigned long long>0x00FEFEFEFEFEFEFE & opponent
        m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
        m_lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & opponent
        t_ = m_t_ & (move << <unsigned int>8)  # top
        rt = m_rt & (move << <unsigned int>7)  # right-top
        r_ = m_r_ & (move >> <unsigned int>1)  # right
        rb = m_rb & (move >> <unsigned int>9)  # right-bottom
        b_ = m_b_ & (move >> <unsigned int>8)  # bottom
        lb = m_lb & (move >> <unsigned int>7)  # left-bottom
        l_ = m_l_ & (move << <unsigned int>1)  # left
        lt = m_lt & (move << <unsigned int>9)  # left-top
        for _ in range(3):
            t_ |= m_t_ & (t_ << <unsigned int>8)
            rt |= m_rt & (rt << <unsigned int>7)
            r_ |= m_r_ & (r_ >> <unsigned int>1)
            rb |= m_rb & (rb >> <unsigned int>9)
            b_ |= m_b_ & (b_ >> <unsigned int>8)
            lb |= m_lb & (lb >> <unsigned int>7)
            l_ |= m_l_ & (l_ << <unsigned int>1)
            lt |= m_lt & (lt << <unsigned int>9)
        if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
            flippable_discs_num |= t_
        if (<unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)) & player:
            flippable_discs_num |= rt
        if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
            flippable_discs_num |= r_
        if (<unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)) & player:
            flippable_discs_num |= rb
        if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
            flippable_discs_num |= b_
        if (<unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)) & player:
            flippable_discs_num |= lb
        if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
            flippable_discs_num |= l_
        if (<unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)) & player:
            flippable_discs_num |= lt
    return flippable_discs_num


# -------------------------------------------------- #
# _put_disc
cdef inline unsigned long long _put_disc_size8_64bit(board, unsigned int color, unsigned int x, unsigned int y):
    """_put_disc_size8_64bit
    """
    cdef:
        unsigned long long put, black_bitboard, white_bitboard, flippable_discs_num, flippable_discs_count
        unsigned int black_score, white_score
        signed int shift_size

    # 配置位置を整数に変換
    shift_size = (63-(y*8+x))
    if shift_size < 0 or shift_size > 63:
        return <unsigned long long>0

    put = <unsigned long long>1 << shift_size

    # ひっくり返せる石を取得
    black_bitboard = board._black_bitboard
    white_bitboard = board._white_bitboard
    black_score = board._black_score
    white_score = board._white_score
    flippable_discs_num = _get_flippable_discs_num_size8_64bit(color, black_bitboard, white_bitboard, put)
    flippable_discs_count = _popcount_size8_64bit(flippable_discs_num)

    # 打つ前の状態を格納
    board.prev += [(black_bitboard, white_bitboard, black_score, white_score)]

    # 自分の石を置いて相手の石をひっくり返す
    if color:
        black_bitboard ^= put | flippable_discs_num
        white_bitboard ^= flippable_discs_num
        black_score += <unsigned int>1 + <unsigned int>flippable_discs_count
        white_score -= <unsigned int>flippable_discs_count
    else:
        white_bitboard ^= put | flippable_discs_num
        black_bitboard ^= flippable_discs_num
        black_score -= <unsigned int>flippable_discs_count
        white_score += <unsigned int>1 + <unsigned int>flippable_discs_count

    board._black_bitboard = black_bitboard
    board._white_bitboard = white_bitboard
    board._black_score = black_score
    board._white_score = white_score
    board._flippable_discs_num = flippable_discs_num

    return flippable_discs_num


cdef inline _put_disc(size, board, color, unsigned int x, unsigned int y):
    """_put_disc
    """
    # 配置位置を整数に変換
    shift_size = ((size*size-1)-(y*size+x))
    if shift_size < 0 or shift_size > size**2-1:
        return 0

    put = 1 << ((size*size-1)-(y*size+x))

    # 反転位置を整数に変換
    flippable_discs = board.get_flippable_discs(color, x, y)
    flippable_discs_num = 0
    cdef:
        unsigned int tmp_x, tmp_y
    for tmp_x, tmp_y in flippable_discs:
        flippable_discs_num |= 1 << ((size*size-1)-(tmp_y*size+tmp_x))

    # 打つ前の状態を格納
    board.prev += [(board._black_bitboard, board._white_bitboard, board._black_score, board._white_score)]

    # 自分の石を置いて相手の石をひっくり返す
    if color == 'black':
        board._black_bitboard ^= put | flippable_discs_num
        board._white_bitboard ^= flippable_discs_num
        board._black_score += 1 + len(flippable_discs)
        board._white_score -= len(flippable_discs)
    else:
        board._white_bitboard ^= put | flippable_discs_num
        board._black_bitboard ^= flippable_discs_num
        board._black_score -= len(flippable_discs)
        board._white_score += 1 + len(flippable_discs)

    board._flippable_discs_num = flippable_discs_num

    return flippable_discs_num


# -------------------------------------------------- #
# _get_board_info
cdef inline _get_board_info_size8_64bit(unsigned long long b, unsigned long long w):
    """_get_board_info_size8_64bit
    """
    cdef:
        unsigned int x, y
        unsigned long long mask = 0x8000000000000000
        signed int board_info[8][8]

    for y in range(8):
        for x in range(8):
            if b & mask:
                board_info[y][x] = 1
            elif w & mask:
                board_info[y][x] = -1
            else:
                board_info[y][x] = 0
            mask >>= 1

    return board_info


cdef _get_board_info_size8(b, w):
    """_get_board_info_size8
    """
    cdef:
        unsigned int x, y
        unsigned int b0 = ((0x10000000000000000 | b) >> 32) & 0xFFFFFFFF
        unsigned int b1 = b & 0xFFFFFFFF
        unsigned int w0 = ((0x10000000000000000 | w) >> 32) & 0xFFFFFFFF
        unsigned int w1 = w & 0x00000000FFFFFFFF
        unsigned int mask0 = 0x80000000
        unsigned int mask1 = 0x80000000

    board_info = []

    for y in range(8):
        tmp = []

        # ビットボード上位32bit
        if y < 4:
            for x in range(8):
                if b0 & mask0:
                    tmp += [1]
                elif w0 & mask0:
                    tmp += [-1]
                else:
                    tmp += [0]
                mask0 >>= 1
        # ビットボード下位32bit
        else:
            for x in range(8):
                if b1 & mask1:
                    tmp += [1]
                elif w1 & mask1:
                    tmp += [-1]
                else:
                    tmp += [0]
                mask1 >>= 1

        board_info += [tmp]

    return board_info


cdef _get_board_info(size, b, w):
    """_get_board_info
    """
    board_info = []
    mask = 1 << (size * size - 1)

    for y in range(size):
        tmp = []

        for x in range(size):
            if b & mask:
                tmp += [1]
            elif w & mask:
                tmp += [-1]
            else:
                tmp += [0]
            mask >>= 1

        board_info += [tmp]

    return board_info


# -------------------------------------------------- #
# _undo
cdef inline _undo(board):
    """_undo
    """
    (board._black_bitboard, board._white_bitboard, board._black_score, board._white_score) = board.prev.pop()
