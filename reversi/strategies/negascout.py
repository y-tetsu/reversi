"""NegaScout
"""

from reversi.strategies.common import Timer, Measure, CPU_TIME
from reversi.strategies.alphabeta import _AlphaBeta


class _NegaScout(_AlphaBeta):
    """
    NegaScout法で次の手を決める
    """
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

        # NegaScout法
        tmp, null_window = None, beta
        for i, move in enumerate(legal_moves):
            if alpha < beta:
                board.put_disc(color, *move)
                tmp = -self._get_score(next_color, board, -null_window, -alpha, depth-1)
                board.undo()

                if alpha < tmp:
                    if tmp <= null_window and i:
                        board.put_disc(color, *move)
                        alpha = -self._get_score(next_color, board, -beta, -tmp, depth-1)
                        board.undo()

                        if Timer.is_timeout(self):
                            return alpha
                    else:
                        alpha = tmp

                null_window = alpha + 1
            else:
                break

        return alpha


class NegaScout(_NegaScout):
    """
    NegaScout法で次の手を決める(時間制限付き)
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
