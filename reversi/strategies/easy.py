"""Easy strategy
"""

import random

from reversi.strategies.common import AbstractStrategy


class Random(AbstractStrategy):
    """Random
    """
    def next_move(self, color, board):
        """next_move
        """
        moves = board.get_legal_moves(color, cache=True)

        return random.choice(moves)


class Greedy(AbstractStrategy):
    """Greedy
           Take as many as possible, random if multiple
    """
    def next_move(self, color, board):
        """next_move
        """
        legal_moves = board.get_legal_moves(color, cache=True)
        max_count = max([len(board.get_flippable_discs(color, *move)) for move in legal_moves])
        moves = [move for move in legal_moves if len(board.get_flippable_discs(color, *move)) == max_count]

        return random.choice(moves)


class Unselfish(AbstractStrategy):
    """Unselfish
           Take as little as possible, random if multiple
    """
    def next_move(self, color, board):
        """next_move
        """
        legal_moves = board.get_legal_moves(color, cache=True)
        min_count = min([len(board.get_flippable_discs(color, *move)) for move in legal_moves])
        moves = [move for move in legal_moves if len(board.get_flippable_discs(color, *move)) == min_count]

        return random.choice(moves)


class SlowStarter(AbstractStrategy):
    """SlowStarter
           Unselfish if the stage is less than 15%, Greedy otherwise
    """
    def __init__(self):
        self.unselfish = Unselfish()
        self.greedy = Greedy()

    def next_move(self, color, board):
        """next_move
        """
        squares = board.size**2
        blanks = sum([row.count(0) for row in board.get_board_info()])

        # stage is less than 15%
        if (squares-blanks)/squares < 0.15:
            return self.unselfish.next_move(color, board)

        # otherwise
        return self.greedy.next_move(color, board)
