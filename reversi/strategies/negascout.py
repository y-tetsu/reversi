"""NegaScout
"""

from reversi.strategies.common import Timer, Measure
from reversi.strategies.alphabeta import _AlphaBeta_
import reversi.strategies.NegaScoutMethods as NegaScoutMethods


class _NegaScout_(_AlphaBeta_):
    """
    NegaScout法で次の手を決める
    """
    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """
        評価値の取得
        """
        return NegaScoutMethods.get_score(self, color, board, alpha, beta, depth, pid)


class _NegaScout(_NegaScout_):
    """NegaScout + Measure
    """
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)

    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """_get_score
        """
        return NegaScoutMethods.get_score_measure(self, color, board, alpha, beta, depth, pid)


class NegaScout_(_NegaScout_):
    """NegaScout + Timer
    """
    @Timer.start(-10000000)
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)

    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """_get_score
        """
        return NegaScoutMethods.get_score_timer(self, color, board, alpha, beta, depth, pid)


class NegaScout(_NegaScout_):
    """NegaScout + Measure + Timer
    """
    @Timer.start(-10000000)
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)

    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """_get_score
        """
        return NegaScoutMethods.get_score_measure_timer(self, color, board, alpha, beta, depth, pid)
