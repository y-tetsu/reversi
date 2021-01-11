"""Disc
"""

from reversi.color import C as c


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
        if c.is_black(color):
            return Black('〇')
        elif c.is_white(color):
            return White('●')
        elif c.is_blank(color):
            return Blank('□')

        return Disc('')


factory = DiscFactory()
D = {color: factory.create(color) for color in c.all}
