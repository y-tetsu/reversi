#!/usr/bin/env python
"""
複数戦略切り替え型
"""

import sys
sys.path.append('../')

from strategies.common import CPU_TIME, AbstractStrategy
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.iterative import NsI_B_TPW, NsI_B_TPW_O


class MultipleSizeError(Exception):
    """
    入力サイズのエラー
    """
    pass


class Multiple(AbstractStrategy):
    """
    複数戦略を切り替える
    """
    def __init__(self, turns=None, strategies=None):
        if len(turns) != len(strategies):
            raise MultipleSizeError

        self.turns = turns
        self.strategies = strategies

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        stones = board.score['black'] + board.score['white']

        # 残り手数が閾値以下
        strategy = self.strategies[-1]

        for i, turn in enumerate(self.turns):
            if stones <= turn:
                strategy = self.strategies[i]
                break

        return strategy.next_move(color, board)


class MultiNegaScout(Multiple):
    """
    20手まで:NsI_B_TPW_O, 20手以降:NsI_B_TPW_O
    """
    def __init__(self, turns=[20, 64], strategies=[NsI_B_TPW_O(), NsI_B_TPW()]):
        super().__init__(turns, strategies)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    print('--- Test For MultiNegaScout Strategy ---')
    multiple = MultiNegaScout()
    assert multiple.turns == [20, 64]
    assert multiple.strategies[0].__class__.__name__ == 'NsI_B_TPW_O'
    assert multiple.strategies[1].__class__.__name__ == 'NsI_B_TPW'

    bitboard8 = BitBoard()
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)

    key = multiple.strategies[0].search.__class__.__name__ + str(os.getpid())
    Measure.count[key] = 0
    move = multiple.next_move('black', bitboard8)
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

    key = multiple.strategies[1].search.__class__.__name__ + str(os.getpid())
    Measure.count[key] = 0
    move = multiple.next_move('black', bitboard8)
    print(move)
    assert move == (3, 6)
    print( 'count     :', Measure.count[key] )
    assert Measure.count[key] >= 2000
