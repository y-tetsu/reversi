import pyximport
pyximport.install()


SLOW_MODE = True

try:
    from ...strategies.TableMethods.GetScoreFast import get_score, get_score_measure, get_score_timer, get_score_measure_timer
    SLOW_MODE = False
except ImportError:
    from ...strategies.AlphaBetaMethods.GetScore import get_score, get_score_measure, get_score_timer, get_score_measure_timer


__all__ = [
    'get_score',
    'get_score_measure',
    'get_score_timer',
    'get_score_measure_timer',
]
