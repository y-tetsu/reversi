"""IterativeDeepning strategy
"""

from reversi.strategies.common import Timer, Measure, AbstractStrategy


class IterativeDeepning(AbstractStrategy):
    """IterativeDeepning
    """
    def __init__(self, depth=None, selector=None, sorter=None, search=None, limit=None):
        self.depth = depth
        self.selector = selector
        self.sorter = sorter
        self.search = search
        self.max_depth = depth
        self.limit = limit

    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        depth, moves, best_move, scores, = self.depth, None, None, {}

        Timer.set_deadline(self.search.__class__.__name__, self.search._MIN)  # 探索クラスのタイムアウトを設定

        moves = board.get_legal_moves(color)
        while True:
            moves = self.selector.select_moves(color, board, moves, scores, depth)                      # 次の手の候補を選択
            moves = self.sorter.sort_moves(color=color, board=board, moves=moves, best_move=best_move)  # 次の手の候補を並び替え
            best_move, scores = self.search.get_best_move(color, board, moves, depth)                   # 最善手を取得

            if Timer.is_timeout(self.search):  # タイムアウト発生時、処理を抜ける
                break

            if self.limit and depth >= self.limit:  # 限界深さに到達時
                break

            depth += 1  # 読みの深さを増やす

        self.max_depth = depth  # 読んだ深さを記録

        return best_move
