from .... import cy


SLOW_MODE = True


if cy.IMPORTED:
    from ....cy.ReversiMethods import evaluate_tpw, evaluate_tpwe
    SLOW_MODE = False
else:
    from ....strategies.coordinator.EvaluatorMethods.Evaluate import evaluate_tpw, evaluate_tpwe


__all__ = [
    'evaluate_tpw',
    'evaluate_tpwe',
]
