#!/usr/bin/env python
"""
オセロの戦略(NegaScout)
"""

import sys
sys.path.append('../')

from strategies.common import CPU_TIME
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.alphabeta import AlphaBeta
from strategies.evaluator import Evaluator_TPW
from strategies.sorter import Sorter, Sorter_O


class NegaScout(AlphaBeta):
    """
    NegaScout法で次の手を決める
    """
    def __init__(self, depth=3, evaluator=None, sorter=None):
        super().__init__(depth, evaluator)
        self.sorter = sorter

    @Measure.countup
    @Timer.timeout
    def _get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        possibles_b = board.get_possibles('black', True)
        possibles_w = board.get_possibles('white', True)
        is_game_end =  True if not possibles_b and not possibles_w else False

        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluator.evaluate(color, board, possibles_b, possibles_w) * sign

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return -self._get_score(next_color, board, -beta, -alpha, depth)

        # 手の候補を並び替え
        moves = self.sorter.sort_moves(color, board, None, None)

        # 最初の手の評価値を取得する
        move = moves.pop(0)
        board.put_stone(color, *move)
        score = -self._get_score(next_color, board, -beta, -alpha, depth-1)
        board.undo()

        if Timer.is_timeout(self):
            return alpha
        else:
            if score >= beta:  # 枝刈り
                return score
            alpha = max(alpha, score)  # 最大値を選択

        # Null Window Search
        for move in moves:
            board.put_stone(color, *move)
            score = -self._get_score(next_color, board, -alpha-1, -alpha, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break
            else:
                if score >= beta:  # 枝刈り
                    return score
                if alpha < score:
                    alpha = score
                    board.put_stone(color, *move)
                    score = -self._get_score(next_color, board, -beta, -alpha, depth-1)
                    board.undo()

                    if Timer.is_timeout(self):
                        break
                    else:
                        if score >= beta:  # 枝刈り
                            return score
                        alpha = max(alpha, score)  # 最大値を選択
        return alpha


class NegaScout_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPW(), sorter=Sorter()):
        super().__init__(evaluator=evaluator, sorter=sorter)


class NegaScout_TPW_O(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(並べ替え:O)
    """
    def __init__(self, evaluator=Evaluator_TPW(), sorter=Sorter_O()):
        super().__init__(evaluator=evaluator, sorter=sorter)


class NegaScout4_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW(), sorter=Sorter()):
        super().__init__(depth, evaluator, sorter=sorter)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    # NegaScout
    print('--- Test For NegaScout Strategy ---')
    negascout = NegaScout4_TPW()

    assert negascout.depth == 4

    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)

    key = negascout.__class__.__name__ + str(os.getpid())

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    assert negascout._get_score('white', bitboard8, -10000000, 10000000, 2) == -15
    assert Measure.count[key] == 20

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    assert negascout._get_score('white', bitboard8, -10000000, 10000000, 3) == 0
    assert Measure.count[key] == 125

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    assert negascout._get_score('white', bitboard8, -10000000, 10000000, 4) == -10
    assert Measure.count[key] == 486

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 1
    assert negascout._get_score('white', bitboard8, -10000000, 10000000, 5) == 1
    assert Measure.count[key] == 630

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    assert negascout._get_score('white', bitboard8, -10000000, 10000000, 6) == -5
    assert Measure.count[key] == 2163

    print(bitboard8)
    assert negascout.next_move('white', bitboard8) == (2, 4)

    print('* black check')
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    assert negascout.next_move('black', bitboard8) == (5, 3)
    assert Measure.count[key] == 1041

    Measure.count[key] = 0
    negascout.depth = 2
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    assert negascout.next_move('black', bitboard8) == (2, 2)
    assert Measure.count[key] == 28

    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    moves = bitboard8.get_possibles('black').keys()  # 手の候補
    assert negascout.get_best_move('black', bitboard8, moves, 5) == ((3, 5), {(2, 2): 8, (2, 3): 10, (5, 3): 10, (1, 5): 10, (2, 5): 10, (3, 5): 12, (4, 5): 12, (6, 5): 12})
