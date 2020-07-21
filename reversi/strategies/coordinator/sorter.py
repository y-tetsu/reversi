"""Sorter
"""

from reversi.strategies.common import AbstractSorter


class Sorter(AbstractSorter):
    """Sorter
    """
    def sort_moves(self, *args, **kwargs):
        """sort_moves
        """
        color, board, moves = kwargs['color'], kwargs['board'], kwargs['moves']

        if moves is None:
            return board.get_legal_moves(color, cache=True)

        return moves


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


class Sorter_O(Sorter):
    """Sorter_O

           開放度による並び替え
    """
    def sort_moves(self, *args, **kwargs):
        """sort_moves
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
        """get_opening

               開放度を求める
        """
        size, board_info, opening = board.size, board.get_board_info(), 0

        directions = [
            (-1,  1), (0,  1), (1,  1),
            (-1,  0),          (1,  0),
            (-1, -1), (0, -1), (1, -1),
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
