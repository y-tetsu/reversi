"""Simulator
"""

import os
import json
import itertools
import datetime
from multiprocessing import Pool

from reversi import Board, BitBoard, Player, NoneDisplay, Game, X
from reversi import C as c
from reversi.strategies import RandomOpening


class Simulator:
    """
    ゲームをシミュレーションする
    """
    def __init__(self,
            players_info,
            setting_file=None,
            board_size=8,
            board_type='bitboard',
            board_name=None,
            first='black',
            matches=10,
            processes=1,
            progress=True,
            parallel='player',
            random_opening=8,
            swap=True,
            perfect_check=False,
            player_names=None,
        ):
        setting = {}
        if setting_file is not None:
            if os.path.isfile(setting_file):
                with open(setting_file, encoding='utf-8') as f:
                    setting = json.load(f)
            else:
                setting = {
                    "board_size": 8,
                    "board_type": "bitboard",
                    "board_name": None,
                    "first": "black",
                    "matches": 10,
                    "processes": 1,
                    "progress": True,
                    "parallel": "player",
                    "random_opening": 8,
                    "swap": True,
                    "perfect_check": False,
                    "player_names": [
                        "Unselfish",
                        "Random",
                        "Greedy",
                        "SlowStarter",
                        "Table",
                    ]
                }

        if 'board_size' in setting:
            self.board_size = setting['board_size']
        else:
            self.board_size = board_size

        if 'board_type' in setting:
            self.board_type = setting['board_type']
        else:
            self.board_type = board_type

        if 'board_name' in setting:
            self.board_name = setting['board_name']
        else:
            self.board_name = board_name

        if 'first' in setting:
            self.first = setting['first']
        else:
            self.first = first

        if 'matches' in setting:
            self.matches = setting['matches']
        else:
            self.matches = matches

        if 'parallel' in setting:
            self.parallel = setting['parallel']
        else:
            self.parallel = parallel

        if 'processes' in setting:
            self.processes = setting['processes']
        else:
            self.processes = processes

        if 'progress' in setting:
            self.progress = setting['progress']
        else:
            self.progress = progress

        if 'random_opening' in setting:
            self.random_opening = setting['random_opening']
        else:
            self.random_opening = random_opening

        if 'swap' in setting:
            self.swap = setting['swap']
        else:
            self.swap = swap

        if 'perfect_check' in setting:
            self.perfect_check = setting['perfect_check']
        else:
            self.perfect_check = perfect_check
        self.perfect_win_txt = './perfect_win.txt'

        if 'player_names' in setting:
            player_names = setting['player_names']
        else:
            player_names = players_info.keys()

        if len(player_names) > 2 or self.swap:
            black_players = [Player('black', c, players_info[c]) for c in player_names]
            white_players = [Player('white', c, players_info[c]) for c in player_names]
        else:
            black_players = [Player('black', list(player_names)[0], players_info[list(player_names)[0]])]
            white_players = [Player('white', list(player_names)[1], players_info[list(player_names)[1]])]

        # Adapt Random Opening
        if self.random_opening:
            for black_player in black_players:
                black_player.strategy = RandomOpening(depth=self.random_opening, base=black_player.strategy)

            for white_player in white_players:
                white_player.strategy = RandomOpening(depth=self.random_opening, base=white_player.strategy)

        self.black_players = black_players
        self.white_players = white_players

        # board_name
        self.hole = 0x0000000000000000
        self.ini_black = None
        self.ini_white = None
        if self.board_name in X:
            self.board_size = 8
            self.hole = X[self.board_name][0]
            self.ini_black = X[self.board_name][1]
            self.ini_white = X[self.board_name][2]
            print(f'[{self.board_name}]')
        print(BitBoard(self.board_size, hole=self.hole, ini_black=self.ini_black, ini_white=self.ini_white))

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
        if self.progress:
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

        if self.progress:
            if self.parallel == 'player':
                print(black.name, white.name)
            else:
                print(black.name, white.name, matches)

        ret = []
        for i in range(matches):
            if (i + 1) % 5 == 0 and self.progress:
                print("    -", black.name, white.name, i + 1)

            board = BitBoard(self.board_size, hole=self.hole, ini_black=self.ini_black, ini_white=self.ini_white) if self.board_type == 'bitboard' else Board(self.board_size, hole=self.hole, ini_black=self.ini_black, ini_white=self.ini_white)
            game = Game(black, white, board, NoneDisplay(), self.first)
            game.play()
            ret.append(game.result)

            for p in [black, white]:
                if hasattr(p.strategy, 'get_result'):
                    p.strategy.get_result(game.result)

            if self.perfect_check:
                from reversi import Elucidator
                Elucidator(board=board).make_perfect_win_txt(self.perfect_win_txt)
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
        str(self)
