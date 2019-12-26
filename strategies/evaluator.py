#!/usr/bin/env python
"""
オセロの評価関数
"""

import sys
sys.path.append('../')

from strategies.common import AbstractEvaluator
from strategies.scorer import TableScorer, PossibilityScorer, OpeningScorer, WinLooseScorer


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


class Evaluator_TP(Evaluator_T):
    """
    盤面の評価値をTable+配置可能数で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a=0, b=-1, x=-25, o=-5, w1=5):
        super().__init__(size, corner, c, a, b, x, o)
        self.possibility = PossibilityScorer(w1)  # 配置可能数による評価値算出

    def evaluate(self, color, board, possibles_b, possibles_w):
        """
        評価値の算出
        """
        possibility = self.possibility.get_score(possibles_b, possibles_w)

        return super().evaluate(color, board, possibles_b, possibles_w) + possibility


class Evaluator_TPO(Evaluator_TP):
    """
    盤面の評価値をTable+配置可能数+開放度で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a=0, b=-1, x=-25, o=-5, w1=5, w2=-0.75):
        super().__init__(size, corner, c, a, b, x, o)
        self.opening = OpeningScorer(w2)  # 開放度による評価値算出

    def evaluate(self, color, board, possibles_b, possibles_w):
        """
        評価値の算出
        """
        opening = self.opening.get_score(board)

        return super().evaluate(color, board, possibles_b, possibles_w) + opening


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
    # Evaluator_TP
    evaluator = Evaluator_TP()

    print('black score', evaluator.evaluate('black', board8, possibles_b, possibles_w))
    assert evaluator.evaluate('black', board8, possibles_b, possibles_w) == -17

    #----------------------------------------------------------------
    # Evaluator_TPO
    evaluator = Evaluator_TPO()

    print('black score', evaluator.evaluate('black', board8, possibles_b, possibles_w))
    assert evaluator.evaluate('black', board8, possibles_b, possibles_w) == -25.25
