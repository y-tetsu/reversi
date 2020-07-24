"""AlphaBeta(NegaAlpha)
"""

from reversi.strategies.common import Timer, Measure, CPU_TIME, AbstractStrategy
from reversi.strategies.coordinator import Evaluator_N


class _AlphaBeta(AbstractStrategy):
    """
    AlphaBeta法で次の手を決める
    """
    def __init__(self, depth=3, evaluator=None):
        self._MIN = -10000000
        self._MAX = 10000000

        self.depth = depth
        self.evaluator = evaluator

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = board.get_legal_moves(color)  # 手の候補
        best_move, _ = self.get_best_move(color, board, moves, self.depth)

        return best_move

    def get_best_move(self, color, board, moves, depth):
        """
        最善手を選ぶ
        """
        best_move, alpha, beta, scores = None, self._MIN, self._MAX, {}

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in moves:
            score = self.get_score(move, color, board, alpha, beta, depth)
            scores[move] = score

            if Timer.is_timeout(self):
                best_move = move if best_move is None else best_move
                break
            else:
                if score > alpha:  # 最善手を更新
                    alpha = score
                    best_move = move

        return best_move, scores

    def get_score(self, move, color, board, alpha, beta, depth):
        """
        手を打った時の評価値を取得
        """
        board.put_disc(color, *move)                                         # 一手打つ
        next_color = 'white' if color == 'black' else 'black'                # 相手の色
        score = -self._get_score(next_color, board, -beta, -alpha, depth-1)  # 評価値を取得
        board.undo()                                                         # 打った手を戻す

        return score

    @Measure.countup
    def _get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        legal_moves_b = board.get_legal_moves('black')
        legal_moves_w = board.get_legal_moves('white')
        is_game_end = True if not legal_moves_b and not legal_moves_w else False

        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluator.evaluate(color=color, board=board, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w) * sign

        # パスの場合
        legal_moves = legal_moves_b if color == 'black' else legal_moves_w
        next_color = 'white' if color == 'black' else 'black'

        if not legal_moves:
            return -self._get_score(next_color, board, -beta, -alpha, depth)

        # 評価値を算出
        for move in legal_moves:
            board.put_disc(color, *move)
            score = -self._get_score(next_color, board, -beta, -alpha, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break

            alpha = max(alpha, score)  # 最大値を選択
            if alpha >= beta:  # 枝刈り
                break

        return alpha


class AlphaBeta(_AlphaBeta):
    """
    AlphaBeta法で次の手を決める(時間制限付き)
    """
    @Timer.start(CPU_TIME, -10000000)
    def next_move(self, color, board):
        """
        次の一手
        """
        return super().next_move(color, board)

    @Timer.timeout
    def _get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        return super()._get_score(color, board, alpha, beta, depth)


class _AlphaBeta_N(_AlphaBeta):
    """
    AlphaBeta法でEvaluator_Nにより次の手を決める
    """
    def __init__(self, depth, evaluator=Evaluator_N()):
        super().__init__(depth=depth, evaluator=evaluator)


class AlphaBeta_N(AlphaBeta):
    """
    AlphaBeta法でEvaluator_Nにより次の手を決める
    """
    def __init__(self, depth, evaluator=Evaluator_N()):
        super().__init__(depth=depth, evaluator=evaluator)
