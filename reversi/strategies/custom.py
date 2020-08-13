"""Custom strategies
"""

from reversi.strategies.common import Measure
from reversi.strategies import Random, MonteCarlo, MinMax, _NegaMax, NegaMax, AlphaBeta_, AlphaBeta, AlphaBeta_old, NegaScout, Switch, FullReading_, _FullReading, FullReading, FullReading_old, _IterativeDeepning_, IterativeDeepning, Usagi, Tora, _Ushi_, Ushi, Nezumi, Neko, Hitsuji, RandomOpening, AB_TI  # noqa: E501
from reversi.strategies.coordinator import Selector, Orderer_B, Orderer_PCB, Evaluator_T, Evaluator_TP, Evaluator_TPO, Evaluator_TPW, Evaluator_TPWE, Evaluator_TPWEC, Evaluator_TPOW, Evaluator_PWE  # noqa: E501


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


class MinMax1_TPW2(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPW(corner=50, c=-20, a1=0, a2=22, b1=-1, b2=-1, b3=-1, x=-35, o1=-5, o2=-5, wp=5, ww=10000)):
        super().__init__(depth, evaluator)


class MinMax1_PWE(MinMax):
    """
    MinMax法でEvaluator_PWEにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_PWE()):
        super().__init__(depth, evaluator)


class MinMax1_TPWE(MinMax):
    """
    MinMax法でEvaluator_TPWEにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class MinMax1_TPWEC(MinMax):
    """
    MinMax法でEvaluator_TPWECにより次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_TPWEC()):
        super().__init__(depth, evaluator)


class MinMax2_TPW(MinMax):
    """
    MinMax法でEvaluator_TPWにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class MinMax2_TPWE(MinMax):
    """
    MinMax法でEvaluator_TPWEにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class MinMax2_TPWEC(MinMax):
    """
    MinMax法でEvaluator_TPWECにより次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_TPWEC()):
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


# ------- #
# NegaMax #
# ------- #
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


class _NegaMax3_TPW(_NegaMax):
    """
    NegaMax法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaMax3_TPW(NegaMax):
    """
    NegaMax法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
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


class AlphaBeta_TPWE_old(AlphaBeta_old):
    """
    AlphaBeta_old法でEvaluator_TPWEにより次の手を決める
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


class NegaScout_TPW2(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPW(corner=50, c=-20, a1=0, a2=22, b1=-1, b2=-1, b3=-1, x=-35, o1=-5, o2=-5, wp=5, ww=10000)):
        super().__init__(evaluator=evaluator)


class NegaScout_TPWE(NegaScout):
    """
    NegaScout法でEvaluator_TPWEにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPWE()):
        super().__init__(evaluator=evaluator)


class NegaScout3_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout3_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaScout4_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout4_TPWE(NegaScout):
    """
    NegaScout法でEvaluator_TPWEにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPWE()):
        super().__init__(depth, evaluator)


class NegaScout4_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPOW()):
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


class AbI_B_TPWE_old(IterativeDeepning):
    """
    AlphaBeta_old法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWE)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_B(), search=AlphaBeta_TPWE_old()):
        super().__init__(depth, selector, orderer, search)


class _AbI_B_TPWE_(_IterativeDeepning_):
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


class NsI_B_TPW2(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPW2)
    """
    def __init__(self, depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout_TPW2()):
        super().__init__(depth, selector, orderer, search)


# ------ #
# Switch #
# ------ #
class SwitchNsI_B_TPW(Switch):
    """
    NsI_B_TPWのパラーメータ切り替え型
    """
    def __init__(
            self,
            turns=[
                15,
                25,
                35,
                45,
                60
            ],
            strategies=[
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPW(corner=100, c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPW(corner=70,  c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPW(corner=50,  c=-20, a1=0, a2=-1, b1=-1, b2=-1, b3=-1, x=-25, o1=-5, o2=-5, wp=5))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPW(corner=30,  c=0,   a1=1, a2=1,  b1=1,  b2=1,  b3=1,  x=0,   o1=1,  o2=1,  wp=6))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPW(corner=5,   c=0,   a1=1, a2=1,  b1=1,  b2=1,  b3=1,  x=0,   o1=1,  o2=1,  wp=8)))   # noqa: E501
            ]):
        super().__init__(turns, strategies)


class SwitchNsI_B_TPWE(Switch):
    """
    NsI_B_TPWEのパラーメータ切り替え型
    """
    def __init__(
            self,
            turns=[
                15,
                25,
                35,
                45,
                60
            ],
            strategies=[
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE())),
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE())),
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPWE())),
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPW(corner=30, c=0, a1=1, a2=1, b1=1, b2=1, b3=1, x=0, o1=1, o2=1, wp=6))),  # noqa: E501
                IterativeDeepning(depth=2, selector=Selector(), orderer=Orderer_B(), search=NegaScout(evaluator=Evaluator_TPW(corner=5,  c=0, a1=1, a2=1, b1=1, b2=1, b3=1, x=0, o1=1, o2=1, wp=8)))   # noqa: E501
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


class AbIF9_B_TPWE_old(FullReading_old):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=AbI_B_TPWE_old()):
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
    def __init__(self, remain=9, base=_AbI_B_TPWE_()):
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


class NsIF9_B_TPW2(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=NsI_B_TPW2()):
        super().__init__(remain, base)


class NsIF9_B_TPWE(FullReading):
    """
    NegaScout法に反復深化法を適用して次の手を決める
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, remain=9, base=NsI_B_TPWE()):
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


class SwitchNsIF9_B_TPW(FullReading):
    """
    SwitchNsI_B_TPW+完全読み開始:残り9手
    """
    def __init__(self, remain=9, base=SwitchNsI_B_TPW()):
        super().__init__(remain, base)


class SwitchNsIF9_B_TPWE(FullReading):
    """
    SwitchNsI_B_TPWE+完全読み開始:残り9手
    """
    def __init__(self, remain=9, base=SwitchNsI_B_TPWE()):
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


class AbIF9J_B_TPWE_old(Ushi):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, base=AbIF9_B_TPWE_old()):
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


class NsIF9J_B_TPW2(Ushi):
    """
    NegaScout法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り9手)
    """
    def __init__(self, base=NsIF9_B_TPW2()):
        super().__init__(base)


class NsIF9J_B_TPWE(Nezumi):
    """
    NegaScout法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPWE, 完全読み開始:残り9手)
    """
    def __init__(self, base=NsIF9_B_TPWE()):
        super().__init__(base)


class SwitchNsIF9J_B_TPW(Nezumi):
    """
    SwitchNsIF9_B_TPW+定石打ち
    (完全読み開始:残り9手)
    """
    def __init__(self, base=SwitchNsIF9_B_TPW()):
        super().__init__(base)


class SwitchNsIF9J_B_TPWE(Neko):
    """
    SwitchNsIF9_B_TPWE+定石打ち
    (完全読み開始:残り9手)
    """
    def __init__(self, base=SwitchNsIF9_B_TPWE()):
        super().__init__(base)


# ------------- #
# RandomOpening #
# ------------- #
class MinMax1Ro_TPW2(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_TPW2
    """
    def __init__(self, depth=8, base=MinMax1_TPW2()):
        super().__init__(depth, base)


class MinMax1Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_TPW
    """
    def __init__(self, depth=8, base=MinMax1_TPW()):
        super().__init__(depth, base)


class MinMax1Ro_PWE(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_PWE
    """
    def __init__(self, depth=8, base=MinMax1_PWE()):
        super().__init__(depth, base)


class MinMax1Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_TPWE
    """
    def __init__(self, depth=8, base=MinMax1_TPWE()):
        super().__init__(depth, base)


class MinMax1Ro_TPWEC(RandomOpening):
    """
    RandamOpening(8手) + MinMax1_TPWEC
    """
    def __init__(self, depth=8, base=MinMax1_TPWEC()):
        super().__init__(depth, base)


class MinMax2Ro_T(RandomOpening):
    """
    RandamOpening(8手) + MinMax2_T
    """
    def __init__(self, depth=8, base=MinMax2_T()):
        super().__init__(depth, base)


class MinMax2Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + MinMax2_TPW
    """
    def __init__(self, depth=8, base=MinMax2_TPW()):
        super().__init__(depth, base)


class MinMax2Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + MinMax2_TPWE
    """
    def __init__(self, depth=8, base=MinMax2_TPWE()):
        super().__init__(depth, base)


class MinMax2F9Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + MinMax2F9_TPWE
    """
    def __init__(self, depth=8, base=MinMax2F9_TPWE()):
        super().__init__(depth, base)


class MinMax2Ro_TPWEC(RandomOpening):
    """
    RandamOpening(8手) + MinMax2_TPWEC
    """
    def __init__(self, depth=8, base=MinMax2_TPWEC()):
        super().__init__(depth, base)


class MinMax3Ro_T(RandomOpening):
    """
    RandamOpening(8手) + MinMax3_T
    """
    def __init__(self, depth=8, base=MinMax3_T()):
        super().__init__(depth, base)


class MinMax3Ro_TP(RandomOpening):
    """
    RandamOpening(8手) + MinMax3_TP
    """
    def __init__(self, depth=8, base=MinMax3_TP()):
        super().__init__(depth, base)


class MinMax3Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + MinMax3_TPW
    """
    def __init__(self, depth=8, base=MinMax3_TPW()):
        super().__init__(depth, base)


class MinMax3Ro_TPOW(RandomOpening):
    """
    RandamOpening(8手) + MinMax3_TPOW
    """
    def __init__(self, depth=8, base=MinMax3_TPOW()):
        super().__init__(depth, base)


class _NegaMax3Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + _NegaMax3_TPW
    """
    def __init__(self, depth=8, base=_NegaMax3_TPW()):
        super().__init__(depth, base)


class NegaMax3Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + NegaMax3_TPW
    """
    def __init__(self, depth=8, base=NegaMax3_TPW()):
        super().__init__(depth, base)


class NegaMax3Ro_TPOW(RandomOpening):
    """
    RandamOpening(8手) + NegaMax3_TPOW
    """
    def __init__(self, depth=8, base=NegaMax3_TPOW()):
        super().__init__(depth, base)


class AlphaBeta4Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4_TPW
    """
    def __init__(self, depth=8, base=AlphaBeta4_TPW()):
        super().__init__(depth, base)


class AlphaBeta4Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4_TPWE
    """
    def __init__(self, depth=8, base=AlphaBeta4_TPWE()):
        super().__init__(depth, base)


class NegaScout3Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + NegaScout3_TPW
    """
    def __init__(self, depth=8, base=NegaScout3_TPW()):
        super().__init__(depth, base)


class NegaScout3Ro_TPOW(RandomOpening):
    """
    RandamOpening(8手) + NegaScout3_TPOW
    """
    def __init__(self, depth=8, base=NegaScout3_TPOW()):
        super().__init__(depth, base)


class NegaScout4Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + NegaScout4_TPW
    """
    def __init__(self, depth=8, base=NegaScout4_TPW()):
        super().__init__(depth, base)


class NegaScout4Ro_TPWE(RandomOpening):
    """
    RandamOpening(8手) + NegaScout4_TPWE
    """
    def __init__(self, depth=8, base=NegaScout4_TPWE()):
        super().__init__(depth, base)


class AB_TI_Ro(RandomOpening):
    """
    RandamOpening(8手) + AB_TI
    """
    def __init__(self, depth=8, base=AB_TI()):
        super().__init__(depth, base)


class AlphaBeta4JRo_TPW(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4J_TPW
    """
    def __init__(self, depth=8, base=AlphaBeta4J_TPW()):
        super().__init__(depth, base)


class AlphaBeta4F9Ro_TPW(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4F9_TPW
    """
    def __init__(self, depth=8, base=AlphaBeta4F9_TPW()):
        super().__init__(depth, base)


class AlphaBeta4F9JRo_TPW(RandomOpening):
    """
    RandamOpening(8手) + AlphaBeta4F9J_TPW
    """
    def __init__(self, depth=8, base=AlphaBeta4F9J_TPW()):
        super().__init__(depth, base)


class AbIF9JRo_B_TPW(RandomOpening):
    """
    RandamOpening(8手) + AbIF9J_B_TPW
    """
    def __init__(self, depth=8, base=AbIF9J_B_TPW()):
        super().__init__(depth, base)


class AbIF9JRo_B_TPWE(RandomOpening):
    """
    RandamOpening(8手) + AbIF9J_B_TPWE
    """
    def __init__(self, depth=8, base=AbIF9J_B_TPWE()):
        super().__init__(depth, base)


class AbIF9JRo_B_TPWEC(RandomOpening):
    """
    RandamOpening(8手) + AbIF9J_B_TPWEC
    """
    def __init__(self, depth=8, base=AbIF9J_B_TPWEC()):
        super().__init__(depth, base)


class NsIF9JRo_B_TPW(RandomOpening):
    """
    RandamOpening(8手) + NsIF9J_B_TPW
    """
    def __init__(self, depth=8, base=NsIF9J_B_TPW()):
        super().__init__(depth, base)


class NsIF9JRo_B_TPW2(RandomOpening):
    """
    RandamOpening(8手) + NsIF9J_B_TPW2
    """
    def __init__(self, depth=8, base=NsIF9J_B_TPW2()):
        super().__init__(depth, base)


class NsIF9JRo_B_TPWE(RandomOpening):
    """
    RandamOpening(8手) + NsIF9J_B_TPWE
    """
    def __init__(self, depth=8, base=NsIF9J_B_TPWE()):
        super().__init__(depth, base)


class SwitchNsIF9JRo_B_TPW(RandomOpening):
    """
    RandamOpening(8手) + SwitchNsIF9J_B_TPW
    """
    def __init__(self, depth=8, base=SwitchNsIF9J_B_TPW()):
        super().__init__(depth, base)


class SwitchNsIF9JRo_B_TPWE(RandomOpening):
    """
    RandamOpening(8手) + SwitchNsIF9J_B_TPWE
    """
    def __init__(self, depth=8, base=SwitchNsIF9J_B_TPWE()):
        super().__init__(depth, base)
