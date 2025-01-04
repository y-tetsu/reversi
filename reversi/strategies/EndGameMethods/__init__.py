from ... import cy


ENDGAME_SIZE8_64BIT_ERROR = True


if cy.IMPORTED:
    from ...cy.ReversiMethods import endgame_next_move as next_move
    from ...cy.ReversiMethods import endgame_get_best_move as get_best_move
    ENDGAME_SIZE8_64BIT_ERROR = False


__all__ = [
    'next_move',
    'get_best_move',
]
