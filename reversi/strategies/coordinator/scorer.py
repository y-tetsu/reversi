"""Scorer
"""

from reversi.strategies.common import AbstractScorer
from reversi.strategies.table import Table

from reversi.board import BitBoard


class TableScorer(AbstractScorer):
    """
    盤面の評価値をTableで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5):
        self.table = Table(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)  # Table戦略を利用する

    def get_score(self, *args, **kwargs):
        """
        評価値の算出
        """
        board = kwargs['board']
        if self.table.size != board.size:  # テーブルサイズの調整
            self.table.set_table(board.size)

        return self.table.get_score(board)  # +側黒優勢、-側白優勢に直す


class PossibilityScorer(AbstractScorer):
    """
    着手可能数に基づいて算出
    """
    def __init__(self, w=5):
        self._W = w

    def get_score(self, *args, **kwargs):
        """
        評価値の算出
        """
        legal_moves_b, legal_moves_w = kwargs['legal_moves_b'], kwargs['legal_moves_w']

        # 置ける場所の数に重みを掛ける
        black_num = len(legal_moves_b)
        white_num = len(legal_moves_w)

        return (black_num - white_num) * self._W


class OpeningScorer(AbstractScorer):
    """
    開放度に基づいて算出
    """
    def __init__(self, w=-0.75):
        self._W = w

    def get_score(self, *args, **kwargs):
        """
        評価値の算出
        """
        board = kwargs['board']
        size, board_info, opening = board.size, board.get_board_info(), 0

        directions = [
            (-1,  1), (0,  1), (1,  1),
            (-1,  0),          (1,  0),
            (-1, -1), (0, -1), (1, -1),
        ]

        # 最後にひっくり返された石の場所を取得する
        if isinstance(board, BitBoard):
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

    def get_score(self, *args, **kwargs):
        """
        評価値の算出
        """
        board, legal_moves_b, legal_moves_w = kwargs['board'], kwargs['legal_moves_b'], kwargs['legal_moves_w']
        ret = None

        # 対局終了時
        if not legal_moves_b and not legal_moves_w:
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
    def get_score(self, *args, **kwargs):
        """
        評価値の算出
        """
        board = kwargs['board']

        return board._black_score - board._white_score


class EdgeScorer(AbstractScorer):
    """
    辺のパターンに基づいて算出
    """
    def __init__(self, ws=100):
        self._WS = ws

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
        self.stable_maskvalue = [
            0xC000000000000000,  # 上左2
            0xE000000000000000,  # 上左3
            0xF000000000000000,  # 上左4
            0xF800000000000000,  # 上左5
            0xFC00000000000000,  # 上左6
            0xFE00000000000000,  # 上左7
            0x0300000000000000,  # 上右2
            0x0700000000000000,  # 上右3
            0x0F00000000000000,  # 上右4
            0x1F00000000000000,  # 上右5
            0x3F00000000000000,  # 上右6
            0x7F00000000000000,  # 上右7
            0xFF00000000000000,  # 上8
            0x0101000000000000,  # 右上2
            0x0101010000000000,  # 右上3
            0x0101010100000000,  # 右上4
            0x0101010101000000,  # 右上5
            0x0101010101010000,  # 右上6
            0x0101010101010100,  # 右上7
            0x0000000000000101,  # 右下2
            0x0000000000010101,  # 右下3
            0x0000000001010101,  # 右下4
            0x0000000101010101,  # 右下5
            0x0000010101010101,  # 右下6
            0x0001010101010101,  # 右下7
            0x0101010101010101,  # 右8
            0x00000000000000C0,  # 下左2
            0x00000000000000E0,  # 下左3
            0x00000000000000F0,  # 下左4
            0x00000000000000F8,  # 下左5
            0x00000000000000FC,  # 下左6
            0x00000000000000FE,  # 下左7
            0x0000000000000003,  # 下右2
            0x0000000000000007,  # 下右3
            0x000000000000000F,  # 下右4
            0x000000000000001F,  # 下右5
            0x000000000000003F,  # 下右6
            0x000000000000007F,  # 下右7
            0x00000000000000FF,  # 下8
            0x8080000000000000,  # 左上2
            0x8080800000000000,  # 左上3
            0x8080808000000000,  # 左上4
            0x8080808080000000,  # 左上5
            0x8080808080800000,  # 左上6
            0x8080808080808000,  # 左上7
            0x0000000000008080,  # 左下2
            0x0000000000808080,  # 左下3
            0x0000000080808080,  # 左下4
            0x0000008080808080,  # 左下5
            0x0000808080808080,  # 左下6
            0x0080808080808080,  # 左下7
            0x8080808080808080,  # 左8
        ]

    def get_score(self, *args, **kwargs):
        """
        評価値の算出
        """
        board = kwargs['board']
        score = 0
        b_bitboard, w_bitboard = board.get_bitboard_info()
        weight = self._WS

        # ボードサイズ8以外は考慮なし
        if board.size != 8:
            return score

        # 確定石
        for maskvalue in self.stable_maskvalue:
            score_b = weight if (b_bitboard & maskvalue) == maskvalue else 0
            score_w = weight if (w_bitboard & maskvalue) == maskvalue else 0
            score += score_b - score_w

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

    def get_score(self, *args, **kwargs):
        """
        評価値の算出
        """
        board = kwargs['board']
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
