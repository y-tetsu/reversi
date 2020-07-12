#!/usr/bin/env python
"""
終盤完全読み
"""

from reversi.strategies.common import Measure, AbstractStrategy
from reversi.strategies.easy import Random
from reversi.strategies.minmax import MinMax2_TPWE
from reversi.strategies.alphabeta import _AlphaBeta_N, AlphaBeta_N, AlphaBeta4_TPW
from reversi.strategies.iterative import AbI_B_TPW, AbI_B_TPWE, AbI_B_TPWEC, NsI_B_TPW, NsI_B_TPW2, NsI_B_TPWE
from reversi.strategies.switch import SwitchNsI_B_TPW, SwitchNsI_B_TPWE


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
