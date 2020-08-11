"""MinMax
"""

import random

from reversi.strategies.common import Measure, AbstractStrategy


class _MinMax_(AbstractStrategy):
    """decide next move by MinMax method
    """
    def __init__(self, depth=3, evaluator=None):
        self._MIN = -10000000
        self._MAX = 10000000

        self.depth = depth
        self.evaluator = evaluator

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

    def get_score(self, color, board, depth):
        """get_score
        """
        # game finish or max-depth
        legal_moves_b_bits = board.get_legal_moves_bits('black')
        legal_moves_w_bits = board.get_legal_moves_bits('white')
        is_game_end = True if not legal_moves_b_bits and not legal_moves_w_bits else False
        if is_game_end or depth <= 0:
            return self.evaluator.evaluate(color=color, board=board, possibility_b=board.get_bit_count(legal_moves_b_bits), possibility_w=board.get_bit_count(legal_moves_w_bits))

        # in case of pass
        legal_moves_bits = legal_moves_b_bits if color == 'black' else legal_moves_w_bits
        next_color = 'white' if color == 'black' else 'black'
        if not legal_moves_bits:
            return self.get_score(next_color, board, depth)

        # get best score
        best_score = self._MIN if color == 'black' else self._MAX
        size = board.size
        mask = 1 << ((size**2)-1)
        for y in range(size):
            for x in range(size):
                if legal_moves_bits & mask:
                    board.put_disc(color, x, y)
                    score = self.get_score(next_color, board, depth-1)
                    board.undo()
                    best_score = max(best_score, score) if color == 'black' else min(best_score, score)
                mask >>= 1

        return best_score


class MinMax(_MinMax_):
    """MinMax + Measure
    """
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)

    @Measure.countup
    def get_score(self, color, board, depth):
        """get_score
        """
        return super().get_score(color, board, depth)
