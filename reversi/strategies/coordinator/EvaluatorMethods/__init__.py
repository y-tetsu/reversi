import os
import pyximport
pyximport.install()


SLOW_MODE = True

try:
    if 'FORCE_EVALUATORMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_EVALUATORMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from ....cy.ReversiMethods import evaluate_tpw, evaluate_tpwe
    SLOW_MODE = False
except ImportError:
    from ....strategies.coordinator.EvaluatorMethods.Evaluate import evaluate_tpw, evaluate_tpwe


__all__ = [
    'evaluate_tpw',
    'evaluate_tpwe',
]
