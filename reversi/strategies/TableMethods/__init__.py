import pyximport
pyximport.install()

SLOW_MODE = True

try:
    from reversi.strategies.TableMethods.GetScoreFast import get_score
    SLOW_MODE = False
except ImportError:
    from reversi.strategies.TableMethods.GetScore import get_score
