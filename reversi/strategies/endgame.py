"""EndGame
"""

import sys

from reversi.strategies.common import Timer, Measure, AbstractStrategy
from reversi.strategies.coordinator import Evaluator_N_Fast
from reversi.strategies.alphabeta import _AlphaBeta_, _AlphaBeta, AlphaBeta_, AlphaBeta
import reversi.strategies.EndGameMethods as EndGameMethods


MAXSIZE64 = 2**63 - 1


class _EndGame_(AbstractStrategy):
    """
    石差読みで次の手を決める
    """
    def __init__(self, depth=10):
        self._MIN = -10000000
        self._MAX = 10000000
        self.evaluator = Evaluator_N_Fast()
        self.depth = depth
        self.alphabeta_n = _AlphaBeta_(depth=depth, evaluator=self.evaluator)
        self.timer = False
        self.measure = False

    def next_move(self, color, board):
        """
        次の一手
        """
        pid = Timer.get_pid(self)  # タイムアウト監視用のプロセスID
        if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard') and not EndGameMethods.ENDGAME_SIZE8_64BIT_ERROR:
            return EndGameMethods.next_move(color, board, self._MIN, self._MAX, self.depth, self.evaluator, pid, self.timer, self.measure)
        return self.alphabeta_n.next_move(color, board)


class _EndGame(_EndGame_):
    """EndGame + Measure
    """
    def __init__(self, depth=10):
        super().__init__(depth)
        self.alphabeta_n = _AlphaBeta(depth=depth, evaluator=self.evaluator)
        self.timer = False
        self.measure = True

    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)


class EndGame_(_EndGame_):
    """EndGame + Timer
    """
    def __init__(self, depth=10):
        super().__init__(depth)
        self.alphabeta_n = AlphaBeta_(depth=depth, evaluator=self.evaluator)
        self.timer = True
        self.measure = False

    @Timer.start(-10000000)
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)


class EndGame(_EndGame_):
    """EndGame + Measure + Timer
    """
    def __init__(self, depth=10):
        super().__init__(depth)
        self.alphabeta_n = AlphaBeta(depth=depth, evaluator=self.evaluator)
        self.timer = True
        self.measure = True

    @Timer.start(-10000000)
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)
