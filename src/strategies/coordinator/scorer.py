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
    def __init__(self, w1=50, w2=100, w3=-15, w4=-30):
        self._W1 = w1
        self._W2 = w2
        self._W3 = w3
        self._W4 = w4

        # ピュア山
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
        self.yama_mask = [
            0xFF00000000000000,
            0x0101010101010101,
            0x00000000000000FF,
            0x8080808080808080
        ]
        self.yama_value = [
            0x7E00000000000000,
            0x0001010101010100,
            0x000000000000007E,
            0x0080808080808000
        ]

        # ピュアウィング
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
        self.wing_mask = [
            0xFF24000000000000,
            0xFF24000000000000,
            0x0103030101030301,
            0x0103030101030301,
            0x00000000000024FF,
            0x00000000000024FF,
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

        return score

    def _get_mask_value(self, b_bitboard, w_bitboard, mask, value, weight):
        """
        マスクした値を取得
        """
        score_b = weight if (b_bitboard & mask) == value else 0
        score_w = weight if (w_bitboard & mask) == value else 0

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
    assert score == 0

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
