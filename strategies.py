#!/usr/bin/env python
"""
オセロの戦略
"""


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


if __name__ == '__main__':
    from board import Board

    board4 = Board()
    board4.print_board()
    strategy = ConsoleUserInput()

    print('\n* 黒の番です')
    x, y = strategy.next_move(Board.BLACK, board4)
    board4.put_stone(Board.BLACK, x, y)
    board4.print_board()

    print('\n* 白の番です')
    x, y = strategy.next_move(Board.WHITE, board4)
    board4.put_stone(Board.WHITE, x, y)
    board4.print_board()
