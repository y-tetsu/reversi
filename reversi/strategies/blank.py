"""Blank
"""

import sys

from reversi.strategies.common import Timer, Measure, AbstractStrategy
from reversi.strategies.coordinator import Evaluator_TPWEB
from reversi.strategies.negascout import _NegaScout_, _NegaScout, NegaScout_, NegaScout
import reversi.strategies.BlankMethods as BlankMethods


MAXSIZE64 = 2**63 - 1


class _Blank_(AbstractStrategy):
    """
    空きマスの状態を形勢判断に加えて次の手を決める
    """
    def __init__(self, depth=4, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000, we=100, wb1=-5, wb2=-20, wb3=-10):
        self._MIN = -10000000
        self._MAX = 10000000
        self.params = [corner, c, a1, a2, b1, b2, b3, x, o1, o2, wp, ww, we, wb1, wb2, wb3]
        self.evaluator = Evaluator_TPWEB(corner=corner, c=c, a1=a1, a2=a2, b1=b1, b2=b2, b3=b3, x=x, o1=o1, o2=o2, wp=wp, ww=ww, we=we, wb1=wb1, wb2=wb2, wb3=wb3)  # noqa: E501
        self.depth = depth
        self.negascout_tpweb = _NegaScout_(depth=depth, evaluator=self.evaluator)
        self.timer = False
        self.measure = False

    def next_move(self, color, board):
        """
        次の一手
        """
        pid = Timer.get_pid(self)  # タイムアウト監視用のプロセスID
        if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard') and not BlankMethods.BLANK_SIZE8_64BIT_ERROR:
            return BlankMethods.next_move(color, board, self.params, self.depth, pid, self.timer, self.measure)
        return self.negascout_tpweb.next_move(color, board)

    def get_best_move(self, color, board, moves, depth=4, pid=None):
        """
        最善手を選ぶ
        """
        best_move, alpha, beta, scores = None, self._MIN, self._MAX, {}
        if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard') and not BlankMethods.BLANK_SIZE8_64BIT_ERROR:
            return BlankMethods.get_best_move(color, board, self.params, moves, alpha, beta, depth, pid, self.timer, self.measure)
        return self.negascout_tpweb.get_best_move(color, board, moves, depth, pid)


class _Blank(_Blank_):
    """Blank + Measure
    """
    def __init__(self, depth=4, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000, we=100, wb1=-5, wb2=-20, wb3=-10):
        super().__init__(depth, corner, c, a1, a2, b1, b2, b3, x, o1, o2, wp, ww, we, wb1, wb2, wb3)
        self.negascout_tpweb = _NegaScout(depth=depth, evaluator=self.evaluator)
        self.timer = False
        self.measure = True

    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)


class Blank_(_Blank_):
    """Blank + Timer
    """
    def __init__(self, depth=4, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000, we=100, wb1=-5, wb2=-20, wb3=-10):
        super().__init__(depth, corner, c, a1, a2, b1, b2, b3, x, o1, o2, wp, ww, we, wb1, wb2, wb3)
        self.negascout_tpweb = NegaScout_(depth=depth, evaluator=self.evaluator)
        self.timer = True
        self.measure = False

    @Timer.start(-10000000)
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)


class Blank(_Blank_):
    """Blank + Measure + Timer
    """
    def __init__(self, depth=4, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000, we=100, wb1=-5, wb2=-20, wb3=-10):
        super().__init__(depth, corner, c, a1, a2, b1, b2, b3, x, o1, o2, wp, ww, we, wb1, wb2, wb3)
        self.negascout_tpweb = NegaScout(depth=depth, evaluator=self.evaluator)
        self.timer = True
        self.measure = True

    @Timer.start(-10000000)
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)
