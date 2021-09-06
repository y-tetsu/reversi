"""Scorer
"""

from reversi.strategies.common import AbstractScorer
from reversi.strategies.table import Table
import reversi.strategies.coordinator.ScorerMethods as ScorerMethods

from reversi.board import BitBoard
from reversi.BitBoardMethods import CythonBitBoard


class TableScorer(AbstractScorer):
    """
    盤面の評価値をTableで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5):
        self.table = Table(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)  # Table戦略を利用する

    def get_score(self, color, board, possibility_b, possibility_w):
        """
        評価値の算出
        """
        if self.table.size != board.size:  # テーブルサイズの調整
            self.table.set_table(board.size)

        return self.table.get_score(board)  # +側黒優勢、-側白優勢に直す


class PossibilityScorer(AbstractScorer):
    """
    着手可能数に基づいて算出
    """
    def __init__(self, w=5):
        self._W = w

    def get_score(self, color, board, possibility_b, possibility_w):
        """
        評価値の算出
        """
        return (possibility_b - possibility_w) * self._W


class OpeningScorer(AbstractScorer):
    """
    開放度に基づいて算出
    """
    def __init__(self, w=-0.75):
        self._W = w

    def get_score(self, color, board, possibility_b, possibility_w):
        """
        評価値の算出
        """
        size, board_info, opening = board.size, board.get_board_info(), 0

        directions = [
            (-1,  1), (0,  1), (1,  1),
            (-1,  0),          (1,  0),
            (-1, -1), (0, -1), (1, -1),
        ]

        # 最後にひっくり返された石の場所を取得する
        if isinstance(board, BitBoard) or isinstance(board, CythonBitBoard):
            flippable_discs = board._flippable_discs_num
            discs = []
            mask = 1 << ((size * size) - 1)
            for y in range(size):
                for x in range(size):
                    if mask & flippable_discs:
                        discs.append([x, y])
                    mask >>= 1
        else:
            discs = board.prev[-1]['flippable_discs']

        # ひっくり返した石の周りをチェックする
        for disc_x, disc_y in discs:
            for dx, dy in directions:
                x, y = disc_x + dx, disc_y + dy

                if 0 <= x < size and 0 <= y < size:
                    if board_info[y][x] == 0:
                        opening += 1  # 石が置かれていない場所をカウント

        return opening * self._W


class WinLoseScorer(AbstractScorer):
    """
    勝敗に基づいて算出
    """
    def __init__(self, w=10000):
        self._W = w

    def get_score(self, color, board, possibility_b, possibility_w):
        """
        評価値の算出
        """
        # 対局終了時
        ret = None
        if not possibility_b and not possibility_w:
            ret = board._black_score - board._white_score

            if ret > 0:    # 黒が勝った
                ret += self._W
            elif ret < 0:  # 白が勝った
                ret -= self._W

        return ret


class NumberScorer(AbstractScorer):
    """
    石数に基づいて算出
    """
    def get_score(self, color, board, possibility_b, possibility_w):
        """
        評価値の算出
        """
        return board._black_score - board._white_score


class EdgeScorer(AbstractScorer):
    """
    辺のパターンに基づいて算出
    """
    def __init__(self, w=100):
        self._W = w

        # 確定石
        # ◎◎―――――― ◎◎◎――――― ◎◎◎◎―――― ◎◎◎◎◎――― ◎◎◎◎◎◎―― ◎◎◎◎◎◎◎―
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        #
        # ――――――◎◎ ―――――◎◎◎ ――――◎◎◎◎ ―――◎◎◎◎◎ ――◎◎◎◎◎◎ ―◎◎◎◎◎◎◎
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        #
        # ◎◎◎◎◎◎◎◎
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        self._get_table()

    def _get_table(self):
        self.edge_table8 = [0x00 for _ in range(0x100)]
        left = 0x80
        right = 0x01
        for row in range(0x100):
            score = 0
            l_r = row & left
            r_l = row & right
            if l_r or r_l:
                for _ in range(6):
                    # 左:右方向
                    l_r >>= 1
                    l_r &= row
                    if l_r:
                        score += self._W
                    # 右:左方向
                    r_l <<= 1
                    r_l &= row
                    if r_l:
                        score += self._W
                if row == 0xFF:
                    score += self._W
            self.edge_table8[row] = score

    def get_score(self, color, board, possibility_b, possibility_w):
        """
        評価値の算出
        """
        size = board.size
        weight = self._W
        score = 0
        b_bitboard, w_bitboard = board.get_bitboard_info()
        all_bitboard = b_bitboard | w_bitboard
        bit_pos = 1 << (size * size - 1)

        lt = bit_pos
        rt = bit_pos >> size-1
        lb = bit_pos >> size*(size-1)
        rb = bit_pos >> size*size-1

        # 四隅のどこかに石がある場合
        if (lt | rt | lb | rb) & all_bitboard:
            if size == 8:
                # 上辺
                b_t = (0xFF00000000000000 & b_bitboard) >> 56
                w_t = (0xFF00000000000000 & w_bitboard) >> 56
                # 下辺
                b_b = 0x00000000000000FF & b_bitboard
                w_b = 0x00000000000000FF & w_bitboard
                # 左辺
                b_l = 0
                if b_bitboard & 0x8000000000000000:
                    b_l += 0x0000000000000080
                if b_bitboard & 0x0080000000000000:
                    b_l += 0x0000000000000040
                if b_bitboard & 0x0000800000000000:
                    b_l += 0x0000000000000020
                if b_bitboard & 0x0000008000000000:
                    b_l += 0x0000000000000010
                if b_bitboard & 0x0000000080000000:
                    b_l += 0x0000000000000008
                if b_bitboard & 0x0000000000800000:
                    b_l += 0x0000000000000004
                if b_bitboard & 0x0000000000008000:
                    b_l += 0x0000000000000002
                if b_bitboard & 0x0000000000000080:
                    b_l += 0x0000000000000001
                w_l = 0
                if w_bitboard & 0x8000000000000000:
                    w_l += 0x0000000000000080
                if w_bitboard & 0x0080000000000000:
                    w_l += 0x0000000000000040
                if w_bitboard & 0x0000800000000000:
                    w_l += 0x0000000000000020
                if w_bitboard & 0x0000008000000000:
                    w_l += 0x0000000000000010
                if w_bitboard & 0x0000000080000000:
                    w_l += 0x0000000000000008
                if w_bitboard & 0x0000000000800000:
                    w_l += 0x0000000000000004
                if w_bitboard & 0x0000000000008000:
                    w_l += 0x0000000000000002
                if w_bitboard & 0x0000000000000080:
                    w_l += 0x0000000000000001
                # 右辺
                b_r = 0
                if b_bitboard & 0x0100000000000000:
                    b_r += 0x0000000000000080
                if b_bitboard & 0x0001000000000000:
                    b_r += 0x0000000000000040
                if b_bitboard & 0x0000010000000000:
                    b_r += 0x0000000000000020
                if b_bitboard & 0x0000000100000000:
                    b_r += 0x0000000000000010
                if b_bitboard & 0x0000000001000000:
                    b_r += 0x0000000000000008
                if b_bitboard & 0x0000000000010000:
                    b_r += 0x0000000000000004
                if b_bitboard & 0x0000000000000100:
                    b_r += 0x0000000000000002
                if b_bitboard & 0x0000000000000001:
                    b_r += 0x0000000000000001
                w_r = 0
                if w_bitboard & 0x0100000000000000:
                    w_r += 0x0000000000000080
                if w_bitboard & 0x0001000000000000:
                    w_r += 0x0000000000000040
                if w_bitboard & 0x0000010000000000:
                    w_r += 0x0000000000000020
                if w_bitboard & 0x0000000100000000:
                    w_r += 0x0000000000000010
                if w_bitboard & 0x0000000001000000:
                    w_r += 0x0000000000000008
                if w_bitboard & 0x0000000000010000:
                    w_r += 0x0000000000000004
                if w_bitboard & 0x0000000000000100:
                    w_r += 0x0000000000000002
                if w_bitboard & 0x0000000000000001:
                    w_r += 0x0000000000000001
                return (self.edge_table8[b_t] - self.edge_table8[w_t]) + (self.edge_table8[b_b] - self.edge_table8[w_b]) + (self.edge_table8[b_l] - self.edge_table8[w_l]) + (self.edge_table8[b_r] - self.edge_table8[w_r])  # noqa: E501

            # 左上
            lt_board = b_bitboard
            lt_sign = 1
            if lt & w_bitboard:
                lt_board = w_bitboard
                lt_sign = -1
            lt_r, lt_b = lt & lt_board, lt & lt_board
            # 右上
            rt_board = b_bitboard
            rt_sign = 1
            if rt & w_bitboard:
                rt_board = w_bitboard
                rt_sign = -1
            rt_l, rt_b = rt & rt_board, rt & rt_board
            # 左下
            lb_board = b_bitboard
            lb_sign = 1
            if lb & w_bitboard:
                lb_board = w_bitboard
                lb_sign = -1
            lb_r, lb_t = lb & lb_board, lb & lb_board
            # 右下
            rb_board = b_bitboard
            rb_sign = 1
            if rb & w_bitboard:
                rb_board = w_bitboard
                rb_sign = -1
            rb_l, rb_t = rb & rb_board, rb & rb_board

            # 確定石の連続数(2個～7個まで)をカウント
            for i in range(size-2):
                # 左上:右方向
                lt_r >>= 1
                lt_r &= lt_board
                if lt_r & lt_board:
                    score += weight * lt_sign
                # 左上:下方向
                lt_b >>= size
                lt_b &= lt_board
                if lt_b & lt_board:
                    score += weight * lt_sign
                # 右上:左方向
                rt_l <<= 1
                rt_l &= rt_board
                if rt_l & rt_board:
                    score += weight * rt_sign
                # 右上:下方向
                rt_b >>= size
                rt_b &= rt_board
                if rt_b & rt_board:
                    score += weight * rt_sign
                # 左下:右方向
                lb_r >>= 1
                lb_r &= lb_board
                if lb_r & lb_board:
                    score += weight * lb_sign
                # 左下:上方向
                lb_t <<= size
                lb_t &= lb_board
                if lb_t & lb_board:
                    score += weight * lb_sign
                # 右下:左方向
                rb_l <<= 1
                rb_l &= rb_board
                if rb_l & rb_board:
                    score += weight * rb_sign
                # 右下:上方向
                rb_t <<= size
                rb_t &= rb_board
                if rb_t & rb_board:
                    score += weight * rb_sign

            # 辺が同じ色で埋まっている場合はさらに加算
            top = int(''.join(['1'] * size + ['0'] * (size*(size-1))), 2)
            if lt_board & top == top:
                score += weight * lt_sign

            left = int(''.join((['1'] + ['0'] * (size-1)) * size), 2)
            if lt_board & left == left:
                score += weight * lt_sign

            right = int(''.join((['0'] * (size-1) + ['1']) * size), 2)
            if rb_board & right == right:
                score += weight * rb_sign

            bottom = int(''.join(['0'] * (size*(size-1)) + ['1'] * size), 2)
            if rb_board & bottom == bottom:
                score += weight * rb_sign

        return score


class CornerScorer(AbstractScorer):
    """
    隅のパターンに基づいて算出
    """
    def __init__(self, w=100):
        self._W = w

        # 確定石
        # Level1
        # 1                1                1
        # □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□
        # ■■■■□□□□ ■■■■□□□□ ■■■■□□□□
        # ●■■■□□□□ ●■■■□□□□ ■■■■□□□□
        # ●◎■■□□□□ ●◎■■□□□□ ●◎■■□□□□
        # ●●●■□□□□ ●●■■□□□□ ●●●■□□□□
        self.level1_maskvalue = [
            # 左下
            [
                0x000000000080C0E0,
                0x000000000080C0C0,
                0x000000000000C0E0,
            ],
            # 左上
            [
                0xE0C0800000000000,
                0xE0C0000000000000,
                0xC0C0800000000000,
            ],
            # 右上
            [
                0x0703010000000000,
                0x0303010000000000,
                0x0703000000000000,
            ],
            # 右下
            [
                0x0000000000010307,
                0x0000000000000307,
                0x0000000000010303,
            ],
        ]
        self.level1_weight = [
            1, 1, 1
        ]

        # Level2
        # 3                3                3                2                2
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # ●■■■□□□□ ●■■■□□□□ ■■■■□□□□ ●■■■□□□□ ■■■■□□□□
        # ●◎■■□□□□ ●◎■■□□□□ ●◎■■□□□□ ●◎■■□□□□ ■■■■□□□□
        # ●◎◎■□□□□ ●◎◎■□□□□ ●◎◎■□□□□ ●◎■■□□□□ ●◎◎■□□□□
        # ●●●●□□□□ ●●●■□□□□ ●●●●□□□□ ●●■■□□□□ ●●●●□□□□
        self.level2_maskvalue = [
            # 左下
            [
                0x0000000080C0E0F0,
                0x0000000080C0E0E0,
                0x0000000000C0E0F0,
                0x0000000080C0C0C0,
                0x000000000000E0F0,
            ],
            # 左上
            [
                0xF0E0C08000000000,
                0xF0E0C00000000000,
                0xE0E0C08000000000,
                0xF0E0000000000000,
                0xC0C0C08000000000,
            ],
            # 右上
            [
                0x0F07030100000000,
                0x0707030100000000,
                0x0F07030000000000,
                0x0303030100000000,
                0x0F07000000000000,
            ],
            # 右下
            [
                0x000000000103070F,
                0x000000000003070F,
                0x0000000001030707,
                0x000000000000070F,
                0x0000000001030303,
            ],
        ]
        self.level2_weight = [
            3, 3, 3, 2, 2
        ]

        # Level3
        # 6                6                6                5                5
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # ●□□□□□□□ ●□□□□□□□ □□□□□□□□ ●□□□□□□□ □□□□□□□□
        # ●◎■■□□□□ ●◎■■□□□□ ●◎■■□□□□ ●◎■■□□□□ ■■■■□□□□
        # ●◎◎■□□□□ ●◎◎■□□□□ ●◎◎■□□□□ ●◎◎■□□□□ ●◎◎■□□□□
        # ●◎◎◎□□□□ ●◎◎◎□□□□ ●◎◎◎□□□□ ●◎◎■□□□□ ●◎◎◎□□□□
        # ●●●●●□□□ ●●●●□□□□ ●●●●●□□□ ●●●■□□□□ ●●●●●□□□
        # 4                4                3                3
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # ●□□□□□□□ □□□□□□□□ ●□□□□□□□ □□□□□□□□
        # ●◎■■□□□□ ■■■■□□□□ ●◎■■□□□□ ■■■■□□□□
        # ●◎■■□□□□ ●◎■■□□□□ ●◎■■□□□□ ■■■■□□□□
        # ●◎◎■□□□□ ●◎◎◎□□□□ ●◎■■□□□□ ●◎◎◎□□□□
        # ●●●■□□□□ ●●●●●□□□ ●●■■□□□□ ●●●●●□□□
        self.level3_maskvalue = [
            # 左下
            [
                0x00000080C0E0F0F8,
                0x00000080C0E0F0F0,
                0x00000000C0E0F0F8,
                0x00000080C0E0E0E0,
                0x0000000000E0F0F8,
                0x00000080C0C0E0E0,
                0x0000000000C0F0F8,
                0x00000080C0C0C0C0,
                0x000000000000F0F8,
            ],
            # 左上
            [
                0xF8F0E0C080000000,
                0xF8F0E0C000000000,
                0xF0F0E0C080000000,
                0xF8F0E00000000000,
                0xE0E0E0C080000000,
                0xF8F0C00000000000,
                0xE0E0C0C080000000,
                0xF8F0000000000000,
                0xC0C0C0C080000000,
            ],
            # 右上
            [
                0x1F0F070301000000,
                0x0F0F070301000000,
                0x1F0F070300000000,
                0x0707070301000000,
                0x1F0F070000000000,
                0x0707030301000000,
                0x1F0F030000000000,
                0x0303030301000000,
                0x1F0F000000000000,
            ],
            # 右下
            [
                0x0000000103070F1F,
                0x0000000003070F1F,
                0x0000000103070F0F,
                0x0000000000070F1F,
                0x0000000103070707,
                0x0000000000030F1F,
                0x0000000103030707,
                0x0000000000000F1F,
                0x0000000103030303,
            ],
        ]
        self.level3_weight = [
            6, 6, 6, 5, 5, 4, 4, 3, 3
        ]

        # Level4
        # 8                8                8                7                7
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # ●□□□□□□□ ●□□□□□□□ □□□□□□□□ ●□□□□□□□ □□□□□□□□
        # ●●□□□□□□ ●●□□□□□□ □□□□□□□□ ●●□□□□□□ □□□□□□□□
        # ●◎◎■□□□□ ●◎◎■□□□□ ●◎◎■□□□□ ●◎◎■□□□□ ●◎■■□□□□
        # ●◎◎◎□□□□ ●◎◎◎□□□□ ●◎◎◎□□□□ ●◎◎■□□□□ ●◎◎◎□□□□
        # ●◎◎◎●□□□ ●◎◎◎□□□□ ●◎◎◎●□□□ ●◎◎◎□□□□ ●◎◎◎●□□□
        # ●●●●●●□□ ●●●●□□□□ ●●●●●●□□ ●●●●□□□□ ●●●●●●□□
        # 6                6                6                6                5
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # ●□□□□□□□ □□□□□□□□ ●□□□□□□□ □□□□□□□□ ●□□□□□□□
        # ●●□□□□□□ □□□□□□□□ ●●□□□□□□ □□□□□□□□ ●●□□□□□□
        # ●◎■■□□□□ ●◎■■□□□□ ●◎◎■□□□□ ■■■■□□□□ ●◎■■□□□□
        # ●◎◎■□□□□ ●◎◎■□□□□ ●◎◎■□□□□ ●◎◎◎□□□□ ●◎◎■□□□□
        # ●◎◎◎□□□□ ●◎◎◎●□□□ ●◎◎■□□□□ ●◎◎◎●□□□ ●◎◎■□□□□
        # ●●●●□□□□ ●●●●●●□□ ●●●■□□□□ ●●●●●●□□ ●●●■□□□□
        # 5                4                4                3                3
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
        # □□□□□□□□ ●□□□□□□□ □□□□□□□□ ●□□□□□□□ □□□□□□□□
        # □□□□□□□□ ●●□□□□□□ □□□□□□□□ ●●□□□□□□ □□□□□□□□
        # ■■■■□□□□ ●◎■■□□□□ ■■■■□□□□ ●◎■■□□□□ ■■■■□□□□
        # ●◎◎■□□□□ ●◎■■□□□□ ●◎■■□□□□ ●◎■■□□□□ ■■■■□□□□
        # ●◎◎◎●□□□ ●◎◎■□□□□ ●◎◎◎●□□□ ●◎■■□□□□ ●◎◎◎●□□□
        # ●●●●●●□□ ●●●■□□□□ ●●●●●●□□ ●●■■□□□□ ●●●●●●□□
        self.level4_maskvalue = [
            # 左下
            [
                0x000080C0E0F0F8FC,
                0x000080C0E0F0F0F0,
                0x00000000E0F0F8FC,
                0x000080C0E0E0F0F0,
                0x00000000C0F0F8FC,
                0x000080C0C0E0F0F0,
                0x00000000C0E0F8FC,
                0x000080C0E0E0E0E0,
                0x0000000000F0F8FC,
                0x000080C0C0E0E0E0,
                0x0000000000E0F8FC,
                0x000080C0C0C0E0E0,
                0x0000000000C0F8FC,
                0x000080C0C0C0C0C0,
                0x000000000000F8FC,
            ],
            # 左上
            [
                0xFCF8F0E0C0800000,
                0xFCF8F0E000000000,
                0xF0F0F0E0C0800000,
                0xFCF8F0C000000000,
                0xF0F0E0E0C0800000,
                0xFCF8E0C000000000,
                0xF0F0E0C0C0800000,
                0xFCF8F00000000000,
                0xE0E0E0E0C0800000,
                0xFCF8E00000000000,
                0xE0E0E0C0C0800000,
                0xFCF8C00000000000,
                0xE0E0C0C0C0800000,
                0xFCF8000000000000,
                0xC0C0C0C0C0800000,
            ],
            # 右上
            [
                0x3F1F0F0703010000,
                0x0F0F0F0703010000,
                0x3F1F0F0700000000,
                0x0F0F070703010000,
                0x3F1F0F0300000000,
                0x0F0F070303010000,
                0x3F1F070300000000,
                0x0707070703010000,
                0x3F1F0F0000000000,
                0x0707070303010000,
                0x3F1F070000000000,
                0x0707030303010000,
                0x3F1F030000000000,
                0x0303030303010000,
                0x3F1F000000000000,
            ],
            # 右下
            [
                0x00000103070F1F3F,
                0x00000000070F1F3F,
                0x00000103070F0F0F,
                0x00000000030F1F3F,
                0x0000010307070F0F,
                0x0000000003071F3F,
                0x0000010303070F0F,
                0x00000000000F1F3F,
                0x0000010307070707,
                0x0000000000071F3F,
                0x0000010303070707,
                0x0000000000031F3F,
                0x0000010303030707,
                0x0000000000001F3F,
                0x0000010303030303,
            ],
        ]
        self.level4_weight = [
            8, 8, 8, 7, 7, 6, 6, 6, 6, 5, 5, 4, 4, 3, 3
        ]

        # Level5
        # 9                9                9
        # □□□□□□□□ □□□□□□□□ □□□□□□□□
        # ●□□□□□□□ ●□□□□□□□ □□□□□□□□
        # ●●□□□□□□ ●●□□□□□□ □□□□□□□□
        # ●●●□□□□□ ●●●□□□□□ □□□□□□□□
        # ●◎◎◎□□□□ ●◎◎◎□□□□ ●◎◎◎□□□□
        # ●◎◎◎●□□□ ●◎◎◎□□□□ ●◎◎◎●□□□
        # ●◎◎◎●●□□ ●◎◎◎□□□□ ●◎◎◎●●□□
        # ●●●●●●●□ ●●●●□□□□ ●●●●●●●□
        self.level5_maskvalue = [
            # 左下
            [
                0x0080C0E0F0F8FCFE,
                0x0080C0E0F0F0F0F0,
                0x00000000F0F8FCFE,
            ],
            # 左上
            [
                0xFEFCF8F0E0C08000,
                0xFEFCF8F000000000,
                0xF0F0F0F0E0C08000,
            ],
            # 右上
            [
                0x7F3F1F0F07030100,
                0x0F0F0F0F07030100,
                0x7F3F1F0F00000000,
            ],
            # 右下
            [
                0x000103070F1F3F7F,
                0x000000000F1F3F7F,
                0x000103070F0F0F0F,
            ],
        ]
        self.level5_weight = [
            9, 9, 9
        ]

    def get_score(self, color, board, possibility_b, possibility_w):
        """
        評価値の算出
        """
        score = 0
        b_bitboard, w_bitboard = board.get_bitboard_info()

        # ボードサイズ8以外は考慮なし
        if board.size != 8:
            return score

        # 左下→左上→右上→右下
        for index in range(4):
            corner_score = 0

            # Level1
            maskvalues = self.level1_maskvalue[index]
            for w_index, maskvalue in enumerate(maskvalues):
                corner_score = self._get_mask_value(b_bitboard, w_bitboard, maskvalue, self.level1_weight[w_index])
                if corner_score:
                    break

            if corner_score:
                # Level5
                maskvalues = self.level5_maskvalue[index]
                for w_index, maskvalue in enumerate(maskvalues):
                    tmp_score = self._get_mask_value(b_bitboard, w_bitboard, maskvalue, self.level5_weight[w_index])
                    if tmp_score:
                        corner_score = tmp_score
                        break

                if not tmp_score:
                    # Level4
                    maskvalues = self.level4_maskvalue[index]
                    for w_index, maskvalue in enumerate(maskvalues):
                        tmp_score = self._get_mask_value(b_bitboard, w_bitboard, maskvalue, self.level4_weight[w_index])
                        if tmp_score:
                            corner_score = tmp_score
                            break

                    if not tmp_score:
                        # Level3
                        maskvalues = self.level3_maskvalue[index]
                        for w_index, maskvalue in enumerate(maskvalues):
                            tmp_score = self._get_mask_value(b_bitboard, w_bitboard, maskvalue, self.level3_weight[w_index])
                            if tmp_score:
                                corner_score = tmp_score
                                break

                        if not tmp_score:
                            # Level2
                            maskvalues = self.level2_maskvalue[index]
                            for w_index, maskvalue in enumerate(maskvalues):
                                tmp_score = self._get_mask_value(b_bitboard, w_bitboard, maskvalue, self.level2_weight[w_index])
                                if tmp_score:
                                    corner_score = tmp_score
                                    break

            score += corner_score

        return score

    def _get_mask_value(self, b_bitboard, w_bitboard, maskvalue, weight):
        """
        マスクした値を取得
        """
        score_b = weight * self._W if (b_bitboard & maskvalue) == maskvalue else 0
        score_w = weight * self._W if (w_bitboard & maskvalue) == maskvalue else 0

        return score_b - score_w


class BlankScorer(AbstractScorer):
    """
    空マスのパターンに基づいて算出
    """
    def __init__(self, w1=-1, w2=-4, w3=-2):
        self._W1 = w1
        self._W2 = w2
        self._W3 = w3

    def get_score(self, color, board, possibility_b, possibility_w):
        """
        評価値の算出
        """
        return ScorerMethods.get_blank_score(board, self._W1, self._W2, self._W3)


class EdgeCornerScorer(AbstractScorer):
    """
    辺と隅のパターンに基づいて算出
    """
    def __init__(self, w1=1, w2=8):
        self._W1 = w1
        self._W2 = w2

    def get_score(self, color, board, possibility_b, possibility_w):
        """
        評価値の算出
        """
        size = board.size
        black_bitboard = board._black_bitboard
        white_bitboard = board._white_bitboard
        all_bitboard = black_bitboard | white_bitboard
        bit_pos = 1 << (size * size - 1)
        corners = [0, size-1, size*size-8, size*size-1]
        score = 0
        for index1, corner1 in enumerate(corners):
            for index2, corner2 in enumerate(corners):
                if index1+index2 == 3 or index1 >= index2:  # 斜め方向は除外し、4辺を1回ずつチェック
                    continue
                d = (corner2 - corner1) // 7
                is_edge_full = True
                edge = 0
                blank_check = bit_pos >> corner1
                # 辺の確定石
                for k in range(size):  # 辺の方向をチェック
                    if not (blank_check & all_bitboard):  # 空きマス発見時
                        is_edge_full = False
                        break
                    if blank_check & black_bitboard:
                        edge += self._W1  # 黒の場合
                    else:
                        edge -= self._W1  # 白の場合
                    blank_check >>= d
                # 四隅のパターン
                corner = 0
                corner_check1 = bit_pos >> corner1
                corner_check2 = bit_pos >> corner2
                if corner_check1 & black_bitboard:
                    corner += 1
                if corner_check2 & black_bitboard:
                    corner += 1
                if corner_check1 & white_bitboard:
                    corner -= 1
                if corner_check2 & white_bitboard:
                    corner -= 1
                # 算出
                if is_edge_full:
                    score += edge      # 辺がすべて埋まっている場合
                elif corner > 0:
                    score += self._W2  # 黒の隅が多い場合
                elif corner < 0:
                    score -= self._W2  # 白の隅が多い場合
        return score
