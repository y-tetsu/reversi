#!/usr/bin/env python
"""
モンテカルロ法
"""

import sys
sys.path.append('../')

import random
import copy

from game import Game
from player import Player
from display import NoneDisplay

from strategies.common import Timer, Measure, CPU_TIME, AbstractStrategy
from strategies.easy import Random


class MonteCarlo(AbstractStrategy):
    """
    MonteCarlo法で次の手を決める
    """
    def __init__(self, count=100, remain=60):
        self.count = count
        self.remain = remain
        self.black_player = Player('black', 'Random_B', Random())
        self.white_player = Player('white', 'Random_W', Random())

    @Measure.time
    @Timer.start(CPU_TIME, -10000000)
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = list(board.get_possibles(color).keys())  # 手の候補を取得
        scores = [0 for _ in range(len(moves))]          # スコアの初期化

        for _ in range(self.count):
            for i, move in enumerate(moves):
                scores[i] += self.playout(color, board, move)  # この手を選んだ時の勝敗を取得

                if Timer.is_timeout(self):
                    break
            if Timer.is_timeout(self):
                break

        best_score = max(scores)  # ベストスコアを取得
        best_moves = [move for i, move in enumerate(moves) if scores[i] == best_score]  # ベストスコアの手を選ぶ

        return random.choice(best_moves)  # 複数ある場合はランダムに選ぶ

    @Measure.countup
    @Timer.timeout
    def playout(self, color, board, move):
        """
        終了までゲームを進めて勝敗を返す
        """
        remain = board.size * board.size - (board.score['black'] + board.score['white'])

        if remain <= self.remain:
            playout_board = copy.deepcopy(board)   # 現在の盤面をコピー
            playout_board.put_stone(color, *move)  # 調べたい手を打つ

            # 勝敗が決まるまでゲームを進める
            next_color = 'white' if color == 'black' else 'black'  # 相手の色を調べる
            game = Game(playout_board, self.black_player, self.white_player, NoneDisplay(), next_color)
            game.play()

            # 結果を返す
            win, ret = Game.BLACK_WIN if color == 'black' else Game.WHITE_WIN, -1

            if game.result.winlose == win:
                ret = 1  # 勝った場合
            elif game.result.winlose == Game.DRAW:
                ret = 0  # 引き分けた場合
        else:
            ret = 0

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

    Timer.set_deadline(montecarlo.__class__.__name__, 0.5, -10000000)
    ret = montecarlo.playout('white', bitboard, (3, 3))
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
