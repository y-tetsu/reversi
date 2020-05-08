#!/usr/bin/env python
"""
GUI版リバーシアプリ
"""

if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from reversi import Reversi, strategies


reversi = Reversi(
        {
            'Unselfish': strategies.Unselfish(),
            'Random': strategies.Random(),
            'Greedy': strategies.Greedy(),
            'SlowStarter': strategies.SlowStarter(),
            'Table': strategies.Table(),
            'MonteCarlo': strategies.MonteCarlo1000(),
            'MinMax': strategies.MinMax2_TPW(),
            'NegaMax': strategies.NegaMax3_TPW(),
            'AlphaBeta': strategies.AlphaBeta4_TPW(),
            'Joseki' : strategies.AlphaBeta4J_TPW(),
            'FullReading' : strategies.AlphaBeta4F9J_TPW(),
            'Iterative': strategies.AbIF9J_B_TPW(),
            'Edge': strategies.AbIF9J_B_TPWE(),
        }
)

reversi.start()
