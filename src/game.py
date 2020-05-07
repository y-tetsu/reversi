#!/usr/bin/env python
"""
ゲームの管理
"""


class Game:
    """
    ゲームを管理する
    """
    BLACK_WIN, WHITE_WIN, DRAW = 0, 1, 2

    def __init__(self, board, black_player, white_player, display, color='black', cancel=None):
        self.board = board
        self.black_player = black_player
        self.white_player = white_player
        self.players = [self.black_player, self.white_player] if color == 'black' else [self.white_player, self.black_player]
        self.display = display
        self.cancel = cancel
        self.result = []

    def play(self):
        """
        ゲームを開始する
        """
        if not self.result:
            self.display.progress(self.board, self.black_player, self.white_player)

            while True:
                playable, foul_player = 0, None

                for player in self.players:
                    # キャンセル許可時
                    if self.cancel:
                        if self.cancel.event.is_set():
                            # キャンセルメニュー設定時は中断
                            break

                    possibles = list(self.board.get_possibles(player.color).keys())

                    if not possibles:
                        continue

                    self.display.turn(player, possibles)

                    player.put_disc(self.board)

                    self.display.move(player, possibles)
                    self.display.progress(self.board, self.black_player, self.white_player)

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
        winner = self.white_player if player.color == self.black_player.color else self.black_player
        self._win(winner)

    def _judge(self):
        """
        結果判定
        """
        black_num, white_num = self.board.score['black'], self.board.score['white']

        if black_num == white_num:
            self._draw()
        else:
            winner = self.black_player if black_num > white_num else self.white_player
            self._win(winner)

    def _win(self, player):
        """
        勝ち
        """
        self.display.win(player)
        winlose = Game.BLACK_WIN if player.color == self.black_player.color else Game.WHITE_WIN
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
            self.black_player.name, self.white_player.name,
            self.board.score['black'], self.board.score['white'],
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
        def next_move(self, disc, board):
            return (1, 1)

    board4x4 = Board(4)
    black_player = Player('black', 'Random', strategies.Random())
    white_player = Player('white', 'Foul', Foul())

    game = Game(board4x4, black_player, white_player, ConsoleDisplay())
    game.play()

    print()
    print(game.result.winlose)
    print(game.result.black_name, game.result.black_num)
    print(game.result.white_name, game.result.white_num)
    print()

    black_player = Player('black', 'Random', strategies.Random())
    white_player = Player('white', 'Table', strategies.Table(4))

    board4x4 = Board(4)
    board4x4.put_disc('black', 1, 0)
    print(board4x4)
    game = Game(board4x4, black_player, white_player, ConsoleDisplay(), 'white')
    game.play()

    print()
    print(game.result.winlose)
    print(game.result.black_name, game.result.black_num)
    print(game.result.white_name, game.result.white_num)
