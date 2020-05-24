#!/usr/bin/env python
"""Reversi Simulator

    This simulator simulates AI-players matches and displays the results.

    Args:
        players (hash)     : all of pair of plyaer names and strategies
        setting file(json) : json file for simulator setting

    simulator_setting.json format:
        board_size     : select board size (even number from 4 to 26)
        board_type     : bitboard or board (bitboard is faster than board)
        matches        : number of matches
        processes      : number of distributed processing
        random_opening : number of turns in the early stages of random moves
        characters     : array of player names to play against
"""

import timeit
from reversi import Simulator, strategies


if __name__ == '__main__':
    simulator = Simulator(
        {
            # ↓↓↓↓↓ Add players here ↓↓↓↓↓
            'Unselfish': strategies.Unselfish(),
            'Random': strategies.Random(),
            'Greedy': strategies.Greedy(),
            'SlowStarter': strategies.SlowStarter(),
            'Table': strategies.Table(),
            'MonteCarlo': strategies.MonteCarlo1000(),
            'MinMax': strategies.MinMax2_TPW(),
            'NegaMax': strategies.NegaMax3_TPW(),
            'AlphaBeta': strategies.AlphaBeta4_TPW(),
            'Joseki': strategies.AlphaBeta4J_TPW(),
            'FullReading': strategies.AlphaBeta4F9J_TPW(),
            'Iterative': strategies.AbIF9J_B_TPW(),
            'Edge': strategies.AbIF9J_B_TPWE(),
            # ↑↑↑↑↑ Add players here ↑↑↑↑↑
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
