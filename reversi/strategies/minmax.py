"""MinMax
"""

import random

from reversi.strategies.common import Measure, AbstractStrategy


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
