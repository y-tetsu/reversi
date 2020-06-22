#!/usr/bin/env python
"""Table
"""

import sys
sys.path.append('../')

import random
import itertools

from reversi.strategies.common import AbstractStrategy


class Table(AbstractStrategy):
    """
    評価テーブルで手を決める(なるべく少なく取る、角を狙う、角のそばは避ける)
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5):
        self._CORNER = corner
        self._C = c
        self._A1 = a1
        self._A2 = a2
        self._B = b
        self._X = x
        self._O = o
        self.set_table(size)

    def set_table(self, size):
        """
        評価テーブル設定
        """
        self.size = size
        table = [[self._B for _ in range(size)] for _ in range(size)]

        # 中
        for num in range(0, size//2, 2):
            if num != size//2 - 1:
                for y, x in itertools.product((num, size-num-1), repeat=2):
                    table[y][x] = self._A1

        for y in range(1, size//2-1, 2):
            for x in range(1, size//2-1, 2):
                if x == y:
                    for tmp_y, tmp_x in itertools.product((y, size-y-1), (x, size-x-1)):
                        table[tmp_y][tmp_x] = self._X

        for y in range(1, size//2-2, 2):
            for x in range(y+1, size-y-1):
                for tmp_y, tmp_x in ((y, x), (size-y-1, x)):
                    table[tmp_y][tmp_x] = self._O
                    table[tmp_x][tmp_y] = self._O

        # 端
        x_min, y_min, x_max, y_max = 0, 0, size - 1, size - 1

        if size >= 6:
            for y in range(size):
                for x in range(size):
                    if (x == x_min or x == x_max) and (y == y_min or y == y_max):
                        table[y][x] = self._CORNER

                        x_sign = 1 if x == x_min else -1
                        y_sign = 1 if y == y_min else -1

                        table[y][x+(1*x_sign)] = self._C
                        table[y][x+(2*x_sign)] = self._A2
                        table[y+(1*y_sign)][x] = self._C
                        table[y+(2*y_sign)][x] = self._A2

        self.table = table

    def get_score(self, color, board):
        """
        評価値を取得する
        """
        sign = 1 if color == 'black' else -1
        board_info = board.get_board_info()
        score = 0

        for y in range(self.size):
            for x in range(self.size):
                score += self.table[y][x] * board_info[y][x] * sign

        return score

    def next_move(self, color, board):
        """
        次の一手
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
