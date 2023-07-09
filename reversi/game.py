"""Game
"""

from reversi import BitBoard, NoneDisplay


class Game:
    """Game
    """
    BLACK_WIN, WHITE_WIN, DRAW = 0, 1, 2

    def __init__(self, black_player, white_player, board=BitBoard(), display=NoneDisplay(), color='black', cancel=None):
        self.black_player = black_player
        self.white_player = white_player
        self.board = board
        self.players = [self.black_player, self.white_player] if color == 'black' else [self.white_player, self.black_player]
        self.display = display
        self.cancel = cancel
        self.result = []

    def play(self):
        """play
        """
        if not self.result:
            self.display.progress(self.board, self.black_player, self.white_player)

            # setup for Player
            for p in [self.black_player, self.white_player]:
                if hasattr(p.strategy, 'setup'):
                    p.strategy.setup(self.board)

            while True:
                playable, foul_player = 0, None

                for player in self.players:
                    if self.cancel:
                        if self.cancel.event.is_set():
                            break

                    legal_moves = self.board.get_legal_moves(player.color)

                    if not legal_moves:
                        continue

                    self.display.turn(player, legal_moves)

                    player.put_disc(self.board)

                    self.display.move(player, legal_moves)
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

            # teardown for Player
            for p in [self.black_player, self.white_player]:
                if hasattr(p.strategy, 'teardown'):
                    p.strategy.teardown(self.board, self.result)

    def _foul(self, player):
        """foul
        """
        self.display.foul(player)
        winner = self.white_player if player.color == self.black_player.color else self.black_player
        self._win(winner)

    def _judge(self):
        """judge
        """
        black_num, white_num = self.board._black_score, self.board._white_score

        if black_num == white_num:
            self._draw()
        else:
            winner = self.black_player if black_num > white_num else self.white_player
            self._win(winner)

    def _win(self, player):
        """win
        """
        self.display.win(player)
        winlose = Game.BLACK_WIN if player.color == self.black_player.color else Game.WHITE_WIN
        self._store_result(winlose)

    def _draw(self):
        """draw
        """
        self.display.draw()
        self._store_result(Game.DRAW)

    def _store_result(self, winlose):
        """store_result
        """
        self.result = GameResult(
            winlose,
            self.black_player.name, self.white_player.name,
            self.board._black_score, self.board._white_score,
        )


class GameResult:
    """GameResult
    """
    def __init__(self, winlose, black_name, white_name, black_num, white_num):
        self.winlose = winlose
        self.black_name = black_name
        self.white_name = white_name
        self.black_num = black_num
        self.white_num = white_num
