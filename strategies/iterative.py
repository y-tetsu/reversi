#!/usr/bin/env python
"""
反復深化法
"""

import sys
sys.path.append('../')

from strategies.common import CPU_TIME, AbstractStrategy
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.alphabeta import AlphaBeta_TPOW
from strategies.selector import Selector, Selector_B, Selector_BC


class IterativeDeepning(AbstractStrategy):
    """
    反復深化法
    """
    def __init__(self, depth=None, selector=None, search=None):
        self.depth = depth
        self.selector = selector
        self.search = search
        self.max_depth = depth

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        depth, best_move, scores, = self.depth, None, {}

        Timer.set_deadline(self.search.__class__.__name__, CPU_TIME)  # 探索クラスのタイムアウトを設定

        while True:
            moves = self.selector.select_moves(color, board, best_move, scores, depth)  # 次の手の候補を選択
            best_move, scores = self.search.get_best_move(color, board, moves, depth)   # 最善手を取得

            if Timer.is_timeout(self.search):  # タイムアウト発生時、処理を抜ける
                break

            depth += 1  # 読みの深さを増やす

        self.max_depth = depth  # 読んだ深さを記録

        return best_move


class AbI_TPOW(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、評価関数:TPOW)
    """
    def __init__(self, depth=2, selector=Selector(), search=AlphaBeta_TPOW()):
        super().__init__(depth, selector, search)


class AbI_B_TPOW(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:B、評価関数:TPOW)
    """
    def __init__(self, depth=2, selector=Selector_B(), search=AlphaBeta_TPOW()):
        super().__init__(depth, selector, search)


class AbI_BC_TPOW(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:BC、評価関数:TPOW)
    """
    def __init__(self, depth=2, selector=Selector_BC(), search=AlphaBeta_TPOW()):
        super().__init__(depth, selector, search)


if __name__ == '__main__':
    import time
    from board import BitBoard

    bitboard8 = BitBoard()
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    print('--- Test For AbI_TPOW Strategy ---')
    iterative = AbI_TPOW()
    assert iterative.depth == 2

    Measure.count['AlphaBeta_TPOW'] = 0
    assert iterative.next_move('black', bitboard8) == (2, 2)
    print( 'max_depth :', iterative.max_depth )
    assert iterative.max_depth >= 5
    print( 'count     :', Measure.count['AlphaBeta_TPOW'] )
    assert Measure.count['AlphaBeta_TPOW'] >= 1000

    print('--- Test For AbI_B_TPOW Strategy ---')
    iterative = AbI_B_TPOW()
    assert iterative.depth == 2

    Measure.count['AlphaBeta_TPOW'] = 0
    assert iterative.next_move('black', bitboard8) == (5, 3)
    print( 'max_depth :', iterative.max_depth )
    assert iterative.max_depth >= 5
    print( 'count     :', Measure.count['AlphaBeta_TPOW'] )
    assert Measure.count['AlphaBeta_TPOW'] >= 1000

    print('--- Test For AbI_BC_TPOW Strategy ---')
    iterative = AbI_BC_TPOW()
    assert iterative.depth == 2

    Measure.count['AlphaBeta_TPOW'] = 0
    assert iterative.next_move('black', bitboard8) == (5, 3)
    print( 'max_depth :', iterative.max_depth )
    assert iterative.max_depth >= 5
    print( 'count     :', Measure.count['AlphaBeta_TPOW'] )
    assert Measure.count['AlphaBeta_TPOW'] >= 1000
