#!/usr/bin/env python
"""
終盤完全読み
"""

import sys
sys.path.append('../')

from strategies.common import CPU_TIME, AbstractStrategy
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.alphabeta import AlphaBeta_S
from strategies.iterative import AbI_BC_TPOW, AbI_BCW_TPOW


class FullReading(AbstractStrategy):
    """
    終盤完全読み
    """
    def __init__(self, remain=None, base=None):
        self.remain = remain
        self.fullreading = AlphaBeta_S(depth=remain)
        self.base = base

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        remain = (board.size * board.size) - (board.score['black'] + board.score['white'])

        # 残り手数が閾値以下
        if remain <= self.remain:
            return self.fullreading.next_move(color, board)  # 完全読み

        return self.base.next_move(color, board)


class AbIF_BC_TPOW(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:BC、評価関数:TPOW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_BC_TPOW()):
        super().__init__(remain, base)


class AbIF_BCW_TPOW(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:BCW、評価関数:TPOW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_BCW_TPOW()):
        super().__init__(remain, base)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    bitboard8 = BitBoard()
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
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

    print('--- Test For AbIF_BC_TPOW Strategy ---')
    strategy = AbIF_BC_TPOW(remain=11)
    assert strategy.remain == 11

    base_key = strategy.base.search.__class__.__name__ + str(os.getpid())
    fullreading_key = strategy.fullreading.__class__.__name__ + str(os.getpid())

    # normal
    Measure.count[base_key] = 0
    move = strategy.next_move('black', bitboard8)
    print(move)
    assert move == (3, 6)
    print( 'count     :', Measure.count[base_key] )
    assert Measure.count[base_key] >= 1000

    bitboard8.put_stone('black', 3, 6)

    # full(Timeout)
    Measure.count[fullreading_key] = 0
    move = strategy.next_move('white', bitboard8)
    print(move)
    assert move == (3, 0)
    print( 'count     :', Measure.count[fullreading_key] )
    print( 'timeout   :', Timer.timeout_flag[fullreading_key] )

    bitboard8.put_stone('white', 3, 5)
    bitboard8.put_stone('black', 1, 3)
    print(bitboard8)

    # full
    strategy = AbIF_BC_TPOW()
    assert strategy.remain == 9
    Measure.count[fullreading_key] = 0
    move = strategy.next_move('white', bitboard8)
    print(move)
    assert move == (7, 0)
    print( 'count     :', Measure.count[fullreading_key] )
    print( 'timeout   :', Timer.timeout_flag[fullreading_key] )
