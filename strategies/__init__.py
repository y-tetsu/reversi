#!/usr/bin/env python
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.input import ConsoleUserInput, WindowUserInput
from strategies.easy import Random, Greedy, Unselfish, SlowStarter, Table
from strategies.minmax import MinMax1, MinMax2, MinMax3, MinMax4, MinMax1_T, MinMax2_T, MinMax3_T, MinMax4_T, MinMax1_TP, MinMax2_TP, MinMax3_TP, MinMax4_TP, MinMax1_TPO, MinMax2_TPO, MinMax3_TPO, MinMax4_TPO, MinMax1_TPOW, MinMax2_TPOW, MinMax3_TPOW, MinMax4_TPOW
from strategies.negamax import NegaMax3, NegaMax1_TPOW, NegaMax2_TPOW, NegaMax3_TPOW, NegaMax4_TPOW
from strategies.alphabeta import AlphaBeta3, AlphaBeta4, AlphaBeta1_TPOW, AlphaBeta2_TPOW, AlphaBeta3_TPOW, AlphaBeta4_TPOW, AB_T4, AB_TI
