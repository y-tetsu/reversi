"""NegaScout
"""

from reversi.strategies.common import Timer, Measure
from reversi.strategies.alphabeta import _AlphaBeta_


class _NegaScout_(_AlphaBeta_):
    """
    NegaScout法で次の手を決める
    """
    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        legal_moves_b_bits = board.get_legal_moves_bits('black')
        legal_moves_w_bits = board.get_legal_moves_bits('white')
        is_game_end = True if not legal_moves_b_bits and not legal_moves_w_bits else False
        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluator.evaluate(color=color, board=board, possibility_b=board.get_bit_count(legal_moves_b_bits), possibility_w=board.get_bit_count(legal_moves_w_bits)) * sign

        # パスの場合
        legal_moves_bits = legal_moves_b_bits if color == 'black' else legal_moves_w_bits
        next_color = 'white' if color == 'black' else 'black'

        if not legal_moves_bits:
            return -self._get_score(next_color, board, -beta, -alpha, depth, pid=pid)

        # NegaScout法
        tmp, null_window, index = None, beta, 0
        size = board.size
        mask = 1 << ((size**2)-1)
        for y in range(size):
            skip = False
            for x in range(size):
                if legal_moves_bits & mask:
                    if alpha < beta:
                        board.put_disc(color, x, y)
                        tmp = -self._get_score(next_color, board, -null_window, -alpha, depth-1, pid=pid)
                        board.undo()

                        if alpha < tmp:
                            if tmp <= null_window and index:
                                board.put_disc(color, x, y)
                                alpha = -self._get_score(next_color, board, -beta, -tmp, depth-1, pid=pid)
                                board.undo()

                                if Timer.is_timeout(pid):
                                    return alpha
                            else:
                                alpha = tmp

                        null_window = alpha + 1
                    else:
                        skip = True
                        break

                    index += 1

                mask >>= 1

            if skip:
                break

        return alpha


class _NegaScout(_NegaScout_):
    """NegaScout + Measure
    """
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)

    @Measure.countup
    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """_get_score
        """
        return super()._get_score(color, board, alpha, beta, depth, pid=pid)


class NegaScout_(_NegaScout_):
    """NegaScout + Timer
    """
    @Timer.start(-10000000)
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)

    @Timer.timeout
    def _get_score(self, color, board, alpha, beta, depth, pid=None):
        """_get_score
        """
        return super()._get_score(color, board, alpha, beta, depth, pid=pid)


class NegaScout(_NegaScout_):
    """NegaScout + Measure + Timer
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
        return super()._get_score(color, board, alpha, beta, depth, pid=pid)
