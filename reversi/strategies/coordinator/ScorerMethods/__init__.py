import os
import pyximport
pyximport.install()


SLOW_MODE = True

try:
    if 'FORCE_SCORERMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_SCORERMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ....cy.CoordinatorMethods import get_blank_score
    SLOW_MODE = False
except ImportError:
    from ....strategies.coordinator.ScorerMethods.GetScore import get_blank_score


__all__ = [
    'get_blank_score',
]
