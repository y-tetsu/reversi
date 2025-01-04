from ... import cy


SLOW_MODE = True
ALPHABETA_SIZE8_64BIT_ERROR = True


if cy.IMPORTED:
    from ...cy.ReversiMethods import alphabeta_get_score as get_score
    from ...cy.ReversiMethods import alphabeta_get_score_measure as get_score_measure
    from ...cy.ReversiMethods import alphabeta_get_score_timer as get_score_timer
    from ...cy.ReversiMethods import alphabeta_get_score_measure_timer as get_score_measure_timer
    from ...cy.ReversiMethods import alphabeta_next_move as next_move
    from ...cy.ReversiMethods import alphabeta_get_best_move as get_best_move
    ALPHABETA_SIZE8_64BIT_ERROR = False
    SLOW_MODE = False
else:
    from ...strategies.AlphaBetaMethods.GetScore import get_score, get_score_measure, get_score_timer, get_score_measure_timer


__all__ = [
    'get_score',
    'get_score_measure',
    'get_score_timer',
    'get_score_measure_timer',
    'next_move',
    'get_best_move',
]
