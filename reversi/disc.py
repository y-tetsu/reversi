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


class DiscDict(dict):
    """DiscDict"""
    __slots__ = ()

    def __getattr__(self, attr):
        return self.get(attr)

    def is_black(self, disc):
        return disc == self.get(c.black)

    def is_white(self, disc):
        return disc == self.get(c.white)

    def is_blank(self, disc):
        return disc == self.get(c.blank)


factory = DiscFactory()
D = DiscDict({color: factory.create(color) for color in c.all})
