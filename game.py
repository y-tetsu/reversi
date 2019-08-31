#!/usr/bin/env python
"""
オセロゲーム
"""

from board import Board


class Game:
    """
    ゲームを管理する
    """
    BLACK_WIN, WHITE_WIN, DRAW = 0, 1, 2

    def __init__(self, board, black, white, display):
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
            self.display.start(self.board, self.black, self.white)

            while True:
                playable = 0
                foul_player = None

                for player in [self.black, self.white]:
                    possibles = self.board.get_possibles(player.stone)

                    if not possibles:
                        continue

                    self.display.turn(player, possibles)
                    captures = player.put_stone(self.board)
                    self.display.move(player, captures, self.board, self.black, self.white)

                    if not captures:
                        foul_player = player
                        break

                    playable += 1

                if foul_player:
                    self._foul(foul_player)
                    break

                if not playable:
                    self._judge()
                    break

    def _foul(self, player):
        """
        反則負け
        """
        if player.stone == self.black.stone:
            self._win(self.white)
        else:
            self._win(self.black)

    def _judge(self):
        """
        結果判定
        """
        if self.board.black_num > self.board.white_num:
            self._win(self.black)
        elif self.board.white_num > self.board.black_num:
            self._win(self.white)
        else:
            self._draw()

    def _win(self, player):
        """
        勝ち
        """
        self.display.win(player)

        if player.stone == Board.BLACK:
            result = Game.BLACK_WIN
        else:
            result = Game.WHITE_WIN

        self.result = GameResult(
            result,
            self.black.name, self.white.name,
            self.board.black_num, self.board.white_num,
        )

    def _draw(self):
        """
        引き分け
        """
        self.display.draw()

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
    from display import ConsoleDisplay
    import strategies

    class Foul():
        def next_move(self, stone, board):
            return (1, 1)

    black = Player(Board.BLACK, "Random", strategies.Random())
    white = Player(Board.WHITE, "Foul", Foul())

    game = Game(Board(4), black, white, ConsoleDisplay())
    game.play()

    print()
    print(game.result.winlose)
    print(game.result.black_name, game.result.black_num)
    print(game.result.white_name, game.result.white_num)

    black = Player(Board.BLACK, "Random", strategies.Random())
    white = Player(Board.WHITE, "Unselfish", strategies.Unselfish())

    game = Game(Board(4), black, white, ConsoleDisplay())
    game.play()

    print()
    print(game.result.winlose)
    print(game.result.black_name, game.result.black_num)
    print(game.result.white_name, game.result.white_num)
