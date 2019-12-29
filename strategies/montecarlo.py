#!/usr/bin/env python
"""
オセロの戦略(MonteCarlo)
"""

import sys
sys.path.append('../')

import random
import copy

from display import NoneDisplay
from player import Player
from game import Game
from strategies.common import CPU_TIME, AbstractStrategy
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.easy import Random


class MonteCarlo(AbstractStrategy):
    """
    MonteCarlo法で次の手を決める
    """
    def __init__(self, count=100):
        self.count = count
        self.black_player = Player('black', 'Random_B', Random())
        self.white_player = Player('white', 'Random_W', Random())

    @Measure.time
    @Timer.start(CPU_TIME)
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = list(board.get_possibles(color).keys())
        next_color = 'white' if color == 'black' else 'black'
        scores = [0 for _ in range(len(moves))]

        for _ in range(self.count):
            for i, move in enumerate(moves):
                test_board = copy.deepcopy(board)
                test_board.put_stone(color, *move)
                scores[i] += self.playout(next_color, test_board)

                if Timer.is_timeout(self):
                    break
            if Timer.is_timeout(self):
                break

        best_score = max(scores)
        best_moves = [move for i, move in enumerate(moves) if scores[i] == best_score]

        return random.choice(best_moves)

    @Measure.countup
    @Timer.timeout
    def playout(self, color, board):
        """
        終了までゲームを進める
        """
        game = Game(board, self.black_player, self.white_player, NoneDisplay(), color)
        game.play()

        winlose, ret = Game.BLACK_WIN if color == 'white' else Game.WHITE_WIN, 0

        if game.result.winlose == winlose:
            ret = 1  # 勝った場合
        elif game.result.winlose == Game.DRAW:
            ret = 0.5  # 引き分けた場合

        return ret


class MonteCarlo30(MonteCarlo):
    """
    MonteCarlo法で次の手を決める(最大一手30回試行)
    """
    def __init__(self, count=30):
        super().__init__(count)


class MonteCarlo100(MonteCarlo):
    """
    MonteCarlo法で次の手を決める(最大一手100回試行)
    """
    def __init__(self, count=100):
        super().__init__(count)


class MonteCarlo1000(MonteCarlo):
    """
    MonteCarlo法で次の手を決める(最大一手1000回試行)
    """
    def __init__(self, count=1000):
        super().__init__(count)


if __name__ == '__main__':
    import time
    from board import BitBoard

    # MonteCarlo
    print('--- Test For MonteCarlo Strategy ---')
    montecarlo = MonteCarlo()

    assert montecarlo.count == 100

    # playout
    bitboard = BitBoard(4)
    bitboard.put_stone('black', 3, 2)
    print(bitboard)

    Timer.set_deadline(montecarlo.__class__.__name__, 0.5)
    ret = montecarlo.playout('white', bitboard)
    print(ret)

    # next_move
    bitboard = BitBoard(8)
    bitboard.put_stone('black', 3, 2)
    bitboard.put_stone('white', 2, 4)
    bitboard.put_stone('black', 1, 5)
    print(bitboard)

    move = montecarlo.next_move('white', bitboard)
    print(move)

    keys = Measure.elp_time.keys()
    for key in keys:
        print()
        print(key)
        print(' count :', Measure.count[key])
        print(' min   :', Measure.elp_time[key]['min'], '(s)')
        print(' max   :', Measure.elp_time[key]['max'], '(s)')
        print(' ave   :', Measure.elp_time[key]['ave'], '(s)')
