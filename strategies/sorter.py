#!/usr/bin/env python
"""
手の候補を並び替え
"""

import sys
sys.path.append('../')

from strategies.common import AbstractSorter


class Sorter(AbstractSorter):
    """
    なにもしない
    """
    def sort_moves(self, board, moves, best_move):
        """
        手の候補を決める
        """
        return moves


class Sorter_B(Sorter):
    """
    前回の最善手を優先的に
    """
    def sort_moves(self, board, moves, best_move):
        """
        手の候補を決める
        """
        if best_move is not None:
            moves.remove(best_move)
            moves.insert(0, best_move)

        return moves


class Sorter_BC(Sorter_B):
    """
    4隅を優先的に
    """
    def sort_moves(self, board, moves, best_move):
        """
        手の候補を決める
        """
        moves = super().sort_moves(board, moves, best_move)

        board_size = board.size
        corners = [(0, 0), (0, board_size-1), (board_size-1, 0), (board_size-1, board_size-1)]

        for corner in corners:
            if corner in moves:
                moves.remove(corner)
                moves.insert(0, corner)

        return moves


if __name__ == '__main__':
    from board import BitBoard
    from strategies.timer import Timer
    from strategies.alphabeta import AlphaBeta_TPOW

    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)
    print(bitboard8)

    moves = list(bitboard8.get_possibles('white').keys())
    best_move = (4, 2)

    print('--- Test For Sorter ---')
    sorter = Sorter()

    moves = sorter.sort_moves(bitboard8, moves, best_move)
    print(moves)
    assert moves == [(2, 2), (4, 2), (2, 4)]

    print('--- Test For Sorter_B ---')
    sorter = Sorter_B()

    moves = sorter.sort_moves(bitboard8, moves, best_move)
    print(moves)
    assert moves == [(4, 2), (2, 2), (2, 4)]

    print('--- Test For Sorter_BC ---')
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 1, 5)
    bitboard8.put_stone('white', 1, 4)
    bitboard8.put_stone('black', 2, 5)
    bitboard8.put_stone('white', 2, 6)
    bitboard8.put_stone('black', 1, 6)
    bitboard8.put_stone('white', 1, 7)
    print(bitboard8)

    sorter = Sorter_BC()

    moves = list(bitboard8.get_possibles('black').keys())
    best_move = (2, 3)
    print(moves)
    moves = sorter.sort_moves(bitboard8, moves, best_move)
    print(moves)
    assert moves == [(0, 7), (2, 3), (0, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)]
