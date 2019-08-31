#!/usr/bin/env python
"""
オセロの戦略
"""

import abc
import re
import random


class AbstractStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next_move(self, stone, board):
        pass


class ConsoleUserInput(AbstractStrategy):
    """
    コンソールからのユーザ入力
    """
    def __init__(self):
        self.digit = re.compile(r'^[0-9]+$')

    def next_move(self, stone, board):
        """
        次の一手
        """
        possibles = list(board.get_possibles(stone).keys())
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


class Random:
    """
    ランダム
    """
    def next_move(self, stone, board):
        """
        次の一手
        """
        return random.choice(list(board.get_possibles(stone).keys()))


class Greedy:
    """
    一番多くとれる手を選ぶ(複数存在する場合はランダム)
    """
    def next_move(self, stone, board):
        """
        次の一手
        """
        possibles = board.get_possibles(stone)
        max_count = max([len(value) for value in possibles.values()])
        moves = [key for key, value in possibles.items() if len(value) == max_count]
        move = random.choice(moves)

        return move


class Unselfish:
    """
    一番少なくとれる手を選ぶ(複数存在する場合はランダム)
    """
    def next_move(self, stone, board):
        """
        次の一手
        """
        possibles = board.get_possibles(stone)
        min_count = min([len(value) for value in possibles.values()])
        moves = [key for key, value in possibles.items() if len(value) == min_count]
        move = random.choice(moves)

        return move


if __name__ == '__main__':
    def input(string):
        print(string + "1")
        return "1"

    from board import Board

    board = Board()
    print(board)
    console_user_input = ConsoleUserInput()

    possibles = board.get_possibles(Board.BLACK)

    for index, value in enumerate(possibles, 1):
        coordinate = (chr(value[0] + 97), str(value[1] + 1))
        print(f'{index:2d}:', coordinate)

    print("User", console_user_input.next_move(Board.BLACK, board))

    random_player = Random()

    print("Random", random_player.next_move(Board.BLACK, board))
