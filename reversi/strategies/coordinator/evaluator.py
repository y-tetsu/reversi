"""Evaluator
"""

from reversi.strategies.common import AbstractEvaluator
from reversi.strategies.coordinator import TableScorer, PossibilityScorer, OpeningScorer, WinLoseScorer, NumberScorer, EdgeScorer, CornerScorer


class Evaluator_T(AbstractEvaluator):
    """Evaluator_T

           盤面の評価値をTableで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5):
        self.scorer = TableScorer(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)  # Tableによる評価値算出

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        return self.scorer.get_score(kwargs['color'], kwargs['board'])


class Evaluator_P(AbstractEvaluator):
    """Evaluator_P

           盤面の評価値を配置可能数で算出
    """
    def __init__(self, wp=5):
        self.scorer = PossibilityScorer(wp)  # 配置可能数による評価値算出

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        return self.scorer.get_score(kwargs['legal_moves_b'], kwargs['legal_moves_w'])


class Evaluator_O(AbstractEvaluator):
    """Evaluator_O

           盤面の評価値を開放度で算出
    """
    def __init__(self, wo=-0.75):
        self.scorer = OpeningScorer(wo)  # 開放度による評価値算出

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        return self.scorer.get_score(kwargs['board'])


class Evaluator_W(AbstractEvaluator):
    """Evaluator_W

           盤面の評価値を勝敗で算出
    """
    def __init__(self, ww=10000):
        self.scorer = WinLoseScorer(ww)  # 勝敗による評価値算出

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        return self.scorer.get_score(kwargs['board'], kwargs['legal_moves_b'], kwargs['legal_moves_w'])


class Evaluator_N(AbstractEvaluator):
    """Evaluator_N

           盤面の評価値を石数で算出
    """
    def __init__(self):
        self.scorer = NumberScorer()  # 石数による評価値算出

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        return self.scorer.get_score(kwargs['board'])


class Evaluator_E(AbstractEvaluator):
    """Evaluator_E

           辺のパターンの評価値を算出
    """
    def __init__(self, w=100):
        self.scorer = EdgeScorer(w)  # 辺のパターンによる評価値算出

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        return self.scorer.get_score(kwargs['board'])


class Evaluator_C(AbstractEvaluator):
    """Evaluator_C

           隅のパターンの評価値を算出
    """
    def __init__(self, w=100):
        self.scorer = CornerScorer(w)  # 隅のパターンによる評価値算出

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        return self.scorer.get_score(kwargs['board'])


class Evaluator_TP(AbstractEvaluator):
    """Evaluator_TP

           盤面の評価値をTable+配置可能数で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5):
        self.t = Evaluator_T(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = Evaluator_P(wp)

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)

        return score_t + score_p


class Evaluator_TPO(AbstractEvaluator):
    """Evaluator_TPO

           盤面の評価値をTable+配置可能数+開放度で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, wo=-0.75):
        self.t = Evaluator_T(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = Evaluator_P(wp)
        self.o = Evaluator_O(wo)

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)
        score_o = self.o.evaluate(*args, **kwargs)

        return score_t + score_p + score_o


class Evaluator_NW(AbstractEvaluator):
    """Evaluator_NW

           盤面の評価値を石数+勝敗で算出
    """
    def __init__(self, ww=10000):
        self.n = Evaluator_N()
        self.w = Evaluator_W(ww)

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_n = self.n.evaluate(*args, **kwargs)

        return score_n


class Evaluator_PW(AbstractEvaluator):
    """Evaluator_PW

           盤面の評価値を配置可能数+勝敗で算出
    """
    def __init__(self, wp=5, ww=10000):
        self.p = Evaluator_P(wp)
        self.w = Evaluator_W(ww)

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_p = self.p.evaluate(*args, **kwargs)

        return score_p


class Evaluator_TPW(AbstractEvaluator):
    """Evaluator_TPW

           盤面の評価値をTable+配置可能数+勝敗で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000):
        self.t = Evaluator_T(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = Evaluator_P(wp)
        self.w = Evaluator_W(ww)

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)

        return score_t + score_p


class Evaluator_TPOW(Evaluator_TPO):
    """Evaluator_TPOW

           盤面の評価値をTable+配置可能数+開放度+勝敗で算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, wo=-0.75, ww=10000):
        self.t = Evaluator_T(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = Evaluator_P(wp)
        self.o = Evaluator_O(wo)
        self.w = Evaluator_W(ww)

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)
        score_o = self.o.evaluate(*args, **kwargs)

        return score_t + score_p + score_o


class Evaluator_TPWE(AbstractEvaluator):
    """Evaluator_TPWE

           盤面の評価値をTable+配置可能数+勝敗+辺のパターンで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000, we=100):
        self.t = Evaluator_T(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = Evaluator_P(wp)
        self.w = Evaluator_W(ww)
        self.e = Evaluator_E(we)

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)
        score_e = self.e.evaluate(*args, **kwargs)

        return score_t + score_p + score_e


class Evaluator_TPWEC(AbstractEvaluator):
    """Eavluator_TPWEC

           盤面の評価値をTable+配置可能数+勝敗+辺のパターン+隅のパターンで算出
    """
    def __init__(self, size=8, corner=50, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5, ww=10000, we=100, wc=120):
        self.t = Evaluator_T(size, corner, c, a1, a2, b1, b2, b3, x, o1, o2)
        self.p = Evaluator_P(wp)
        self.w = Evaluator_W(ww)
        self.e = Evaluator_E(we)
        self.c = Evaluator_C(wc)

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_t = self.t.evaluate(*args, **kwargs)
        score_p = self.p.evaluate(*args, **kwargs)
        score_e = self.e.evaluate(*args, **kwargs)
        score_c = self.c.evaluate(*args, **kwargs)

        return score_t + score_p + score_e + score_c


class Evaluator_PWE(AbstractEvaluator):
    """Evaluator_PWE

           盤面の評価値を配置可能数+勝敗+辺のパターンで算出
    """
    def __init__(self, size=8, wp=10, ww=10000, we=75):
        self.p = Evaluator_P(wp)
        self.w = Evaluator_W(ww)
        self.e = Evaluator_E(we)

    def evaluate(self, *args, **kwargs):
        """evaluate
        """
        score_w = self.w.evaluate(*args, **kwargs)

        # 勝敗が決まっている場合
        if score_w is not None:
            return score_w

        score_p = self.p.evaluate(*args, **kwargs)
        score_e = self.e.evaluate(*args, **kwargs)

        return score_p + score_e
