from .... import cy


SLOW_MODE = True


if cy.IMPORTED:
    from ....cy.ReversiMethods import get_blank_score
    SLOW_MODE = False
else:
    from ....strategies.coordinator.ScorerMethods.GetScore import get_blank_score


__all__ = [
    'get_blank_score',
]
