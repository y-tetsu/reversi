"""Move
"""


LOWER = 'lower'


class Move:
    """Move"""
    def __init__(self, *args, case=LOWER):
        self.x = None
        self.y = None
        self.str = None
        self.case = case
        if len(args) == 1:
            # TODO: add check if args[0] is str
            self.str = args[0]
            self.x, self.y = self.to_xy(self.str)
        elif len(args) == 2:
            # TODO: add check if args[:2] are int
            self.x, self.y = args[:2]
            self.str = self.to_str(self.x, self.y)
        else:
            # TODO: add raise TypeError
            pass

    def to_xy(self, str_move):
        str_move = list(str_move.lower())
        # TODO: add len check for str_move
        x = ord(str_move.pop(0)) - ord('a')
        y = int("".join(str_move)) - 1
        # TODO: add range check for x, y
        return x, y

    def to_str(self, x, y):
        # TODO: add range check for x, y
        key = 'a' if self.case == LOWER else 'A'
        return chr(ord(key) + x) + str(y + 1)


M = Move()
