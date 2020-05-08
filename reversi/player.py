#!/usr/bin/env python
"""
プレイヤーの管理
"""

from reversi.disc import DiscFactory


class Player:
    """
    プレイヤーを管理する
    """
    def __init__(self, color, name, strategy):
        self.color = color
        factory = DiscFactory()
        self.disc = factory.create(color)
        self.name = name
        self.strategy = strategy
        self.move = (None, None)
        self.captures = []

    def __str__(self):
        return self.disc + self.name

    def put_disc(self, board):
        """
        次の手を決めて石を置く
        """
        self.move = self.strategy.next_move(self.color, board)    # 戦略に基づいた次の一手
        self.captures =  board.put_disc(self.color, *self.move)  # ボードに手を打つ


if __name__ == '__main__':
    from board import Board
    from strategies import ConsoleUserInput

    board4 = Board(4)
    print(board4)

    p1 = Player('black', 'ユーザ1', ConsoleUserInput())
    p2 = Player('white', 'ユーザ2', ConsoleUserInput())

    for player in [p1, p2]:
        legal_moves = board4.get_legal_moves(player.color)

        if legal_moves:
            print(player, 'の番です')

            for index, value in enumerate(legal_moves, 1):
                coordinate = (chr(value[0] + 97), str(value[1] + 1))
                print(f'{index:2d}:', coordinate)

            player.put_disc(board4)
            print(board4)
