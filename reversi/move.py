"""Move
"""


LOWER = 'lower'
UPPER = 'upper'


class Move(tuple):
    """Move"""
    def __new__(cls, *args, case=LOWER):
        x, y = cls._get_xy(*args)
        cls = super().__new__(cls, (x, y))
        return cls

    def __init__(self, *args, case=LOWER):
        self.__x, self.__y = self[:2]
        self.__str = self.to_str(self.__x, self.__y, case=case.lower())
        self.__case = case.lower()

    def __iter__(self):
        return (i for i in (self.__x, self.__y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({}, {}) "{}"'.format(class_name, self.__x, self.__y, self.__str)

    def __str__(self):
        return self.__str

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
        y = int(''.join(str_move)) - 1
        return x, y

    def to_str(self, x, y, case=None):
        if x is None or y is None:
            return ''
        case = case.lower() if case else self.__case
        key = 'a' if case != UPPER else 'A'
        return chr(ord(key) + x) + str(y + 1)


M = Move()
