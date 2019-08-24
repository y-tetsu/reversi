#!/usr/bin/env python
"""
オセロシミュレーター
"""

import itertools
from game import Game
from board import Board


class Simulator:
    """
    ゲームをシミュレーションする
    """
    def __init__(self, blacks, whites, matches, board_size=8):
        self.blacks = blacks
        self.whites = whites
        self.matches = matches
        self.board_size = board_size
        self.game_results = []
        self.total = []

    def __str__(self):
        board_size = "\nSize : " + str(self.board_size) + "\n"
        header = "           | " + " ".join([f'{key:10s}' for key in self.total]) + "| Total\n"
        hr = "-----------------------------------------------------------------------\n"

        body = ""
        for key1 in self.total:
            row = f'{key1:10s} | '
            wins, matches = 0, 0

            for key2 in self.total:
                if key1 == key2:
                    row += "------    "
                    continue

                wins += self.total[key1][key2]['wins']
                matches += self.total[key1][key2]['matches']
                ratio = self.total[key1][key2]['wins'] / self.total[key1][key2]['matches'] * 100
                ratio = f'{ratio:3.1f}%'
                row += f'{ratio:>6s}    '

            row += "| "
            ratio = wins / matches * 100
            ratio = f'{ratio:3.1f}%'
            row += f'{ratio:>6s} ({wins} / {matches})'
            body += f'{row}\n'

        return board_size + header + hr + body + hr

    def start(self):
        """
        シミュレーションを開始する
        """
        for black, white in itertools.product(self.blacks, self.whites):
            if black.name == white.name:
                continue

            for _ in range(self.matches):
                game = Game(Board(self.board_size), black, white, False)
                game.play()
                self.game_results.append(game.result)

        self._totalize_results()

    def _totalize_results(self):
        """
        結果の集計

        """
        total = {}

        for result in self.game_results:
            win = result[0]
            black = result[1][0]
            white = result[1][1]

            if black not in total:
                total[black] = {}

            if white not in total[black]:
                total[black][white] = {'matches': 0, 'wins': 0}

            if win == Game.BLACK_WIN:
                total[black][white]['wins'] += 1

            total[black][white]['matches'] += 1

            if white not in total:
                total[white] = {}

            if black not in total[white]:
                total[white][black] = {'matches': 0, 'wins': 0}

            if win == Game.WHITE_WIN:
                total[white][black]['wins'] += 1

            total[white][black]['matches'] += 1

        self.total = total


if __name__ == '__main__':
    import timeit
    from player import Player
    import strategies

    characters = [
        ("Random", strategies.Random()),
        ("Greedy", strategies.Greedy()),
        ("Unselfish", strategies.Unselfish()),
    ]

    blacks = [Player(Board.BLACK, *character) for character in characters]
    whites = [Player(Board.WHITE, *character) for character in characters]

    simulator = Simulator(blacks, whites, 25)

    elapsed_time = timeit.timeit('simulator.start()', globals=globals(), number=1)
    print(simulator, elapsed_time, "(s)")
