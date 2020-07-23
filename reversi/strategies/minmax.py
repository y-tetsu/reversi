"""MinMax
"""

import random

from reversi.strategies.common import Measure, AbstractStrategy
from reversi.strategies.coordinator import Evaluator_T, Evaluator_TP, Evaluator_TPO, Evaluator_TPW, Evaluator_TPWE, Evaluator_TPWEC, Evaluator_TPOW, Evaluator_PWE  # noqa: E501


class MinMax(AbstractStrategy):
    """decide next move by MinMax method
    """
    def __init__(self, depth=3, evaluator=None):
        self._MIN = -10000000
        self._MAX = 10000000

        self.depth = depth
        self.evaluator = evaluator

    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        # select best move
        next_color = 'white' if color == 'black' else 'black'
        next_moves = {}
        best_score = self._MIN if color == 'black' else self._MAX
        legal_moves = board.get_legal_moves(color)
        for move in legal_moves:
            board.put_disc(color, *move)
            score = self.get_score(next_color, board, self.depth-1)
            board.undo()
            best_score = max(best_score, score) if color == 'black' else min(best_score, score)

            # memorize next moves
            if score not in next_moves:
                next_moves[score] = []
            next_moves[score].append(move)

        return random.choice(next_moves[best_score])  # random choice if many best scores

    @Measure.countup
    def get_score(self, color, board, depth):
        """get_score
        """
        # game finish or max-depth
        legal_moves_b = board.get_legal_moves('black')
        legal_moves_w = board.get_legal_moves('white')
        is_game_end = True if not legal_moves_b and not legal_moves_w else False
        if is_game_end or depth <= 0:
            return self.evaluator.evaluate(color=color, board=board, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)

        # in case of pass
        legal_moves = legal_moves_b if color == 'black' else legal_moves_w
        next_color = 'white' if color == 'black' else 'black'
        if not legal_moves:
            return self.get_score(next_color, board, depth)

        # get best score
        best_score = self._MIN if color == 'black' else self._MAX
        for move in legal_moves:
            board.put_disc(color, *move)
            score = self.get_score(next_color, board, depth-1)
            board.undo()
            best_score = max(best_score, score) if color == 'black' else min(best_score, score)

        return best_score


class MinMax1_T(MinMax):
    """
    MinMax法でEvaluator_Tにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax2_T(MinMax):
    """
    MinMax法でEvaluator_Tにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax3_T(MinMax):
    """
    MinMax法でEvaluator_Tにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax4_T(MinMax):
    """
    MinMax法でEvaluator_Tにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax1_TP(MinMax):
    """
    MinMax法でEvaluator_TPにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TP()):
        super().__init__(depth, evaluator)


class MinMax2_TP(MinMax):
    """
    MinMax法でEvaluator_TPにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TP()):
        super().__init__(depth, evaluator)


class MinMax3_TP(MinMax):
    """
    MinMax法でEvaluator_TPにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TP()):
        super().__init__(depth, evaluator)


class MinMax4_TP(MinMax):
    """
    MinMax法でEvaluator_TPにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TP()):
        super().__init__(depth, evaluator)


class MinMax1_TPO(MinMax):
    """
    MinMax法でEvaluator_TPOにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPO()):
        super().__init__(depth, evaluator)


class MinMax2_TPO(MinMax):
    """
    MinMax法でEvaluator_TPOにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPO()):
        super().__init__(depth, evaluator)


class MinMax3_TPO(MinMax):
    """
    MinMax法でEvaluator_TPOにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPO()):
        super().__init__(depth, evaluator)


class MinMax4_TPO(MinMax):
    """
    MinMax法でEvaluator_TPOにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPO()):
        super().__init__(depth, evaluator)


class MinMax1_TPW(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class MinMax1_TPW2(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPW(corner=50, c=-20, a1=0, a2=22, b1=-1, b2=-1, b3=-1, x=-35, o1=-5, o2=-5, wp=5, ww=10000)):
        super().__init__(depth, evaluator)


class MinMax1_PWE(MinMax):
    """
    MinMax法でEvaluator_PWEにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_PWE()):
        super().__init__(depth, evaluator)


class MinMax1_TPWE(MinMax):
    """
    MinMax法でEvaluator_TPWEにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class MinMax1_TPWEC(MinMax):
    """
    MinMax法でEvaluator_TPWECにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPWEC()):
        super().__init__(depth, evaluator)


class MinMax2_TPW(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class MinMax2_TPWE(MinMax):
    """
    MinMax法でEvaluator_TPWEにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class MinMax2_TPWEC(MinMax):
    """
    MinMax法でEvaluator_TPWECにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPWEC()):
        super().__init__(depth, evaluator)


class MinMax3_TPW(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class MinMax4_TPW(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class MinMax1_TPOW(MinMax):
    """
    MinMax法でEvaluator_TPOWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class MinMax2_TPOW(MinMax):
    """
    MinMax法でEvaluator_TPOWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class MinMax3_TPOW(MinMax):
    """
    MinMax法でEvaluator_TPOWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class MinMax4_TPOW(MinMax):
    """
    MinMax法でEvaluator_TPOWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)
