from ... import cy


SLOW_MODE = True
MONTECARLO_SIZE8_64BIT_ERROR = True


if cy.IMPORTED:
    from ...cy.ReversiMethods import playout
    from ...cy.ReversiMethods import montecarlo_next_move as next_move
    SLOW_MODE = False
    MONTECARLO_SIZE8_64BIT_ERROR = False


__all__ = [
    'playout',
    'next_move',
]
