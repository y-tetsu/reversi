#!/usr/bin/env python
"""
手の候補を並び替え
"""

import sys
sys.path.append('../../')

from strategies.common import AbstractSorter


class Sorter(AbstractSorter):
    """
    なにもしない
    """
    def sort_moves(self, *args, **kwargs):
        """
        手の候補を決める
        """
        color, board, moves = kwargs['color'], kwargs['board'], kwargs['moves']

        if moves is None:
            return list(board.get_possibles(color).keys())

        return moves


class Sorter_B(Sorter):
    """
    前回の最善手を優先的に
    """
    def sort_moves(self, *args, **kwargs):
        """
        手の候補を決める
        """
        moves = super().sort_moves(*args, **kwargs)

        best_move = kwargs['best_move']

        if best_move is not None:
            moves.remove(best_move)
            moves.insert(0, best_move)

        return moves


class Sorter_C(Sorter):
    """
    4隅を優先的に
    """
    def sort_moves(self, *args, **kwargs):
        """
        手の候補を決める
        """
        moves = super().sort_moves(*args, **kwargs)

        board = kwargs['board']
        board_size = board.size
        corners = [(0, 0), (0, board_size-1), (board_size-1, 0), (board_size-1, board_size-1)]

        for corner in corners:
            if corner in moves:
                moves.remove(corner)
                moves.insert(0, corner)

        return moves


class Sorter_O(Sorter):
    """
    開放度による並び替え
    """
    def sort_moves(self, *args, **kwargs):
        """
        手の候補を決める
        """
        moves = super().sort_moves(*args, **kwargs)

        color, board = kwargs['color'], kwargs['board']
        openings = {}

        for move in moves:
            reversibles = board.put_disc(color, *move)
            opening = self.get_opening(board, reversibles)
            openings[move] = opening
            board.undo()

        return [key for key, _ in sorted(openings.items(), key=lambda x:x[1])]

    def get_opening(self, board, reversibles):
        """
        開放度を求める
        """
        size, board_info, opening = board.size, board.get_board_info(), 0

        directions = [
            [-1,  1], [ 0,  1], [ 1,  1],
            [-1,  0],           [ 1,  0],
            [-1, -1], [ 0, -1], [ 1, -1],
        ]

        # ひっくり返した石の周りをチェックする
        for disc_x, disc_y in reversibles:
            for dx, dy in directions:
                x, y = disc_x + dx, disc_y + dy

                if 0 <= x < size and 0 <= y < size:
                    if board_info[y][x] == 0:
                        opening += 1  # 石が置かれていない場所をカウント

        return opening


class Sorter_BC(AbstractSorter):
    """
    Sorter_B → Sorter_C
    """
    def __init__(self):
        self.sorter_b = Sorter_B()
        self.sorter_c = Sorter_C()

    def sort_moves(self, *args, **kwargs):
        """
        手の候補を決める
        """
        kwargs['moves'] = self.sorter_b.sort_moves(*args, **kwargs)
        kwargs['moves'] = self.sorter_c.sort_moves(*args, **kwargs)

        return kwargs['moves']


class Sorter_CB(AbstractSorter):
    """
    Sorter_C → Sorter_B
    """
    def __init__(self):
        self.sorter_b = Sorter_B()
        self.sorter_c = Sorter_C()

    def sort_moves(self, *args, **kwargs):
        """
        手の候補を決める
        """
        kwargs['moves'] = self.sorter_c.sort_moves(*args, **kwargs)
        kwargs['moves'] = self.sorter_b.sort_moves(*args, **kwargs)

        return kwargs['moves']


if __name__ == '__main__':
    from board import BitBoard
    from common.timer import Timer

    bitboard8 = BitBoard(8)
    bitboard8.put_disc('black', 3, 2)
    print(bitboard8)

    best_move = (4, 2)

    print('--- Test For Sorter ---')
    sorter = Sorter()

    moves = sorter.sort_moves(color='white', board=bitboard8, moves=None, best_move=best_move)
    print(moves)
    assert moves == [(2, 2), (4, 2), (2, 4)]

    print('--- Test For Sorter_B ---')
    sorter = Sorter_B()

    moves = sorter.sort_moves(color='white', board=bitboard8, moves=None, best_move=best_move)
    print(moves)
    assert moves == [(4, 2), (2, 2), (2, 4)]

    bitboard8.put_disc('white', 2, 4)
    bitboard8.put_disc('black', 1, 5)
    bitboard8.put_disc('white', 1, 4)
    bitboard8.put_disc('black', 2, 5)
    bitboard8.put_disc('white', 2, 6)
    bitboard8.put_disc('black', 1, 6)
    bitboard8.put_disc('white', 1, 7)
    print(bitboard8)

    print('--- Test For Sorter_C ---')
    sorter = Sorter_C()
    moves = sorter.sort_moves(color='black', board=bitboard8, moves=None, best_move=best_move)
    print(moves)
    assert moves == [(0, 7), (0, 3), (2, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)]

    print('--- Test For Sorter_BC ---')
    sorter = Sorter_BC()

    best_move = (2, 3)
    moves = sorter.sort_moves(color='black', board=bitboard8, moves=None, best_move=best_move)
    print(moves)
    assert moves == [(0, 7), (2, 3), (0, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)]

    print('--- Test For Sorter_CB ---')
    sorter = Sorter_CB()

    best_move = (2, 3)
    moves = sorter.sort_moves(color='black', board=bitboard8, moves=None, best_move=best_move)
    print(moves)
    assert moves == [(2, 3), (0, 7), (0, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)]

    print('--- Test For Sorter_O ---')
    sorter = Sorter_O()

    moves = sorter.sort_moves(color='black', board=bitboard8, moves=None, best_move=None)
    print(moves)
    assert moves == [(2, 3), (0, 5), (0, 7), (2, 7), (0, 3), (5, 4), (4, 5), (5, 5), (0, 6), (0, 4)]
