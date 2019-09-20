#!/usr/bin/env python
"""
オセロの戦略
"""

import abc
import re
import random
import time


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
            user_in = input(">> ")

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


if __name__ == '__main__':
    def input(string):
        print(string + "1")
        return "1"

    from board import Board

    board = Board()
    print(board)
    console_user_input = ConsoleUserInput()

    possibles = board.get_possibles('black')

    for index, value in enumerate(possibles, 1):
        coordinate = (chr(value[0] + 97), str(value[1] + 1))
        print(f'{index:2d}:', coordinate)

    print("User", console_user_input.next_move('black', board))

    random_player = Random()
    print("Random", random_player.next_move('black', board))

    from board import Board
    from player import Player

    board4x4 = Board(4)
    print(board4x4)

    p1 = Player('black', "Random", Random())
    p2 = Player('white', "Greedy", Greedy())

    while True:
        cnt = 0

        for player in [p1, p2]:
            if board4x4.get_possibles(player.color):
                print(player, "の番です")
                player.put_stone(board4x4)
                move = "(" + chr(player.move[0] + 97) + ", " + str(player.move[1] + 1) + ")"
                print(move + "に置きました\n")
                print(board4x4)
                cnt += 1

        if not cnt:
            print("\n終了")
            break
