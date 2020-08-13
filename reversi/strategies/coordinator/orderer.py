"""Orderer
"""

from reversi.strategies.common import AbstractOrderer


class Orderer(AbstractOrderer):
    """Orderer
    """
    def move_ordering(self, *args, **kwargs):
        """move_ordering
        """
        return kwargs['moves']


class Orderer_B(Orderer):
    """Orderer_B

           前回の最善手を優先的に
    """
    def move_ordering(self, *args, **kwargs):
        """move_ordering
        """
        moves = super().move_ordering(*args, **kwargs)

        best_move = kwargs['best_move']

        if best_move is not None:
            moves.remove(best_move)
            moves.insert(0, best_move)

        return moves


class Orderer_C(Orderer):
    """Orderer_C

           4隅を優先的に
    """
    def move_ordering(self, *args, **kwargs):
        """move_ordering
        """
        moves = super().move_ordering(*args, **kwargs)

        board = kwargs['board']
        board_size = board.size
        corners = [(0, 0), (0, board_size-1), (board_size-1, 0), (board_size-1, board_size-1)]

        for corner in corners:
            if corner in moves:
                moves.remove(corner)
                moves.insert(0, corner)

        return moves


class Orderer_BC(AbstractOrderer):
    """Orderer_B → Orderer_C
    """
    def __init__(self):
        self.sorter_b = Orderer_B()
        self.sorter_c = Orderer_C()

    def move_ordering(self, *args, **kwargs):
        """move_ordering
        """
        kwargs['moves'] = self.sorter_b.move_ordering(*args, **kwargs)
        kwargs['moves'] = self.sorter_c.move_ordering(*args, **kwargs)

        return kwargs['moves']


class Orderer_CB(AbstractOrderer):
    """Orderer_C → Orderer_B
    """
    def __init__(self):
        self.sorter_b = Orderer_B()
        self.sorter_c = Orderer_C()

    def move_ordering(self, *args, **kwargs):
        """move_ordering
        """
        kwargs['moves'] = self.sorter_c.move_ordering(*args, **kwargs)
        kwargs['moves'] = self.sorter_b.move_ordering(*args, **kwargs)

        return kwargs['moves']
