#!/usr/bin/env python
"""Table Strategy

    This is a example of table reversi strategy.

    In the <strategy.Table>,
    the evaluation value is calculated by multiplying the weighted table on the board
    and the disk on the board. The highest one will be chosen next move.

    Arg:
        corner : corner weight
        c      : c weight
        a1     : a1 weight
        a2     : a2 weight
        b1     : b1 weight
        b2     : b2 weight
        b3     : b3 weight
        x      : x weight
        o1     : o1 weight
        o2     : o2 weight

    Table position is below.

    (size=8)
    ---------------------------------------------------------
    |corner|  c   |  a2  |  b3  |  b3  |  a2  |  c   |corner|
    ---------------------------------------------------------
    |  c   |  x   |  o1  |  o2  |  o2  |  o1  |  x   |  c   |
    ---------------------------------------------------------
    |  a2  |  o1  |  a1  |  b2  |  b2  |  a1  |  o1  |  a2  |
    ---------------------------------------------------------
    |  b3  |  o2  |  b2  |  b1  |  b1  |  b2  |  o2  |  b3  |
    ---------------------------------------------------------
    |  b3  |  o2  |  b2  |  b1  |  b1  |  b2  |  o2  |  b3  |
    ---------------------------------------------------------
    |  a2  |  o1  |  a1  |  b2  |  b2  |  a1  |  o1  |  a2  |
    ---------------------------------------------------------
    |  c   |  x   |  o1  |  o2  |  o2  |  o1  |  x   |  c   |
    ---------------------------------------------------------
    |corner|  c   |  a2  |  b3  |  b3  |  a2  |  c   |corner|
    ---------------------------------------------------------
"""

from reversi import Reversi
from reversi.strategies import Table


if __name__ == '__main__':
    Reversi(
        {
            'Table': Table(
                corner=50,
                c=-20,
                a1=0,
                a2=-1,
                b1=-1,
                b2=-1,
                b3=-1,
                x=-25,
                o1=-5,
                o2=-5,
            ),
        }
    ).start()
