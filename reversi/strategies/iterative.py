"""IterativeDeepning strategy
"""

from reversi.strategies.common import Timer, Measure, AbstractStrategy


class _IterativeDeepning_(AbstractStrategy):
    """IterativeDeepning + Timer
    """
    def __init__(self, depth=None, selector=None, orderer=None, search=None, limit=None):
        self.depth = depth
        self.selector = selector
        self.orderer = orderer
        self.search = search
        self.max_depth = depth
        self.limit = limit

    def next_move(self, color, board):
        """next_move
        """
        depth, moves, best_move, scores, = self.depth, None, None, {}

        pid = Timer.get_pid(self.search)           # タイムアウト監視用のプロセスID
        Timer.set_deadline(pid, self.search._MIN)  # 探索クラスのタイムアウトを設定

        moves = board.get_legal_moves(color)
        while True:
            moves = self.selector.select_moves(color, board, moves, scores, depth)                          # 次の手の候補を選択
            moves = self.orderer.move_ordering(color=color, board=board, moves=moves, best_move=best_move)  # 次の手の候補を並び替え
            best_move, scores = self.search.get_best_move(color, board, moves, depth, pid)                  # 最善手を取得

            if Timer.is_timeout(pid):  # タイムアウト発生時、処理を抜ける
                break

            if self.limit and depth >= self.limit:  # 限界深さに到達時
                break

            depth += 1  # 読みの深さを増やす

        self.max_depth = depth  # 読んだ深さを記録

        return best_move


class IterativeDeepning(_IterativeDeepning_):
    """IterativeDeepning + Measure + Timer
    """
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)
