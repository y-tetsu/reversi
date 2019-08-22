#!/usr/bin/env python
"""
オセロの戦略
"""

import random


class ConsoleUserInput:
    """
    コンソールからのユーザ入力
    """
    def next_move(self, stone, board):
        """
        次の一手
        """
        possibles = list(board.get_possibles(stone).keys())
        select = None

        while True:
            for index, value in enumerate(possibles, 1):
                coordinate = (chr(value[0] + 97), str(value[1] + 1))
                print(f'{index:2d}:', coordinate)

            user_in = input(">> ")

            if user_in.isdecimal():
                select = int(user_in) - 1

                if 0 <= select < len(possibles):
                    break

        return possibles[select]


class Random:
    """
    ランダム
    """
    def next_move(self, stone, board):
        """
        次の一手
        """
        possibles = list(board.get_possibles(stone).keys())
        select = random.randint(0, len(possibles) - 1)

        return possibles[select]


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
    from board import Board
    from player import Player

    board4 = Board(4)
    print(board4)

    p1 = Player(Board.BLACK, "BLACK: コンピュータ(Greedy)", Greedy())
    p2 = Player(Board.WHITE, "WHITE: コンピュータ(Unselfish)", Unselfish())

    while True:
        cnt = 0

        for player in [p1, p2]:
            if board4.get_possibles(player.stone):
                print("\n" + player.name + "の番です")
                player.put_stone(board4)
                move = "(" + chr(player.move[0] + 97) + ", " + str(player.move[1] + 1) + ")"
                print(move + "に置きました")
                print(board4)
                cnt += 1

        if not cnt:
            print("\n終了")
            break
