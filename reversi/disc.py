"""Disc
"""

from reversi.color import C as c


class Disc(str):
    """Disc"""
    __slots__ = ()


class Green(Disc):
    pass


class Black(Disc):
    pass


class White(Disc):
    pass


class Blank(Disc):
    pass


class Hole(Disc):
    pass


class DiscFactory:
    """Disc Factory"""
    def create(self, color):
        """create disc object"""
        if c.is_green(color):
            return Green('◎')
        elif c.is_black(color):
            return Black('〇')
        elif c.is_white(color):
            return White('●')
        elif c.is_blank(color):
            return Blank('□')
        elif c.is_hole(color):
            return Hole('　')

        return Disc('')


class DiscDictAttributeError(Exception):
    pass


class DiscDict(dict):
    """DiscDict"""
    __slots__ = ()

    def __getattr__(self, attr):
        return self.get(attr)

    def __setitem__(self, key, value):
        raise DiscDictAttributeError("'DiscDict' object does not support item assignment.")

    def __delitem__(self, key):
        raise DiscDictAttributeError("'DiscDict' object does not support item deletion.")

    def is_green(self, disc):
        return disc == self.get(c.green)

    def is_black(self, disc):
        return disc == self.get(c.black)

    def is_white(self, disc):
        return disc == self.get(c.white)

    def is_blank(self, disc):
        return disc == self.get(c.blank)

    def is_hole(self, disc):
        return disc == self.get(c.hole)


factory = DiscFactory()
D = DiscDict({color: factory.create(color) for color in c.all})
