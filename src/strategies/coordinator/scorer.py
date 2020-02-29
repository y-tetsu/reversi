#!/usr/bin/env python
"""
評価値算出
"""

import sys
sys.path.append('../../')

from strategies.common import AbstractScorer
from strategies.table import Table

from board import Board, BitBoard


class TableScorer(AbstractScorer):
    """
    盤面の評価値をTableで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5):
        self.table = Table(size, corner, c, a1, a2, b, x, o)  # Table戦略を利用する

    def get_score(self, color, board):
        """
        評価値の算出
        """
        if self.table.size != board.size:  # テーブルサイズの調整
            self.table.set_table(board.size)

        sign = 1 if color == 'black' else -1

        return self.table.get_score(color, board) * sign  # +側黒優勢、-側白優勢に直す


class PossibilityScorer(AbstractScorer):
    """
    着手可能数に基づいて算出
    """
    def __init__(self, w=5):
        self._W = w

    def get_score(self, possibles_b, possibles_w):
        """
        評価値の算出
        """
        # 置ける場所の数に重みを掛ける
        black_num = len(list(possibles_b.keys()))
        white_num = len(list(possibles_w.keys()))

        return (black_num - white_num) * self._W


class OpeningScorer(AbstractScorer):
    """
    開放度に基づいて算出
    """
    def __init__(self, w=-0.75):
        self._W = w

    def get_score(self, board):
        """
        評価値の算出
        """
        size, board_info, opening = board.size, board.get_board_info(), 0

        directions = [
            [-1,  1], [ 0,  1], [ 1,  1],
            [-1,  0],           [ 1,  0],
            [-1, -1], [ 0, -1], [ 1, -1],
        ]

        # 最後にひっくり返された石の場所を取得する
        if isinstance(board, BitBoard):
            reversibles = board.prev[-1]['reversibles']

            stones = []
            mask = 1 << ((size * size) - 1)

            for y in range(size):
                for x in range(size):
                    if mask & reversibles:
                        stones.append([x, y])
                    mask >>= 1
        else:
            stones = board.prev[-1]['reversibles']

        # ひっくり返した石の周りをチェックする
        for stone_x, stone_y in stones:
            for dx, dy in directions:
                x, y = stone_x + dx, stone_y + dy

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

    def get_score(self, board, possibles_b, possibles_w):
        """
        評価値の算出
        """
        ret = None

        # 対局終了時
        if not possibles_b and not possibles_w:
            ret = board.score['black'] - board.score['white']

            if ret > 0:    # 黒が勝った
                ret += self._W
            elif ret < 0:  # 白が勝った
                ret -= self._W

        return ret


class NumberScorer(AbstractScorer):
    """
    石数に基づいて算出
    """
    def get_score(self, board):
        """
        評価値の算出
        """
        return board.score['black'] - board.score['white']


class EdgeScorer(AbstractScorer):
    """
    辺のパターンに基づいて算出
    """
    def __init__(self, w1=47, w2=28, w3=0, w4=-3, w5=0, w6=100, w7=100, w8=100, w9=100, w10=100, w11=100, w12=100):
        self._W1 = w1
        self._W2 = w2
        self._W3 = w3
        self._W4 = w4
        self._W5 = w5
        self._W6 = w6
        self._W7 = w7
        self._W8 = w8
        self._W9 = w9
        self._W10 = w10
        self._W11 = w11
        self._W12 = w12

        # ピュア山
        # ◇◎◎◎◎◎◎◇
        # □◇◎◎◎◎◇□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        self.pureyama_mask = [
            0xFF7E000000000000,
            0x0103030303030301,
            0x0000000000007EFF,
            0x80C0C0C0C0C0C080
        ]
        self.pureyama_value = [
            0x7E3C000000000000,
            0x0001030303030100,
            0x0000000000003C7E,
            0x0080C0C0C0C08000
        ]

        # 山
        # ◇◎◎◎◎◎◎◇
        # □◇――――◇□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        self.yama_mask = [
            0xFF42000000000000,
            0x0103010101010301,
            0x00000000000042FF,
            0x80C080808080C080
        ]
        self.yama_value = [
            0x7E00000000000000,
            0x0001010101010100,
            0x000000000000007E,
            0x0080808080808000
        ]

        # ピュアウィング
        # ◇◎◎◎◎◎◇◇
        # □◇◎◎◎◎◇□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        self.purewing_mask = [
            0xFF7E000000000000,
            0xFF7E000000000000,
            0x0103030303030301,
            0x0103030303030301,
            0x0000000000007EFF,
            0x0000000000007EFF,
            0x80C0C0C0C0C0C080,
            0x80C0C0C0C0C0C080
        ]
        self.purewing_value = [
            0x7C3C000000000000,
            0x3E3C000000000000,
            0x0001030303030000,
            0x0000030303030100,
            0x0000000000003C7C,
            0x0000000000003C3E,
            0x0080C0C0C0C00000,
            0x0000C0C0C0C08000
        ]

        # ウィング
        # ◇◎◎◎◎◎◇◇
        # □◇◎――◎◇□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        self.wing_mask = [
            0xFF66000000000000,
            0xFF66000000000000,
            0x0103030101030301,
            0x0103030101030301,
            0x00000000000066FF,
            0x00000000000066FF,
            0x80C0C08080C0C080,
            0x80C0C08080C0C080
        ]
        self.wing_value = [
            0x7C24000000000000,
            0x3E24000000000000,
            0x0001030101030000,
            0x0000030101030100,
            0x000000000000247C,
            0x000000000000243E,
            0x0080C08080C00000,
            0x0000C08080C08000
        ]

        # ブロック
        # □□◎◎◎◎□□
        # □□×――×□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        # □□□□□□□□
        self.block_mask = [
            0xFF66000000000000,
            0x0103030101030301,
            0x00000000000066FF,
            0x80C0C0C0C0C0C080
        ]
        self.block_value = [
            0x3C00000000000000,
            0x0000010101010000,
            0x000000000000003C,
            0x0000808080800000
        ]

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
        self.stable_mask = [
            0xC000000000000000,
            0xE000000000000000,
            0xF000000000000000,
            0xF800000000000000,
            0xFC00000000000000,
            0xFE00000000000000,
            0x0300000000000000,
            0x0700000000000000,
            0x0F00000000000000,
            0x1F00000000000000,
            0x3F00000000000000,
            0x7F00000000000000,
            0xFF00000000000000,
            0x0101000000000000,
            0x0101010000000000,
            0x0101010100000000,
            0x0101010101000000,
            0x0101010101010000,
            0x0101010101010100,
            0x0000000000000101,
            0x0000000000010101,
            0x0000000001010101,
            0x0000000101010101,
            0x0000010101010101,
            0x0001010101010101,
            0x0101010101010101,
            0x00000000000000C0,
            0x00000000000000E0,
            0x00000000000000F0,
            0x00000000000000F8,
            0x00000000000000FC,
            0x00000000000000FE,
            0x0000000000000003,
            0x0000000000000007,
            0x000000000000000F,
            0x000000000000001F,
            0x000000000000003F,
            0x000000000000007F,
            0x00000000000000FF,
            0x8080000000000000,
            0x8080800000000000,
            0x8080808000000000,
            0x8080808080000000,
            0x8080808080800000,
            0x8080808080808000,
            0x0000000000008080,
            0x0000000000808080,
            0x0000000080808080,
            0x0000008080808080,
            0x0000808080808080,
            0x0080808080808080,
            0x8080808080808080,
        ]
        self.stable_value = [
            0xC000000000000000,
            0xE000000000000000,
            0xF000000000000000,
            0xF800000000000000,
            0xFC00000000000000,
            0xFE00000000000000,
            0x0300000000000000,
            0x0700000000000000,
            0x0F00000000000000,
            0x1F00000000000000,
            0x3F00000000000000,
            0x7F00000000000000,
            0xFF00000000000000,
            0x0101000000000000,
            0x0101010000000000,
            0x0101010100000000,
            0x0101010101000000,
            0x0101010101010000,
            0x0101010101010100,
            0x0000000000000101,
            0x0000000000010101,
            0x0000000001010101,
            0x0000000101010101,
            0x0000010101010101,
            0x0001010101010101,
            0x0101010101010101,
            0x00000000000000C0,
            0x00000000000000E0,
            0x00000000000000F0,
            0x00000000000000F8,
            0x00000000000000FC,
            0x00000000000000FE,
            0x0000000000000003,
            0x0000000000000007,
            0x000000000000000F,
            0x000000000000001F,
            0x000000000000003F,
            0x000000000000007F,
            0x00000000000000FF,
            0x8080000000000000,
            0x8080800000000000,
            0x8080808000000000,
            0x8080808080000000,
            0x8080808080800000,
            0x8080808080808000,
            0x0000000000008080,
            0x0000000000808080,
            0x0000000080808080,
            0x0000008080808080,
            0x0000808080808080,
            0x0080808080808080,
            0x8080808080808080,
        ]
        self.stable_weight = [
            self._W6,
            self._W7,
            self._W8,
            self._W9,
            self._W10,
            self._W11,
            self._W6,
            self._W7,
            self._W8,
            self._W9,
            self._W10,
            self._W11,
            self._W12,
        ]

    def get_score(self, board):
        """
        評価値の算出
        """
        score = 0
        b_bitboard, w_bitboard = board.get_bitboard_info()

        # ボードサイズ8以外は考慮なし
        if board.size != 8:
            return score

        # ピュア山値
        for mask, value in zip(self.pureyama_mask, self.pureyama_value):
            score += self._get_mask_value(b_bitboard, w_bitboard, mask, value, self._W1)

        # 山値
        for mask, value in zip(self.yama_mask, self.yama_value):
            score += self._get_mask_value(b_bitboard, w_bitboard, mask, value, self._W2)

        # ピュアウィング
        for mask, value in zip(self.purewing_mask, self.purewing_value):
            score += self._get_mask_value(b_bitboard, w_bitboard, mask, value, self._W3)

        # ウィング
        for mask, value in zip(self.wing_mask, self.wing_value):
            score += self._get_mask_value(b_bitboard, w_bitboard, mask, value, self._W4)

        # ブロック
        for mask, value in zip(self.block_mask, self.block_value):
            score += self._get_mask_value(b_bitboard, w_bitboard, mask, value, self._W5)

        # 確定石
        for i, (mask, value) in enumerate(zip(self.stable_mask, self.stable_value)):
            score += self._get_mask_value(b_bitboard, w_bitboard, mask, value, self.stable_weight[i%13])

        return score

    def _get_mask_value(self, b_bitboard, w_bitboard, mask, value, weight):
        """
        マスクした値を取得
        """
        score_b = weight if (b_bitboard & mask) == value else 0
        score_w = weight if (w_bitboard & mask) == value else 0

        return score_b - score_w


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

    def get_score(self, board):
        """
        評価値の算出
        """
        score = 0
        b_bitboard, w_bitboard = board.get_bitboard_info()

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


if __name__ == '__main__':
    from board import BitBoard

    board8 = BitBoard(8)
    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 2)
    board8.put_stone('black', 2, 3)
    board8.put_stone('white', 4, 2)
    board8.put_stone('black', 1, 1)
    board8.put_stone('white', 0, 0)

    possibles_b = board8.get_possibles('black', True)
    possibles_w = board8.get_possibles('white', True)

    print(board8)

    #------------------------------------------------------
    # TableScorer
    scorer = TableScorer()

    print('black score', scorer.get_score('black', board8))
    print('white score', scorer.get_score('white', board8))
    assert scorer.get_score('black', board8) == -22
    assert scorer.get_score('white', board8) == -22

    #------------------------------------------------------
    # PossibilityScorer
    scorer = PossibilityScorer()

    print('score', scorer.get_score(possibles_b, possibles_w))
    assert scorer.get_score(possibles_b, possibles_w) == 5

    #------------------------------------------------------
    # OpeningScorer
    scorer = OpeningScorer()

    print('score', scorer.get_score(board8))
    assert scorer.get_score(board8) == -8.25

    #------------------------------------------------------
    # WinLoseScorer
    scorer = WinLoseScorer()

    print('score', scorer.get_score(board8, [], []))
    assert scorer.get_score(board8, [], []) == -10006

    print('score', scorer.get_score(board8, possibles_b, possibles_w))
    assert scorer.get_score(board8, possibles_b, possibles_w) is None

    #------------------------------------------------------
    # NumberScorer
    scorer = NumberScorer()

    print('score', scorer.get_score(board8))
    assert scorer.get_score(board8) == -6

    #------------------------------------------------------
    # EdgeScorer
    scorer = EdgeScorer()

    # ピュア山/山
    board8 = BitBoard(8)
    board8._black_bitboard = 0x7E00000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 28

    board8._black_bitboard = 0x7E3C000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 75

    board8._black_bitboard = 0xFE3C000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 600

    board8._black_bitboard = 0x7E3C000000003C7E
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 150

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0x0081C3C3C3C38100
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == -150

    # ピュアウィング/ウィング
    board8._black_bitboard = 0x7C3C000000003C7C
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == -6

    board8._black_bitboard = 0x0081C3C3C3C30000
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == -6

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0x3E3C000000003C3E
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 6

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0x0000C3C3C3C38100
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 6

    board8._black_bitboard = 0x0080C0C0C0C00000
    board8._white_bitboard = 0x0000030103030100
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 0

    # ブロック
    board8._black_bitboard = 0xBC00000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 0

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0x3C0081818181003C
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 0

    # 確定石
    board8._black_bitboard = 0xC000000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 100

    board8._black_bitboard = 0xE000000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 200

    board8._black_bitboard = 0xFF00000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 1300

    board8._black_bitboard = 0xFF818181818181FF
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 5200

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0xC3810000000081C3
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == -800

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0xF7810080800081FF
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == -2200

    #------------------------------------------------------
    # CornerScorer
    scorer = CornerScorer()

    def rotate_90(bits): # 90°回転
        bits_tmp = [['0' for i in range(8)] for j in range(8)]

        check = 1 << 63
        for y in range(8):
            for x in range(8):
                if bits & check:
                    bits_tmp[y][x] = '1'
                check >>= 1

        import numpy as np

        bits_tmp = np.rot90(np.array(bits_tmp))
        bits = int(''.join(bits_tmp.flatten()), 2)

        return bits

    # Level1
    # 左下
    print('bottom left')
    for i in scorer.level1_maskvalue[0]:
        print('0x' + format(i, '016X') + ',')

    # 左上
    print('top left')
    for i in scorer.level1_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右上
    print('top right')
    for i in scorer.level1_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右下
    print('bottom right')
    for i in scorer.level1_maskvalue[0]:
        values = rotate_90(i)
        print('0x' + format(values, '016X') + ',')

    board8 = BitBoard(8)
    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 0

    board8._black_bitboard = 0xE7C380000080C0C0
    board8._white_bitboard = 0x0000000000010303
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 200

    # Level2
    # 左下
    print('bottom left')
    for i in scorer.level2_maskvalue[0]:
        print('0x' + format(i, '016X') + ',')

    # 左上
    print('top left')
    for i in scorer.level2_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右上
    print('top right')
    for i in scorer.level2_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右下
    print('bottom right')
    for i in scorer.level2_maskvalue[0]:
        values = rotate_90(i)
        print('0x' + format(values, '016X') + ',')

    board8 = BitBoard(8)
    board8._black_bitboard = 0x0000000080C0E0F0
    board8._white_bitboard = 0xF7E703010000070F
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == -400

    # Level3
    # 左下
    print('bottom left')
    for i in scorer.level3_maskvalue[0]:
        print('0x' + format(i, '016X') + ',')

    # 左上
    print('top left')
    for i in scorer.level3_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右上
    print('top right')
    for i in scorer.level3_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右下
    print('bottom right')
    for i in scorer.level3_maskvalue[0]:
        values = rotate_90(i)
        print('0x' + format(values, '016X') + ',')

    board8 = BitBoard(8)
    board8._black_bitboard = 0x00000080C0E0F0F8
    board8._white_bitboard = 0x0303030301000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 300

    board8._black_bitboard = 0x0000000103070707
    board8._white_bitboard = 0xF8F0C00000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 100

    # Level4
    # 左下
    print('bottom left')
    for i in scorer.level4_maskvalue[0]:
        print('0x' + format(i, '016X') + ',')

    # 左上
    print('top left')
    for i in scorer.level4_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右上
    print('top right')
    for i in scorer.level4_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右下
    print('bottom right')
    for i in scorer.level4_maskvalue[0]:
        values = rotate_90(i)
        print('0x' + format(values, '016X') + ',')

    board8 = BitBoard(8)
    board8._black_bitboard = 0xF08080C0E0F0F8FD
    board8._white_bitboard = 0x0F0F070703010000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 100

    board8._black_bitboard = 0xFCF8000000C0F8FC
    board8._white_bitboard = 0x0303030303010000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 400

    # Level5
    # 左下
    print('bottom left')
    for i in scorer.level5_maskvalue[0]:
        print('0x' + format(i, '016X') + ',')

    # 左上
    print('top left')
    for i in scorer.level5_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右上
    print('top right')
    for i in scorer.level5_maskvalue[0]:
        values = rotate_90(i)
        values = rotate_90(values)
        print('0x' + format(values, '016X') + ',')

    # 右下
    print('bottom right')
    for i in scorer.level5_maskvalue[0]:
        values = rotate_90(i)
        print('0x' + format(values, '016X') + ',')

    board8 = BitBoard(8)
    board8._black_bitboard = 0xFFFCF8F0E0C08000
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 900

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0x0F0F0F0F07030100
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == -900

    board8._black_bitboard = 0xFFFEFCF8F0000000
    board8._white_bitboard = 0x000000000F1F3F7F
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 0
