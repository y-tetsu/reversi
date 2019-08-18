#!/usr/bin/env python
"""
オセロの戦略
"""


def console_user_input(stone, board):
    """
    コンソールからのユーザ入力
    """
    possibles = list(board.get_possibles(stone).keys())
    color = "黒" if stone == board.BLACK else "白"
    select = None

    while True:
        print(f'\n* {color}の番です')

        for index, value in enumerate(possibles, 1):
            coordinate = (chr(value[0] + 97), str(value[1] + 1))
            print(f'{index:2d}:', coordinate)

        user_in = input(">> ")

        if user_in.isdecimal():
            select = int(user_in) - 1

            if 0 <= select < len(possibles):
                break

    return possibles[select]


if __name__ == '__main__':
    from board import Board

    board4 = Board()
    board4.print_board()

    x, y = console_user_input(Board.BLACK, board4)
    board4.put_stone(Board.BLACK, x, y)
    board4.print_board()

    x, y = console_user_input(Board.WHITE, board4)
    board4.put_stone(Board.WHITE, x, y)
    board4.print_board()
