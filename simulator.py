#!/usr/bin/env python
"""
オセロシミュレーター
"""

import itertools
from game import Game
from board import Board, BitBoard
from display import NoneDisplay


class Simulator:
    """
    ゲームをシミュレーションする
    """
    def __init__(self, black_players, white_players, matches, board_size=8, board_type='bitboard'):
        self.black_players = black_players
        self.white_players = white_players
        self.matches = matches
        self.board_size = board_size
        self.board_type = board_type
        self.game_results = []
        self.total = []

    def __str__(self):
        board_size = '\nSize : ' + str(self.board_size) + '\n'
        header = '                | ' + ' '.join([f'{key:15s}' for key in self.total]) + ' | Total  | Win   Lose  Draw  Match\n'
        hr = '----------------------------------------------------------------------------------------------------\n'

        body = ''
        for key1 in self.total:
            row = f'{key1:15s} | '
            wins, draws, matches = 0, 0, 0

            for key2 in self.total:
                if key1 == key2:
                    row += '------          '
                    continue

                wins += self.total[key1][key2]['wins']
                draws += self.total[key1][key2]['draws']
                matches += self.total[key1][key2]['matches']
                ratio = self.total[key1][key2]['wins'] / self.total[key1][key2]['matches'] * 100
                ratio = f'{ratio:3.1f}%'
                row += f'{ratio:>6s}          '

            row += '| '
            ratio = wins / matches * 100
            ratio = f'{ratio:3.1f}%'
            loses = matches - wins - draws
            row += f'{ratio:>6s} | {wins:>5d} {loses:>5d} {draws:>5d} {matches:>5d}'
            body += f'{row}\n'

        return board_size + header + hr + body + hr

    def start(self):
        """
        シミュレーションを開始する
        """
        for black_player, white_player in itertools.product(self.black_players, self.white_players):
            if black_player.name == white_player.name:
                continue

            for _ in range(self.matches):
                board = BitBoard(self.board_size) if self.board_type == 'bitboard' else Board(self.board_size)

                game = Game(board, black_player, white_player, NoneDisplay())
                game.play()
                self.game_results.append(game.result)

        self._totalize_results()

    def _totalize_results(self):
        """
        結果の集計

        """
        total = {}

        for result in self.game_results:
            winlose = result.winlose
            black_name = result.black_name
            white_name = result.white_name

            if black_name not in total:
                total[black_name] = {}

            if white_name not in total[black_name]:
                total[black_name][white_name] = {'matches': 0, 'wins': 0, 'draws': 0}

            if winlose == Game.BLACK_WIN:
                total[black_name][white_name]['wins'] += 1
            elif winlose == Game.DRAW:
                total[black_name][white_name]['draws'] += 1

            total[black_name][white_name]['matches'] += 1

            if white_name not in total:
                total[white_name] = {}

            if black_name not in total[white_name]:
                total[white_name][black_name] = {'matches': 0, 'wins': 0, 'draws': 0}

            if winlose == Game.WHITE_WIN:
                total[white_name][black_name]['wins'] += 1
            elif winlose == Game.DRAW:
                total[white_name][black_name]['draws'] += 1

            total[white_name][black_name]['matches'] += 1

        self.total = total


if __name__ == '__main__':
    import timeit
    import os
    import json
    from player import Player
    import strategies

    setting_file, setting = './setting.json', {}

    if os.path.isfile(setting_file):
        with open(setting_file) as f:
            setting = json.load(f)
    else:
        setting = {
            "board_size": 8,
            "board_type": "bitboard",
            "matches": 10,
            "characters": [
                "Unselfish",
                "Random",
                "Greedy",
                "SlowStarter",
                "Table"
            ]
        }

    strategy_list = {
        'Unselfish': strategies.Unselfish(),
        'Random': strategies.Random(),
        'Greedy': strategies.Greedy(),
        'SlowStarter': strategies.SlowStarter(),
        'Table': strategies.Table(),
    }

    black_players = [Player('black', c, strategy_list[c]) for c in setting['characters']]
    white_players = [Player('white', c, strategy_list[c]) for c in setting['characters']]

    simulator = Simulator(black_players, white_players, setting['matches'], setting['board_size'], setting['board_type'])

    elapsed_time = timeit.timeit('simulator.start()', globals=globals(), number=1)
    print(simulator, elapsed_time, '(s)')
