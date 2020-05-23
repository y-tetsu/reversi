#!/usr/bin/env python
"""
Strategy Customization
  1. original strategy
  2. external strategy
"""

from reversi import Reversi, strategies


class Original(strategies.common.AbstractStrategy):
    """
    Original strategy
    """
    def next_move(self, color, board):
        """
        next move
        """
        move = None
        legal_moves = list(board.get_legal_moves(color).keys())

        #-------------------------
        # 1. Please customize here for original strategy
        #  1.1 Check your color and board.
        #  1.2 Decide your next move and set result.
        # ↓↓↓↓↓
        move = legal_moves[0]
        # ↑↑↑↑↑
        #-------------------------

        return move


if __name__ == '__main__':
    s = {
        'Original': Original(),
        #-------------------------
        # 2. Please customize here for external strategy
        #     strategies.External('execute command', timeouttime)
        # ↓↓↓↓↓
        'External': strategies.External('py -3.7 ./extra/python/topleft/topleft.py', 60),
        # ↑↑↑↑↑
        #-------------------------
    }
    Reversi(s).start()
