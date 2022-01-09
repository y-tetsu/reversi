"""Move
"""


LOWER = 'lower'


class Move(tuple):
    """Move"""
    def __new__(cls, *args, case=LOWER):
        x, y = cls._get_xy(*args)
        cls = super().__new__(cls, (x, y))
        return cls

    def __init__(self, *args, case=LOWER):
        self.__x, self.__y = self[:2]
        self.__str = self.to_str(self.__x, self.__y, case=case)
        self.__case = case

    def __iter__(self):
        return (i for i in (self.__x, self.__y))

    @classmethod
    def _get_xy(cls, *args):
        x, y = None, None
        if len(args) == 1:
            x, y = cls.to_xy(args[0])
        elif len(args) == 2:
            x, y = args[:2]
        return (x, y)

    @classmethod
    def to_xy(cls, str_move):
        str_move = list(str_move.lower())
        x = ord(str_move.pop(0)) - ord('a')
        y = int("".join(str_move)) - 1
        return x, y

    def to_str(self, x, y, case=None):
        if x is None or y is None:
            return None
        case = case if case else self.__case
        key = 'a' if case == LOWER else 'A'
        return chr(ord(key) + x) + str(y + 1)


M = Move()
