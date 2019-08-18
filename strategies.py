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


if __name__ == '__main__':
    from board import Board
    from player import Player

    board4 = Board()
    board4.print_board()

    p1 = Player(Board.BLACK, "あなた", ConsoleUserInput())
    p2 = Player(Board.WHITE, "COM(ランダム)", Random())

    while True:
        move = 0

        for player in [p1, p2]:
            if board4.get_possibles(player.stone):
                print("\n" + player.name + "の番です")
                player.put_stone(board4)
                print(player.move, "に置きました")
                board4.print_board()
                move += 1

        if not move:
            print("\n終了")
            break
