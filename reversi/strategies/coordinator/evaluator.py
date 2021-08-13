"""Evaluator
"""

from reversi.strategies.common import AbstractEvaluator
from reversi.strategies.coordinator import TableScorer, PossibilityScorer, OpeningScorer, WinLoseScorer, NumberScorer, EdgeScorer, CornerScorer, BlankScorer, EdgeCornerScorer  # noqa: E501
import reversi.strategies.coordinator.EvaluatorMethods as EvaluatorMethods


class Evaluator(AbstractEvaluator):
    """General Evaluator
    """
    def __init__(self, separated=[], combined=[]):
        self.separated = separated
        self.combined = combined

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        for scorer in self.separated:
            score = scorer.get_score(*args, **kwargs)
            if score is not None:
                return score

        score = 0
        for scorer in self.combined:
            score += scorer.get_score(*args, **kwargs)

        return score


class Evaluator_T(AbstractEvaluator):
    """Specific Evaluator Table

           盤面の評価値をTableで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5):
        self.scorer = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)  # Tableによる評価値算出

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        return self.scorer.get_score(board=board)


class Evaluator_P(AbstractEvaluator):
    """Specific Evaluator Possibility

           盤面の評価値を配置可能数で算出
    """
    def __init__(self, wp=5):
        self.scorer = PossibilityScorer(wp)  # 配置可能数による評価値算出

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        return self.scorer.get_score(possibility_b=possibility_b, possibility_w=possibility_w)


class Evaluator_O(AbstractEvaluator):
    """Specific Evaluator Opening

           盤面の評価値を開放度で算出
    """
    def __init__(self, wo=-0.75):
        self.scorer = OpeningScorer(wo)  # 開放度による評価値算出

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        return self.scorer.get_score(board=board)


class Evaluator_W(AbstractEvaluator):
    """Specific Evaluator WinLose

           盤面の評価値を勝敗で算出
    """
    def __init__(self, ww=10000):
        self.scorer = WinLoseScorer(ww)  # 勝敗による評価値算出

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        return self.scorer.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)


class Evaluator_N(AbstractEvaluator):
    """Specific Evaluator Number

           盤面の評価値を石数で算出
    """
    def __init__(self):
        self.scorer = NumberScorer()  # 石数による評価値算出

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        return self.scorer.get_score(board=board)


class Evaluator_N_Fast(AbstractEvaluator):
    """Specific Evaluator Number

           盤面の評価値を石数で算出
    """
    def evaluate(self, color, board, possibility_b, possibility_w):
        return board._black_score - board._white_score


class Evaluator_E(AbstractEvaluator):
    """Specific Evaluator Edge

           辺のパターンの評価値を算出
    """
    def __init__(self, w=100):
        self.scorer = EdgeScorer(w)  # 辺のパターンによる評価値算出

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        return self.scorer.get_score(board=board)


class Evaluator_C(AbstractEvaluator):
    """Specific Evaluator Corner

           隅のパターンの評価値を算出
    """
    def __init__(self, w=100):
        self.scorer = CornerScorer(w)  # 隅のパターンによる評価値算出

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        return self.scorer.get_score(board=board)


class Evaluator_B(AbstractEvaluator):
    """Specific Evaluator Blank

           空きマスのパターンの評価値を算出
    """
    def __init__(self, w1=-1, w2=-4, w3=-2):
        self.scorer = BlankScorer(w1, w2, w3)  # 空マスのパターンによる評価値算出

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        return self.scorer.get_score(board=board)


class Evaluator_Ec(AbstractEvaluator):
    """Specific Evaluator EdgeCorner

           辺と隅のパターンの評価値を算出
    """
    def __init__(self, w1=1, w2=8):
        self.scorer = EdgeCornerScorer(w1, w2)  # 辺と隅のパターンによる評価値算出

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        return self.scorer.get_score(board=board)


class Evaluator_TP(AbstractEvaluator):
    """Specific Evaluator Table + Possibility

           盤面の評価値をTable+配置可能数で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5):
        self.t = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = PossibilityScorer(wp)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_t = self.t.get_score(board=board)
        score_p = self.p.get_score(possibility_b=possibility_b, possibility_w=possibility_w)

        return score_t + score_p


class Evaluator_TPO(AbstractEvaluator):
    """Specific Evaluator Table + Possibility + Opening

           盤面の評価値をTable+配置可能数+開放度で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, wo=-0.75):
        self.t = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = PossibilityScorer(wp)
        self.o = OpeningScorer(wo)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_t = self.t.get_score(board=board)
        score_p = self.p.get_score(possibility_b=possibility_b, possibility_w=possibility_w)
        score_o = self.o.get_score(board=board)

        return score_t + score_p + score_o


class Evaluator_NW(AbstractEvaluator):
    """Specific Evaluator Number + WinLose

           盤面の評価値を石数+勝敗で算出
    """
    def __init__(self, ww=10000):
        self.n = NumberScorer()
        self.w = WinLoseScorer(ww)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_n = self.n.get_score(board=board)

        return score_n


class Evaluator_PW(AbstractEvaluator):
    """Specific Evaluator Possibility + WinLose

           盤面の評価値を配置可能数+勝敗で算出
    """
    def __init__(self, wp=5, ww=10000):
        self.p = PossibilityScorer(wp)
        self.w = WinLoseScorer(ww)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_p = self.p.get_score(possibility_b=possibility_b, possibility_w=possibility_w)

        return score_p


class Evaluator_TPW(AbstractEvaluator):
    """Specific Evaluator Table + Possibility + WinLose

           盤面の評価値をTable+配置可能数+勝敗で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000):
        self.t = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = PossibilityScorer(wp)
        self.w = WinLoseScorer(ww)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.get_score(board=board)
        score_p = self.p.get_score(possibility_b=possibility_b, possibility_w=possibility_w)

        return score_t + score_p


class Evaluator_TPW_Fast(AbstractEvaluator):
    """Specific Evaluator Table + Possibility + WinLose

           盤面の評価値をTable+配置可能数+勝敗で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000):
        self.t = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = PossibilityScorer(wp)
        self.w = WinLoseScorer(ww)
        self.params = [wp, ww]

    def evaluate(self, color, board, possibility_b, possibility_w):
        return EvaluatorMethods.evaluate_tpw(self.t, self.params, color, board, possibility_b, possibility_w)


class Evaluator_TPOW(AbstractEvaluator):
    """Specific Evaluator Table + Possibility + Opening + WinLose

           盤面の評価値をTable+配置可能数+開放度+勝敗で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, wo=-0.75, ww=10000):
        self.t = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = PossibilityScorer(wp)
        self.o = OpeningScorer(wo)
        self.w = WinLoseScorer(ww)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.get_score(board=board)
        score_p = self.p.get_score(possibility_b=possibility_b, possibility_w=possibility_w)
        score_o = self.o.get_score(board=board)

        return score_t + score_p + score_o


class Evaluator_TPWE(AbstractEvaluator):
    """Specific Evaluator Table + Possibility + WinLose + Edge

           盤面の評価値をTable+配置可能数+勝敗+辺のパターンで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000, we=100):
        self.t = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = PossibilityScorer(wp)
        self.w = WinLoseScorer(ww)
        self.e = EdgeScorer(we)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.get_score(board=board)
        score_p = self.p.get_score(possibility_b=possibility_b, possibility_w=possibility_w)
        score_e = self.e.get_score(board=board)

        return score_t + score_p + score_e


class Evaluator_TPWE_Fast(AbstractEvaluator):
    """Specific Evaluator Table + Possibility + WinLose + Edge

           盤面の評価値をTable+配置可能数+勝敗+辺のパターンで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000, we=100):
        self.t = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = PossibilityScorer(wp)
        self.w = WinLoseScorer(ww)
        self.e = EdgeScorer(we)
        self.params = [wp, ww, we]

    def evaluate(self, color, board, possibility_b, possibility_w):
        return EvaluatorMethods.evaluate_tpwe(self.t, self.params, color, board, possibility_b, possibility_w)


class Evaluator_TPWEC(AbstractEvaluator):
    """Specific Eavluator Table + Possibility + WinLose + Edge + Corner

           盤面の評価値をTable+配置可能数+勝敗+辺のパターン+隅のパターンで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000, we=100, wc=120):
        self.t = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = PossibilityScorer(wp)
        self.w = WinLoseScorer(ww)
        self.e = EdgeScorer(we)
        self.c = CornerScorer(wc)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.get_score(board=board)
        score_p = self.p.get_score(possibility_b=possibility_b, possibility_w=possibility_w)
        score_e = self.e.get_score(board=board)
        score_c = self.c.get_score(board=board)

        return score_t + score_p + score_e + score_c


class Evaluator_PWE(AbstractEvaluator):
    """Specific Evaluator Possibility + WinLose + Edge

           盤面の評価値を配置可能数+勝敗+辺のパターンで算出
    """
    def __init__(self, size=8, wp=10, ww=10000, we=75):
        self.p = PossibilityScorer(wp)
        self.w = WinLoseScorer(ww)
        self.e = EdgeScorer(we)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_p = self.p.get_score(possibility_b=possibility_b, possibility_w=possibility_w)
        score_e = self.e.get_score(board=board)

        return score_p + score_e


class Evaluator_BW(AbstractEvaluator):
    """Specific Evaluator Blank + WinLose

           盤面の評価値を空きマス+勝敗で算出
    """
    def __init__(self, wb1=-1, wb2=-4, wb3=-2, ww=10000):
        self.b = BlankScorer(wb1, wb2, wb3)
        self.w = WinLoseScorer(ww)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_b = self.b.get_score(board=board)

        return score_b


class Evaluator_EcW(AbstractEvaluator):
    """Specific Evaluator EdgeCorner + WinLose

           盤面の評価値を辺と隅のパターン+勝敗で算出
    """
    def __init__(self, wec1=1, wec2=8, ww=10000):
        self.ec = EdgeCornerScorer(wec1, wec2)
        self.w = WinLoseScorer(ww)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_ec = self.ec.get_score(board=board)

        return score_ec


class Evaluator_BWEc(AbstractEvaluator):
    """Specific Evaluator Blank + WinLose + EdgeCorner

           盤面の評価値を空きマスと辺と隅のパターン+勝敗で算出
    """
    def __init__(self, wb1=-1, wb2=-4, wb3=-2, we1=1, we2=8, ww=10000):
        self.b = BlankScorer(wb1, wb2, wb3)
        self.ec = EdgeCornerScorer(we1, we2)
        self.w = WinLoseScorer(ww)

    def evaluate(self, color, board, possibility_b, possibility_w):
        """evaluate
        """
        score_w = self.w.get_score(board=board, possibility_b=possibility_b, possibility_w=possibility_w)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_b = self.b.get_score(board=board)
        score_ec = self.ec.get_score(board=board)

        return score_b + score_ec
