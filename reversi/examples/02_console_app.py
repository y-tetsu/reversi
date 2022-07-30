"""Reversi Console Application

    This is a reversi with various boards that can be played on the console.
"""

from reversi import Reversic, strategies


Reversic(
    {
        'Random': strategies.Random(),
        'SlowStarter': strategies.SlowStarter(),
        'Blank': strategies.SwitchJ_BlankI_EndGame16(),
    },
).start()
