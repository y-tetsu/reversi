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
    def select_moves(self, color, board, best_move, scores, depth):
        """
        手の候補を決める
        """
        return list(board.get_possibles(color).keys())


class Selector_B(Selector):
    """
    前回の最善手を最初に調べる
    """
    def select_moves(self, color, board, best_move, scores, depth):
        """
        手の候補を決める
        """
        moves = super().select_moves(color, board, best_move, scores, depth)

        if best_move is not None:
            moves.remove(best_move)
            moves.insert(0, best_move)

        return moves


if __name__ == '__main__':
    from board import BitBoard

    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)
    print(bitboard8)

    print('--- Test For Selector ---')
    selector = Selector()

    moves = selector.select_moves('white', bitboard8, None, None, None)
    print(moves)
    assert moves == [(2, 2), (4, 2), (2, 4)]

    print('--- Test For Selector_B ---')
    selector = Selector_B()

    moves = selector.select_moves('white', bitboard8, (4, 2), None, None)
    print(moves)
    assert moves == [(4, 2), (2, 2), (2, 4)]
