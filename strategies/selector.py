#!/usr/bin/env python
"""
選択的探索
"""

import sys
sys.path.append('../')

from strategies.common import AbstractSelector


class Selector(AbstractSelector):
    """
    ボードの打てる場所を返す
    """
    def select_moves(self, color, board, best_move, scores):
        """
        手の候補を決める
        """
        return list(board.get_possibles(color).keys())


if __name__ == '__main__':
    from board import BitBoard

    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)
    print(bitboard8)

    print('--- Test For Selector ---')
    selector = Selector()

    moves = selector.select_moves('white', bitboard8, None, None)
    print(moves)
    assert moves == [(2, 2), (4, 2), (2, 4)]
