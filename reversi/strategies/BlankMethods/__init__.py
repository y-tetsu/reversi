from ... import cy


BLANK_SIZE8_64BIT_ERROR = True


if cy.IMPORTED:
    from ...cy.ReversiMethods import blank_next_move as next_move
    from ...cy.ReversiMethods import blank_get_best_move as get_best_move
    BLANK_SIZE8_64BIT_ERROR = False


__all__ = [
    'next_move',
    'get_best_move',
]
