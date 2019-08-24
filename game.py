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
            self.print_if_display(self.board)

            while True:
                cnt = 0

                for player in [self.black, self.white]:
                    if self.board.get_possibles(player.stone):
                        self.print_if_display("\n" + player.name + " の番です")

                        if player.put_stone(self.board):
                            x = chr(player.move[0] + 97)
                            y = str(player.move[1] + 1)
                            self.print_if_display((x, y), "に置きました")
                            self.print_if_display(self.board)
                            cnt += 1
                        else:
                            self.foul(player)
                            break

                if not cnt:
                    self.judge()
                    break

    def print_if_display(self, *messages):
        """
        表示
        """
        if self.display:
            print(*messages)

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
        self.print_if_display("\n" + self.black.name + " の勝ちです")

        self.result = GameResult(
            Game.BLACK_WIN,
            self.black.name, self.white.name,
            self.board.black_num, self.board.white_num,
        )

    def white_win(self):
        """
        白の勝ち
        """
        self.print_if_display("\n" + self.white.name + " の勝ちです")

        self.result = GameResult(
            Game.WHITE_WIN,
            self.black.name, self.white.name,
            self.board.black_num, self.board.white_num,
        )

    def draw(self):
        """
        引き分け
        """
        self.print_if_display("\n引き分けです")

        self.result = GameResult(
            Game.DRAW,
            self.black.name, self.white.name,
            self.board.black_num, self.board.white_num,
        )


class GameResult:
    """
    ゲームの結果
    """
    def __init__(self, winlose, black_name, white_name, black_num, white_num):
        self.winlose = winlose
        self.black_name = black_name
        self.white_name = white_name
        self.black_num = black_num
        self.white_num = white_num


if __name__ == '__main__':
    from board import Board
    from player import Player
    import strategies

    black = Player(Board.BLACK, "Random", strategies.Random())
    white = Player(Board.WHITE, "Greedy", strategies.Greedy())

    game = Game(Board(4), black, white)
    game.play()

    print(game.result.winlose)
    print(game.result.black_name, game.result.black_num)
    print(game.result.white_name, game.result.white_num)
