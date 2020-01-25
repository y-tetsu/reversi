#!/usr/bin/env python
"""
簡易戦略集
"""

import sys
sys.path.append('../')

import random
import itertools

import numpy as np

from strategies.common import AbstractStrategy


class Random(AbstractStrategy):
    """
    ランダム
    """
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = list(board.get_possibles(color).keys())

        return random.choice(moves)


class Greedy(AbstractStrategy):
    """
    なるべく多くとり、複数ある場合はランダム
    """
    def next_move(self, color, board):
        """
        次の一手
        """
        possibles = board.get_possibles(color)
        max_count = max([len(value) for value in possibles.values()])
        moves = [key for key, value in possibles.items() if len(value) == max_count]

        return random.choice(moves)


class Unselfish(AbstractStrategy):
    """
    Greedyの逆
    """
    def next_move(self, color, board):
        """
        次の一手
        """
        possibles = board.get_possibles(color)
        min_count = min([len(value) for value in possibles.values()])
        moves = [key for key, value in possibles.items() if len(value) == min_count]

        return random.choice(moves)


class SlowStarter(AbstractStrategy):
    """
    15%未満:Unselfish、15%以上:Greedy
    """
    def __init__(self):
        self.unselfish = Unselfish()
        self.greedy = Greedy()

    def next_move(self, color, board):
        """
        次の一手
        """
        squares = board.size**2
        blanks = sum([row.count(0) for row in board.get_board_info()])

        # 序盤
        if (squares-blanks)/squares < 0.15:
            return self.unselfish.next_move(color, board)

        # 序盤以降
        return self.greedy.next_move(color, board)


class Table(AbstractStrategy):
    """
    評価テーブルで手を決める(なるべく少なく取る、角を狙う、角のそばは避ける)
    """
    def __init__(self, size=8, corner=50, c=-20, a=0, b=-1, x=-25, o=-5):
        self._CORNER = corner
        self._C = c
        self._A = a
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
                    table[y][x] = self._A

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
                        table[y][x+(2*x_sign)] = self._B
                        table[y+(1*y_sign)][x] = self._C
                        table[y+(2*y_sign)][x] = self._B

        self.table = np.array(table)

    def get_score(self, color, board):
        """
        評価値を取得する
        """
        sign = 1 if color == 'black' else -1
        board_info = np.array(board.get_board_info())
        score = (board_info * self.table * sign).sum()

        return score

    def next_move(self, color, board):
        """
        次の一手
        """
        if self.size != board.size:
            self.set_table(board.size)

        possibles = board.get_possibles(color)
        max_score = None
        moves = {}

        for move in possibles.keys():
            board.put_stone(color, *move)
            score = self.get_score(color, board)

            if max_score is None or score > max_score:
                max_score = score

            if score not in moves:
                moves[score] = []

            moves[score].append(move)
            board.undo()

        return random.choice(moves[max_score])


if __name__ == '__main__':
    from board import Board
    from player import Player

    board4x4 = Board(4)
    print(board4x4)

    p1 = Player('black', 'Random', Random())
    p2 = Player('white', 'SlowStarter', SlowStarter())

    while True:
        cnt = 0

        for player in [p1, p2]:
            if board4x4.get_possibles(player.color):
                print(player, 'の番です')
                player.put_stone(board4x4)
                move = '(' + chr(player.move[0] + 97) + ', ' + str(player.move[1] + 1) + ')'
                print(move + 'に置きました\n')
                print(board4x4)
                cnt += 1

        if not cnt:
            print('\n終了')
            break

    table4 = Table(4)
    table4_ret = [
        [0, -1, -1, 0],
        [-1, -1, -1, -1],
        [-1, -1, -1, -1],
        [0, -1, -1, 0],
    ]
    assert (table4.table == np.array(table4_ret)).all()

    table8 = Table(8)
    table8_ret = [
        [50, -20, -1, -1, -1, -1, -20, 50],
        [-20, -25, -5, -5, -5, -5, -25, -20],
        [-1, -5, 0, -1, -1, 0, -5, -1],
        [-1, -5, -1, -1, -1, -1, -5, -1],
        [-1, -5, -1, -1, -1, -1, -5, -1],
        [-1, -5, 0, -1, -1, 0, -5, -1],
        [-20, -25, -5, -5, -5, -5, -25, -20],
        [50, -20, -1, -1, -1, -1, -20, 50],
    ]
    assert (table8.table == np.array(table8_ret)).all()

    table16 = Table(16)
    table16_ret = [
        [50, -20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -20, 50],
        [-20, -25, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -25, -20],
        [-1, -5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -5, -1],
        [-1, -5, -1, -25, -5, -5, -5, -5, -5, -5, -5, -5, -25, -1, -5, -1],
        [-1, -5, -1, -5, 0, -1, -1, -1, -1, -1, -1, 0, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -25, -5, -5, -5, -5, -25, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -5, 0, -1, -1, 0, -5, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -5, -1, -1, -1, -1, -5, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -5, -1, -1, -1, -1, -5, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -5, 0, -1, -1, 0, -5, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -25, -5, -5, -5, -5, -25, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, 0, -1, -1, -1, -1, -1, -1, 0, -5, -1, -5, -1],
        [-1, -5, -1, -25, -5, -5, -5, -5, -5, -5, -5, -5, -25, -1, -5, -1],
        [-1, -5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -5, -1],
        [-20, -25, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -25, -20],
        [50, -20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -20, 50],
    ]
    assert (table16.table == np.array(table16_ret)).all()

    board8 = Board(8)
    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 2)
    board8.put_stone('black', 2, 3)
    board8.put_stone('white', 4, 2)
    board8.put_stone('black', 1, 1)
    board8.put_stone('white', 0, 0)
    print(board8)
    for row in table8.table:
        print(row)
    print('black score', table8.get_score('black', board8))
    print('white score', table8.get_score('white', board8))
    assert table8.get_score('black', board8) == -22
    assert table8.get_score('white', board8) == 22
    print('next black', table8.next_move('black', board8))
    print('next white', table8.next_move('white', board8))
    assert table8.next_move('black', board8) == (5, 2)
    assert table8.next_move('white', board8) == (2, 5)

    print("pre", table8.table)
    table8.next_move('black', Board(4))
    print("aft", table8.table)
    assert (table8.table == np.array(table4_ret)).all
