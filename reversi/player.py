"""Player
"""

from reversi.disc import DiscFactory


class Player:
    """Player
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
        """put_disc
        """
        self.move = self.strategy.next_move(self.color, board)   # decide next move by strategy
        self.captures =  board.put_disc(self.color, *self.move)  # put disc on board
