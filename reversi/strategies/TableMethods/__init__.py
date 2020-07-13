import pyximport
pyximport.install()


SLOW_MODE = True

try:
    from ...strategies.TableMethods.GetScoreFast import get_score
    SLOW_MODE = False
except ImportError:
    from ...strategies.TableMethods.GetScore import get_score


__all__ = [
    'get_score',
]
