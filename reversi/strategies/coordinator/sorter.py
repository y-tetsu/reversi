"""Sorter
"""

from reversi.strategies.common import AbstractSorter


class Sorter(AbstractSorter):
    """Sorter
    """
    def sort_moves(self, *args, **kwargs):
        """sort_moves
        """
        return kwargs['moves']


class Sorter_B(Sorter):
    """Sorter_B

           前回の最善手を優先的に
    """
    def sort_moves(self, *args, **kwargs):
        """sort_moves
        """
        moves = super().sort_moves(*args, **kwargs)

        best_move = kwargs['best_move']

        if best_move is not None:
            moves.remove(best_move)
            moves.insert(0, best_move)

        return moves


class Sorter_C(Sorter):
    """Sorter_C

           4隅を優先的に
    """
    def sort_moves(self, *args, **kwargs):
        """sort_moves
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


class Sorter_BC(AbstractSorter):
    """Sorter_B → Sorter_C
    """
    def __init__(self):
        self.sorter_b = Sorter_B()
        self.sorter_c = Sorter_C()

    def sort_moves(self, *args, **kwargs):
        """sort_moves
        """
        kwargs['moves'] = self.sorter_b.sort_moves(*args, **kwargs)
        kwargs['moves'] = self.sorter_c.sort_moves(*args, **kwargs)

        return kwargs['moves']


class Sorter_CB(AbstractSorter):
    """Sorter_C → Sorter_B
    """
    def __init__(self):
        self.sorter_b = Sorter_B()
        self.sorter_c = Sorter_C()

    def sort_moves(self, *args, **kwargs):
        """sort_moves
        """
        kwargs['moves'] = self.sorter_c.sort_moves(*args, **kwargs)
        kwargs['moves'] = self.sorter_b.sort_moves(*args, **kwargs)

        return kwargs['moves']
