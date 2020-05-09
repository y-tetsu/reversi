#!/usr/bin/env python
"""
対戦シミュレーター
"""

if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import timeit

from reversi import Simulator, strategies


if __name__ == '__main__':
    simulator = Simulator(
        {
            'Unselfish': strategies.Unselfish(),
            'Random': strategies.Random(),
            'Greedy': strategies.Greedy(),
            'SlowStarter': strategies.SlowStarter(),
            'Table': strategies.Table(),
            'MinMax2': strategies.MinMax2(),
            'NegaMax3': strategies.NegaMax3(),
            'AlphaBeta4': strategies.AlphaBeta4(),
            'AB_T4': strategies.AB_T4(),
            'AB_TI': strategies.AB_TI(),
            'MinMax1_T': strategies.MinMax1_T(),
            'MinMax2_T': strategies.MinMax2_T(),
            'MinMax3_T': strategies.MinMax3_T(),
            'MinMax4_T': strategies.MinMax4_T(),
            'MinMax1_TP': strategies.MinMax1_TP(),
            'MinMax2_TP': strategies.MinMax2_TP(),
            'MinMax3_TP': strategies.MinMax3_TP(),
            'MinMax4_TP': strategies.MinMax4_TP(),
            'MinMax1_TPO': strategies.MinMax1_TPO(),
            'MinMax2_TPO': strategies.MinMax2_TPO(),
            'MinMax3_TPO': strategies.MinMax3_TPO(),
            'MinMax4_TPO': strategies.MinMax4_TPO(),
            'MinMax2_TPW': strategies.MinMax2_TPW(),
            'NegaMax3_TPW': strategies.NegaMax3_TPW(),
            'AlphaBeta4_TPW': strategies.AlphaBeta4_TPW(),
            'NegaScout4_TPW': strategies.NegaScout4_TPW(),
            'AbI_B_TPW': strategies.AbI_B_TPW(),
            'MonteCarlo30': strategies.MonteCarlo30(),
            'MonteCarlo100': strategies.MonteCarlo100(),
            'MonteCarlo1000': strategies.MonteCarlo1000(),
            'NsI_B_TPW': strategies.NsI_B_TPW(),
            'NsIF9J_B_TPW': strategies.NsIF9J_B_TPW(),
            'NsIF10_B_TPW': strategies.NsIF10_B_TPW(),
            'NsIF11_B_TPW': strategies.NsIF11_B_TPW(),
            'NsIF12_B_TPW': strategies.NsIF12_B_TPW(),
            'MinMax3Ro_TPW': strategies.MinMax3Ro_TPW(),
            '_NegaMax3Ro_TPW': strategies._NegaMax3Ro_TPW(),
            'NegaMax3Ro_TPW': strategies.NegaMax3Ro_TPW(),
            'AlphaBeta4Ro_TPW': strategies.AlphaBeta4Ro_TPW(),
            'AlphaBeta4JRo_TPW': strategies.AlphaBeta4JRo_TPW(),
            'AlphaBeta4Ro_TPWE': strategies.AlphaBeta4Ro_TPWE(),
            'AlphaBeta4F9Ro_TPW': strategies.AlphaBeta4F9Ro_TPW(),
            'AlphaBeta4F9JRo_TPW': strategies.AlphaBeta4F9JRo_TPW(),
            'NegaScout3Ro_TPW': strategies.NegaScout3Ro_TPW(),
            'NegaScout4Ro_TPW': strategies.NegaScout4Ro_TPW(),
            'NegaScout4Ro_TPWE': strategies.NegaScout4Ro_TPWE(),
            'MinMax1Ro_PWE': strategies.MinMax1Ro_PWE(),
            'MinMax1Ro_TPW': strategies.MinMax1Ro_TPW(),
            'MinMax1Ro_TPWE': strategies.MinMax1Ro_TPWE(),
            'MinMax1Ro_TPWEC': strategies.MinMax1Ro_TPWEC(),
            'MinMax1Ro_TPW2': strategies.MinMax1Ro_TPW2(),
            'MinMax2Ro_T': strategies.MinMax2Ro_T(),
            'MinMax2Ro_TPW': strategies.MinMax2Ro_TPW(),
            'MinMax2Ro_TPWE': strategies.MinMax2Ro_TPWE(),
            'MinMax2Ro_TPWEC': strategies.MinMax2Ro_TPWEC(),
            'MinMax3Ro_T': strategies.MinMax3Ro_T(),
            'MinMax3Ro_TP': strategies.MinMax3Ro_TP(),
            'AB_TI_Ro': strategies.AB_TI_Ro(),
            'AbIRo_B_TPW': strategies.AbI_B_TPW(),
            'NsIRo_B_TPW': strategies.NsI_B_TPW(),
            'AbIF9JRo_B_TPW': strategies.AbIF9JRo_B_TPW(),
            'AbIF9JRo_B_TPWE': strategies.AbIF9JRo_B_TPWE(),
            'AbIF9JRo_B_TPWEC': strategies.AbIF9JRo_B_TPWEC(),
            'NsIF9JRo_B_TPW': strategies.NsIF9JRo_B_TPW(),
            'NsIF9JRo_B_TPW2': strategies.NsIF9JRo_B_TPW2(),
            'NsIF9JRo_B_TPWE': strategies.NsIF9JRo_B_TPWE(),
            'SwitchNsIF9JRo_B_TPW': strategies.SwitchNsIF9JRo_B_TPW(),
            'SwitchNsIF9JRo_B_TPWE': strategies.SwitchNsIF9JRo_B_TPWE(),
            'RandomF11': strategies.RandomF11(),
            'TopLeft': strategies.External('py -3.7 ./extra/python/topleft/topleft.py', 3),
        },
        './simulator_setting.json',
    )

    elapsed_time = timeit.timeit('simulator.start()', globals=globals(), number=1)
    print(simulator, elapsed_time, '(s)')

    if simulator.processes == 1:
        keys = strategies.Measure.elp_time.keys()
        for key in keys:
            print()
            print(key)
            print(' min :', strategies.Measure.elp_time[key]['min'], '(s)')
            print(' max :', strategies.Measure.elp_time[key]['max'], '(s)')
            print(' ave :', strategies.Measure.elp_time[key]['ave'], '(s)')
