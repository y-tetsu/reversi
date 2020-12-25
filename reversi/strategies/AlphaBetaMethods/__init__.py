import os
import pyximport
pyximport.install()


SLOW_MODE = True

try:
    if 'FORCE_ALPHABETAMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_ALPHABETAMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ...strategies.AlphaBetaMethods.GetScoreFast import get_score, get_score_measure, get_score_timer, get_score_measure_timer
    SLOW_MODE = False
except ImportError:
    from ...strategies.AlphaBetaMethods.GetScore import get_score, get_score_measure, get_score_timer, get_score_measure_timer


__all__ = [
    'get_score',
    'get_score_measure',
    'get_score_timer',
    'get_score_measure_timer',
]
