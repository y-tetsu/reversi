#!/usr/bin/env python
"""Easy Strategy

    This is a example of easy reversi strategy.
"""

import random
from reversi import Reversi, strategies


class Easy(strategies.common.AbstractStrategy):
    """Easy

     This is a easy reversi strategy.
     The specification is as following.
        - Preferentially get corners
        - Avoid near corners
        - Random choice
    """

    def next_move(self, color, board):
        """tuple (x, y): Return next move

        Args:
            color (str) : 'black' or 'white'
            board (obj) : Board(BitBoard) object
        """
        move = None
        legal_moves = list(board.get_legal_moves(color).keys())
        size = board.size

        # Preferentially get corners
        for corner in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]:
            if corner in legal_moves:
                move = corner
                break

        # Aboid near corners
        else:
            next_moves = [i for i in legal_moves]
            near_corners = [
                             (1, 0),         (size-2, 0),
                (0, 1),      (1, 1),         (size-2, 1),      (size-1, 1),

                (0, size-2), (1, size-2),    (size-2, size-2), (size-1, size-2),
                             (1, size-1),    (size-2, size-1),
            ]
            for near_corner in near_corners:
                if near_corner in next_moves:
                    next_moves.remove(near_corner)

            # Random choice
            if next_moves:
                move = random.choice(next_moves)
            else:
                move = random.choice(legal_moves)

        return move


if __name__ == '__main__':
    Reversi(
        {
            'Easy': Easy(),
        }
    ).start()
