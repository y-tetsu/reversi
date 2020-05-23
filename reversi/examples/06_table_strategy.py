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
        b      : b weight
        x      : x weight
        o      : o weight

    Table position is below.

    (size=8)
    ---------------------------------------------------------
    |corner|  c   |  a2  |  b   |  b   |  a2  |  c   |corner|
    ---------------------------------------------------------
    |  c   |  x   |  o   |  o   |  o   |  o   |  x   |  c   |
    ---------------------------------------------------------
    |  a2  |  o   |  a1  |  b   |  b   |  a1  |  o   |  a2  |
    ---------------------------------------------------------
    |  b   |  o   |  b   |  b   |  b   |  b   |  o   |  b   |
    ---------------------------------------------------------
    |  b   |  o   |  b   |  b   |  b   |  b   |  o   |  b   |
    ---------------------------------------------------------
    |  a2  |  o   |  a1  |  b   |  b   |  a1  |  o   |  a2  |
    ---------------------------------------------------------
    |  c   |  x   |  o   |  o   |  o   |  o   |  x   |  c   |
    ---------------------------------------------------------
    |corner|  c   |  a2  |  b   |  b   |  a2  |  c   |corner|
    ---------------------------------------------------------
"""

from reversi import Reversi, strategies


if __name__ == '__main__':
    Reversi(
        {
            'Table': strategies.Table(
                corner=100,
                c=-20,
                a1=5,
                a2=10,
                b=3,
                x=-30,
                o=-5,
            ),
        }
    ).start()
