#!/usr/bin/env python
"""
オセロの戦略(AlphaBeta)
"""

import sys
sys.path.append('../')

from strategies.common import CPU_TIME
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.easy import Table
from strategies.negamax import NegaMax_, NegaMax
from strategies.evaluator import Evaluator_TPOW


class AlphaBeta(NegaMax):
    """
    AlphaBeta法で次の手を決める
    """
    @Measure.time
    @Timer.start(CPU_TIME)
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = board.get_possibles(color).keys()  # 手の候補
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
        board.put_stone(color, *move)                                        # 一手打つ
        next_color = 'white' if color == 'black' else 'black'                # 相手の色
        score = -self._get_score(next_color, board, -beta, -alpha, depth-1)  # 評価値を取得
        board.undo()                                                         # 打った手を戻す

        return score

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

        # 評価値を算出
        for move in possibles.keys():
            board.put_stone(color, *move)
            score = -self._get_score(next_color, board, -beta, -alpha, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break
            else:
                alpha = max(alpha, score)  # 最大値を選択
                if alpha >= beta:  # 枝刈り
                    break

        return alpha


class AlphaBeta_TPOW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPOWにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPOW()):
        super().__init__(evaluator=evaluator)


class AlphaBeta1_TPOW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPOWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class AlphaBeta2_TPOW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPOWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class AlphaBeta3_TPOW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPOWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class AlphaBeta4_TPOW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPOWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class AlphaBeta_(NegaMax_):
    """
    AlphaBeta法で次の手を決める
    """
    @Measure.time
    @Timer.start(CPU_TIME)
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = board.get_possibles(color).keys()  # 手の候補

        return self.get_best_move(color, board, moves, self.depth)

    def get_best_move(self, color, board, moves, depth):
        """
        最善手を選ぶ
        """
        best_move, alpha, beta = None, self._MIN, self._MAX

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in moves:
            score = self.get_score(move, color, board, alpha, beta, depth)

            if Timer.is_timeout(self):
                best_move = move if best_move is None else best_move
                break
            else:
                if score > alpha:  # 最善手を更新
                    alpha = score
                    best_move = move

        return best_move

    def get_score(self, move, color, board, alpha, beta, depth):
        """
        手を打った時の評価値を取得
        """
        board.put_stone(color, *move)                                        # 一手打つ
        next_color = 'white' if color == 'black' else 'black'                # 相手の色
        score = -self._get_score(next_color, board, -beta, -alpha, depth-1)  # 評価値を取得
        board.undo()                                                         # 打った手を戻す

        return score

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
            return self.evaluate(color, board, possibles_b, possibles_w)

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return -self._get_score(next_color, board, -beta, -alpha, depth)

        # 評価値を算出
        for move in possibles.keys():
            board.put_stone(color, *move)
            score = -self._get_score(next_color, board, -beta, -alpha, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break
            else:
                alpha = max(alpha, score)  # 最大値を選択
                if alpha >= beta:  # 枝刈り
                    break

        return alpha


class AlphaBeta1(AlphaBeta_):
    """
    AlphaBeta法で次の手を決める(1手読み)
    """
    def __init__(self, depth=1):
        super().__init__(depth)


class AlphaBeta2(AlphaBeta_):
    """
    AlphaBeta法で次の手を決める(2手読み)
    """
    def __init__(self, depth=2):
        super().__init__(depth)


class AlphaBeta3(AlphaBeta_):
    """
    AlphaBeta法で次の手を決める(3手読み)
    """
    def __init__(self, depth=3):
        super().__init__(depth)


class AlphaBeta4(AlphaBeta_):
    """
    AlphaBeta法で次の手を決める(4手読み)
    """
    def __init__(self, depth=4):
        super().__init__(depth)


class AB_T(AlphaBeta_):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める
    """
    def __init__(self, depth=3, corner=50, c=-20, a=0, b=-1, x=-25, o=-5, w1=10000, w2=16, w3=2, w4=0.5, min_value=-10000000, max_value=10000000):
        super().__init__(depth, w1, w2, w3, min_value, max_value)
        self.table = Table(8, corner, c, a, b, x, o)  # Table戦略を利用する
        self._W4 = w4

    @Measure.time
    @Timer.start(CPU_TIME)
    def next_move(self, color, board):
        """
        次の一手
        """
        if self.table.size != board.size:  # テーブルサイズの調整
            self.table.set_table(board.size)

        return super().next_move(color, board)

    def evaluate(self, color, board, possibles_b, possibles_w):
        """
        評価値の算出
        """
        ret = super().evaluate(color, board, possibles_b, possibles_w)  # 元の評価
        ret += self.table.get_score(color, board) * self._W4            # テーブル評価を追加

        return ret


class AB_T4(AB_T):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める(4手読み)
    """
    def __init__(self, depth=4):
        super().__init__(depth)


class AB_TI(AB_T):
    """
    AB_Tに反復深化法を適用して次の手を決める
    """
    def __init__(self, depth=2, corner=50, c=-20, a=0, b=-1, x=-25, o=-5, w1=10000, w2=16, w3=2, w4=0.5, min_value=-10000000, max_value=10000000):
        super().__init__(depth, corner, c, a, b, x, o, w1, w2, w3, w4, min_value, max_value)

    @Measure.time
    @Timer.start(CPU_TIME)
    def next_move(self, color, board):
        """
        次の一手
        """
        if self.table.size != board.size:  # テーブルサイズの調整
            self.table.set_table(board.size)

        depth, best_move = self.depth, None

        while True:
            moves = list(board.get_possibles(color).keys())

            # 前回の最善手を優先的に
            if best_move is not None:
                moves.remove(best_move)
                moves.insert(0, best_move)

            # 4隅はさらに優先的に調べる
            for corner in [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]:
                if corner in moves:
                    moves.remove(corner)
                    moves.insert(0, corner)

            best_move = super().get_best_move(color, board, moves, depth)  # 最善手

            if Timer.is_timeout(self):  # タイムアウト
                break

            depth += 1  # 次の読みの深さ

        return best_move


if __name__ == '__main__':
    import time
    from board import BitBoard

    # AlphaBeta
    print('--- Test For AlphaBeta Strategy ---')
    alphabeta = AlphaBeta3_TPOW()

    assert alphabeta.depth == 3

    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)

    Measure.count['AlphaBeta3_TPOW'] = 0
    Timer.timeout_flag['AlphaBeta3_TPOW'] = False
    Timer.deadline['AlphaBeta3_TPOW'] = time.time() + CPU_TIME
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 2) == -12.75
    assert Measure.count['AlphaBeta3_TPOW'] == 16

    Measure.count['AlphaBeta3_TPOW'] = 0
    Timer.timeout_flag['AlphaBeta3_TPOW'] = False
    Timer.deadline['AlphaBeta3_TPOW'] = time.time() + CPU_TIME
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 3) == 2.25
    assert Measure.count['AlphaBeta3_TPOW'] == 63

    Measure.count['AlphaBeta3_TPOW'] = 0
    Timer.timeout_flag['AlphaBeta3_TPOW'] = False
    Timer.deadline['AlphaBeta3_TPOW'] = time.time() + CPU_TIME
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 4) == -8.25
    assert Measure.count['AlphaBeta3_TPOW'] == 247

    Measure.count['AlphaBeta3_TPOW'] = 0
    Timer.timeout_flag['AlphaBeta3_TPOW'] = False
    Timer.deadline['AlphaBeta3_TPOW'] = time.time() + 1
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 5) == 4.0
    assert Measure.count['AlphaBeta3_TPOW'] == 693

    Measure.count['AlphaBeta3_TPOW'] = 0
    Timer.timeout_flag['AlphaBeta3_TPOW'] = False
    Timer.deadline['AlphaBeta3_TPOW'] = time.time() + 3
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 6) == -3.5
    assert Measure.count['AlphaBeta3_TPOW'] == 2659

    print(bitboard8)
    assert alphabeta.next_move('white', bitboard8) == (2, 4)

    print('* black check')
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count['AlphaBeta3_TPOW'] = 0
    Timer.timeout_flag['AlphaBeta3_TPOW'] = False
    Timer.deadline['AlphaBeta3_TPOW'] = time.time() + 3
    assert alphabeta.next_move('black', bitboard8) == (2, 2)
    assert Measure.count['AlphaBeta3_TPOW'] == 148

    Measure.count['AlphaBeta3_TPOW'] = 0
    alphabeta.depth = 2
    Timer.timeout_flag['AlphaBeta3_TPOW'] = False
    Timer.deadline['AlphaBeta3_TPOW'] = time.time() + 3
    assert alphabeta.next_move('black', bitboard8) == (4, 5)
    assert Measure.count['AlphaBeta3_TPOW'] == 30

    Timer.timeout_flag['AlphaBeta3_TPOW'] = False
    Timer.deadline['AlphaBeta3_TPOW'] = time.time() + 3
    moves = bitboard8.get_possibles('black').keys()  # 手の候補
    assert alphabeta.get_best_move('black', bitboard8, moves, 5) == ((3, 5), {(2, 2): 5.75, (2, 3): 9.25, (5, 3): 9.25, (1, 5): 9.25, (2, 5): 9.25, (3, 5): 11.25, (4, 5): 11.25, (6, 5): 11.25})
