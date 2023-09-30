"""Mcts(MonteCarlo Tree Search)
"""
import random
import math

from reversi import C as c
from reversi import BitBoard
from reversi.strategies.common import Timer, Measure, AbstractStrategy
from reversi.strategies.montecarlo import MonteCarlo
from reversi.strategies.MonteCarloMethods import playout


class Mcts(AbstractStrategy):
    """モンテカルロ木探索で次の手を選ぶ
    """
    def __init__(self, count=1000, remain=60):
        self.count = count
        self.remain = remain  # モンテカルロ法開始手数
        self.root = None
        self.timer = True
        self.measure = True

    @Measure.time
    @Timer.start(-10000000)
    def next_move(self, color, board):
        """次の一手
        """
        pid = Timer.get_pid(self)  # タイムアウト監視用のプロセスID

        self.root = Node(color, board)
        self.root.expand()

        # 指定回数分のシミュレーションを実行する
        for _ in range(self.count):
            self._evaluate(pid=pid)
            if Timer.is_timeout(pid):
                break

        # 試行回数が最大の手を返す
        legal_moves = board.get_legal_moves(color)
        counts = []
        for child in self.root.child_nodes:
            counts.append(child.count)

        return legal_moves[self.root.argmax(counts)]

    @Measure.countup
    @Timer.timeout
    def _evaluate(self, pid=None):
        """シミュレーションを実行する
        """
        self.root.evaluate()


class Node:
    """モンテカルロ木探索のノード
    """
    def __init__(self, color, board, excount=10):
        self.color = color
        self.board = self.copy_board(board)
        self.excount = excount

        self.total = 0           # 累積価値
        self.count = 0           # 試行回数
        self.child_nodes = None  # 子ノード群

    def copy_board(self, board):
        """盤面の複製
        """
        size = board.size
        b, w, h = board.get_bitboard_info()
        return BitBoard(size, h, b, w)

    def board_has_legal_moves(self):
        """置く場所があるか
        """
        # 黒プレイヤーが打てるか
        moves = self.board.get_legal_moves(c.black)
        if moves:
            return True

        # 白プレイヤーが打てるか
        moves = self.board.get_legal_moves(c.white)
        if moves:
            return True

        return False

    def get_winlose(self):
        """勝敗を取得する
        """
        # 打てる場所がある場合
        if self.board_has_legal_moves():
            return None
        # 決着がついている
        if self.board._black_score == self.board._white_score:
            return 'draw'
        if self.board._black_score > self.board._white_score:
            if self.color == c.black:
                return 'win'
            else:
                return 'lose'
        else:
            if self.color == c.black:
                return 'lose'
            else:
                return 'win'

    def expand(self):
        """子ノードの展開
        """
        moves = self.board.get_legal_moves(self.color)
        move_color = self.color
        next_color = c.black if self.color == c.white else c.white
        self.child_nodes = []
        if moves:
            for move in moves:
                board = self.copy_board(self.board)
                board.put_disc(move_color, *move)
                self.child_nodes.append(Node(next_color, board))
        else:
            if self.board.get_legal_moves(next_color):
                self.child_nodes.append(Node(next_color, self.board))

    def get_max_ucb1_child_node(self):
        """UCB1が最大の子ノードを取得
        """
        # 試行回数0のノードを返す
        for child in self.child_nodes:
            if child.count == 0:
                return child

        # UCB1を計算する
        all_count = 0
        for child in self.child_nodes:
            all_count += child.count
        ucb1_values = []
        for child in self.child_nodes:
            total = child.total
            count = child.count
            log_a = math.log(all_count)
            ucb1 = (-total)/count + (2*log_a/count)**0.5
            ucb1_values.append(ucb1)

        return self.child_nodes[self.argmax(ucb1_values)]

    def argmax(self, values):
        """リストの最大値のインデックスを返す
        """
        max_value = max(values)
        return values.index(max_value)

    def evaluate(self):
        """局面の評価
        """
        # ゲーム終了時
        winlose = self.get_winlose()
        if winlose:
            value = 0
            if winlose == 'win':
                value = 1
            elif winlose == 'lose':
                value = -1
            self.total += value
            self.count += 1

        # 子ノードが存在しない場合
        elif not self.child_nodes:
            # ランダムに手を選び決着まで手を進める
            color = self.color
            moves = self.board.get_legal_moves(color)
            # パスの場合
            if not moves:
                color = c.black if self.color == c.white else c.white
                moves = self.board.get_legal_moves(color)
            value = playout(self.color, self.board, random.choice(moves))
            self.total += value
            self.count += 1
            # 子ノードの展開
            if self.count == self.excount:
                self.expand()

        # 子ノードが存在する場合
        else:
            value = -self.get_max_ucb1_child_node().evaluate()
            self.total += value
            self.count += 1

        return value
