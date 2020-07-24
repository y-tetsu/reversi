"""FullReading
"""

from reversi.strategies.common import Measure, AbstractStrategy
from reversi.strategies import _AlphaBeta_N, AlphaBeta_N


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
