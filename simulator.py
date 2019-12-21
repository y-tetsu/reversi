#!/usr/bin/env python
"""
オセロシミュレーター
"""

import itertools
from multiprocessing import Pool

from game import Game
from board import Board, BitBoard
from display import NoneDisplay
from measure import Measure


class Simulator:
    """
    ゲームをシミュレーションする
    """
    def __init__(self, black_players, white_players, matches, board_size=8, board_type='bitboard', processes=1):
        self.black_players = black_players
        self.white_players = white_players
        self.matches = matches
        self.board_size = board_size
        self.board_type = board_type
        self.processes = processes
        self.game_results = []
        self.total = []

    def __str__(self):
        board_size = '\nSize : ' + str(self.board_size) + '\n'
        header1 = '                | ' + ' '.join([f'{key:15s}' for key in self.total]) + '\n'
        hr1 = '-'*18 + '-'*15*len(self.total) + '-'*(len(self.total)-1) + '\n'

        body1 = ''
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

            body1 += f'{row}\n'

        header2 = '                | Total  | Win   Lose  Draw  Match\n'
        hr2 = '--------------------------------------------------\n'

        body2 = ''
        for key1 in self.total:
            row = f'{key1:15s} | '
            wins, draws, matches = 0, 0, 0

            for key2 in self.total:
                if key1 == key2:
                    continue

                wins += self.total[key1][key2]['wins']
                draws += self.total[key1][key2]['draws']
                matches += self.total[key1][key2]['matches']
                ratio = self.total[key1][key2]['wins'] / self.total[key1][key2]['matches'] * 100
                ratio = f'{ratio:3.1f}%'

            ratio = wins / matches * 100
            ratio = f'{ratio:3.1f}%'
            loses = matches - wins - draws
            row += f'{ratio:>6s} | {wins:>5d} {loses:>5d} {draws:>5d} {matches:>5d}'
            body2 += f'{row}\n'

        return board_size + header1 + hr1 + body1 + hr1 + '\n' + header2 + hr2 + body2 + hr2

    def start(self):
        """
        シミュレーションを開始する
        """
        print('processes', self.processes)

        if self.processes > 1:
            with Pool(processes=self.processes) as pool:
                ret = pool.map(self._game_play, itertools.product(self.black_players, self.white_players))
                self.game_results = list(itertools.chain.from_iterable(ret))  # 1次元配列に展開する
        else:
            for players in itertools.product(self.black_players, self.white_players):
                self.game_results += self._game_play(players)

        self._totalize_results()

    def _game_play(self, players):
        """
        ゲームを実行
        """
        black, white = players

        if black.name == white.name:
            return []

        print(black.name, white.name)

        ret = []

        for _ in range(self.matches):
            board = BitBoard(self.board_size) if self.board_type == 'bitboard' else Board(self.board_size)

            game = Game(board, black, white, NoneDisplay())
            game.play()

            ret.append(game.result)

        return ret

    def _totalize_results(self):
        """
        結果の集計

        """
        total = {}

        for result in self.game_results:
            if result:
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
            "processes": 1,
            "characters": [
                "Unselfish",
                "Random",
                "Greedy",
                "SlowStarter",
                "Table",
            ]
        }

    strategy_list = {
        'Unselfish': strategies.Unselfish(),
        'Random': strategies.Random(),
        'Greedy': strategies.Greedy(),
        'SlowStarter': strategies.SlowStarter(),
        'Table': strategies.Table(),
        'MinMax1': strategies.MinMax1(),
        'MinMax2': strategies.MinMax2(),
        'MinMax3': strategies.MinMax3(),
        'MinMax4': strategies.MinMax4(),
        'NegaMax1': strategies.NegaMax1(),
        'NegaMax2': strategies.NegaMax2(),
        'NegaMax3': strategies.NegaMax3(),
        'NegaMax4': strategies.NegaMax4(),
        'AlphaBeta1': strategies.AlphaBeta1(),
        'AlphaBeta2': strategies.AlphaBeta2(),
        'AlphaBeta3': strategies.AlphaBeta3(),
        'AlphaBeta4': strategies.AlphaBeta4(),
        'AlphaBeta5': strategies.AlphaBeta5(),
        'AB_T1': strategies.AB_T1(),
        'AB_T2': strategies.AB_T2(),
        'AB_T3': strategies.AB_T3(),
        'AB_T4': strategies.AB_T4(),
        'AB_T5': strategies.AB_T5(),
        'AB_TI': strategies.AB_TI(),
    }

    black_players = [Player('black', c, strategy_list[c]) for c in setting['characters']]
    white_players = [Player('white', c, strategy_list[c]) for c in setting['characters']]

    simulator = Simulator(
        black_players,
        white_players,
        setting['matches'],
        setting['board_size'],
        setting['board_type'],
        setting['processes']
    )

    elapsed_time = timeit.timeit('simulator.start()', globals=globals(), number=1)
    print(simulator, elapsed_time, '(s)')

    if setting['processes'] == 1:
        keys = Measure.elp_time.keys()
        for key in keys:
            print()
            print(key)
            print(' min :', Measure.elp_time[key]['min'], '(s)')
            print(' max :', Measure.elp_time[key]['max'], '(s)')
            print(' ave :', Measure.elp_time[key]['ave'], '(s)')
