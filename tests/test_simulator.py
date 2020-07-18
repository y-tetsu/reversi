"""Tests of simulator.py
"""

import unittest
from test.support import captured_stdout
import os
import json

from reversi import Simulator
from reversi.strategies import Unselfish, Random, Greedy, SlowStarter, Table, RandomOpening, _AlphaBeta
from reversi.strategies.coordinator import Evaluator_TPW


class TestSimulator(unittest.TestCase):
    """simulator
    """
    def test_simulator_init(self):
        # No Setting File
        players_info = {
            'Unselfish': Unselfish(),
            'Random': Random(),
            'Greedy': Greedy(),
            'SlowStarter': SlowStarter(),
            'Table': Table(),
        }
        simulator = Simulator(players_info, 'No Setting File')

        self.assertEqual(simulator.matches, 10)
        self.assertEqual(simulator.board_size, 8)
        self.assertEqual(simulator.board_type, "bitboard")
        self.assertEqual(simulator.processes, 1)
        self.assertEqual(simulator.random_opening, 8)

        for index, strategy in enumerate(players_info.keys()):
            self.assertEqual(simulator.black_players[index].name, strategy)
            self.assertIsInstance(simulator.black_players[index].strategy, RandomOpening)
            self.assertEqual(simulator.black_players[index].strategy.depth, 8)
            self.assertIsInstance(simulator.black_players[index].strategy.base, type(players_info[strategy]))
            self.assertEqual(simulator.white_players[index].name, strategy)
            self.assertIsInstance(simulator.white_players[index].strategy, RandomOpening)
            self.assertEqual(simulator.white_players[index].strategy.depth, 8)
            self.assertIsInstance(simulator.white_players[index].strategy.base, type(players_info[strategy]))

        self.assertEqual(simulator.game_results, [])
        self.assertEqual(simulator.total, [])
        self.assertEqual(simulator.result_ratio, {})

        # Setting File
        json_file = './simulator_setting.json'
        simulator_setting = {
            "board_size": 4,
            "matches": 100,
            "processes": 2,
            "random_opening": 0,
        }
        with open(json_file, 'w') as f:
            json.dump(simulator_setting, f)

        players_info = {
            'Unselfish': Unselfish(),
            'Random': Random(),
        }
        simulator = Simulator(players_info, json_file)

        os.remove(json_file)

        self.assertEqual(simulator.matches, 100)
        self.assertEqual(simulator.board_size, 4)
        self.assertEqual(simulator.board_type, "bitboard")
        self.assertEqual(simulator.processes, 2)
        self.assertEqual(simulator.random_opening, 0)

        for index, strategy in enumerate(players_info.keys()):
            self.assertEqual(simulator.black_players[index].name, strategy)
            self.assertIsInstance(simulator.black_players[index].strategy, type(players_info[strategy]))
            self.assertEqual(simulator.white_players[index].name, strategy)
            self.assertIsInstance(simulator.white_players[index].strategy, type(players_info[strategy]))

        self.assertEqual(simulator.game_results, [])
        self.assertEqual(simulator.total, [])
        self.assertEqual(simulator.result_ratio, {})

    def test_simulator_str(self):
        json_file = './simulator_setting.json'
        simulator_setting = {
            "board_size": 4,
            "matches": 5,
            "processes": 1,
            "random_opening": 0,
        }
        with open(json_file, 'w') as f:
            json.dump(simulator_setting, f)

        players_info = {
            'AlphaBeta1': _AlphaBeta(depth=2, evaluator=Evaluator_TPW()),
            'AlphaBeta2': _AlphaBeta(depth=2, evaluator=Evaluator_TPW()),
        }
        simulator = Simulator(players_info, json_file)
        os.remove(json_file)

        with captured_stdout() as stdout:
            simulator.start()
            print(simulator)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "processes 1")
        self.assertEqual(lines[1], "AlphaBeta1 AlphaBeta2")
        self.assertEqual(lines[2], "    - AlphaBeta1 AlphaBeta2 5")
        self.assertEqual(lines[3], "AlphaBeta2 AlphaBeta1")
        self.assertEqual(lines[4], "    - AlphaBeta2 AlphaBeta1 5")
        self.assertEqual(lines[5], "")
        self.assertEqual(lines[6], "Size : 4")
        self.assertEqual(lines[7], "                          | AlphaBeta1                AlphaBeta2               ")
        self.assertEqual(lines[8], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[9], "AlphaBeta1                | ------                     50.0%                    ")
        self.assertEqual(lines[10], "AlphaBeta2                |  50.0%                    ------                    ")
        self.assertEqual(lines[11], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[12], "")
        self.assertEqual(lines[13], "                          | Total  | Win   Lose  Draw  Match")
        self.assertEqual(lines[14], "------------------------------------------------------------")
        self.assertEqual(lines[15], "AlphaBeta1                |  50.0% |     5     5     0    10")
        self.assertEqual(lines[16], "AlphaBeta2                |  50.0% |     5     5     0    10")
        self.assertEqual(lines[17], "------------------------------------------------------------")
