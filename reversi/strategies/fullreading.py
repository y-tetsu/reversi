"""FullReading
"""

from reversi.strategies.common import Measure, AbstractStrategy
from reversi.strategies import _AlphaBetaN_, _AlphaBetaN, AlphaBetaN_, AlphaBetaN, AlphaBetaN_old


class _FullReading_(AbstractStrategy):
    """終盤完全読み
    """
    def __init__(self, remain=None, base=None):
        self.remain = remain
        self.fullreading = _AlphaBetaN_(depth=remain)
        self.base = base

    def next_move(self, color, board):
        """次の一手
        """
        remain = (board.size * board.size) - (board._black_score + board._white_score)

        # 残り手数が閾値以下
        if remain <= self.remain:
            return self.fullreading.next_move(color, board)  # 完全読み

        return self.base.next_move(color, board)


class _FullReading(_FullReading_):
    """終盤完全読み + Measure
    """
    def __init__(self, remain=None, base=None):
        self.remain = remain
        self.fullreading = _AlphaBetaN(depth=remain)
        self.base = base

    @Measure.time
    def next_move(self, color, board):
        """次の一手
        """
        return super().next_move(color, board)


class FullReading_(_FullReading_):
    """終盤完全読み + Timer
    """
    def __init__(self, remain=None, base=None):
        self.remain = remain
        self.fullreading = AlphaBetaN_(depth=remain)
        self.base = base


class FullReading(_FullReading_):
    """終盤完全読み + Measure + Timer
    """
    def __init__(self, remain=None, base=None):
        self.remain = remain
        self.fullreading = AlphaBetaN(depth=remain)
        self.base = base

    @Measure.time
    def next_move(self, color, board):
        """次の一手
        """
        return super().next_move(color, board)


class FullReading_old(_FullReading_):
    """終盤完全読み + Measure + Timer
    """
    def __init__(self, remain=None, base=None):
        self.remain = remain
        self.fullreading = AlphaBetaN_old(depth=remain)
        self.base = base

    @Measure.time
    def next_move(self, color, board):
        """次の一手
        """
        return super().next_move(color, board)
