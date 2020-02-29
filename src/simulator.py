#!/usr/bin/env python
"""
対戦シミュレーター
"""

import itertools
from multiprocessing import Pool

from game import Game
from board import Board, BitBoard
from display import NoneDisplay


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
        header1 = '                          | ' + ' '.join([f'{key:25s}' for key in self.total]) + '\n'
        hr1 = '-'*25 + '---' + '-'*25*len(self.total) + '-'*(len(self.total)-1) + '\n'

        body1 = ''
        for key1 in self.total:
            row = f'{key1:25s} | '
            wins, draws, matches = 0, 0, 0

            for key2 in self.total:
                if key1 == key2:
                    row += '------                    '
                    continue

                wins += self.total[key1][key2]['wins']
                draws += self.total[key1][key2]['draws']
                matches += self.total[key1][key2]['matches']
                ratio = self.total[key1][key2]['wins'] / self.total[key1][key2]['matches'] * 100
                ratio = f'{ratio:3.1f}%'
                row += f'{ratio:>6s}                    '

            body1 += f'{row}\n'

        header2 = '                          | Total  | Win   Lose  Draw  Match\n'
        hr2 = '------------------------------------------------------------\n'

        body2 = ''
        for key1 in self.total:
            row = f'{key1:25s} | '
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

        for i in range(self.matches):
            if (i + 1) % 5 == 0:
                print("    -", black.name, white.name, i + 1)

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
        'AlphaBeta4Ro_TPWE': strategies.AlphaBeta4Ro_TPWE(),
        'AlphaBeta4F9Ro_TPW': strategies.AlphaBeta4F9Ro_TPW(),
        'AlphaBeta4F9JRo_TPW': strategies.AlphaBeta4F9JRo_TPW(),
        'NegaScout3Ro_TPW': strategies.NegaScout3Ro_TPW(),
        'NegaScout4Ro_TPW': strategies.NegaScout4Ro_TPW(),
        'NegaScout4Ro_TPWE': strategies.NegaScout4Ro_TPWE(),
        'MinMax1Ro_TPW': strategies.MinMax1Ro_TPW(),
        'MinMax1Ro_TPWE': strategies.MinMax1Ro_TPWE(),
        'MinMax1Ro_TPWEC': strategies.MinMax1Ro_TPWEC(),
        'MinMax1Ro_TPW2': strategies.MinMax1Ro_TPW2(),
        'MinMax2Ro_T': strategies.MinMax2Ro_T(),
        'MinMax2Ro_TPW': strategies.MinMax2Ro_TPW(),
        'MinMax2Ro_TPWE': strategies.MinMax2Ro_TPWE(),
        'MinMax3Ro_T': strategies.MinMax3Ro_T(),
        'MinMax3Ro_TP': strategies.MinMax3Ro_TP(),
        'AB_TI_Ro': strategies.AB_TI_Ro(),
        'AbIRo_B_TPW': strategies.AbI_B_TPW(),
        'NsIRo_B_TPW': strategies.NsI_B_TPW(),
        'AbIF9JRo_B_TPW': strategies.AbIF9JRo_B_TPW(),
        'AbIF9JRo_B_TPWE': strategies.AbIF9JRo_B_TPWE(),
        'NsIF9JRo_B_TPW': strategies.NsIF9JRo_B_TPW(),
        'NsIF9JRo_B_TPW2': strategies.NsIF9JRo_B_TPW2(),
        'NsIF9JRo_B_TPWE': strategies.NsIF9JRo_B_TPWE(),
        'SwitchNsIF9JRo_B_TPW': strategies.SwitchNsIF9JRo_B_TPW(),
        'SwitchNsIF9JRo_B_TPWE': strategies.SwitchNsIF9JRo_B_TPWE(),
        'RandomF11': strategies.RandomF11(),
        'TopLeft': strategies.External('python ./strategies/ex/python/topleft.py', 3),
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
        keys = strategies.Measure.elp_time.keys()
        for key in keys:
            print()
            print(key)
            print(' min :', strategies.Measure.elp_time[key]['min'], '(s)')
            print(' max :', strategies.Measure.elp_time[key]['max'], '(s)')
            print(' ave :', strategies.Measure.elp_time[key]['ave'], '(s)')
