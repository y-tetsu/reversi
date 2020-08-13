"""AlphaBeta(NegaAlpha)
"""

from reversi.strategies.common import Timer, Measure, AbstractStrategy
from reversi.strategies.coordinator import Evaluator_N
import reversi.strategies.AlphaBetaMethods as AlphaBetaMethods


class _AlphaBeta_(AbstractStrategy):
    """
    AlphaBeta法で次の手を決める
    """
    def __init__(self, depth=3, evaluator=None):
        self._MIN = -10000000
        self._MAX = 10000000

        self.depth = depth
        self.evaluator = evaluator

    def next_move(self, color, board):
        """
        次の一手
        """
        pid = Timer.get_pid(self)             # タイムアウト監視用のプロセスID
        moves = board.get_legal_moves(color)  # 手の候補
        best_move, _ = self.get_best_move(color, board, moves, self.depth, pid)

        return best_move

    def get_best_move(self, color, board, moves, depth, pid=None):
        """
        最善手を選ぶ
        """
        best_move, alpha, beta, scores = None, self._MIN, self._MAX, {}

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
        return AlphaBetaMethods.get_score(self, color, board, alpha, beta, depth, pid)


class _AlphaBeta(_AlphaBeta_):
    """AlphaBeta + Measure
    """
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)

    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """_get_score
        """
        return AlphaBetaMethods.get_score_measure(self, color, board, alpha, beta, depth, pid)


class AlphaBeta_(_AlphaBeta_):
    """AlphaBeta + Timer
    """
    @Timer.start(-10000000)
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)

    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """_get_score
        """
        return AlphaBetaMethods.get_score_timer(self, color, board, alpha, beta, depth, pid)


class AlphaBeta(_AlphaBeta_):
    """AlphaBeta + Measure + Timer
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
        return AlphaBetaMethods.get_score_measure_timer(self, color, board, alpha, beta, depth, pid)


class AlphaBeta_old(_AlphaBeta_):
    """AlphaBeta_old + Measure + Timer
    """
    @Timer.start(-10000000)
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)

    @Timer.timeout
    @Measure.countup
    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """_get_score
        """
        # ゲーム終了 or 最大深さに到達
        legal_moves_b_bits = board.get_legal_moves_bits('black')
        legal_moves_w_bits = board.get_legal_moves_bits('white')
        is_game_end = True if not legal_moves_b_bits and not legal_moves_w_bits else False
        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluator.evaluate(color=color, board=board, possibility_b=board.get_bit_count(legal_moves_b_bits), possibility_w=board.get_bit_count(legal_moves_w_bits)) * sign  # noqa: E501

        # パスの場合
        legal_moves_bits = legal_moves_b_bits if color == 'black' else legal_moves_w_bits
        next_color = 'white' if color == 'black' else 'black'
        if not legal_moves_bits:
            return -self._get_score(next_color, board, -beta, -alpha, depth, pid=pid)

        # 評価値を算出
        size = board.size
        mask = 1 << ((size**2)-1)
        for y in range(size):
            for x in range(size):
                if legal_moves_bits & mask:
                    board.put_disc(color, x, y)
                    score = -self._get_score(next_color, board, -beta, -alpha, depth-1, pid=pid)
                    board.undo()

                    if Timer.is_timeout(pid):
                        return alpha

                    alpha = max(alpha, score)  # 最大値を選択
                    if alpha >= beta:  # 枝刈り
                        return alpha

                mask >>= 1

        return alpha


class _AlphaBetaN_(_AlphaBeta_):
    """
    AlphaBeta法でEvaluator_Nにより次の手を決める
    """
    def __init__(self, depth, evaluator=Evaluator_N()):
        super().__init__(depth=depth, evaluator=evaluator)


class _AlphaBetaN(_AlphaBeta):
    """
    AlphaBeta法でEvaluator_Nにより次の手を決める
    """
    def __init__(self, depth, evaluator=Evaluator_N()):
        super().__init__(depth=depth, evaluator=evaluator)


class AlphaBetaN_(AlphaBeta_):
    """
    AlphaBeta法でEvaluator_Nにより次の手を決める
    """
    def __init__(self, depth, evaluator=Evaluator_N()):
        super().__init__(depth=depth, evaluator=evaluator)


class AlphaBetaN(AlphaBeta):
    """
    AlphaBeta法でEvaluator_Nにより次の手を決める
    """
    def __init__(self, depth, evaluator=Evaluator_N()):
        super().__init__(depth=depth, evaluator=evaluator)


class AlphaBetaN_old(AlphaBeta_old):
    """
    AlphaBeta_old法でEvaluator_Nにより次の手を決める
    """
    def __init__(self, depth, evaluator=Evaluator_N()):
        super().__init__(depth=depth, evaluator=evaluator)
