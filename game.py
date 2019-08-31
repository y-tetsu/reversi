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
            self._print_if_display(self.board)

            while True:
                playable = 0
                foul_player = None

                for player in [self.black, self.white]:
                    if self.board.get_possibles(player.stone):
                        self._print_if_display("\n" + player.name + " の番です")

                        if player.put_stone(self.board):
                            x = chr(player.move[0] + 97)
                            y = str(player.move[1] + 1)
                            self._print_if_display((x, y), "に置きました")
                            self._print_if_display(self.board)
                            playable += 1
                        else:
                            foul_player = player
                            break

                if foul_player:
                    self._foul(foul_player)
                    break

                if not playable:
                    self._judge()
                    break

    def _print_if_display(self, *messages):
        """
        表示
        """
        if self.display:
            print(*messages)

    def _foul(self, player):
        """
        反則負け
        """
        if player.stone == self.black.stone:
            self._win(self.white.name, Game.WHITE_WIN)
        else:
            self._win(self.black.name, Game.BLACK_WIN)

    def _judge(self):
        """
        結果判定
        """
        if self.board.black_num > self.board.white_num:
            self._win(self.black.name, Game.BLACK_WIN)
        elif self.board.white_num > self.board.black_num:
            self._win(self.white.name, Game.WHITE_WIN)
        else:
            self._draw()

    def _win(self, name, result):
        """
        勝ち
        """
        self._print_if_display("\n" + name + " の勝ちです")

        self.result = GameResult(
            result,
            self.black.name, self.white.name,
            self.board.black_num, self.board.white_num,
        )

    def _draw(self):
        """
        引き分け
        """
        self._print_if_display("\n引き分けです")

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

    class Foul():
        def next_move(self, stone, board):
            return (1, 1)

    black = Player(Board.BLACK, "Random", strategies.Random())
    white = Player(Board.WHITE, "Foul", Foul())

    game = Game(Board(4), black, white)
    game.play()

    print(game.result.winlose)
    print(game.result.black_name, game.result.black_num)
    print(game.result.white_name, game.result.white_num)
