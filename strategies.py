#!/usr/bin/env python
"""
オセロの戦略
"""

import abc
import re
import random
import time
import itertools


class AbstractStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next_move(self, color, board):
        pass


class ConsoleUserInput(AbstractStrategy):
    """
    コンソールからのユーザ入力
    """
    def __init__(self):
        self.digit = re.compile(r'^[0-9]+$')

    def next_move(self, color, board):
        """
        次の一手
        """
        possibles = list(board.get_possibles(color).keys())
        select = None

        while True:
            user_in = input('>> ')

            if self._is_digit(user_in):
                select = int(user_in) - 1

                if 0 <= select < len(possibles):
                    break

        return possibles[select]

    def _is_digit(self, string):
        """
        半角数字の判定
        """
        return self.digit.match(string) is not None


class WindowUserInput(AbstractStrategy):
    """
    ウィンドウからのユーザ入力
    """
    def __init__(self, window):
        self.window = window

    def next_move(self, color, board):
        """
        次の一手
        """
        moves = list(board.get_possibles(color).keys())
        self.window.board.selectable_moves(moves)

        while True:
            if self.window.board.event.is_set():
                move = self.window.board.move
                self.window.board.event.clear()

                if move in moves:
                    self.window.board.unselectable_moves(moves)
                    break

            time.sleep(0.01)

        return move


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

        # 序盤以降
        if (squares-blanks)/squares >= 0.15:
            return self.greedy.next_move(color, board)

        # 序盤
        return self.unselfish.next_move(color, board)


class Table(AbstractStrategy):
    """
    評価関数で手を決める(なるべく少なく取る、角を狙う、角のそばは避ける)
    """
    CORNER, C, A, B, X, O = 50, -20, 0, -1, -25, -5

    def __init__(self, board_size):
        self.table = [[Table.B for _ in range(board_size)] for _ in range(board_size)]

        # 中
        for num in range(0, board_size//2, 2):
            if num != board_size//2 - 1:
                for y, x in itertools.product((num, board_size-num-1), repeat=2):
                    self.table[y][x] = Table.A

        for y in range(1, board_size//2-1, 2):
            for x in range(1, board_size//2-1, 2):
                if x == y:
                    for tmp_y, tmp_x in itertools.product((y, board_size-y-1), (x, board_size-x-1)):
                        self.table[tmp_y][tmp_x] = Table.X

        for y in range(1, board_size//2-2, 2):
            for x in range(y+1, board_size-y-1):
                for tmp_y, tmp_x in ((y, x), (board_size-y-1, x)):
                    self.table[tmp_y][tmp_x] = Table.O
                    self.table[tmp_x][tmp_y] = Table.O

        # 端
        x_min, y_min, x_max, y_max = 0, 0, board_size - 1, board_size - 1

        if board_size >= 6:
            for y in range(board_size):
                for x in range(board_size):
                    if (x == x_min or x == x_max) and (y == y_min or y == y_max):
                        self.table[y][x] = Table.CORNER

                        x_sign = 1 if x == x_min else -1
                        y_sign = 1 if y == y_min else -1

                        self.table[y][x+(1*x_sign)] = Table.C
                        self.table[y][x+(2*x_sign)] = Table.B
                        self.table[y+(1*y_sign)][x] = Table.C
                        self.table[y+(2*y_sign)][x] = Table.B

        for row in self.table:
            print(row)

    def next_move(self, color, board):
        """
        次の一手
        """
        return (0, 0)


if __name__ == '__main__':
    def input(string):
        print(string + '1')
        return '1'

    from board import Board

    board = Board()
    print(board)
    console_user_input = ConsoleUserInput()

    possibles = board.get_possibles('black')

    for index, value in enumerate(possibles, 1):
        coordinate = (chr(value[0] + 97), str(value[1] + 1))
        print(f'{index:2d}:', coordinate)

    print('User', console_user_input.next_move('black', board))

    random_player = Random()
    print('Random', random_player.next_move('black', board))

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

    test4 = Player('white', 'Table', Table(4))
    print()
    test6 = Player('white', 'Table', Table(6))
    print()
    test8 = Player('white', 'Table', Table(8))
    print()
    test10 = Player('white', 'Table', Table(10))
    print()
    test12 = Player('white', 'Table', Table(12))
    print()
    test14 = Player('white', 'Table', Table(14))
    print()
    test16 = Player('white', 'Table', Table(16))
    print()
    test26 = Player('white', 'Table', Table(26))
    print()
