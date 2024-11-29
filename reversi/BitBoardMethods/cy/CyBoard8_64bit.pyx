#cython: language_level=3, profile=False, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""CyBoard8_64bit
"""

from collections import namedtuple

MIN_BOARD_SIZE = 4
MAX_BOARD_SIZE = 26


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


cdef inline unsigned long long _popcount_size8_64bit(unsigned long long bits):
    """_popcount_size8_64bit
    """
    bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
    bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
    bits = bits + (bits >> <unsigned int>8)
    bits = bits + (bits >> <unsigned int>16)
    return (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F


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
