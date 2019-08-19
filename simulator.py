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
    def __init__(self, board_size, blacks, whites, matches):
        self.board_size = board_size
        self.blacks = blacks
        self.whites = whites
        self.matches = matches
        self.results = []

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
                self.results.append(game.result)

        self.print_result()

    def print_result(self):
        """
        シミュレーション結果の表示

        """
        table = {}

        for result in self.results:
            win = result[0]
            black = result[1][0]
            white = result[1][1]

            if black not in table:
                table[black] = {}

            if white not in table[black]:
                table[black][white] = {'matches': 0, 'wins': 0}

            if win == Game.BLACK_WIN:
                table[black][white]['wins'] += 1

            table[black][white]['matches'] += 1

            if white not in table:
                table[white] = {}

            if black not in table[white]:
                table[white][black] = {'matches': 0, 'wins': 0}

            if win == Game.WHITE_WIN:
                table[white][black]['wins'] += 1

            table[white][black]['matches'] += 1

        print("\nSize :", self.board_size)
        print("           | " + "".join([f'{key:10s}' for key in table]) + "| Total")
        print("-----------------------------------------------------------------------")

        for key1 in table:
            print(f'{key1:10s} | ', end="")
            wins, matches = 0, 0

            for key2 in table:
                if key1 == key2:
                    print("------    ", end="")
                    continue

                wins += table[key1][key2]['wins']
                matches += table[key1][key2]['matches']

                ratio = table[key1][key2]['wins'] / table[key1][key2]['matches'] * 100
                ratio = f'{ratio:3.1f}%'

                print(f'{ratio:>6s}    ', end="")

            print("| ", end="")
            ratio = wins / matches * 100
            ratio = f'{ratio:3.1f}%'
            print(f'{ratio:>6s} ({wins} / {matches})')

        print("-----------------------------------------------------------------------")


if __name__ == '__main__':
    import timeit
    from player import Player
    import strategies

    characters = [
        ("Random", strategies.Random()),
        ("Max", strategies.Max()),
        ("Min", strategies.Min()),
    ]

    blacks = [Player(Board.BLACK, *character) for character in characters]
    whites = [Player(Board.WHITE, *character) for character in characters]

    simulator = Simulator(6, blacks, whites, 250)

    print(timeit.timeit('simulator.start()', globals=globals(), number=1), "(s)")
