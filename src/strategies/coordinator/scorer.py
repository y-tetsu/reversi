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
    def __init__(self, w1=50, w2=100, w3=-15, w4=-30, w5=10, w6=10, w7=10, w8=10, w9=10, w10=10, w11=10, w12=10):
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
    角のパターンに基づいて算出
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
        # Level3
        # Level4
        # Level5

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
                pass
                # Level2
                # Level3
                # Level4
                # Level5

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
    assert score == 100

    board8._black_bitboard = 0x7E3C000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 150

    board8._black_bitboard = 0xFE3C000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 60

    board8._black_bitboard = 0x7E3C000000003C7E
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 300

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0x0081C3C3C3C38100
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == -300

    # ピュアウィング/ウィング
    board8._black_bitboard = 0x7C3C000000003C7C
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == -90

    board8._black_bitboard = 0x0081C3C3C3C30000
    board8._white_bitboard = 0x0000000000000000
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == -90

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0x3E3C000000003C3E
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 90

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0x0000C3C3C3C38100
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == 90

    board8._black_bitboard = 0x0080C0C0C0C00000
    board8._white_bitboard = 0x0000030103030100
    print(board8)
    score = scorer.get_score(board8)
    print('score', score)
    assert score == -15

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
    assert score == -40

    # 確定石
    board8._black_bitboard = 0xC000000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 10

    board8._black_bitboard = 0xE000000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 20

    board8._black_bitboard = 0xFF00000000000000
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 130

    board8._black_bitboard = 0xFF818181818181FF
    board8._white_bitboard = 0x0000000000000000
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == 520

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0xC3810000000081C3
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == -80

    board8._black_bitboard = 0x0000000000000000
    board8._white_bitboard = 0xF7810080800081FF
    print(board8)

    score = scorer.get_score(board8)
    print('score', score)
    assert score == -220

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

    # Level1
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
