"""Disc
"""


class Disc(str):
    """Disc"""
    __slots__ = ()


class Black(Disc):
    pass


class White(Disc):
    pass


class Blank(Disc):
    pass


class DiscFactory:
    """Disc Factory"""
    def create(self, color):
        """create disc object"""
        ret = ''

        if color == 'black':
            ret = Black('〇')
        elif color == 'white':
            ret = White('●')
        elif color == 'blank':
            ret = Blank('□')

        return ret
