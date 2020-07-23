"""IterativeDeepning strategy
"""

from reversi.strategies.common import Timer, Measure, AbstractStrategy
from reversi.strategies.alphabeta import AlphaBeta_TPW, AlphaBeta_TPWE, AlphaBeta_TPWEC
from reversi.strategies.negascout import NegaScout_TPW, NegaScout_TPW2, NegaScout_TPWE
from reversi.strategies.coordinator import Selector, Sorter_B


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


class AbI_B_TPW(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPW)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=AlphaBeta_TPW()):
        super().__init__(depth, selector, sorter, search)


class AbI_B_TPWE(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWE)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=AlphaBeta_TPWE()):
        super().__init__(depth, selector, sorter, search)


class AbI_B_TPWEC(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWEC)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=AlphaBeta_TPWEC()):
        super().__init__(depth, selector, sorter, search)


class NsI_B_TPW(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPW)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=NegaScout_TPW()):
        super().__init__(depth, selector, sorter, search)


class NsI_B_TPWE(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWE)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=NegaScout_TPWE()):
        super().__init__(depth, selector, sorter, search)


class NsI_B_TPW2(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPW2)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=NegaScout_TPW2()):
        super().__init__(depth, selector, sorter, search)
