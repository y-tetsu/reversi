#!/usr/bin/env python
"""
オセロの評価関数
"""

import sys
sys.path.append('../')

from strategies.common import AbstractEvaluator
from strategies.scorer import TableScorer, WinLooseScorer


class Evaluator_T(AbstractEvaluator):
    """
    盤面の評価値をTableで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a=0, b=-1, x=-25, o=-5):
        self.table = TableScorer(size, corner, c, a, b, x, o)  # Tableによる評価値算出

    def evaluate(self, color, board, possibles_b, possibles_w):
        """
        評価値の算出
        """
        return self.table.get_score(color, board)


class Evaluator_TW(Evaluator_T):
    """
    盤面の評価値をTable+勝敗で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a=0, b=-1, x=-25, o=-5, w1=10000):
        super().__init__(size, corner, c, a, b, x, o)
        self.winloose = WinLooseScorer(w1)  # 勝敗による評価値算出

    def evaluate(self, color, board, possibles_b, possibles_w):
        """
        評価値の算出
        """
        winloose = self.winloose.get_score(board, possibles_b, possibles_w)

        if winloose is not None:
            return winloose

        return self.table.get_score(color, board)


if __name__ == '__main__':
    from board import Board

    board8 = Board(8)
    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 2)
    board8.put_stone('black', 2, 3)
    board8.put_stone('white', 4, 2)
    board8.put_stone('black', 1, 1)
    board8.put_stone('white', 0, 0)

    possibles_b = board8.get_possibles('black', True)
    possibles_w = board8.get_possibles('white', True)

    print(board8)

    #----------------------------------------------------------------
    # Evaluator_T
    evaluator = Evaluator_T()

    print('black score', evaluator.evaluate('black', board8, [], []))
    print('white score', evaluator.evaluate('white', board8, [], []))
    assert evaluator.evaluate('black', board8, [], []) == -22
    assert evaluator.evaluate('white', board8, [], []) == -22

    #----------------------------------------------------------------
    # Evaluator_TW
    evaluator = Evaluator_TW()

    print('black score', evaluator.evaluate('black', board8, [], []))
    assert evaluator.evaluate('black', board8, [], []) == -10006

    print('black score', evaluator.evaluate('black', board8, possibles_b, possibles_w))
    assert evaluator.evaluate('black', board8, possibles_b, possibles_w) == -22
