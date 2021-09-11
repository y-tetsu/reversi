"""NegaScout
"""

import sys

from reversi.strategies.common import Timer, Measure, AbstractStrategy
import reversi.strategies.NegaScoutMethods as NegaScoutMethods


MAXSIZE64 = 2**63 - 1


class _NegaScout_(AbstractStrategy):
    """
    NegaScout法で次の手を決める
    """
    def __init__(self, depth=3, evaluator=None):
        self._MIN = -10000000
        self._MAX = 10000000

        self.depth = depth
        self.evaluator = evaluator
        self.timer = False
        self.measure = False

    def next_move(self, color, board):
        """
        次の一手
        """
        pid = Timer.get_pid(self)  # タイムアウト監視用のプロセスID

        if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard') and not NegaScoutMethods.NEGASCOUT_SIZE8_64BIT_ERROR:
            return NegaScoutMethods.next_move(color, board, self._MIN, self._MAX, self.depth, self.evaluator, pid, self.timer, self.measure)

        moves = board.get_legal_moves(color)  # 手の候補
        best_move, _ = self.get_best_move(color, board, moves, self.depth, pid)

        return best_move

    def get_best_move(self, color, board, moves, depth, pid=None):
        """
        最善手を選ぶ
        """
        best_move, alpha, beta, scores = None, self._MIN, self._MAX, {}

        if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard') and not NegaScoutMethods.NEGASCOUT_SIZE8_64BIT_ERROR:
            return NegaScoutMethods.get_best_move(color, board, moves, alpha, beta, depth, self.evaluator, pid, self.timer, self.measure)

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in moves:
            score = self.get_score(move, color, board, alpha, beta, depth, pid)
            scores[move] = score
            if Timer.is_timeout(pid):
                best_move = move if best_move is None else best_move
                break
            else:
                if score > alpha:  # 最善手を更新
                    alpha = score
                    best_move = move

        return best_move, scores

    def get_score(self, move, color, board, alpha, beta, depth, pid=None):
        """
        手を打った時の評価値を取得
        """
        board.put_disc(color, *move)                                                  # 一手打つ
        next_color = 'white' if color == 'black' else 'black'                         # 相手の色
        score = -self._get_score(next_color, board, -beta, -alpha, depth-1, pid=pid)  # 評価値を取得
        board.undo()                                                                  # 打った手を戻す

        return score

    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """
        評価値の取得
        """
        return NegaScoutMethods.get_score(self, color, board, alpha, beta, depth, pid)


class _NegaScout(_NegaScout_):
    """NegaScout + Measure
    """
    def __init__(self, depth=3, evaluator=None):
        super().__init__(depth, evaluator)
        self.timer = False
        self.measure = True

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
    def __init__(self, depth=3, evaluator=None):
        super().__init__(depth, evaluator)
        self.timer = True
        self.measure = False

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
    def __init__(self, depth=3, evaluator=None):
        super().__init__(depth, evaluator)
        self.timer = True
        self.measure = True

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
