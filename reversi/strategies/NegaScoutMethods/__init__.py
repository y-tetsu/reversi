import os
import pyximport
pyximport.install()


SLOW_MODE = True
NEGASCOUT_SIZE8_64BIT_ERROR = True

try:
    if 'FORCE_NEGASCOUTMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_NEGASCOUTMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ...strategies.NegaScoutMethods.GetScoreFast import get_score, get_score_measure, get_score_timer, get_score_measure_timer
    SLOW_MODE = False
except ImportError:
    from ...strategies.NegaScoutMethods.GetScore import get_score, get_score_measure, get_score_timer, get_score_measure_timer

try:
    if 'FORCE_NEGASCOUTMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_NEGASCOUTMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ...strategies.NegaScoutMethods.NextMoveSize8_64bit import next_move, get_best_move
    NEGASCOUT_SIZE8_64BIT_ERROR = False
except ImportError:
    pass


__all__ = [
    'get_score',
    'get_score_measure',
    'get_score_timer',
    'get_score_measure_timer',
    'next_move',
    'get_best_move',
]
