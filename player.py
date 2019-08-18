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
        self.next_move = strategy

    def put_stone(self, board):
        """
        次の手を決めて石を置く
        """
        x, y = self.next_move(self.stone, board)

        return board.put_stone(self.stone, x, y)


if __name__ == '__main__':
    from board import Board
    import strategies

    board4 = Board()
    board4.print_board()

    p1 = Player(Board.BLACK, "ユーザ1", strategies.console_user_input)
    p2 = Player(Board.WHITE, "ユーザ2", strategies.console_user_input)

    while True:
        move = 0

        for player in [p1, p2]:
            if board4.get_possibles(player.stone):
                print("\n" + player.name + "の番です")
                player.put_stone(board4)
                board4.print_board()
                move += 1

        if not move:
            print("\n終了")
            break
