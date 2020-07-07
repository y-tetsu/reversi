#!/usr/bin/env python
"""
ネガスカウト法
"""

import sys
sys.path.append('../')

from reversi.strategies.common import Timer, Measure, CPU_TIME
from reversi.strategies.alphabeta import _AlphaBeta
from reversi.strategies.coordinator import Evaluator_TPW, Evaluator_TPWE, Evaluator_TPOW


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
        is_game_end =  True if not legal_moves_b and not legal_moves_w else False

        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluator.evaluate(color=color, board=board, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w) * sign

        # パスの場合
        legal_moves = legal_moves_b if color == 'black' else legal_moves_w
        next_color = 'white' if color == 'black' else 'black'

        if not legal_moves:
            return -self._get_score(next_color, board, -beta, -alpha, depth)

        # 手の候補
        moves = list(board.get_legal_moves(color, cache=True).keys())

        # NegaScout法
        tmp, null_window = None, beta
        for i, move in enumerate(moves):
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


class NegaScout_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPW()):
        super().__init__(evaluator=evaluator)


class NegaScout_TPW2(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPW(corner=50, c=-20, a1=0, a2=22, b1=-1, b2=-1, b3=-1, x=-35, o1=-5, o2=-5, wp=5, ww=10000)):
        super().__init__(evaluator=evaluator)


class NegaScout_TPWE(NegaScout):
    """
    NegaScout法でEvaluator_TPWEにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPWE()):
        super().__init__(evaluator=evaluator)


class NegaScout3_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout3_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaScout4_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout4_TPWE(NegaScout):
    """
    NegaScout法でEvaluator_TPWEにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class NegaScout4_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)
