#!/usr/bin/env python
"""
複数戦略切り替え型
"""

import sys
sys.path.append('../')

from strategies.common import Timer, Measure, CPU_TIME, AbstractStrategy
from strategies.iterative import NsI_B_TPW, NsI_BC_TPW
from strategies.negascout import NegaScout_TPW
from strategies.coordinator import Evaluator_TPW


class SwitchSizeError(Exception):
    """
    入力サイズのエラー
    """
    pass


class Switch(AbstractStrategy):
    """
    複数戦略を切り替える
    """
    def __init__(self, turns=None, strategies=None):
        if len(turns) != len(strategies):
            raise SwitchSizeError

        self.turns = turns
        self.strategies = strategies

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        stones = board.score['black'] + board.score['white']

        # 現在の手数が閾値以下
        strategy = self.strategies[-1]

        for i, turn in enumerate(self.turns):
            if stones - 4 <= turn:
                strategy = self.strategies[i]
                break

        return strategy.next_move(color, board)


class SwitchNegaScout(Switch):
    """
    パラーメータ切り替え型
    """
    def __init__(
            self,
            turns=[
                15,
                25,
                35,
                45,
                60
            ],
            strategies=[
                NsI_B_TPW(search=NegaScout_TPW(evaluator=Evaluator_TPW(corner=100, c=-20, a1= 0, a2=-1, b=-1, x=-25, o=-5, wp= 5))),
                NsI_B_TPW(search=NegaScout_TPW(evaluator=Evaluator_TPW(corner= 70, c=-20, a1= 0, a2=-1, b=-1, x=-25, o=-5, wp= 5))),
                NsI_B_TPW(search=NegaScout_TPW(evaluator=Evaluator_TPW(corner= 30, c=-10, a1= 0, a2= 0, b= 0, x=-15, o=-3, wp= 5))),
                NsI_B_TPW(search=NegaScout_TPW(evaluator=Evaluator_TPW(corner=  1, c=  1, a1= 1, a2= 1, b= 1, x=  1, o= 1, wp= 5))),
                NsI_B_TPW(search=NegaScout_TPW(evaluator=Evaluator_TPW(corner=  1, c=  1, a1= 1, a2= 1, b= 1, x=  1, o= 1, wp= 5)))
            ]):
        super().__init__(turns, strategies)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    print('--- Test For SwitchNegaScout Strategy ---')
    switch = SwitchNegaScout()
    assert switch.turns == [20, 40, 60]
    assert switch.strategies[0].__class__.__name__ == 'NsI_B_TPW'
    assert switch.strategies[1].__class__.__name__ == 'NsI_B_TPW'
    assert switch.strategies[2].__class__.__name__ == 'NsI_BC_TPW'

    assert switch.strategies[0].search.evaluator.table.table._CORNER == 70
    assert switch.strategies[1].search.evaluator.table.table._CORNER == 50
    assert switch.strategies[2].search.evaluator.table.table._CORNER == 50

    assert switch.strategies[0].search.evaluator.table.table._C == -20
    assert switch.strategies[1].search.evaluator.table.table._C == -20
    assert switch.strategies[2].search.evaluator.table.table._C == -10

    assert switch.strategies[0].search.evaluator.possibility._W == 2
    assert switch.strategies[1].search.evaluator.possibility._W == 5
    assert switch.strategies[2].search.evaluator.possibility._W == 5

    bitboard8 = BitBoard()
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)

    key = switch.strategies[0].search.__class__.__name__ + str(os.getpid())
    Measure.count[key] = 0
    move = switch.next_move('black', bitboard8)
    print(move)
    assert move == (5, 3)
    print( 'count     :', Measure.count[key] )
    assert Measure.count[key] >= 800

    bitboard8.put_stone('black', 4, 5)
    bitboard8.put_stone('white', 5, 6)
    bitboard8.put_stone('black', 4, 6)
    bitboard8.put_stone('white', 3, 7)
    bitboard8.put_stone('black', 4, 7)
    bitboard8.put_stone('white', 5, 7)
    bitboard8.put_stone('black', 1, 4)
    bitboard8.put_stone('white', 0, 4)
    bitboard8.put_stone('black', 6, 5)
    bitboard8.put_stone('white', 5, 3)
    bitboard8.put_stone('black', 2, 5)
    bitboard8.put_stone('white', 4, 1)
    bitboard8.put_stone('black', 2, 3)
    bitboard8.put_stone('white', 3, 1)
    bitboard8.put_stone('black', 5, 1)
    bitboard8.put_stone('white', 2, 2)
    bitboard8.put_stone('black', 5, 0)
    bitboard8.put_stone('white', 2, 1)
    bitboard8.put_stone('black', 0, 5)
    bitboard8.put_stone('white', 0, 6)
    bitboard8.put_stone('black', 6, 3)
    bitboard8.put_stone('white', 6, 4)
    bitboard8.put_stone('black', 7, 4)
    bitboard8.put_stone('white', 6, 2)
    bitboard8.put_stone('black', 7, 3)
    bitboard8.put_stone('white', 4, 0)
    bitboard8.put_stone('black', 1, 2)
    bitboard8.put_stone('white', 7, 5)
    bitboard8.put_stone('black', 1, 0)
    bitboard8.put_stone('white', 7, 2)
    bitboard8.put_stone('black', 2, 0)
    bitboard8.put_stone('white', 6, 0)
    bitboard8.put_stone('black', 7, 6)
    bitboard8.put_stone('white', 7, 7)
    bitboard8.put_stone('black', 6, 7)
    bitboard8.put_stone('white', 1, 5)
    bitboard8.put_stone('black', 2, 7)
    bitboard8.put_stone('white', 6, 6)
    bitboard8.put_stone('black', 6, 1)
    bitboard8.put_stone('white', 2, 6)
    bitboard8.put_stone('black', 1, 6)
    bitboard8.put_stone('white', 7, 1)
    print(bitboard8)

    key = switch.strategies[1].search.__class__.__name__ + str(os.getpid())
    Measure.count[key] = 0
    move = switch.next_move('black', bitboard8)
    print(move)
    assert move == (3, 6)
    print( 'count     :', Measure.count[key] )
    assert Measure.count[key] >= 2000
