"""Player
"""

from reversi.disc import D as d


class Player:
    """Player
    """
    def __init__(self, color, name, strategy):
        self.color = color
        self.disc = d[color]
        self.name = name
        self.strategy = strategy
        self.move = (None, None)
        self.captures = []

    def __str__(self):
        return self.disc + self.name

    def put_disc(self, board):
        """put_disc
        """
        self.move = self.strategy.next_move(self.color, board)  # decide next move by strategy
        captures = board.put_disc(self.color, *self.move)  # put disc on board

        # bits to array
        self.captures.clear()
        size = board.size
        mask = 1 << (size*size-1)
        for y in range(size):
            for x in range(size):
                if captures & mask:
                    self.captures += [(x, y)]
                mask >>= 1
