import os
import pyximport
pyximport.install()


SLOW_MODE = True
ALPHABETA_SIZE8_64BIT_ERROR = True

try:
    if 'FORCE_ALPHABETAMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_ALPHABETAMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ...strategies.AlphaBetaMethods.GetScoreFast import get_score, get_score_measure, get_score_timer, get_score_measure_timer
    SLOW_MODE = False
except ImportError:
    from ...strategies.AlphaBetaMethods.GetScore import get_score, get_score_measure, get_score_timer, get_score_measure_timer

try:
    if 'FORCE_ALPHABETAMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_ALPHABETAMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ...strategies.AlphaBetaMethods.NextMoveSize8_64bit import next_move
    ALPHABETA_SIZE8_64BIT_ERROR = False
except ImportError:
    pass


__all__ = [
    'get_score',
    'get_score_measure',
    'get_score_timer',
    'get_score_measure_timer',
    'next_move',
]
