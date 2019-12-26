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
    from board import Board
    # AlphaBeta
    print('--- Test For AlphaBeta Strategy ---')
    board8 = Board(8)
    alphabeta = AlphaBeta()
    assert alphabeta.depth == 3
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert alphabeta.evaluate('black', board8, b, w) == 0

    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 4)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert alphabeta.evaluate('black', board8, b, w) == 2

    board8.put_stone('black', 1, 5)
    board8.put_stone('white', 1, 4)
    board8.put_stone('black', 2, 5)
    board8.put_stone('white', 1, 6)
    board8.put_stone('black', 0, 7)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert alphabeta.evaluate('black', board8, b, w) == 22

    board8.put_stone('black', 1, 3)
    board8.put_stone('black', 2, 3)
    board8.put_stone('black', 4, 5)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert alphabeta.evaluate('white', board8, b, w) == -10014

    from board import BitBoard
    print('- bitboard -')
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + CPU_TIME
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 2) == -6
    assert Measure.count['AlphaBeta'] == 16

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + CPU_TIME
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 3) == 2
    assert Measure.count['AlphaBeta'] == 58

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + CPU_TIME
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 4) == -4
    assert Measure.count['AlphaBeta'] == 226

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + 1
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 5) == 2
    assert Measure.count['AlphaBeta'] == 617

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + 3
    assert alphabeta._get_score('white', bitboard8, -10000000, 10000000, 6) == -4
    assert Measure.count['AlphaBeta'] == 1865

    print(bitboard8)
    assert alphabeta.next_move('white', bitboard8) == (2, 4)

    print('* black check')
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + 3
    assert alphabeta.next_move('black', bitboard8) == (2, 2)
    assert Measure.count['AlphaBeta'] == 170

    Measure.count['AlphaBeta'] = 0
    alphabeta.depth = 2
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + 3
    assert alphabeta.next_move('black', bitboard8) == (2, 2)
    assert Measure.count['AlphaBeta'] == 29

    # AB_T
    print('--- Test For AB_T Strategy ---')
    print('- bitboard -')
    ab_t = AB_T()
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count['AB_T'] = 0
    Timer.timeout_flag['AB_T'] = False
    Timer.deadline['AB_T'] = time.time() + 3
    assert ab_t.next_move('black', bitboard8) == (2, 2)
    assert Measure.count['AB_T'] == 148

    # AB_TI
    print('--- Test For AB_TI Strategy ---')
    print('- bitboard -')
    ab_ti = AB_TI()
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count['AB_TI'] = 0
    Timer.timeout_flag['AB_TI'] = False
    assert ab_ti.next_move('black', bitboard8) == (5, 3)
    assert Measure.count['AB_TI'] >= 1500
