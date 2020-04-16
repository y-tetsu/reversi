#!/usr/bin/env python
"""
終盤完全読み
"""

import sys
sys.path.append('../')

from strategies.common import Timer, Measure, CPU_TIME, AbstractStrategy
from strategies.easy import Random
from strategies.minmax import MinMax2_TPWE
from strategies.alphabeta import _AlphaBeta_N, AlphaBeta_N, AlphaBeta4_TPW
from strategies.iterative import AbI_B_TPW, AbI_B_TPWE, AbI_B_TPWEC, NsI_B_TPW, NsI_B_TPW2, NsI_B_TPWE
from strategies.switch import SwitchNsI_B_TPW, SwitchNsI_B_TPWE


class FullReading(AbstractStrategy):
    """
    終盤完全読み
    """
    def __init__(self, remain=None, base=None):
        self.remain = remain
        self.fullreading = AlphaBeta_N(depth=remain)
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


class _FullReading(FullReading):
    """
    終盤完全読み(時間制限なし)
    """
    def __init__(self, remain=None, base=None):
        self.remain = remain
        self.fullreading = _AlphaBeta_N(depth=remain)
        self.base = base


class MinMax2F9_TPWE(FullReading):
    """
    MinMax法で2手先を読む
    (評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=MinMax2_TPWE()):
        super().__init__(remain, base)


class AlphaBeta4F9_TPW(FullReading):
    """
    AlphaBeta法で4手先を読む
    (評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AlphaBeta4_TPW()):
        super().__init__(remain, base)


class AbIF9_B_TPW(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_B_TPW()):
        super().__init__(remain, base)


class AbIF9_B_TPWE(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_B_TPWE()):
        super().__init__(remain, base)


class AbIF9_B_TPWEC(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWEC, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_B_TPWEC()):
        super().__init__(remain, base)


class NsIF9_B_TPW(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=NsI_B_TPW()):
        super().__init__(remain, base)


class NsIF9_B_TPW2(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=NsI_B_TPW2()):
        super().__init__(remain, base)


class NsIF9_B_TPWE(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=NsI_B_TPWE()):
        super().__init__(remain, base)


class NsIF10_B_TPW(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り10手)
    """
    def __init__(self, remain=10, base=NsI_B_TPW()):
        super().__init__(remain, base)


class NsIF11_B_TPW(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り11手)
    """
    def __init__(self, remain=11, base=NsI_B_TPW()):
        super().__init__(remain, base)


class NsIF12_B_TPW(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り12手)
    """
    def __init__(self, remain=12, base=NsI_B_TPW()):
        super().__init__(remain, base)


class SwitchNsIF9_B_TPW(FullReading):
    """
    SwitchNsI_B_TPW+完全読み開始:残り9手
    """
    def __init__(self, remain=9, base=SwitchNsI_B_TPW()):
        super().__init__(remain, base)


class SwitchNsIF9_B_TPWE(FullReading):
    """
    SwitchNsI_B_TPWE+完全読み開始:残り9手
    """
    def __init__(self, remain=9, base=SwitchNsI_B_TPWE()):
        super().__init__(remain, base)


class RandomF11(_FullReading):
    """
    ランダムに手を読む
    (4x4のみ完全読み:残り11手)
    """
    def __init__(self, remain=11, base=Random()):
        super().__init__(remain, base)

    @Measure.time
    def next_move(self, color, board):
        if board.size == 4:
            return super().next_move(color, board)

        return self.base.next_move(color, board)


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

    print('--- Test For AbIF9_B_TPW Strategy ---')
    strategy = AbIF9_B_TPW(remain=11)
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
    bitboard8.put_stone('white', 0, 7)
    bitboard8.put_stone('black', 1, 7)
    print(bitboard8)

    # full
    strategy = AbIF9_B_TPW()
    assert strategy.remain == 9
    Measure.count[fullreading_key] = 0
    move = strategy.next_move('white', bitboard8)
    print(move)
    assert move == (7, 0)
    print( 'count     :', Measure.count[fullreading_key] )
    assert Measure.count[fullreading_key] == 859
    print( 'timeout   :', Timer.timeout_flag[fullreading_key] )
    assert Timer.timeout_flag[fullreading_key] == False
