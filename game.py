#!/usr/bin/env python
"""
オセロゲーム
"""


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
            self.display.progress(self.board, self.black, self.white)

            while True:
                playable, foul_player = 0, None

                for player in [self.black, self.white]:
                    possibles = list(self.board.get_possibles(player.stone).keys())

                    if not possibles:
                        continue

                    self.display.turn(player, possibles)

                    player.put_stone(self.board)

                    self.display.move(player, possibles)
                    self.display.progress(self.board, self.black, self.white)

                    if not player.captures:
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
        self.display.foul(player)
        winner = self.white if player.stone == self.black.stone else self.black
        self._win(winner)

    def _judge(self):
        """
        結果判定
        """
        black_num, white_num = self.board.num[self.black.stone], self.board.num[self.white.stone]

        if black_num == white_num:
            self._draw()
        else:
            winner = self.black if black_num > white_num else self.white
            self._win(winner)

    def _win(self, player):
        """
        勝ち
        """
        self.display.win(player)
        winlose = Game.BLACK_WIN if player.stone == self.black.stone else Game.WHITE_WIN
        self._store_result(winlose)

    def _draw(self):
        """
        引き分け
        """
        self.display.draw()
        self._store_result(Game.DRAW)

    def _store_result(self, winlose):
        """
        結果を格納する
        """
        self.result = GameResult(
            winlose,
            self.black.name, self.white.name,
            self.board.num[self.black.stone], self.board.num[self.white.stone],
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

    board4x4 = Board(4)
    black = Player(board4x4.black, "Random", strategies.Random())
    white = Player(board4x4.white, "Foul", Foul())

    game = Game(board4x4, black, white, ConsoleDisplay())
    game.play()

    print()
    print(game.result.winlose)
    print(game.result.black_name, game.result.black_num)
    print(game.result.white_name, game.result.white_num)
    print()

    board4x4 = Board(4)
    black = Player(board4x4.black, "Random", strategies.Random())
    white = Player(board4x4.white, "Unselfish", strategies.Unselfish())

    game = Game(board4x4, black, white, ConsoleDisplay())
    game.play()

    print()
    print(game.result.winlose)
    print(game.result.black_name, game.result.black_num)
    print(game.result.white_name, game.result.white_num)
