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
        self.captures = []

    def __str__(self):
        return self.stone + self.name

    def put_stone(self, board):
        """
        次の手を決めて石を置く
        """
        self.move = self.strategy.next_move(self.stone, board)
        self.captures =  board.put(self.stone, *self.move)


if __name__ == '__main__':
    from board import Board
    from strategies import ConsoleUserInput

    board4 = Board(4)
    print(board4)

    p1 = Player(board4.black, "ユーザ1", ConsoleUserInput())
    p2 = Player(board4.white, "ユーザ2", ConsoleUserInput())

    for player in [p1, p2]:
        possibles = board4.get_possibles(player.stone)

        if possibles:
            print(player, "の番です")

            for index, value in enumerate(possibles, 1):
                coordinate = (chr(value[0] + 97), str(value[1] + 1))
                print(f'{index:2d}:', coordinate)

            player.put_stone(board4)
            print(board4)
