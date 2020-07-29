"""Switch
"""

from reversi.strategies.common import Measure, AbstractStrategy


class SwitchSizeError(Exception):
    """
    入力サイズのエラー
    """
    pass


class Switch(AbstractStrategy):
    """
    複数戦略を切り替える
    """
    def __init__(self, turns=None, strategies=None):
        if len(turns) != len(strategies):
            raise SwitchSizeError

        self.turns = turns
        self.strategies = strategies

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        disc_num = board._black_score + board._white_score

        # 現在の手数が閾値以下
        strategy = self.strategies[-1]

        for i, turn in enumerate(self.turns):
            if disc_num - 4 <= turn:
                strategy = self.strategies[i]
                break

        return strategy.next_move(color, board)


# if __name__ == '__main__':
#     import os
#     from board import BitBoard
#     from reversi.strategies.iterative import IterativeDeepning
#
#     print('--- Test For SwitchNsI_B_TPW Strategy ---')
#     switch = SwitchNsI_B_TPW()
#     assert switch.turns == [15, 25, 35, 45, 60]
#     assert switch.strategies[0].__class__.__name__ == 'IterativeDeepning'
#     assert switch.strategies[1].__class__.__name__ == 'IterativeDeepning'
#     assert switch.strategies[2].__class__.__name__ == 'IterativeDeepning'
#     assert switch.strategies[3].__class__.__name__ == 'IterativeDeepning'
#     assert switch.strategies[4].__class__.__name__ == 'IterativeDeepning'
#
#     assert switch.strategies[0].search.evaluator.t.scorer.table._CORNER == 100
#     assert switch.strategies[1].search.evaluator.t.scorer.table._CORNER == 70
#     assert switch.strategies[2].search.evaluator.t.scorer.table._CORNER == 50
#     assert switch.strategies[3].search.evaluator.t.scorer.table._CORNER == 30
#     assert switch.strategies[4].search.evaluator.t.scorer.table._CORNER == 5
#
#     assert switch.strategies[0].search.evaluator.t.scorer.table._C == -20
#     assert switch.strategies[1].search.evaluator.t.scorer.table._C == -20
#     assert switch.strategies[2].search.evaluator.t.scorer.table._C == -20
#     assert switch.strategies[3].search.evaluator.t.scorer.table._C == 0
#     assert switch.strategies[4].search.evaluator.t.scorer.table._C == 0
#
#     assert switch.strategies[0].search.evaluator.t.scorer.table._A1 == 0
#     assert switch.strategies[1].search.evaluator.t.scorer.table._A1 == 0
#     assert switch.strategies[2].search.evaluator.t.scorer.table._A1 == 0
#     assert switch.strategies[3].search.evaluator.t.scorer.table._A1 == 1
#     assert switch.strategies[4].search.evaluator.t.scorer.table._A1 == 1
#
#     assert switch.strategies[0].search.evaluator.t.scorer.table._A2 == -1
#     assert switch.strategies[1].search.evaluator.t.scorer.table._A2 == -1
#     assert switch.strategies[2].search.evaluator.t.scorer.table._A2 == -1
#     assert switch.strategies[3].search.evaluator.t.scorer.table._A2 == 1
#     assert switch.strategies[4].search.evaluator.t.scorer.table._A2 == 1
#
#     assert switch.strategies[0].search.evaluator.t.scorer.table._B == -1
#     assert switch.strategies[1].search.evaluator.t.scorer.table._B == -1
#     assert switch.strategies[2].search.evaluator.t.scorer.table._B == -1
#     assert switch.strategies[3].search.evaluator.t.scorer.table._B == 1
#     assert switch.strategies[4].search.evaluator.t.scorer.table._B == 1
#
#     assert switch.strategies[0].search.evaluator.t.scorer.table._X == -25
#     assert switch.strategies[1].search.evaluator.t.scorer.table._X == -25
#     assert switch.strategies[2].search.evaluator.t.scorer.table._X == -25
#     assert switch.strategies[3].search.evaluator.t.scorer.table._X == 0
#     assert switch.strategies[4].search.evaluator.t.scorer.table._X == 0
#
#     assert switch.strategies[0].search.evaluator.t.scorer.table._O == -5
#     assert switch.strategies[1].search.evaluator.t.scorer.table._O == -5
#     assert switch.strategies[2].search.evaluator.t.scorer.table._O == -5
#     assert switch.strategies[3].search.evaluator.t.scorer.table._O == 1
#     assert switch.strategies[4].search.evaluator.t.scorer.table._O == 1
#
#     assert switch.strategies[0].search.evaluator.p.scorer._W == 5
#     assert switch.strategies[1].search.evaluator.p.scorer._W == 5
#     assert switch.strategies[2].search.evaluator.p.scorer._W == 5
#     assert switch.strategies[3].search.evaluator.p.scorer._W == 6
#     assert switch.strategies[4].search.evaluator.p.scorer._W == 8
#
#     bitboard8 = BitBoard()
#     bitboard8.put_disc('black', 3, 2)
#     bitboard8.put_disc('white', 2, 4)
#     bitboard8.put_disc('black', 5, 5)
#     bitboard8.put_disc('white', 4, 2)
#     bitboard8.put_disc('black', 5, 2)
#     bitboard8.put_disc('white', 5, 4)
#
#     key = switch.strategies[0].search.__class__.__name__ + str(os.getpid())
#     Measure.count[key] = 0
#     move = switch.next_move('black', bitboard8)
#     print(move)
#     assert move == (5, 3)
#     print('count     :', Measure.count[key])
#     assert Measure.count[key] >= 800
#
#     bitboard8.put_disc('black', 4, 5)
#     bitboard8.put_disc('white', 5, 6)
#     bitboard8.put_disc('black', 4, 6)
#     bitboard8.put_disc('white', 3, 7)
#     bitboard8.put_disc('black', 4, 7)
#     bitboard8.put_disc('white', 5, 7)
#     bitboard8.put_disc('black', 1, 4)
#     bitboard8.put_disc('white', 0, 4)
#     bitboard8.put_disc('black', 6, 5)
#     bitboard8.put_disc('white', 5, 3)
#     bitboard8.put_disc('black', 2, 5)
#     bitboard8.put_disc('white', 4, 1)
#     bitboard8.put_disc('black', 2, 3)
#     bitboard8.put_disc('white', 3, 1)
#     bitboard8.put_disc('black', 5, 1)
#     bitboard8.put_disc('white', 2, 2)
#     bitboard8.put_disc('black', 5, 0)
#     bitboard8.put_disc('white', 2, 1)
#     bitboard8.put_disc('black', 0, 5)
#     bitboard8.put_disc('white', 0, 6)
#     bitboard8.put_disc('black', 6, 3)
#     bitboard8.put_disc('white', 6, 4)
#     bitboard8.put_disc('black', 7, 4)
#     bitboard8.put_disc('white', 6, 2)
#     bitboard8.put_disc('black', 7, 3)
#     bitboard8.put_disc('white', 4, 0)
#     bitboard8.put_disc('black', 1, 2)
#     bitboard8.put_disc('white', 7, 5)
#     bitboard8.put_disc('black', 1, 0)
#     bitboard8.put_disc('white', 7, 2)
#     bitboard8.put_disc('black', 2, 0)
#     bitboard8.put_disc('white', 6, 0)
#     bitboard8.put_disc('black', 7, 6)
#     bitboard8.put_disc('white', 7, 7)
#     bitboard8.put_disc('black', 6, 7)
#     bitboard8.put_disc('white', 1, 5)
#     bitboard8.put_disc('black', 2, 7)
#     bitboard8.put_disc('white', 6, 6)
#     bitboard8.put_disc('black', 6, 1)
#     bitboard8.put_disc('white', 2, 6)
#     bitboard8.put_disc('black', 1, 6)
#     bitboard8.put_disc('white', 7, 1)
#     print(bitboard8)
#
#     key = switch.strategies[1].search.__class__.__name__ + str(os.getpid())
#     Measure.count[key] = 0
#     move = switch.next_move('black', bitboard8)
#     print(move)
#     assert move == (3, 6)
#     print('count     :', Measure.count[key])
#     assert Measure.count[key] >= 2000
#
#     print('--- Test For SwitchNsI_B_TPWE Strategy ---')
#     switch = SwitchNsI_B_TPWE()
#     key = switch.strategies[1].search.__class__.__name__ + str(os.getpid())
#     Measure.count[key] = 0
#     move = switch.next_move('black', bitboard8)
#     print(move)
#     assert move == (3, 6)
#     print('count     :', Measure.count[key])
#     assert Measure.count[key] >= 2000
