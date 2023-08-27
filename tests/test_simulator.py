"""Tests of simulator.py
"""

import unittest
from test.support import captured_stdout
import os
import sys
import io
import json

from reversi import Simulator
from reversi.strategies import AbstractStrategy, Unselfish, Random, Greedy, SlowStarter, Table, RandomOpening, _AlphaBeta
from reversi.strategies.coordinator import Evaluator_TPW


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


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
        self.assertEqual(simulator.parallel, "player")
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

        # Setting File1
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

        # Setting File2
        json_file = './simulator_setting.json'
        simulator_setting = {
            "board_size": 12,
            "board_type": 'board',
            "matches": 500,
            "processes": 1,
            "random_opening": 4,
            "player_names": [
                "Random",
                "Table",
            ]
        }
        with open(json_file, 'w') as f:
            json.dump(simulator_setting, f)

        players_info = {
            'Unselfish': Unselfish(),
            'Random': Random(),
            'Greedy': Greedy(),
            'Table': Table(),
        }
        simulator = Simulator(players_info, json_file)

        os.remove(json_file)

        self.assertEqual(simulator.matches, 500)
        self.assertEqual(simulator.board_size, 12)
        self.assertEqual(simulator.board_type, "board")
        self.assertEqual(simulator.processes, 1)
        self.assertEqual(simulator.random_opening, 4)
        self.assertEqual(len(simulator.black_players), 2)
        self.assertEqual(len(simulator.white_players), 2)
        self.assertEqual(simulator.black_players[0].name, "Random")
        self.assertEqual(simulator.white_players[0].name, "Random")
        self.assertEqual(simulator.black_players[1].name, "Table")
        self.assertEqual(simulator.white_players[1].name, "Table")
        self.assertIsInstance(simulator.black_players[0].strategy.base, type(Random()))
        self.assertIsInstance(simulator.white_players[0].strategy.base, type(Random()))
        self.assertIsInstance(simulator.black_players[1].strategy.base, type(Table()))
        self.assertIsInstance(simulator.white_players[1].strategy.base, type(Table()))
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

    def test_simulator_draw(self):
        json_file = './simulator_setting.json'
        simulator_setting = {
            "board_size": 4,
            "matches": 10,
            "processes": 1,
            "random_opening": 0,
        }
        with open(json_file, 'w') as f:
            json.dump(simulator_setting, f)

        class Draw(AbstractStrategy):
            def next_move(self, color, board):
                depth = board._black_score + board._white_score - 4
                move = None
                if depth == 0:
                    move = (1, 0)
                elif depth == 1:
                    move = (0, 0)
                elif depth == 2:
                    move = (0, 1)
                elif depth == 3:
                    move = (0, 2)
                elif depth == 4:
                    move = (0, 3)
                elif depth == 5:
                    move = (2, 3)
                elif depth == 6:
                    move = (1, 3)
                elif depth == 7:
                    move = (2, 0)
                elif depth == 8:
                    move = (3, 3)
                elif depth == 9:
                    move = (3, 2)
                elif depth == 10:
                    move = (3, 0)
                elif depth == 11:
                    move = (3, 1)

                return move

        players_info = {
            'Draw1': Draw(),
            'Draw2': Draw(),
        }
        simulator = Simulator(players_info, json_file)

        os.remove(json_file)

        with captured_stdout() as stdout:
            simulator.start()
            print(simulator)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "processes 1")
        self.assertEqual(lines[1], "Draw1 Draw2")
        self.assertEqual(lines[2], "    - Draw1 Draw2 5")
        self.assertEqual(lines[3], "    - Draw1 Draw2 10")
        self.assertEqual(lines[4], "Draw2 Draw1")
        self.assertEqual(lines[5], "    - Draw2 Draw1 5")
        self.assertEqual(lines[6], "    - Draw2 Draw1 10")
        self.assertEqual(lines[7], "")
        self.assertEqual(lines[8], "Size : 4")
        self.assertEqual(lines[9], "                          | Draw1                     Draw2                    ")
        self.assertEqual(lines[10], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[11], "Draw1                     | ------                      0.0%                    ")
        self.assertEqual(lines[12], "Draw2                     |   0.0%                    ------                    ")
        self.assertEqual(lines[13], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[14], "")
        self.assertEqual(lines[15], "                          | Total  | Win   Lose  Draw  Match")
        self.assertEqual(lines[16], "------------------------------------------------------------")
        self.assertEqual(lines[17], "Draw1                     |   0.0% |     0     0    20    20")
        self.assertEqual(lines[18], "Draw2                     |   0.0% |     0     0    20    20")
        self.assertEqual(lines[19], "------------------------------------------------------------")

    def test_simulator_multi_process(self):
        json_file = './simulator_setting.json'
        simulator_setting = {
            "board_size": 4,
            "matches": 5,
            "processes": 2,
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
        self.assertEqual(lines[0], "processes 2")
        self.assertEqual(lines[1], "")
        self.assertEqual(lines[2], "Size : 4")
        self.assertEqual(lines[3], "                          | AlphaBeta1                AlphaBeta2               ")
        self.assertEqual(lines[4], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[5], "AlphaBeta1                | ------                     50.0%                    ")
        self.assertEqual(lines[6], "AlphaBeta2                |  50.0%                    ------                    ")
        self.assertEqual(lines[7], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[8], "")
        self.assertEqual(lines[9], "                          | Total  | Win   Lose  Draw  Match")
        self.assertEqual(lines[10], "------------------------------------------------------------")
        self.assertEqual(lines[11], "AlphaBeta1                |  50.0% |     5     5     0    10")
        self.assertEqual(lines[12], "AlphaBeta2                |  50.0% |     5     5     0    10")
        self.assertEqual(lines[13], "------------------------------------------------------------")

    def test_simulator_multi_process_parallel_by_game(self):
        json_file = './simulator_setting2.json'
        simulator_setting = {
            "board_size": 4,
            "matches": 5,
            "processes": 2,
            "parallel": "game",
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
        self.assertEqual(lines[0], "processes 2")
        self.assertEqual(lines[1], "")
        self.assertEqual(lines[2], "Size : 4")
        self.assertEqual(lines[3], "                          | AlphaBeta1                AlphaBeta2               ")
        self.assertEqual(lines[4], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[5], "AlphaBeta1                | ------                     50.0%                    ")
        self.assertEqual(lines[6], "AlphaBeta2                |  50.0%                    ------                    ")
        self.assertEqual(lines[7], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[8], "")
        self.assertEqual(lines[9], "                          | Total  | Win   Lose  Draw  Match")
        self.assertEqual(lines[10], "------------------------------------------------------------")
        self.assertEqual(lines[11], "AlphaBeta1                |  50.0% |     5     5     0    10")
        self.assertEqual(lines[12], "AlphaBeta2                |  50.0% |     5     5     0    10")
        self.assertEqual(lines[13], "------------------------------------------------------------")

    def test_simulator_white_win(self):
        json_file = './simulator_setting.json'
        simulator_setting = {
            "board_size": 4,
            "matches": 10,
            "processes": 1,
            "random_opening": 0,
        }
        with open(json_file, 'w') as f:
            json.dump(simulator_setting, f)

        class WhiteWin(AbstractStrategy):
            done = False
            def next_move(self, color, board):
                depth = board._black_score + board._white_score - 4
                move = None
                if depth == 0:
                    move = (1, 0)
                elif depth == 1:
                    move = (0, 0)
                elif depth == 2:
                    move = (0, 1)
                elif depth == 3:
                    move = (2, 0)
                elif depth == 4:
                    move = (3, 0)
                elif depth == 5:
                    move = (0, 2)
                elif depth == 6:
                    move = (0, 3)
                elif depth == 7:
                    move = (3, 2)
                elif depth == 8:
                    move = (2, 3)

                return move

            def get_result(self, result):
                if not self.done:
                    print(result.winlose)
                    self.done = True

        players_info = {
            'WhiteWin1': WhiteWin(),
            'WhiteWin2': WhiteWin(),
        }
        simulator = Simulator(players_info, json_file)

        os.remove(json_file)

        with captured_stdout() as stdout:
            simulator.start()
            print(simulator)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "processes 1")
        self.assertEqual(lines[1], "WhiteWin1 WhiteWin2")
        self.assertEqual(lines[2], "1")
        self.assertEqual(lines[3], "1")
        self.assertEqual(lines[4], "    - WhiteWin1 WhiteWin2 5")
        self.assertEqual(lines[5], "    - WhiteWin1 WhiteWin2 10")
        self.assertEqual(lines[6], "WhiteWin2 WhiteWin1")
        self.assertEqual(lines[7], "    - WhiteWin2 WhiteWin1 5")
        self.assertEqual(lines[8], "    - WhiteWin2 WhiteWin1 10")
        self.assertEqual(lines[9], "")
        self.assertEqual(lines[10], "Size : 4")
        self.assertEqual(lines[11], "                          | WhiteWin1                 WhiteWin2                ")
        self.assertEqual(lines[12], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[13], "WhiteWin1                 | ------                     50.0%                    ")
        self.assertEqual(lines[14], "WhiteWin2                 |  50.0%                    ------                    ")
        self.assertEqual(lines[15], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[16], "")
        self.assertEqual(lines[17], "                          | Total  | Win   Lose  Draw  Match")
        self.assertEqual(lines[18], "------------------------------------------------------------")
        self.assertEqual(lines[19], "WhiteWin1                 |  50.0% |    10    10     0    20")
        self.assertEqual(lines[20], "WhiteWin2                 |  50.0% |    10    10     0    20")
        self.assertEqual(lines[21], "------------------------------------------------------------")

    def test_simulator_white_win_parallel_by_game(self):
        json_file = './simulator_setting.json'
        simulator_setting = {
            "board_size": 4,
            "matches": 10,
            "processes": 1,
            "parallel": "game",
            "random_opening": 0,
        }
        with open(json_file, 'w') as f:
            json.dump(simulator_setting, f)

        class WhiteWin(AbstractStrategy):
            done = False
            def next_move(self, color, board):
                depth = board._black_score + board._white_score - 4
                move = None
                if depth == 0:
                    move = (1, 0)
                elif depth == 1:
                    move = (0, 0)
                elif depth == 2:
                    move = (0, 1)
                elif depth == 3:
                    move = (2, 0)
                elif depth == 4:
                    move = (3, 0)
                elif depth == 5:
                    move = (0, 2)
                elif depth == 6:
                    move = (0, 3)
                elif depth == 7:
                    move = (3, 2)
                elif depth == 8:
                    move = (2, 3)

                return move

            def get_result(self, result):
                if not self.done:
                    print(result.winlose)
                    self.done = True


        players_info = {
            'WhiteWin1': WhiteWin(),
            'WhiteWin2': WhiteWin(),
        }
        simulator = Simulator(players_info, json_file)

        os.remove(json_file)

        with captured_stdout() as stdout:
            simulator.start()
            print(simulator)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "processes 1")
        self.assertEqual(lines[1], "WhiteWin1 WhiteWin2 10")
        self.assertEqual(lines[2], "1")
        self.assertEqual(lines[3], "1")
        self.assertEqual(lines[4], "    - WhiteWin1 WhiteWin2 5")
        self.assertEqual(lines[5], "    - WhiteWin1 WhiteWin2 10")
        self.assertEqual(lines[6], "WhiteWin2 WhiteWin1 10")
        self.assertEqual(lines[7], "    - WhiteWin2 WhiteWin1 5")
        self.assertEqual(lines[8], "    - WhiteWin2 WhiteWin1 10")
        self.assertEqual(lines[9], "")
        self.assertEqual(lines[10], "Size : 4")
        self.assertEqual(lines[11], "                          | WhiteWin1                 WhiteWin2                ")
        self.assertEqual(lines[12], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[13], "WhiteWin1                 | ------                     50.0%                    ")
        self.assertEqual(lines[14], "WhiteWin2                 |  50.0%                    ------                    ")
        self.assertEqual(lines[15], "-------------------------------------------------------------------------------")
        self.assertEqual(lines[16], "")
        self.assertEqual(lines[17], "                          | Total  | Win   Lose  Draw  Match")
        self.assertEqual(lines[18], "------------------------------------------------------------")
        self.assertEqual(lines[19], "WhiteWin1                 |  50.0% |    10    10     0    20")
        self.assertEqual(lines[20], "WhiteWin2                 |  50.0% |    10    10     0    20")
        self.assertEqual(lines[21], "------------------------------------------------------------")

    def test_simulator_board_name(self):
        json_file = './simulator_setting.json'
        simulator_setting = {
            "board_name": "Diamond",
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
        with captured_stdout() as stdout:
            simulator = Simulator(players_info, json_file)
        os.remove(json_file)
        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "[Diamond]")
        self.assertEqual(lines[1], "   a b c d e f g h")
        self.assertEqual(lines[2], " 1　　　□□　　　")
        self.assertEqual(lines[3], " 2　　□□□□　　")
        self.assertEqual(lines[4], " 3　□□□□□□　")
        self.assertEqual(lines[5], " 4□□□●〇□□□")
        self.assertEqual(lines[6], " 5□□□〇●□□□")
        self.assertEqual(lines[7], " 6　□□□□□□　")
        self.assertEqual(lines[8], " 7　　□□□□　　")
        self.assertEqual(lines[9], " 8　　　□□　　　")
