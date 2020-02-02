#!/usr/bin/env python
"""
ネガマックス法
"""

import sys
sys.path.append('../')

import random

from strategies.common import Timer, Measure, CPU_TIME, AbstractStrategy
from strategies.coordinator import Evaluator_TPW, Evaluator_TPOW


class _NegaMax(AbstractStrategy):
    """
    NegaMax法で次の手を決める
    """
    def __init__(self, depth=3, evaluator=None):
        self._MIN = -10000000

        self.depth = depth
        self.evaluator = evaluator

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        next_color = 'white' if color == 'black' else 'black'
        moves, max_score = {}, self._MIN

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in board.get_possibles(color).keys():
            board.put_stone(color, *move)                             # 一手打つ
            score = -self.get_score(next_color, board, self.depth-1)  # 評価値を取得
            board.undo()                                              # 打った手を戻す

            if Timer.is_timeout(self):      # タイムアウト発生時
                if max_score not in moves:  # 候補がない場合は現在の手を返す
                    return move
                break
            else:
                max_score = max(max_score, score)  # 最大値を選択
                if score not in moves:             # 次の候補を記憶
                    moves[score] = []
                moves[score].append(move)

        return random.choice(moves[max_score])  # 複数候補がある場合はランダムに選ぶ

    @Measure.countup
    def get_score(self, color, board, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        possibles_b = board.get_possibles('black', True)
        possibles_w = board.get_possibles('white', True)
        is_game_end =  True if not possibles_b and not possibles_w else False

        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluator.evaluate(color=color, board=board, possibles_b=possibles_b, possibles_w=possibles_w) * sign

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return -self.get_score(next_color, board, depth)

        # 評価値を算出
        max_score = self._MIN

        for move in possibles.keys():
            board.put_stone(color, *move)
            score = -self.get_score(next_color, board, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break
            else:
                max_score = max(max_score, score)  # 最大値を選択

        return max_score


class NegaMax(_NegaMax):
    """
    NegaMax法で次の手を決める(時間制限付き)
    """
    @Timer.start(CPU_TIME, -10000000)
    def next_move(self, color, board):
        """
        次の一手
        """
        return super().next_move(color, board)

    @Timer.timeout
    def get_score(self, color, board, depth):
        """
        評価値の取得
        """
        return super().get_score(color, board, depth)


class NegaMax1_TPOW(NegaMax):
    """
    NegaMax法でEvaluator_TPOWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaMax2_TPOW(NegaMax):
    """
    NegaMax法でEvaluator_TPOWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class _NegaMax3_TPW(_NegaMax):
    """
    NegaMax法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaMax3_TPW(NegaMax):
    """
    NegaMax法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaMax3_TPOW(NegaMax):
    """
    NegaMax法でEvaluator_TPOWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaMax4_TPOW(NegaMax):
    """
    NegaMax法でEvaluator_TPOWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)

    print('--- Test For NegaMax Strategy ---')
    negamax = NegaMax3_TPOW()
    assert negamax.depth == 3

    key = negamax.__class__.__name__ + str(os.getpid())

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    score = negamax.get_score('white', bitboard8, 2)
    print(score)
    assert score == -10.75
    assert Measure.count[key] == 18

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    score = negamax.get_score('white', bitboard8, 3)
    print(score)
    assert score == 6.25
    assert Measure.count[key] == 79

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    score = negamax.get_score('white', bitboard8, 4)
    print(score)
    assert score == -8.25
    assert Measure.count[key] == 428

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 5
    score = negamax.get_score('white', bitboard8, 5)
    print(score)
    assert score == 4
    assert Measure.count[key] == 2478

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 5
    score = negamax.get_score('white', bitboard8, 6)
    print(score)
    assert score == -3.5
    assert Measure.count[key] == 16251

    print(bitboard8)
    assert negamax.next_move('white', bitboard8) == (2, 4)

    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 5
    assert negamax.next_move('black', bitboard8) == (2, 2)
    assert Measure.count[key] == 575

    Measure.count[key] = 0
    negamax.depth = 2
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 2
    assert negamax.next_move('black', bitboard8) == (4, 5)
    assert Measure.count[key] == 70
