#!/usr/bin/env python
"""
評価値算出
"""

import sys
sys.path.append('../')

from strategies.common import AbstractScorer
from strategies.easy import Table

from board import Board, BitBoard


class TableScorer(AbstractScorer):
    """
    盤面の評価値をTableで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a=0, b=-1, x=-25, o=-5):
        self.table = Table(size, corner, c, a, b, x, o)  # Table戦略を利用する

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
    配置可能数に基づいて算出
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


class StonesScorer(AbstractScorer):
    """
    石数に基づいて算出
    """
    def get_score(self, board):
        """
        評価値の算出
        """
        return board.score['black'] - board.score['white']


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
    # StonesScorer
    scorer = StonesScorer()

    print('score', scorer.get_score(board8))
    assert scorer.get_score(board8) == -6
