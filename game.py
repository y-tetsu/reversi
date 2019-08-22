#!/usr/bin/env python
"""
オセロゲーム
"""


class Game:
    """
    ゲームを管理する
    """
    BLACK_WIN, WHITE_WIN, DRAW = 0, 1, 2

    def __init__(self, board, black, white, display=True):
        self.board = board
        self.black = black
        self.white = white
        self.display = display
        self.result = []

    def play(self):
        """
        ゲームを開始する
        """
        if not self.result:
            if self.display:
                print(self.board)

            while True:
                cnt = 0

                for player in [self.black, self.white]:
                    if self.board.get_possibles(player.stone):
                        if self.display:
                            print("\n" + player.name + " の番です")

                        if player.put(self.board):
                            if self.display:
                                x = chr(player.move[0] + 97)
                                y = str(player.move[1] + 1)
                                print((x, y), "に置きました")
                                print(self.board)

                            cnt += 1
                        else:
                            self.foul(player)
                            break

                if not cnt:
                    self.judge()
                    break

    def judge(self):
        """
        結果判定
        """
        if self.board.black_num > self.board.white_num:
            self.black_win()
        elif self.board.white_num > self.board.black_num:
            self.white_win()
        else:
            self.draw()

    def foul(self, player):
        """
        反則負け
        """
        if player.stone == self.black.stone:
            self.white_win()
        else:
            self.black_win()

    def black_win(self):
        """
        黒の勝ち
        """
        self.result = [
            Game.BLACK_WIN,
            (self.black.name, self.white.name),
            (self.board.black_num, self.board.white_num),
        ]

        if self.display:
            print("\n" + self.black.name + " の勝ちです")

    def white_win(self):
        """
        白の勝ち
        """
        self.result = [
            Game.WHITE_WIN,
            (self.black.name, self.white.name),
            (self.board.black_num, self.board.white_num),
        ]

        if self.display:
            print("\n" + self.white.name + " の勝ちです")

    def draw(self):
        """
        引き分け
        """
        self.result = [
            Game.DRAW,
            (self.black.name, self.white.name),
            (self.board.black_num, self.board.white_num),
        ]

        if self.display:
            print("\n引き分けです")


if __name__ == '__main__':
    from board import Board
    from player import Player
    import strategies

    black = Player(Board.BLACK, "Random", strategies.Random())
    white = Player(Board.WHITE, "Max", strategies.Max())

    game = Game(Board(4), black, white)
    game.play()
