import os
import pyximport
pyximport.install()


BLANK_SIZE8_64BIT_ERROR = True

try:
    if 'FORCE_BLANKMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_BLANKMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ...cy.StrategiesMethods import blank_next_move as next_move
    from ...cy.StrategiesMethods import blank_get_best_move as get_best_move
    BLANK_SIZE8_64BIT_ERROR = False
except ImportError:
    pass


__all__ = [
    'next_move',
    'get_best_move',
]
