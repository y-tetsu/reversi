"""Reversi Console Application

    This is a reversi with various boards that can be played on the console.
"""

from reversi import Reversic, strategies


Reversic(
    {
        'X': strategies.Random(),
        'M-10': strategies.MonteCarlo(count=10),
        'M-100': strategies.MonteCarlo(count=100),
        'M-1000': strategies.MonteCarlo(count=1000),
        'TheEnd': strategies.MonteCarlo_EndGame(count=10000, end=14),
    },
).start()
