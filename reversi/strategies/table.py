"""Table
"""

import sys
import random
import itertools

from reversi.strategies.common import AbstractStrategy
import reversi.strategies.TableMethods as TableMethods

sys.path.append('../')


class Table(AbstractStrategy):
    """select move by evaluation table
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5):
        self._CORNER = corner
        self._C = c
        self._A1 = a1
        self._A2 = a2
        self._B1 = b1
        self._B2 = b2
        self._B3 = b3
        self._X = x
        self._O1 = o1
        self._O2 = o2
        self.set_table(size)

    def set_table(self, size):
        """set_table
        """
        self.size = size
        table = [[self._B3 for _ in range(size)] for _ in range(size)]

        # B1
        table[size//2-1][size//2-1] = self._B1
        table[size//2-1][size//2] = self._B1
        table[size//2][size//2-1] = self._B1
        table[size//2][size//2] = self._B1

        # A1
        for num in range(0, size//2, 2):
            if num != size//2 - 1:
                for y, x in itertools.product((num, size-num-1), repeat=2):
                    table[y][x] = self._A1

        # B2
        for y in range(2, size//2-1, 2):
            for x in range(y+1, size-y-1):
                for tmp_y, tmp_x in ((y, x), (size-y-1, x)):
                    table[tmp_y][tmp_x] = self._B2
                    table[tmp_x][tmp_y] = self._B2

        # X
        for y in range(1, size//2-1, 2):
            for x in range(1, size//2-1, 2):
                if x == y:
                    x2 = size - x - 1
                    y2 = size - y - 1
                    for tmp_y, tmp_x in itertools.product((y, y2), (x, x2)):
                        table[tmp_y][tmp_x] = self._X

        # O1, O2
        for y in range(1, size//2-1, 2):
            for tmp_y, tmp_x in ((y, y+1), (y, size-y-2), (size-y-1, y+1), (size-y-1, size-y-2)):
                table[tmp_y][tmp_x] = self._O1
                table[tmp_x][tmp_y] = self._O1

            for x in range(y+2, size-y-2):
                for tmp_y, tmp_x in ((y, x), (size-y-1, x)):
                    table[tmp_y][tmp_x] = self._O2
                    table[tmp_x][tmp_y] = self._O2

        # CORNER、C、A2
        x_min, y_min, x_max, y_max = 0, 0, size - 1, size - 1
        for y in range(size):
            for x in range(size):
                if (x == x_min or x == x_max) and (y == y_min or y == y_max):
                    table[y][x] = self._CORNER

                    x_sign = 1 if x == x_min else -1
                    y_sign = 1 if y == y_min else -1

                    table[y][x+(1*x_sign)] = self._C
                    table[y+(1*y_sign)][x] = self._C

                    if size >= 6:
                        table[y][x+(2*x_sign)] = self._A2
                        table[y+(2*y_sign)][x] = self._A2

        self.table = table

    def get_score(self, color, board):
        """get_score
        """
        return TableMethods.get_score(color, self.table, board)

    def next_move(self, color, board):
        """next move
        """
        if self.size != board.size:
            self.set_table(board.size)

        legal_moves = board.get_legal_moves(color)
        max_score = None
        moves = {}

        for move in legal_moves.keys():
            board.put_disc(color, *move)
            score = self.get_score(color, board)

            if max_score is None or score > max_score:
                max_score = score

            if score not in moves:
                moves[score] = []

            moves[score].append(move)
            board.undo()

        return random.choice(moves[max_score])
