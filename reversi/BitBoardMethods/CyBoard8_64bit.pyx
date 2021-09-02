#cython: language_level=3
"""CyBoard8_64bit
"""

from collections import namedtuple

from reversi.disc import D as d
from reversi.board import MIN_BOARD_SIZE, MAX_BOARD_SIZE


class CythonBitBoard():
    """Cython BitBoard
    """
    def __init__(self):
        self.size = 8
        (self._black_score, self._white_score) = (2, 2)
        self.prev = []
        self._black_bitboard = 1 << 35
        self._black_bitboard |= 1 << 28
        self._white_bitboard = 1 << 36
        self._white_bitboard |= 1 << 27

        # 置ける場所の検出用マスク
        BitMask = namedtuple('BitMask', 'h v d u ur r br b bl l ul')
        size = self.size
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

    def _is_invalid_size(self, size):
        return not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0)

    def __str__(self):
        header = '   ' + ' '.join([chr(97 + i) for i in range(8)]) + '\n'
        board = [[d.blank for _ in range(8)] for _ in range(8)]
        mask = 1 << 63
        for y in range(8):
            for x in range(8):
                if self._black_bitboard & mask:
                    board[y][x] = d.black
                elif self._white_bitboard & mask:
                    board[y][x] = d.white
                mask >>= 1

        body = ''
        for num, row in enumerate(board, 1):
            body += f'{num:2d}' + ''.join([value for value in row]) + '\n'

        return header + body

    def get_legal_moves(self, str color):
        return _get_legal_moves_size8_64bit(color, self._black_bitboard, self._white_bitboard)

    def get_legal_moves_bits(self, str color):
        return _get_legal_moves_bits_size8_64bit(color, self._black_bitboard, self._white_bitboard)

    def get_flippable_discs(self, str color, x, y):
        return _get_flippable_discs_size8_64bit(color, self._black_bitboard, self._white_bitboard, x, y)

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

    def get_bit_count(self, bits):
        return _get_bit_count_size8_64bit(bits)

    def get_bitboard_info(self):
        return self._black_bitboard, self._white_bitboard

    def undo(self):
        (self._black_bitboard, self._white_bitboard, self._black_score, self._white_score) = self.prev.pop()


cdef inline _get_legal_moves_size8_64bit(str color, unsigned long long b, unsigned long long w):
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


cdef inline unsigned long long _get_legal_moves_bits_size8_64bit(str color, unsigned long long b, unsigned long long w):
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


cdef inline _get_flippable_discs_size8_64bit(str color, unsigned long long black_bitboard, unsigned long long white_bitboard, unsigned int x, unsigned int y):
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned int direction1, direction2
        unsigned long long buff, next_put
        unsigned long long move = 0
        unsigned long long player, opponent, flippable_discs = 0

    if color == 'black':
        player = black_bitboard
        opponent = white_bitboard
    else:
        player = white_bitboard
        opponent = black_bitboard

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
        next_put = <unsigned long long>0xFFFFFFFFFFFFFF00 & (put << <unsigned int>8)  # top
    elif direction == 1:
        next_put = <unsigned long long>0x7F7F7F7F7F7F7F00 & (put << <unsigned int>7)  # right-top
    elif direction == 2:
        next_put = <unsigned long long>0x7F7F7F7F7F7F7F7F & (put >> <unsigned int>1)  # right
    elif direction == 3:
        next_put = <unsigned long long>0x007F7F7F7F7F7F7F & (put >> <unsigned int>9)  # right-bottom
    elif direction == 4:
        next_put = <unsigned long long>0x00FFFFFFFFFFFFFF & (put >> <unsigned int>8)  # bottom
    elif direction == 5:
        next_put = <unsigned long long>0x00FEFEFEFEFEFEFE & (put >> <unsigned int>7)  # left-bottom
    elif direction == 6:
        next_put = <unsigned long long>0xFEFEFEFEFEFEFEFE & (put << <unsigned int>1)  # left
    elif direction == 7:
        next_put = <unsigned long long>0xFEFEFEFEFEFEFE00 & (put << <unsigned int>9)  # left-top
    else:
        next_put = <unsigned long long>0                                              # unexpected

    return next_put


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
    flippable_discs_num = _get_flippable_discs_num_size8_64bit(color, black_bitboard, white_bitboard, shift_size)
    flippable_discs_count = _get_bit_count_size8_64bit(flippable_discs_num)

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


cdef inline unsigned long long _get_flippable_discs_num_size8_64bit(unsigned int color, unsigned long long black_bitboard, unsigned long long white_bitboard, unsigned int shift_size):
    """_get_flippable_discs_num_size8_64bit
    """
    cdef:
        unsigned int direction1, direction2
        unsigned long long buff, next_put
        unsigned long long move = 0
        unsigned long long player, opponent, flippable_discs_num = 0

    if color:
        player = black_bitboard
        opponent = white_bitboard
    else:
        player = white_bitboard
        opponent = black_bitboard

    move = <unsigned long long>1 << shift_size

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
            flippable_discs_num |= buff

    return flippable_discs_num


cdef inline unsigned long long _get_bit_count_size8_64bit(unsigned long long bits):
    """_get_bit_count_size8_64bit
    """
    bits = (bits & <unsigned long long>0x5555555555555555) + (bits >> <unsigned int>1 & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + (bits >> <unsigned int>2 & <unsigned long long>0x3333333333333333)
    bits = (bits & <unsigned long long>0x0F0F0F0F0F0F0F0F) + (bits >> <unsigned int>4 & <unsigned long long>0x0F0F0F0F0F0F0F0F)
    bits = (bits & <unsigned long long>0x00FF00FF00FF00FF) + (bits >> <unsigned int>8 & <unsigned long long>0x00FF00FF00FF00FF)
    bits = (bits & <unsigned long long>0x0000FFFF0000FFFF) + (bits >> <unsigned int>16 & <unsigned long long>0x0000FFFF0000FFFF)

    return (bits & <unsigned long long>0x00000000FFFFFFFF) + (bits >> <unsigned int>32 & <unsigned long long>0x00000000FFFFFFFF)


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
