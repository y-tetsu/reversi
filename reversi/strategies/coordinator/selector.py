#!/usr/bin/env python
"""
選択的探索
"""

import sys
sys.path.append('../../')

from strategies.common import AbstractSelector


class Selector(AbstractSelector):
    """
    ボードの打てる場所を返す
    """
    def select_moves(self, color, board, moves, scores, depth):
        """
        手の候補を決める
        """
        if moves is None:
            return list(board.get_legal_moves(color).keys())

        return moves


class Selector_W(Selector):
    """
    ワースト値に基づいて手を絞る
    """
    def __init__(self, depth=3, limit=3):
        self.depth = depth
        self.limit = limit

    def select_moves(self, color, board, moves, scores, depth):
        """
        手の候補を決める
        """
        moves = super().select_moves(color, board, moves, scores, depth)

        if depth >= self.depth:  # 一定以上の深さの場合
            worst_score = min([score for score in scores.values()])
            worst_moves = [key for key in scores.keys() if scores[key] == worst_score]

            # 次の手の候補数がリミット以上の間は絞る
            if len(moves) - len(worst_moves) >= self.limit:
                for worst_move in worst_moves:
                    moves.remove(worst_move)  # 最もスコアの低い手を削除

        return moves


if __name__ == '__main__':
    import os
    import time

    from board import BitBoard
    from strategies.common import Timer
    from strategies.alphabeta import AlphaBeta_TPW

    bitboard8 = BitBoard(8)
    bitboard8.put_disc('black', 3, 2)
    print(bitboard8)

    print('--- Test For Selector ---')
    selector = Selector()

    moves = selector.select_moves('white', bitboard8, None, None, None)
    print(moves)
    assert moves == [(2, 2), (4, 2), (2, 4)]

    bitboard8.put_disc('white', 2, 4)
    bitboard8.put_disc('black', 1, 5)
    bitboard8.put_disc('white', 1, 4)
    bitboard8.put_disc('black', 2, 5)
    bitboard8.put_disc('white', 2, 6)
    bitboard8.put_disc('black', 1, 6)
    bitboard8.put_disc('white', 1, 7)
    print(bitboard8)

    print('--- Test For Selector_W ---')
    print(bitboard8)

    strategy = AlphaBeta_TPW()
    selector = Selector_W()

    assert selector.depth == 3
    assert selector.limit == 3

    moves = bitboard8.get_legal_moves('black')

    print(strategy.__class__.__name__)
    Timer.set_deadline(strategy.__class__.__name__, -1000000)
    best_move, scores = strategy.get_best_move('black', bitboard8, moves, 4)

    moves = selector.select_moves('black', bitboard8, None, scores, 2)
    print(moves)
    assert moves == [(0, 3), (2, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (0, 7), (2, 7)]
    moves = selector.select_moves('black', bitboard8, None, scores, 5)
    print(moves)
    print(scores)
    assert moves == [(2, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (0, 7), (2, 7)]
