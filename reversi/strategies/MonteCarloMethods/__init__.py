import os
import pyximport
pyximport.install()


SLOW_MODE = True
MONTECARLO_SIZE8_64BIT_ERROR = True


try:
    if 'FORCE_MONTECARLOMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_MONTECARLOMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ...strategies.MonteCarloMethods.PlayoutSize8_64bit import playout
    SLOW_MODE = False
    MONTECARLO_SIZE8_64BIT_ERROR = False
except ImportError:
    pass


__all__ = [
    'playout',
]
