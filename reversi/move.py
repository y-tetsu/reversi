"""Move
"""


LOWER = 'lower'


class Move:
    """Move"""
    def __init__(self, case=LOWER):
        self.case = case

    def to_xy(self, str_move):
        str_move = list(str_move.lower())
        # TODO: add len check for str_move
        x = ord(str_move.pop(0)) - ord('a')
        y = int("".join(str_move)) - 1
        # TODO: add range check for x, y
        return (x, y)

    def to_str(self, x, y):
        # TODO: add range check for x, y
        key = 'a' if self.case == LOWER else 'A'
        return chr(ord(key) + x) + str(y + 1)


M = Move()
