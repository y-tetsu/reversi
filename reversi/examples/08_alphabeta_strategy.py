"""AlphaBeta Strategy

    This is a example of alpha beta reversi strategy.

    In the <strategy.AlphaBeta>,
    the alpha beta method is used to select the best move by reading the board
    up to the specified depth according to the specified evaluation method.

    This is an example of reading 4 moves ahead and selecting a move
    using the Table strategy's board parameters.

    Arg:
        depth     : depth of reading the move
        evaluator : how to calculate the evaluation value of the board

    Evaluator_TP:
        This will return the results of the evaluation of the Table strategy's board parameters
        and possible number of moves.

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
            wp     : possible number of moves weight
"""

from reversi import Reversi
from reversi.strategies import AlphaBeta
from reversi.strategies.coordinator import Evaluator_TP


if __name__ == '__main__':
    Reversi(
        {
            'AlphaBeta': AlphaBeta(
                depth=4,
                evaluator=Evaluator_TP(
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
                    wp=5,
                ),
            ),
        }
    ).start()
