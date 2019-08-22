#!/usr/bin/env python
"""
オセロプレイヤー
"""


class Player:
    """
    プレイヤーを管理する
    """
    def __init__(self, stone, name, strategy):
        self.stone = stone
        self.name = name
        self.strategy = strategy
        self.move = (None, None)

    def put_stone(self, board):
        """
        次の手を決めて石を置く
        """
        self.move = self.strategy.next_move(self.stone, board)

        return board.put_stone(self.stone, *self.move)


if __name__ == '__main__':
    from board import Board
    from strategies import ConsoleUserInput

    board4 = Board(4)
    print(board4)

    p1 = Player(Board.BLACK, "ユーザ1", ConsoleUserInput())
    p2 = Player(Board.WHITE, "ユーザ2", ConsoleUserInput())

    while True:
        move = 0

        for player in [p1, p2]:
            if board4.get_possibles(player.stone):
                print("\n" + player.name + "の番です")
                player.put_stone(board4)
                print(board4)
                move += 1

        if not move:
            print("\n終了")
            break
