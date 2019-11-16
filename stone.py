#!/usr/bin/env python
"""
オセロの石
"""


class Stone(str):
    """
    石の基底クラス
    """
    __slots__ = ()  # データを持たない


class Black(Stone):
    pass


class White(Stone):
    pass


class Blank(Stone):
    pass


class StoneFactory:
    """
    石ファクトリ
    """
    def create(self, color):
        """
        石オブジェクトを生成する
        """
        ret = ''

        if color == 'black':
            ret = Black('〇')
        elif color == 'white':
            ret = White('●')
        elif color == 'blank':
            ret = Blank('□')

        return ret


if __name__ == '__main__':
    from collections import namedtuple

    factory = StoneFactory()

    CheckStone = namedtuple('CheckStone', 'color cls mark')
    black = CheckStone('black', Black, '〇')
    white = CheckStone('white', White, '●')
    blank = CheckStone('blank', Blank, '□')

    for check in (black, white, blank):
        obj = factory.create(check.color)
        print(type(obj), obj)
        assert isinstance(obj, check.cls)
        assert obj == check.mark
