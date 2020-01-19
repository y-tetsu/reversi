#!/usr/bin/env python
"""
序盤はランダムに手を選ぶ
"""

import sys
sys.path.append('../')

from strategies.common import CPU_TIME, AbstractStrategy
from strategies.measure import Measure
from strategies.easy import Random
from strategies.proto import AB_TI
from strategies.minmax import MinMax3_TPW, MinMax3_TPOW
from strategies.negamax import NegaMax3_TPW, NegaMax3_TPOW
from strategies.alphabeta import AlphaBeta3_TPW, AlphaBeta3_TPOW
from strategies.negascout import NegaScout3_TPW, NegaScout3_TPOW
from strategies.joseki import AbIF11J_B_TPW, SwitchNsF12J


class RandomOpening(AbstractStrategy):
    """
    序盤はランダムに手を選ぶ
    """
    def __init__(self, depth=None, base=None):
        self.depth = depth
        self.random = Random()
        self.base = base

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        depth = board.score['black'] + board.score['white'] - 4

        # 現在の手数が閾値以下
        if depth <= self.depth:
            return self.random.next_move(color, board)

        return self.base.next_move(color, board)


class MinMax3Ro_TPW(RandomOpening):
    """
    RandamOpening(10手) + MinMax3_TPW
    """
    def __init__(self, depth=10, base=MinMax3_TPW()):
        super().__init__(depth, base)


class MinMax3Ro_TPOW(RandomOpening):
    """
    RandamOpening(10手) + MinMax3_TPOW
    """
    def __init__(self, depth=10, base=MinMax3_TPOW()):
        super().__init__(depth, base)


class NegaMax3Ro_TPW(RandomOpening):
    """
    RandamOpening(10手) + NegaMax3_TPW
    """
    def __init__(self, depth=10, base=NegaMax3_TPW()):
        super().__init__(depth, base)


class NegaMax3Ro_TPOW(RandomOpening):
    """
    RandamOpening(10手) + NegaMax3_TPOW
    """
    def __init__(self, depth=10, base=NegaMax3_TPOW()):
        super().__init__(depth, base)


class AlphaBeta3Ro_TPW(RandomOpening):
    """
    RandamOpening(10手) + AlphaBeta3_TPW
    """
    def __init__(self, depth=10, base=AlphaBeta3_TPW()):
        super().__init__(depth, base)


class AlphaBeta3Ro_TPOW(RandomOpening):
    """
    RandamOpening(10手) + AlphaBeta3_TPOW
    """
    def __init__(self, depth=10, base=AlphaBeta3_TPOW()):
        super().__init__(depth, base)


class NegaScout3Ro_TPW(RandomOpening):
    """
    RandamOpening(10手) + NegaScout3_TPW
    """
    def __init__(self, depth=10, base=NegaScout3_TPW()):
        super().__init__(depth, base)


class NegaScout3Ro_TPOW(RandomOpening):
    """
    RandamOpening(10手) + NegaScout3_TPOW
    """
    def __init__(self, depth=10, base=NegaScout3_TPOW()):
        super().__init__(depth, base)


class AB_TIRo(RandomOpening):
    """
    RandamOpening(10手) + AB_TI
    """
    def __init__(self, depth=10, base=AB_TI()):
        super().__init__(depth, base)


class AbIF11JRo_B_TPW(RandomOpening):
    """
    RandamOpening(10手) + AbIF11J_B_TPW
    """
    def __init__(self, depth=10, base=AbIF11J_B_TPW()):
        super().__init__(depth, base)


class SwitchNsF12JRo(RandomOpening):
    """
    RandamOpening(10手) + SwitchNsF12J
    """
    def __init__(self, depth=10, base=SwitchNsF12J()):
        super().__init__(depth, base)


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
    print(bitboard8)

    randomopening = AbIF11JRo_B_TPW()
    move = randomopening.next_move('white', bitboard8)
    print(move)

    bitboard8.put_stone('white', 3, 7)

    move = randomopening.next_move('white', bitboard8)
    print(move)

    bitboard8.put_stone('black', 4, 7)

    move = randomopening.next_move('white', bitboard8)
    print(move)
