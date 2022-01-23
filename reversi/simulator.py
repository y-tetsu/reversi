"""Simulator
"""

import os
import json
import itertools
from multiprocessing import Pool

from reversi import Board, BitBoard, Player, NoneDisplay, Game
from reversi.strategies import RandomOpening


class Simulator:
    """
    ゲームをシミュレーションする
    """
    def __init__(self, players_info, setting_file):
        if os.path.isfile(setting_file):
            with open(setting_file) as f:
                setting = json.load(f)
        else:
            setting = {
                "board_size": 8,
                "board_type": "bitboard",
                "matches": 10,
                "processes": 1,
                "parallel": "player",
                "random_opening": 8,
                "player_names": [
                    "Unselfish",
                    "Random",
                    "Greedy",
                    "SlowStarter",
                    "Table",
                ]
            }

        self.matches = setting['matches']
        self.parallel = setting['parallel']
        self.board_size = setting['board_size']

        if 'board_type' in setting:
            self.board_type = setting['board_type']
        else:
            self.board_type = "bitboard"

        self.processes = setting['processes']
        self.random_opening = setting['random_opening']

        if 'player_names' in setting:
            black_players = [Player('black', c, players_info[c]) for c in setting['player_names']]
            white_players = [Player('white', c, players_info[c]) for c in setting['player_names']]
        else:
            black_players = [Player('black', c, players_info[c]) for c in players_info.keys()]
            white_players = [Player('white', c, players_info[c]) for c in players_info.keys()]

        # Adapt Random Opening
        if self.random_opening:
            for black_player in black_players:
                black_player.strategy = RandomOpening(depth=self.random_opening, base=black_player.strategy)

            for white_player in white_players:
                white_player.strategy = RandomOpening(depth=self.random_opening, base=white_player.strategy)

        self.black_players = black_players
        self.white_players = white_players

        self.game_results = []
        self.total = []
        self.result_ratio = {}

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

            ratio = wins / matches * 100
            ratio_par = f'{ratio:3.1f}%'
            loses = matches - wins - draws
            row += f'{ratio_par:>6s} | {wins:>5d} {loses:>5d} {draws:>5d} {matches:>5d}'
            body2 += f'{row}\n'

            self.result_ratio[key1] = ratio

        return board_size + header1 + hr1 + body1 + hr1 + '\n' + header2 + hr2 + body2 + hr2

    def start(self):
        """
        シミュレーションを開始する
        """
        print('processes', self.processes)
        self.result_ratio = {}

        if self.processes > 1:
            if self.parallel == "player":
                with Pool(processes=self.processes) as pool:
                    players = list(itertools.product(self.black_players, self.white_players))
                    infos = zip(itertools.repeat(self.matches, len(players)), players)
                    ret = pool.map(self._game_play, infos)
                    self.game_results = list(itertools.chain.from_iterable(ret))  # 1次元配列に展開する
            else:
                with Pool(processes=self.processes) as pool:
                    for players in itertools.product(self.black_players, self.white_players):
                        matches = list(itertools.repeat(self.matches // self.processes, self.processes))
                        for i in range(self.matches % self.processes):
                            matches[i] += 1
                        infos = zip(matches, itertools.repeat(players, len(matches)))
                        ret = pool.map(self._game_play, infos)
                        self.game_results += list(itertools.chain.from_iterable(ret))  # 1次元配列に展開する
        else:
            for players in itertools.product(self.black_players, self.white_players):
                info = (self.matches, players)
                self.game_results += self._game_play(info)

        self._totalize_results()

    def _game_play(self, info):
        """
        ゲームを実行
        """
        matches, (black, white) = info

        if black.name == white.name:
            return []

        if self.parallel == 'player':
            print(black.name, white.name)
        else:
            print(black.name, white.name, matches)

        ret = []
        for i in range(matches):
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
