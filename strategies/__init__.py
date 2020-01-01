#!/usr/bin/env python
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.input import ConsoleUserInput, WindowUserInput
from strategies.easy import Random, Greedy, Unselfish, SlowStarter, Table
from strategies.minmax import MinMax1_T, MinMax2_T, MinMax3_T, MinMax4_T, MinMax1_TP, MinMax2_TP, MinMax3_TP, MinMax4_TP, MinMax1_TPO, MinMax2_TPO, MinMax3_TPO, MinMax4_TPO, MinMax1_TPOW, MinMax2_TPOW, MinMax3_TPOW, MinMax4_TPOW
from strategies.negamax import NegaMax1_TPOW, NegaMax2_TPOW, NegaMax3_TPOW, NegaMax4_TPOW
from strategies.alphabeta import AlphaBeta1_TPOW, AlphaBeta2_TPOW, AlphaBeta3_TPOW, AlphaBeta4_TPOW
from strategies.iterative import AbI_TPOW, AbI_B_TP, AbI_B_TPO, AbI_B_TPW, AbI_B_TPOW, AbI_BC_TPOW, AbI_W_BC_TPOW
from strategies.fullreading import AbIF5_B_TPOW, AbIF7_B_TPOW, AbIF9_B_TPOW, AbIF11_B_TPW, AbIF13_B_TPW, AbIF11_B_TPOW, AbIF13_B_TPOW, AbIF15_B_TPOW, AbIF7_BC_TPOW, AbIF7_W_BC_TPOW
from strategies.montecarlo import MonteCarlo30, MonteCarlo100, MonteCarlo1000
from strategies.proto import MinMax2, NegaMax3, AlphaBeta4, AB_T4, AB_TI
