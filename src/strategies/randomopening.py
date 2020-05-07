#!/usr/bin/env python
"""
序盤はランダムに手を選ぶ
"""

import sys
sys.path.append('../')

from strategies.common import Measure, CPU_TIME, AbstractStrategy
from strategies.easy import Random
from strategies.proto import AB_TI
from strategies.minmax import MinMax1_TPW, MinMax1_TPW2, MinMax1_TPWE, MinMax1_TPWEC, MinMax1_PWE, MinMax2_T, MinMax2_TPW, MinMax2_TPWE, MinMax2_TPWEC, MinMax3_T, MinMax3_TP, MinMax3_TPW, MinMax3_TPOW
from strategies.negamax import _NegaMax3_TPW, NegaMax3_TPW, NegaMax3_TPOW
from strategies.alphabeta import AlphaBeta4_TPW, AlphaBeta4_TPWE
from strategies.negascout import NegaScout3_TPW, NegaScout3_TPOW, NegaScout4_TPW, NegaScout4_TPWE
from strategies.fullreading import MinMax2F9_TPWE, AlphaBeta4F9_TPW
from strategies.joseki import AlphaBeta4J_TPW, AlphaBeta4F9J_TPW, AbIF9J_B_TPW, AbIF9J_B_TPWE, AbIF9J_B_TPWEC, NsIF9J_B_TPW, NsIF9J_B_TPW2, NsIF9J_B_TPWE, SwitchNsIF9J_B_TPW, SwitchNsIF9J_B_TPWE


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


class MinMax1Ro_TPW2(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_TPW2
    """
    def __init__(self, depth=8, base=MinMax1_TPW2()):
        super().__init__(depth, base)


class MinMax1Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_TPW
    """
    def __init__(self, depth=8, base=MinMax1_TPW()):
        super().__init__(depth, base)


class MinMax1Ro_PWE(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_PWE
    """
    def __init__(self, depth=8, base=MinMax1_PWE()):
        super().__init__(depth, base)


class MinMax1Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_TPWE
    """
    def __init__(self, depth=8, base=MinMax1_TPWE()):
        super().__init__(depth, base)


class MinMax1Ro_TPWEC(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_TPWEC
    """
    def __init__(self, depth=8, base=MinMax1_TPWEC()):
        super().__init__(depth, base)


class MinMax2Ro_T(RandomOpening):
    """
    RandamOpening(8手) + MinMax2_T
    """
    def __init__(self, depth=8, base=MinMax2_T()):
        super().__init__(depth, base)


class MinMax2Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + MinMax2_TPW
    """
    def __init__(self, depth=8, base=MinMax2_TPW()):
        super().__init__(depth, base)


class MinMax2Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + MinMax2_TPWE
    """
    def __init__(self, depth=8, base=MinMax2_TPWE()):
        super().__init__(depth, base)


class MinMax2F9Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + MinMax2F9_TPWE
    """
    def __init__(self, depth=8, base=MinMax2F9_TPWE()):
        super().__init__(depth, base)


class MinMax2Ro_TPWEC(RandomOpening):
    """
    RandamOpening(8手) + MinMax2_TPWEC
    """
    def __init__(self, depth=8, base=MinMax2_TPWEC()):
        super().__init__(depth, base)


class MinMax3Ro_T(RandomOpening):
    """
    RandamOpening(8手) + MinMax3_T
    """
    def __init__(self, depth=8, base=MinMax3_T()):
        super().__init__(depth, base)


class MinMax3Ro_TP(RandomOpening):
    """
    RandamOpening(8手) + MinMax3_TP
    """
    def __init__(self, depth=8, base=MinMax3_TP()):
        super().__init__(depth, base)


class MinMax3Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + MinMax3_TPW
    """
    def __init__(self, depth=8, base=MinMax3_TPW()):
        super().__init__(depth, base)


class MinMax3Ro_TPOW(RandomOpening):
    """
    RandamOpening(8手) + MinMax3_TPOW
    """
    def __init__(self, depth=8, base=MinMax3_TPOW()):
        super().__init__(depth, base)


class _NegaMax3Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + _NegaMax3_TPW
    """
    def __init__(self, depth=8, base=_NegaMax3_TPW()):
        super().__init__(depth, base)


class NegaMax3Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + NegaMax3_TPW
    """
    def __init__(self, depth=8, base=NegaMax3_TPW()):
        super().__init__(depth, base)


class NegaMax3Ro_TPOW(RandomOpening):
    """
    RandamOpening(8手) + NegaMax3_TPOW
    """
    def __init__(self, depth=8, base=NegaMax3_TPOW()):
        super().__init__(depth, base)


class AlphaBeta4Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4_TPW
    """
    def __init__(self, depth=8, base=AlphaBeta4_TPW()):
        super().__init__(depth, base)


class AlphaBeta4Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4_TPWE
    """
    def __init__(self, depth=8, base=AlphaBeta4_TPWE()):
        super().__init__(depth, base)


class NegaScout3Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + NegaScout3_TPW
    """
    def __init__(self, depth=8, base=NegaScout3_TPW()):
        super().__init__(depth, base)


class NegaScout3Ro_TPOW(RandomOpening):
    """
    RandamOpening(8手) + NegaScout3_TPOW
    """
    def __init__(self, depth=8, base=NegaScout3_TPOW()):
        super().__init__(depth, base)


class NegaScout4Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + NegaScout4_TPW
    """
    def __init__(self, depth=8, base=NegaScout4_TPW()):
        super().__init__(depth, base)


class NegaScout4Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + NegaScout4_TPWE
    """
    def __init__(self, depth=8, base=NegaScout4_TPWE()):
        super().__init__(depth, base)


class AB_TI_Ro(RandomOpening):
    """
    RandamOpening(8手) + AB_TI
    """
    def __init__(self, depth=8, base=AB_TI()):
        super().__init__(depth, base)


class AlphaBeta4JRo_TPW(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4J_TPW
    """
    def __init__(self, depth=8, base=AlphaBeta4J_TPW()):
        super().__init__(depth, base)


class AlphaBeta4F9Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4F9_TPW
    """
    def __init__(self, depth=8, base=AlphaBeta4F9_TPW()):
        super().__init__(depth, base)


class AlphaBeta4F9JRo_TPW(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4F9J_TPW
    """
    def __init__(self, depth=8, base=AlphaBeta4F9J_TPW()):
        super().__init__(depth, base)


class AbIF9JRo_B_TPW(RandomOpening):
    """
    RandamOpening(8手) + AbIF9J_B_TPW
    """
    def __init__(self, depth=8, base=AbIF9J_B_TPW()):
        super().__init__(depth, base)


class AbIF9JRo_B_TPWE(RandomOpening):
    """
    RandamOpening(8手) + AbIF9J_B_TPWE
    """
    def __init__(self, depth=8, base=AbIF9J_B_TPWE()):
        super().__init__(depth, base)


class AbIF9JRo_B_TPWEC(RandomOpening):
    """
    RandamOpening(8手) + AbIF9J_B_TPWEC
    """
    def __init__(self, depth=8, base=AbIF9J_B_TPWEC()):
        super().__init__(depth, base)


class NsIF9JRo_B_TPW(RandomOpening):
    """
    RandamOpening(8手) + NsIF9J_B_TPW
    """
    def __init__(self, depth=8, base=NsIF9J_B_TPW()):
        super().__init__(depth, base)


class NsIF9JRo_B_TPW2(RandomOpening):
    """
    RandamOpening(8手) + NsIF9J_B_TPW2
    """
    def __init__(self, depth=8, base=NsIF9J_B_TPW2()):
        super().__init__(depth, base)


class NsIF9JRo_B_TPWE(RandomOpening):
    """
    RandamOpening(8手) + NsIF9J_B_TPWE
    """
    def __init__(self, depth=8, base=NsIF9J_B_TPWE()):
        super().__init__(depth, base)


class SwitchNsIF9JRo_B_TPW(RandomOpening):
    """
    RandamOpening(8手) + SwitchNsIF9J_B_TPW
    """
    def __init__(self, depth=8, base=SwitchNsIF9J_B_TPW()):
        super().__init__(depth, base)


class SwitchNsIF9JRo_B_TPWE(RandomOpening):
    """
    RandamOpening(8手) + SwitchNsIF9J_B_TPWE
    """
    def __init__(self, depth=8, base=SwitchNsIF9J_B_TPWE()):
        super().__init__(depth, base)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    bitboard8 = BitBoard()
    bitboard8.put_disc('black', 3, 2)
    bitboard8.put_disc('white', 2, 4)
    bitboard8.put_disc('black', 5, 5)
    bitboard8.put_disc('white', 4, 2)
    bitboard8.put_disc('black', 5, 2)
    bitboard8.put_disc('white', 5, 4)
    bitboard8.put_disc('black', 4, 5)
    bitboard8.put_disc('white', 5, 6)
    bitboard8.put_disc('black', 4, 6)
    print(bitboard8)

    randomopening = AbIF9JRo_B_TPW()
    move = randomopening.next_move('white', bitboard8)
    print(move)

    bitboard8.put_disc('white', 3, 7)

    move = randomopening.next_move('white', bitboard8)
    print(move)

    bitboard8.put_disc('black', 4, 7)

    move = randomopening.next_move('white', bitboard8)
    print(move)
