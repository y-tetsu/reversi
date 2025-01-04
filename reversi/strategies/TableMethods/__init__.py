from ... import cy


SLOW_MODE = True


if cy.IMPORTED:
    from ...cy.ReversiMethods import table_get_score as get_score
    SLOW_MODE = False
else:
    from ...strategies.TableMethods.GetScore import get_score


__all__ = [
    'get_score',
]
