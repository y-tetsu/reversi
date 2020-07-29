"""AlphaBeta Strategy

    This is a example of alpha-beta reversi strategy.

    In the <strategy.AlphaBeta>,
    the alpha-beta method is used to select the best move by reading the board
    up to the specified depth according to the specified evaluation method.

    This is an example of reading 4 moves ahead and selecting a move
    evaluating board by TableScorer, PossibilityScorer and WinLoseScorer.

    Arg:
        depth     : depth of reading the move
        evaluator : how to calculate the evaluation value of the board

    Evaluator:
        This will return the score by any Scorers.

        Arg:
            separated : list of Scorer. Scorers in this list return score separatedly.
            comibined : list of Scorer. Scorers in this list return comibined score.

    TableScorer:
        This will return the table weighted score.

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

    PossibilityScorer:
        This will return the possible number of moves weighted score.

        Arg:
            w : possible number of moves weight

    WinLoseScorer:
        This will return the possitive score if player win,
        or when lose, return the negative socre, otherwise return None.

        Arg:
            w : winlose weight
"""

from reversi import Reversi
from reversi.strategies import AlphaBeta
from reversi.strategies.coordinator import Evaluator, TableScorer, PossibilityScorer, WinLoseScorer


Reversi(
    {
        'AlphaBeta': AlphaBeta(
            depth=4,
            evaluator=Evaluator(
                separated=[
                    WinLoseScorer(
                        w=10000,
                    ),
                ],
                combined=[
                    TableScorer(
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
                    PossibilityScorer(
                        w=5,
                    ),
                ],
            ),
        ),
    }
).start()
