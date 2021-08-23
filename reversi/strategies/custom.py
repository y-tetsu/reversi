"""Custom strategies
"""

from reversi.strategies.common import Measure
from reversi.strategies import Random, MonteCarlo, MinMax, NegaMax, AlphaBeta_, AlphaBeta, NegaScout, Switch, FullReading_, _FullReading, FullReading, IterativeDeepning_, IterativeDeepning, Usagi, Tora, _Ushi_, Ushi, Nezumi, Neko, Hitsuji  # noqa: E501
from reversi.strategies.coordinator import Selector, Orderer_B, Orderer_PCB, Evaluator_T, Evaluator_TP, Evaluator_TPO, Evaluator_TPW, Evaluator_TPWE, Evaluator_TPWEB, Evaluator_TPWE_Fast, Evaluator_TPWEC, Evaluator_TPOW, Evaluator_PWE  # noqa: E501


# ---------- #
# MonteCarlo #
# ---------- #
class MonteCarlo30(MonteCarlo):
    """
    MonteCarlo法で次の手を決める(最大一手30回試行)
    """
    def __init__(self, count=30):
        super().__init__(count)


class MonteCarlo100(MonteCarlo):
    """
    MonteCarlo法で次の手を決める(最大一手100回試行)
    """
    def __init__(self, count=100):
        super().__init__(count)


class MonteCarlo1000(MonteCarlo):
    """
    MonteCarlo法で次の手を決める(最大一手1000回試行)
    """
    def __init__(self, count=1000):
        super().__init__(count)


# ------ #
# MinMax #
# ------ #
class MinMax1_T(MinMax):
    """
    MinMax法でEvaluator_Tにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax2_T(MinMax):
    """
    MinMax法でEvaluator_Tにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax3_T(MinMax):
    """
    MinMax法でEvaluator_Tにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax4_T(MinMax):
    """
    MinMax法でEvaluator_Tにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax1_TP(MinMax):
    """
    MinMax法でEvaluator_TPにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TP()):
        super().__init__(depth, evaluator)


class MinMax2_TP(MinMax):
    """
    MinMax法でEvaluator_TPにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TP()):
        super().__init__(depth, evaluator)


class MinMax3_TP(MinMax):
    """
    MinMax法でEvaluator_TPにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TP()):
        super().__init__(depth, evaluator)


class MinMax4_TP(MinMax):
    """
    MinMax法でEvaluator_TPにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TP()):
        super().__init__(depth, evaluator)


class MinMax1_TPO(MinMax):
    """
    MinMax法でEvaluator_TPOにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPO()):
        super().__init__(depth, evaluator)


class MinMax2_TPO(MinMax):
    """
    MinMax法でEvaluator_TPOにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPO()):
        super().__init__(depth, evaluator)


class MinMax3_TPO(MinMax):
    """
    MinMax法でEvaluator_TPOにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPO()):
        super().__init__(depth, evaluator)


class MinMax4_TPO(MinMax):
    """
    MinMax法でEvaluator_TPOにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPO()):
        super().__init__(depth, evaluator)


class MinMax1_TPW(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class MinMax2_TPW(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class MinMax3_TPW(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class MinMax4_TPW(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class MinMax1_TPOW(MinMax):
    """
    MinMax法でEvaluator_TPOWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class MinMax2_TPOW(MinMax):
    """
    MinMax法でEvaluator_TPOWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class MinMax3_TPOW(MinMax):
    """
    MinMax法でEvaluator_TPOWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class MinMax4_TPOW(MinMax):
    """
    MinMax法でEvaluator_TPOWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class MinMax1_TPWE(MinMax):
    """
    MinMax法でEvaluator_TPWEにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class MinMax2_TPWE(MinMax):
    """
    MinMax法でEvaluator_TPWEにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class MinMax3_TPWE(MinMax):
    """
    MinMax法でEvaluator_TPWEにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class MinMax4_TPWE(MinMax):
    """
    MinMax法でEvaluator_TPWEにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class MinMax1_TPWEC(MinMax):
    """
    MinMax法でEvaluator_TPWECにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPWEC()):
        super().__init__(depth, evaluator)


class MinMax2_TPWEC(MinMax):
    """
    MinMax法でEvaluator_TPWECにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPWEC()):
        super().__init__(depth, evaluator)


class MinMax3_TPWEC(MinMax):
    """
    MinMax法でEvaluator_TPWECにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPWEC()):
        super().__init__(depth, evaluator)


class MinMax4_TPWEC(MinMax):
    """
    MinMax法でEvaluator_TPWECにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPWEC()):
        super().__init__(depth, evaluator)


class MinMax1_PWE(MinMax):
    """
    MinMax法でEvaluator_PWEにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_PWE()):
        super().__init__(depth, evaluator)


class MinMax2_PWE(MinMax):
    """
    MinMax法でEvaluator_PWEにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_PWE()):
        super().__init__(depth, evaluator)


class MinMax3_PWE(MinMax):
    """
    MinMax法でEvaluator_PWEにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_PWE()):
        super().__init__(depth, evaluator)


class MinMax4_PWE(MinMax):
    """
    MinMax法でEvaluator_PWEにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_PWE()):
        super().__init__(depth, evaluator)


# ------- #
# NegaMax #
# ------- #
class NegaMax1_TPW(NegaMax):
    """
    NegaMax法でEvaluator_TPWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaMax2_TPW(NegaMax):
    """
    NegaMax法でEvaluator_TPWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaMax3_TPW(NegaMax):
    """
    NegaMax法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaMax4_TPW(NegaMax):
    """
    NegaMax法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaMax1_TPOW(NegaMax):
    """
    NegaMax法でEvaluator_TPOWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaMax2_TPOW(NegaMax):
    """
    NegaMax法でEvaluator_TPOWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaMax3_TPOW(NegaMax):
    """
    NegaMax法でEvaluator_TPOWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaMax4_TPOW(NegaMax):
    """
    NegaMax法でEvaluator_TPOWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


# --------- #
# AlphaBeta #
# --------- #
class AlphaBeta_TPW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPW()):
        super().__init__(evaluator=evaluator)


class AlphaBeta_TPWE(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWEにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPWE()):
        super().__init__(evaluator=evaluator)


class AlphaBeta_TPWE_(AlphaBeta_):
    """
    AlphaBeta法でEvaluator_TPWEにより次の手を決める(メジャーなし)
    """
    def __init__(self, evaluator=Evaluator_TPWE()):
        super().__init__(evaluator=evaluator)


class AlphaBeta_TPWEC(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWECにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPWEC()):
        super().__init__(evaluator=evaluator)


class AlphaBeta1_TPW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class AlphaBeta2_TPW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class AlphaBeta3_TPW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class AlphaBeta4_TPW(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class AlphaBeta1_TPWE(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWEにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class AlphaBeta2_TPWE(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWEにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class AlphaBeta3_TPWE(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWEにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class AlphaBeta4_TPWE(AlphaBeta):
    """
    AlphaBeta法でEvaluator_TPWEにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


# --------- #
# NegaScout #
# --------- #
class NegaScout_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPW()):
        super().__init__(evaluator=evaluator)


class NegaScout_TPWE(NegaScout):
    """
    NegaScout法でEvaluator_TPWEにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPWE()):
        super().__init__(evaluator=evaluator)


class NegaScout_TPWEB(NegaScout):
    """
    NegaScout法でEvaluator_TPWEBにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPWEB()):
        super().__init__(evaluator=evaluator)


class NegaScout1_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout2_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout3_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout4_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout1_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaScout2_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaScout3_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaScout4_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaScout1_TPWE(NegaScout):
    """
    NegaScout法でEvaluator_TPWEにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class NegaScout2_TPWE(NegaScout):
    """
    NegaScout法でEvaluator_TPWEにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class NegaScout3_TPWE(NegaScout):
    """
    NegaScout法でEvaluator_TPWEにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class NegaScout4_TPWE(NegaScout):
    """
    NegaScout法でEvaluator_TPWEにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


# ----------------- #
# IterativeDeepning #
# ----------------- #
class AbI_B_TPW(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPW)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta_TPW()):
        super().__init__(depth, selector, orderer, search)


class AbI_B_TPWE(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWE)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta_TPWE()):
        super().__init__(depth, selector, orderer, search)


class AbI_PCB_TPWE(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:PCB、評価関数:TPWE)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_PCB(), search=AlphaBeta_TPWE()):
        super().__init__(depth, selector, orderer, search)


class AbI_B_TPWE_(IterativeDeepning_):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWE)(メジャーなし)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta_TPWE_()):
        super().__init__(depth, selector, orderer, search)


class AbI_B_TPWEC(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWEC)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta_TPWEC()):
        super().__init__(depth, selector, orderer, search)


class NsI_B_TPW(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPW)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout_TPW()):
        super().__init__(depth, selector, orderer, search)


class NsI_B_TPWE(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWE)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout_TPWE()):
        super().__init__(depth, selector, orderer, search)


class NsI_B_TPWEB(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWEB)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout_TPWEB()):
        super().__init__(depth, selector, orderer, search)


# ------ #
# Switch #
# ------ #
class SwitchAbI_B_TPWE(Switch):
    """
    AbI_B_TPWEのパラーメータ切り替え型
    """
    def __init__(
            self,
            turns=[
                12,
                24,
                36,
                48,
                60
            ],
            strategies=[
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta(evaluator=Evaluator_TPWE(corner=50, c=-20, a1=-10, a2=0,  b1=-4, b2=-2, b3=-2, x=-25, o1=-13, o2=-5, wp=4, ww=9999,  we=91))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta(evaluator=Evaluator_TPWE(corner=44, c=-18, a1=-4,  a2=-2, b1=-2, b2=-4, b3=-3, x=-40, o1=-10, o2=-8, wp=4, ww=10001, we=95))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta(evaluator=Evaluator_TPWE(corner=41, c=-14, a1=-1,  a2=-4, b1=-4, b2=-1, b3=2,  x=-38, o1=-5,  o2=-5, wp=4, ww=9996,  we=103))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta(evaluator=Evaluator_TPWE(corner=62, c=-19, a1=1,   a2=0,  b1=-1, b2=0,  b3=1,  x=-25, o1=-4,  o2=-2, wp=8, ww=9990,  we=94))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta(evaluator=Evaluator_TPWE(corner=50, c=-23, a1=0,   a2=-9, b1=-2, b2=-2, b3=16, x=-25, o1=-9,  o2=-8, wp=8, ww=9998,  we=93)))    # noqa: E501
            ]):
        super().__init__(turns, strategies)


class SwitchNsI_B_TPWE(Switch):
    """
    NsI_B_TPWEのパラーメータ切り替え型
    """
    def __init__(
            self,
            turns=[
                12,
                24,
                36,
                48,
                60
            ],
            # generation 843
            strategies=[
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=50, c=-20, a1=-10, a2=0,  b1=-4, b2=-2, b3=-2, x=-25, o1=-13, o2=-5, wp=4, ww=9999,  we=91))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=44, c=-18, a1=-4,  a2=-2, b1=-2, b2=-4, b3=-3, x=-40, o1=-10, o2=-8, wp=4, ww=10001, we=95))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=41, c=-14, a1=-1,  a2=-4, b1=-4, b2=-1, b3=2,  x=-38, o1=-5,  o2=-5, wp=4, ww=9996,  we=103))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=62, c=-19, a1=1,   a2=0,  b1=-1, b2=0,  b3=1,  x=-25, o1=-4,  o2=-2, wp=8, ww=9990,  we=94))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=50, c=-23, a1=0,   a2=-9, b1=-2, b2=-2, b3=16, x=-25, o1=-9,  o2=-8, wp=8, ww=9998,  we=93)))    # noqa: E501
            ]):
        super().__init__(turns, strategies)


class SwitchNsI_B_TPWE_F(Switch):
    """
    NsI_B_TPWEのパラーメータ切り替え型
    """
    def __init__(
            self,
            turns=[
                12,
                24,
                36,
                48,
                60
            ],
            # generation 843
            strategies=[
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE_Fast(corner=50, c=-20, a1=-10, a2=0,  b1=-4, b2=-2, b3=-2, x=-25, o1=-13, o2=-5, wp=4, ww=9999,  we=91))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE_Fast(corner=44, c=-18, a1=-4,  a2=-2, b1=-2, b2=-4, b3=-3, x=-40, o1=-10, o2=-8, wp=4, ww=10001, we=95))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE_Fast(corner=41, c=-14, a1=-1,  a2=-4, b1=-4, b2=-1, b3=2,  x=-38, o1=-5,  o2=-5, wp=4, ww=9996,  we=103))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE_Fast(corner=62, c=-19, a1=1,   a2=0,  b1=-1, b2=0,  b3=1,  x=-25, o1=-4,  o2=-2, wp=8, ww=9990,  we=94))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE_Fast(corner=50, c=-23, a1=0,   a2=-9, b1=-2, b2=-2, b3=16, x=-25, o1=-9,  o2=-8, wp=8, ww=9998,  we=93)))    # noqa: E501
            ]):
        super().__init__(turns, strategies)


class SwitchNsI_B_TPWE_Type2(Switch):
    """
    NsI_B_TPWEのパラーメータ切り替え型
    """
    def __init__(
            self,
            turns=[
                12,
                24,
                36,
                48,
                60
            ],
            # generation 1279
            strategies=[
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=42, c=-17, a1=-7,  a2=2,   b1=-7, b2=-6, b3=-3, x=-26, o1=-23, o2=-9,  wp=4,  ww=10002, we=84))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=39, c=-12, a1=-3,  a2=-3,  b1=-5, b2=-4, b3=-2, x=-34, o1=-9,  o2=-7,  wp=4,  ww=10003, we=82))),   # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=43, c=-20, a1=-2,  a2=-2,  b1=-2, b2=-2, b3=3,  x=-32, o1=-4,  o2=-6,  wp=4,  ww=9996,  we=114))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=67, c=-19, a1=-6,  a2=1,   b1=-1, b2=0,  b3=3,  x=-24, o1=-5,  o2=-2,  wp=10, ww=9993,  we=101))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE(corner=47, c=-37, a1=-11, a2=-15, b1=5,  b2=-3, b3=16, x=-24, o1=-6,  o2=-15, wp=12, ww=9999,  we=87)))    # noqa: E501
            ]):
        super().__init__(turns, strategies)


# ----------- #
# FullReading #
# ----------- #
class MinMax2F9_TPWE(FullReading):
    """
    MinMax法で2手先を読む
    (評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=MinMax2_TPWE()):
        super().__init__(remain, base)


class AlphaBeta4F9_TPW(FullReading):
    """
    AlphaBeta法で4手先を読む
    (評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AlphaBeta4_TPW()):
        super().__init__(remain, base)


class AlphaBeta4F10_TPW(FullReading):
    """
    AlphaBeta法で4手先を読む
    (評価関数:TPW, 完全読み開始:残り10手)
    """
    def __init__(self, remain=10, base=AlphaBeta4_TPW()):
        super().__init__(remain, base)


class AbIF9_B_TPW(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_B_TPW()):
        super().__init__(remain, base)


class AbIF9_B_TPWE(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_B_TPWE()):
        super().__init__(remain, base)


class AbIF9_PCB_TPWE(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:PCB、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_PCB_TPWE()):
        super().__init__(remain, base)


class AbIF10_B_TPWE(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り10手)
    """
    def __init__(self, remain=10, base=AbI_B_TPWE()):
        super().__init__(remain, base)


class AbIF10_PCB_TPWE(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:PCB、評価関数:TPWE, 完全読み開始:残り10手)
    """
    def __init__(self, remain=10, base=AbI_PCB_TPWE()):
        super().__init__(remain, base)


class AbIF9_B_TPWE_(FullReading_):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(メジャーなし)
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_B_TPWE_()):
        super().__init__(remain, base)


class AbIF9_B_TPWEC(FullReading):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWEC, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_B_TPWEC()):
        super().__init__(remain, base)


class NsIF9_B_TPW(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=NsI_B_TPW()):
        super().__init__(remain, base)


class NsIF9_B_TPWE(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=NsI_B_TPWE()):
        super().__init__(remain, base)


class NsIF10_B_TPWE(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り10手)
    """
    def __init__(self, remain=10, base=NsI_B_TPWE()):
        super().__init__(remain, base)


class NsIF10_B_TPWEB(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWEB, 完全読み開始:残り10手)
    """
    def __init__(self, remain=10, base=NsI_B_TPWEB()):
        super().__init__(remain, base)


class NsIF10_B_TPW(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り10手)
    """
    def __init__(self, remain=10, base=NsI_B_TPW()):
        super().__init__(remain, base)


class NsIF11_B_TPW(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り11手)
    """
    def __init__(self, remain=11, base=NsI_B_TPW()):
        super().__init__(remain, base)


class NsIF12_B_TPW(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り12手)
    """
    def __init__(self, remain=12, base=NsI_B_TPW()):
        super().__init__(remain, base)


class SwitchAbIF9_B_TPWE(FullReading):
    """
    SwitchAbI_B_TPWE+完全読み開始:残り9手
    """
    def __init__(self, remain=9, base=SwitchAbI_B_TPWE()):
        super().__init__(remain, base)


class SwitchNsIF9_B_TPWE(FullReading):
    """
    SwitchNsI_B_TPWE+完全読み開始:残り9手
    """
    def __init__(self, remain=9, base=SwitchNsI_B_TPWE()):
        super().__init__(remain, base)


class SwitchNsIF10_B_TPWE(FullReading):
    """
    SwitchNsI_B_TPWE+完全読み開始:残り10手
    """
    def __init__(self, remain=10, base=SwitchNsI_B_TPWE()):
        super().__init__(remain, base)


class SwitchNsIF10_B_TPWE_F(FullReading):
    """
    SwitchNsI_B_TPWE_F+完全読み開始:残り10手
    """
    def __init__(self, remain=10, base=SwitchNsI_B_TPWE_F()):
        super().__init__(remain, base)


class SwitchNsIF10_B_TPWE_Type2(FullReading):
    """
    SwitchNsI_B_TPWE_Type2+完全読み開始:残り10手
    """
    def __init__(self, remain=10, base=SwitchNsI_B_TPWE_Type2()):
        super().__init__(remain, base)


class RandomF11(_FullReading):
    """
    ランダムに手を読む
    (4x4のみ完全読み:残り11手)
    """
    def __init__(self, remain=11, base=Random()):
        super().__init__(remain, base)

    @Measure.time
    def next_move(self, color, board):
        if board.size == 4:
            return super().next_move(color, board)

        return self.base.next_move(color, board)


# ------ #
# Joseki #
# ------ #
class AlphaBeta4J_TPW(Usagi):
    """
    AlphaBeta法で4手先読みして次の手を決める+定石打ち
    (評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, base=AlphaBeta4_TPW()):
        super().__init__(base)


class AlphaBeta4F9J_TPW(Tora):
    """
    AlphaBeta法で4手先読みして次の手を決める+定石打ち
    (評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, base=AlphaBeta4F9_TPW()):
        super().__init__(base)


class AlphaBeta4F10J_TPW(Tora):
    """
    AlphaBeta法で4手先読みして次の手を決める+定石打ち
    (評価関数:TPW, 完全読み開始:残り10手)
    """
    def __init__(self, base=AlphaBeta4F10_TPW()):
        super().__init__(base)


class AbIF9J_B_TPW(Nezumi):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, base=AbIF9_B_TPW()):
        super().__init__(base)


class AbIF9J_B_TPWE(Ushi):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, base=AbIF9_B_TPWE()):
        super().__init__(base)


class AbIF9J_PCB_TPWE(Ushi):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:PCB、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, base=AbIF9_PCB_TPWE()):
        super().__init__(base)


class AbIF10J_B_TPWE(Ushi):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り10手)
    """
    def __init__(self, base=AbIF10_B_TPWE()):
        super().__init__(base)


class AbIF10J_PCB_TPWE(Ushi):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:PCB、評価関数:TPWE, 完全読み開始:残り10手)
    """
    def __init__(self, base=AbIF10_PCB_TPWE()):
        super().__init__(base)


class AbIF9J_B_TPWE_(_Ushi_):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち(メジャーなし)
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, base=AbIF9_B_TPWE_()):
        super().__init__(base)


class AbIF9J_B_TPWEC(Hitsuji):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPWEC, 完全読み開始:残り9手)
    """
    def __init__(self, base=AbIF9_B_TPWEC()):
        super().__init__(base)


class NsIF9J_B_TPW(Ushi):
    """
    NegaScout法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, base=NsIF9_B_TPW()):
        super().__init__(base)


class NsIF9J_B_TPWE(Nezumi):
    """
    NegaScout法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, base=NsIF9_B_TPWE()):
        super().__init__(base)


class NsIF10J_B_TPWE(Neko):
    """
    NegaScout法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り10手)
    """
    def __init__(self, base=NsIF10_B_TPWE()):
        super().__init__(base)


class NsIF10J_B_TPWEB(Ushi):
    """
    NegaScout法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPWEB, 完全読み開始:残り10手)
    """
    def __init__(self, base=NsIF10_B_TPWEB()):
        super().__init__(base)


class SwitchAbIF9J_B_TPWE(Ushi):
    """
    SwitchNsIF9_B_TPWE+定石打ち
    (完全読み開始:残り9手)
    """
    def __init__(self, base=SwitchAbIF9_B_TPWE()):
        super().__init__(base)


class SwitchNsIF9J_B_TPWE(Neko):
    """
    SwitchNsIF9_B_TPWE+定石打ち
    (完全読み開始:残り9手)
    """
    def __init__(self, base=SwitchNsIF9_B_TPWE()):
        super().__init__(base)


class SwitchNsIF10J_B_TPWE(Neko):
    """
    SwitchNsIF10_B_TPWE+定石打ち
    (完全読み開始:残り10手)
    """
    def __init__(self, base=SwitchNsIF10_B_TPWE()):
        super().__init__(base)


class SwitchNsIF10J_B_TPWE_F(Neko):
    """
    SwitchNsIF10_B_TPWE_F+定石打ち
    (完全読み開始:残り10手)
    """
    def __init__(self, base=SwitchNsIF10_B_TPWE_F()):
        super().__init__(base)


class SwitchNsIF10J_B_TPWE_Type2(Hitsuji):
    """
    SwitchNsIF10_B_TPWE_Type2+定石打ち
    (完全読み開始:残り10手)
    """
    def __init__(self, base=SwitchNsIF10_B_TPWE_Type2()):
        super().__init__(base)
