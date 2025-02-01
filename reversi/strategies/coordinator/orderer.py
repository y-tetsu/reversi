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


class Orderer_P(Orderer):
    """Orderer_P

           相手の着手可能数が少ないものを優先
    """
    def move_ordering(self, *args, **kwargs):
        """move_ordering
        """
        moves = super().move_ordering(*args, **kwargs)
        board = kwargs['board']
        color = kwargs['color']
        opponent = 'white' if color == 'black' else 'black'
        opponent_p = []
        for move in moves:
            board.put_disc(color, *move)
            opponent_p += [(move, board.get_bit_count(board.get_legal_moves_bits(opponent)))]
            board.undo()

        return [i[0] for i in sorted(opponent_p, key=lambda x: x[1])]


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


class Orderer_PCB(AbstractOrderer):
    """Orderer_P → Orderer_C → Orderer_B
    """
    def __init__(self):
        self.sorter_p = Orderer_P()
        self.sorter_b = Orderer_B()
        self.sorter_c = Orderer_C()

    def move_ordering(self, *args, **kwargs):
        """move_ordering
        """
        kwargs['moves'] = self.sorter_p.move_ordering(*args, **kwargs)
        kwargs['moves'] = self.sorter_c.move_ordering(*args, **kwargs)
        kwargs['moves'] = self.sorter_b.move_ordering(*args, **kwargs)

        return kwargs['moves']
