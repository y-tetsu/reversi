#!/usr/bin/env python
"""
アルファベータ法(ネガアルファ法)
"""

import sys
sys.path.append('../')

from reversi.strategies.common import Timer, Measure, CPU_TIME, AbstractStrategy
from reversi.strategies.negamax import NegaMax
from reversi.strategies.coordinator import Evaluator_TPW, Evaluator_TPWE, Evaluator_TPWEC, Evaluator_N


class _AlphaBeta(AbstractStrategy):
    """
    AlphaBeta法で次の手を決める
    """
    def __init__(self, depth=3, evaluator=None):
        self._MIN = -10000000
        self._MAX = 10000000

        self.depth = depth
        self.evaluator = evaluator

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = board.get_legal_moves(color).keys()  # 手の候補
        best_move, _ = self.get_best_move(color, board, moves, self.depth)

        return best_move

    def get_best_move(self, color, board, moves, depth):
        """
        最善手を選ぶ
        """
        best_move, alpha, beta, scores = None, self._MIN, self._MAX, {}

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in moves:
            score = self.get_score(move, color, board, alpha, beta, depth)
            scores[move] = score

            if Timer.is_timeout(self):
                best_move = move if best_move is None else best_move
                break
            else:
                if score > alpha:  # 最善手を更新
                    alpha = score
                    best_move = move

        return best_move, scores

    def get_score(self, move, color, board, alpha, beta, depth):
        """
        手を打った時の評価値を取得
        """
        board.put_disc(color, *move)                                         # 一手打つ
        next_color = 'white' if color == 'black' else 'black'                # 相手の色
        score = -self._get_score(next_color, board, -beta, -alpha, depth-1)  # 評価値を取得
        board.undo()                                                         # 打った手を戻す

        return score

    @Measure.countup
    def _get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        legal_moves_b = board.get_legal_moves('black', True)
        legal_moves_w = board.get_legal_moves('white', True)
        is_game_end =  True if not legal_moves_b and not legal_moves_w else False

        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluator.evaluate(color=color, board=board, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w) * sign

        # パスの場合
        legal_moves = legal_moves_b if color == 'black' else legal_moves_w
        next_color = 'white' if color == 'black' else 'black'

        if not legal_moves:
            return -self._get_score(next_color, board, -beta, -alpha, depth)

        # 評価値を算出
        for move in legal_moves.keys():
            board.put_disc(color, *move)
            score = -self._get_score(next_color, board, -beta, -alpha, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break

            alpha = max(alpha, score)  # 最大値を選択
            if alpha >= beta:  # 枝刈り
                break

        return alpha


class AlphaBeta(_AlphaBeta):
    """
    AlphaBeta法で次の手を決める(時間制限付き)
    """
    @Timer.start(CPU_TIME, -10000000)
    def next_move(self, color, board):
        """
        次の一手
        """
        return super().next_move(color, board)

    @Timer.timeout
    def _get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        return super()._get_score(color, board, alpha, beta, depth)


class _AlphaBeta_N(_AlphaBeta):
    """
    AlphaBeta法でEvaluator_Nにより次の手を決める
    """
    def __init__(self, depth, evaluator=Evaluator_N()):
        super().__init__(depth=depth, evaluator=evaluator)


class AlphaBeta_N(AlphaBeta):
    """
    AlphaBeta法でEvaluator_Nにより次の手を決める
    """
    def __init__(self, depth, evaluator=Evaluator_N()):
        super().__init__(depth=depth, evaluator=evaluator)


class AlphaBeta_TPW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPW()):
        super().__init__(evaluator=evaluator)


class AlphaBeta_TPWE(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWEにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPWE()):
        super().__init__(evaluator=evaluator)


class AlphaBeta_TPWEC(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWECにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPWEC()):
        super().__init__(evaluator=evaluator)


class AlphaBeta3_TPW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class AlphaBeta4_TPW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class AlphaBeta4_TPWE(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWEにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    # AlphaBeta
    print('--- Test For AlphaBeta Strategy ---')
    alphabeta = AlphaBeta3_TPW()

    assert alphabeta.depth == 3

    bitboard8 = BitBoard(8)
    bitboard8.put_disc('black', 3, 2)

    key = alphabeta.__class__.__name__ + str(os.getpid())

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    score = alphabeta._get_score('white', bitboard8, -10000000, 10000000, 2)
    print(score)
    print(Measure.count[key])
    assert score == -13
    assert Measure.count[key] == 16

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    score = alphabeta._get_score('white', bitboard8, -10000000, 10000000, 3)
    print(score)
    print(Measure.count[key])
    assert score == 4
    assert Measure.count[key] == 62

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    score = alphabeta._get_score('white', bitboard8, -10000000, 10000000, 4)
    print(score)
    print(Measure.count[key])
    assert score == -9
    assert Measure.count[key] == 263

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 1
    score = alphabeta._get_score('white', bitboard8, -10000000, 10000000, 5)
    print(score)
    print(Measure.count[key])
    assert score == 1
    assert Measure.count[key] == 812

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    score = alphabeta._get_score('white', bitboard8, -10000000, 10000000, 6)
    print(score)
    print(Measure.count[key])
    assert score == -5
    assert Measure.count[key] == 2548

    print(bitboard8)
    assert alphabeta.next_move('white', bitboard8) == (2, 4)

    print('* black check')
    bitboard8.put_disc('white', 2, 4)
    bitboard8.put_disc('black', 5, 5)
    bitboard8.put_disc('white', 4, 2)
    bitboard8.put_disc('black', 5, 2)
    bitboard8.put_disc('white', 5, 4)
    print(bitboard8)

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    move = alphabeta.next_move('black', bitboard8)
    print(move)
    assert move == (2, 2)
    print(Measure.count[key])
    assert Measure.count[key] == 180

    Measure.count[key] = 0
    alphabeta.depth = 2
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    move = alphabeta.next_move('black', bitboard8)
    print(move)
    assert move == (2, 2)
    print(Measure.count[key])
    assert Measure.count[key] == 27

    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    moves = bitboard8.get_legal_moves('black').keys()  # 手の候補
    print( alphabeta.get_best_move('black', bitboard8, moves, 5) )
    assert alphabeta.get_best_move('black', bitboard8, moves, 5) == ((2, 2), {(2, 2): 8, (2, 3): 8, (5, 3): 8, (1, 5): 8, (2, 5): 8, (3, 5): 8, (4, 5): 8, (6, 5): 8})
