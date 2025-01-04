#cython: language_level=3, profile=False, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
# Cython Reversi Methods

import sys
import time
from collections import namedtuple

from libc.stdlib cimport rand

from reversi.strategies.common import Timer, Measure
from reversi.recorder import Recorder


DEF ENDGAME_BEST_MATCH = 0
DEF BLACK_MAX = 1
DEF WHITE_MAX = 2
DEF BLACK_SHORTEST = 3
DEF WHITE_SHORTEST = 4

DEF SHORTEST_REWARD = 10000

DEF POSITIVE_INFINITY = 10000000
DEF NEGATIVE_INFINITY = -10000000
DEF MAX_POSSIBILITY = 40  # 着手可能数の最大(想定)
DEF POSSIBILITY_RANGE = MAX_POSSIBILITY * 2 + 1
DEF BUCKET_SIZE = MAX_POSSIBILITY
DEF TRANSPOSITION_TABLE_DEPTH = 3  # 置換表を有効にする残りの探索深さ

DEF MAXSIZE64 = 2**63 - 1

DEF MIN_BOARD_SIZE = 4
DEF MAX_BOARD_SIZE = 26


cdef:
    double timer_deadline
    unsigned long long[64] legal_moves_bit_list, pbb, pwb, rec_pbb, rec_pwb
    unsigned long long bb, wb, hb, fd, rec_bb, rec_wb, measure_count
    unsigned long tx = 123456789, ty = 362436069, tz = 521288629, tw = 88675123
    unsigned int[64] legal_moves_x, legal_moves_y, pbs, pws, rec_pbs, rec_pws
    unsigned int rol, rec, rec_depth, bs, ws, max_depth, start_depth, tail, is_timer_enabled, timer_timeout
    signed int[8][8] t_table= [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    # {{{ --- signed int[8][256] table_values= [ ---
    signed int[8][256] table_values= [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    # --- signed int[8][256] table_values= [ --- }}}
    signed int[256] edge_table8 = [0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 6, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 5, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 4, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 5, 2, 2, 2, 3, 2, 2, 2, 4, 2, 2, 2, 3, 2, 2, 2, 5, 3, 3, 3, 4, 3, 3, 3, 5, 4, 4, 4, 5, 5, 5, 6, 13]
    signed int[64] montecarlo_scores
    signed int[8] directions_x = [-1, 0, 1, -1, 1, -1, 0, 1], directions_y = [-1, -1, -1, 0, 0, 1, 1, 1]
    signed int rec_score, timer_timeout_value, taker_sign, corner, c, a1, a2, b1, b2, b3, wx, o1, o2, wp, ww, we, wb1, wb2, wb3
    dict tp_table = {}  # Trans Position Table


# ================================================== #
# for Python

# -------------------------------------------------- #
# next_move
def endgame_next_move(color, board, depth, pid, timer, measure, role):
    timer, measure = (False, False) if pid is None else (timer, measure)
    return _next_move('endgame', color, board, depth, pid, timer, measure, role, None)


def blank_next_move(color, board, params, depth, pid, timer, measure):
    timer, measure = (False, False) if pid is None else (timer, measure)
    return _next_move('blank', color, board, depth, pid, timer, measure, None, params)


def alphabeta_next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure):
    timer, measure = (False, False) if pid is None else (timer, measure)
    return _alphabeta_next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure)


def negascout_next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure):
    timer, measure = (False, False) if pid is None else (timer, measure)
    return _negascout_next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure)


def montecarlo_next_move(color, board, count, pid, timer, measure):
    timer, measure = (False, False) if pid is None else (timer, measure)
    return _montecarlo_next_move(color, board, count, pid, timer, measure)


# -------------------------------------------------- #
# get_best_move
def endgame_get_best_move(color, board, moves, alpha, beta, depth, pid, timer, measure, role, recorder):
    timer, measure = (False, False) if pid is None else (timer, measure)
    return _get_best_move_wrap('endgame', color, board, moves, alpha, beta, depth, pid, timer, measure, role, recorder, None)


def blank_get_best_move(color, board, params, moves, alpha, beta, depth, pid, timer, measure):
    timer, measure = (False, False) if pid is None else (timer, measure)
    return _get_best_move_wrap('blank', color, board, moves, alpha, beta, depth, pid, timer, measure, None, 0, params)


def alphabeta_get_best_move(color, board, moves, alpha, beta, depth, evaluator, pid, timer, measure):
    timer, measure = (False, False) if pid is None else (timer, measure)
    return _alphabeta_get_best_move_wrap(color, board, moves, alpha, beta, depth, evaluator, pid, timer, measure)


def negascout_get_best_move(color, board, moves, alpha, beta, depth, evaluator, pid, timer, measure):
    timer, measure = (False, False) if pid is None else (timer, measure)
    return _negascout_get_best_move_wrap(color, board, moves, alpha, beta, depth, evaluator, pid, timer, measure)


# -------------------------------------------------- #
# get_score
def alphabeta_get_score(alphabeta, color, board, alpha, beta, depth, pid):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _alphabeta_get_score_size8_64bit(alphabeta, color, board, alpha, beta, depth, pid, 0, 0)
    return _alphabeta_get_score(alphabeta, color, board, alpha, beta, depth, pid, 0, 0)


def alphabeta_get_score_measure(alphabeta, color, board, alpha, beta, depth, pid):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _alphabeta_get_score_size8_64bit(alphabeta, color, board, alpha, beta, depth, pid, 1, 0)
    return _alphabeta_get_score(alphabeta, color, board, alpha, beta, depth, pid, 1, 0)


def alphabeta_get_score_timer(alphabeta, color, board, alpha, beta, depth, pid):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _alphabeta_get_score_size8_64bit(alphabeta, color, board, alpha, beta, depth, pid, 0, 1)
    return _alphabeta_get_score(alphabeta, color, board, alpha, beta, depth, pid, 0, 1)


def alphabeta_get_score_measure_timer(alphabeta, color, board, alpha, beta, depth, pid):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _alphabeta_get_score_size8_64bit(alphabeta, color, board, alpha, beta, depth, pid, 1, 1)
    return _alphabeta_get_score(alphabeta, color, board, alpha, beta, depth, pid, 1, 1)


def negascout_get_score(negascout, color, board, alpha, beta, depth, pid):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _negascout_get_score_size8_64bit(_negascout_get_score_size8_64bit, negascout, color, board, alpha, beta, depth, pid)
    return _negascout_get_score(_negascout_get_score, negascout, color, board, alpha, beta, depth, pid)


def negascout_get_score_measure(negascout, color, board, alpha, beta, depth, pid):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _negascout_get_score_measure_size8_64bit(_negascout_get_score_measure_size8_64bit, negascout, color, board, alpha, beta, depth, pid)
    return _negascout_get_score_measure(_negascout_get_score_measure, negascout, color, board, alpha, beta, depth, pid)


def negascout_get_score_timer(negascout, color, board, alpha, beta, depth, pid):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _negascout_get_score_timer_size8_64bit(_negascout_get_score_timer_size8_64bit, negascout, color, board, alpha, beta, depth, pid)
    return _negascout_get_score_timer(_negascout_get_score_timer, negascout, color, board, alpha, beta, depth, pid)


def negascout_get_score_measure_timer(negascout, color, board, alpha, beta, depth, pid):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _negascout_get_score_measure_timer_size8_64bit(_negascout_get_score_measure_timer_size8_64bit, negascout, color, board, alpha, beta, depth, pid)
    return _negascout_get_score_measure_timer(_negascout_get_score_measure_timer, negascout, color, board, alpha, beta, depth, pid)


def table_get_score(table, board):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _table_get_score_size8_64bit(table, board)
    return _table_get_score(table, board)


# -------------------------------------------------- #
# playout
def playout(color, board, move):
    return _board_playout(color, board, move)


# ================================================== #
# for Cython

# -------------------------------------------------- #
# _next_move
cdef inline tuple _next_move(str name, str color, board, int depth, str pid, int timer, int measure, str role, params):
    global is_timer_enabled, timer_deadline, timer_timeout, timer_timeout_value, measure_count,legal_moves_bit_list, legal_moves_x, legal_moves_y, bb, wb, hb, bs, ws, max_depth, corner, c, a1, a2, b1, b2, b3, wx, o1, o2, wp, ww, we, wb1, wb2, wb3
    cdef:
        unsigned long long legal_moves, mask = 0x8000000000000000
        unsigned int int_color = 0, x, y, index = 0
        signed int alpha = NEGATIVE_INFINITY, beta = POSITIVE_INFINITY
    # タイマーとメジャー準備
    measure_count = 0
    timer_timeout = <unsigned int>0
    is_timer_enabled = timer
    if is_timer_enabled and pid:
        timer_deadline = Timer.deadline[pid]
        timer_timeout_value = Timer.timeout_value[pid]
    if measure and pid:
        if pid not in Measure.count:
            Measure.count[pid] = <unsigned int>0
        measure_count = Measure.count[pid]
    # 次の手番
    if color == 'black':
        int_color = <unsigned int>1
    # ボード情報取得
    bb, wb, hb = board.get_bitboard_info()
    bs = board._black_score
    ws = board._white_score
    # By Strategies
    max_depth = 64
    if name == 'endgame':
        # 役割
        beta = _set_role(role, beta)
        # 棋譜初期化(無効)
        _init_recorder(<unsigned int>0, depth)
    elif name == 'blank':
        # 評価パラメータ取得
        corner = params[0]
        c = params[1]
        a1 = params[2]
        a2 = params[3]
        b1 = params[4]
        b2 = params[5]
        b3 = params[6]
        wx = params[7]
        o1 = params[8]
        o2 = params[9]
        wp = params[10]
        ww = params[11]
        we = params[12]
        wb1 = params[13]
        wb2 = params[14]
        wb3 = params[15]
        _set_t_table()
    # 最大深さ調整
    if depth > <int>(max_depth - (bs + ws)):
        depth =  <int>max_depth - (bs + ws)
    # 最善手を取得
    legal_moves = _get_legal_moves_bits(int_color, bb, wb, hb)
    for y in range(8):
        for x in range(8):
            if legal_moves & mask:
                legal_moves_bit_list[index] = mask
                legal_moves_x[index] = x
                legal_moves_y[index] = y
                index += 1
            mask >>= 1
    best_move, scores = _get_best_move(name, int_color, index, legal_moves_bit_list, legal_moves_x, legal_moves_y, alpha, beta, depth)
    # タイマーとメジャー格納
    if measure and pid:
        Measure.count[pid] = measure_count
    if is_timer_enabled and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return best_move


# -------------------------------------------------- #
# _get_best_move_wrap
cdef inline _get_best_move_wrap(str name, str color, board, moves, signed int alpha, signed int beta, int depth, str pid, int timer, int measure, str role, int recorder, params):
    global is_timer_enabled, timer_deadline, timer_timeout, timer_timeout_value, measure_count, bb, wb, hb, bs, ws, max_depth, rec, rec_depth, rec_bb, rec_wb, rec_pbb, rec_pbs, rec_pwb, rec_pws
    cdef:
        unsigned long long[64] moves_bit_list
        unsigned long long put
        unsigned int[64] moves_x, moves_y
        unsigned int x, y, i, index = 0, int_color = 0
        signed int lshift
        list prev
    # タイマーとメジャー準備
    measure_count = 0
    timer_timeout = <unsigned int>0
    is_timer_enabled = timer
    if is_timer_enabled and pid:
        timer_deadline = Timer.deadline[pid]
        timer_timeout_value = Timer.timeout_value[pid]
    if measure and pid:
        if pid not in Measure.count:
            Measure.count[pid] = <unsigned int>0
        measure_count = Measure.count[pid]
    # 次の手番
    if color == 'black':
        int_color = <unsigned int>1
    # ボード情報取得
    bb, wb, hb = board.get_bitboard_info()
    bs = board._black_score
    ws = board._white_score
    # 最大深さ調整
    if depth > <int>(max_depth - (bs + ws)):
        depth =  <int>max_depth - (bs + ws)
    # By Strategies
    if name == 'endgame':
        # 役割
        beta = _set_role(role, beta)
        # 棋譜初期化(無効)
        _init_recorder(<unsigned int>0, depth)
    elif name == 'blank':
        # 評価パラメータ取得
        corner = params[0]
        c = params[1]
        a1 = params[2]
        a2 = params[3]
        b1 = params[4]
        b2 = params[5]
        b3 = params[6]
        wx = params[7]
        o1 = params[8]
        o2 = params[9]
        wp = params[10]
        ww = params[11]
        we = params[12]
        wb1 = params[13]
        wb2 = params[14]
        wb3 = params[15]
        _set_t_table()
    # 最善手を取得
    for x, y in moves:
        lshift = (63-(y*8+x))
        put = <unsigned long long>1 << lshift
        moves_bit_list[index] = put
        moves_x[index] = x
        moves_y[index] = y
        index += 1
    best_move, scores = _get_best_move(name, int_color, index, moves_bit_list, moves_x, moves_y, alpha, beta, depth)
    # タイマーとメジャー格納
    if measure and pid:
        Measure.count[pid] = measure_count
    if is_timer_enabled and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    if rec:
        prev = []
        for i in range(rec_depth):
            prev += [(rec_pbb[i], rec_pwb[i], rec_pbs[i], rec_pws[i])]
        return (best_move, scores, str(Recorder().get_record_by_custom(8, rec_bb, rec_wb, prev)))
    return (best_move, scores)


# -------------------------------------------------- #
# _get_best_move
cdef inline _get_best_move(str name, unsigned int int_color, unsigned int index, unsigned long long[64] moves_bit_list, unsigned int[64] moves_x, unsigned int[64] moves_y, signed int alpha, signed int beta, int depth):
    global timer_timeout, rol, tp_table
    cdef:
        unsigned int int_color_next = 1, i, best = 64
        signed int score = alpha
    scores, tp_table = {}, {}
    # 手番
    if int_color:
        int_color_next = <unsigned int>0
    # 各手のスコア取得
    if name == 'endgame':
        if rol == ENDGAME_BEST_MATCH:
            for i in range(index):
                _put_disc(int_color, moves_bit_list[i])
                score = -_endgame_get_score(int_color_next, -beta, -alpha, depth-1, <unsigned int>0)
                _undo()
                scores[(moves_x[i], moves_y[i])] = score
                if timer_timeout:
                    if best == 64:
                        best = i
                    break
                if score > alpha:  # 最善手を更新
                    alpha = score
                    best = i
        else:
            for i in range(index):
                _put_disc(int_color, moves_bit_list[i])
                score = _endgame_get_score_taker(int_color_next, alpha, beta, depth-1, <unsigned int>0)
                _undo()
                scores[(moves_x[i], moves_y[i])] = score
                if timer_timeout:
                    if best == 64:
                        best = i
                    break
                if score > alpha:  # 最善手を更新
                    alpha = score
                    best = i
    elif name == 'blank':
        best = 0
        for i in range(index):
            _put_disc(int_color, moves_bit_list[i])
            score = -_blank_get_score(int_color_next, -beta, -alpha, depth-1, <unsigned int>0)
            _undo()
            scores[(moves_x[i], moves_y[i])] = score
            if timer_timeout:
                break
            if score > alpha:  # 最善手を更新
                alpha = score
                best = i
    return (moves_x[best], moves_y[best]), scores


# -------------------------------------------------- #
# EndGame Methods
cdef inline void _init_recorder(unsigned int recorder, unsigned int  depth):
    global rec, rec_score, rec_depth, start_depth, rec_bb, rec_wb, rec_pbb, rec_pwb, rec_pbs, rec_pws
    cdef:
        unsigned int i
    rec = recorder
    rec_score = <signed int>0
    rec_depth = <unsigned int>0
    rec_bb = <unsigned long long>0
    rec_wb = <unsigned long long>0
    for i in range(64):
        rec_pbb[i] = <unsigned long long>0
        rec_pwb[i] = <unsigned long long>0
        rec_pbs[i] = <unsigned int>0
        rec_pws[i] = <unsigned int>0
    start_depth = depth


cdef inline signed int _set_role(str role, signed int beta):
    global rol, hb, max_depth, taker_sign
    rol = ENDGAME_BEST_MATCH
    max_depth = <unsigned int>64 - <unsigned int>_popcount(hb)
    if role != 'best_match':
        # TODO : MUCH_TAKER:確定石の場所を記憶し、相手が確定石に置く手を後回しにする
        if role == 'black_max':
            beta = <signed int>max_depth
            rol = BLACK_MAX
            taker_sign = <signed int>1
        elif role == 'white_max':
            beta = <signed int>max_depth
            rol = WHITE_MAX
            taker_sign = <signed int>-1
        elif role == 'black_shortest':
            beta = <signed int>SHORTEST_REWARD * 64
            rol = BLACK_SHORTEST
            taker_sign = <signed int>1
        elif role == 'white_shortest':
            beta = <signed int>SHORTEST_REWARD * 64
            rol = WHITE_SHORTEST
            taker_sign = <signed int>-1
    return beta


cdef inline signed int _endgame_get_score(unsigned int int_color, signed int alpha, signed int beta, unsigned int depth, unsigned int pas):
    global timer_timeout, measure_count, bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail, is_timer_enabled, max_depth
    cdef:
        unsigned long long legal_moves_bits, move, count
        unsigned int i, is_game_end = 0, int_color_next = 1, x, y
        signed int timeout, score, sign = -1
    # タイムアウト判定
    if is_timer_enabled:
        timeout = check_timeout()
        if timeout:
            return timeout
    # 探索ノード数カウント
    measure_count += 1
    # 合法手を取得
    legal_moves_bits = _get_legal_moves_bits(int_color, bb, wb, hb)
    # 前回パス and 打てる場所なし の場合ゲーム終了
    if pas and not legal_moves_bits:
        is_game_end = <unsigned int>1
    # 最大深さに到達 or ゲーム終了
    if not depth or is_game_end:
        if int_color:
            sign = <signed int>1
        return <signed int>((<signed int>bs - <signed int>ws) * <signed int>sign)
    # 次の手番
    if int_color:
        int_color_next = <unsigned int>0
    # パスの場合
    if not legal_moves_bits:
        return -_endgame_get_score(int_color_next, -beta, -alpha, depth, <unsigned int>1)
    # 最終1手
    if bs + ws == <unsigned int>(max_depth - 1):
        measure_count += 1
        count = _popcount(_get_flippable_discs_num(int_color, bb, wb, legal_moves_bits))
        if rol == ENDGAME_BEST_MATCH:
            if int_color:
                return <signed int>(<signed int>bs - <signed int>ws + <signed int>(1 + count*2))
            else:
                return <signed int>-(<signed int>bs - <signed int>ws - <signed int>(1 + count*2))
    # 評価値を算出
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        _put_disc(int_color, move)
        score = -_endgame_get_score(int_color_next, -beta, -alpha, depth-1, <unsigned int>0)
        _undo()
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする
        if score > alpha:
            alpha = score
        if timer_timeout:
            return alpha
        if alpha >= beta:  # 枝刈り
            return alpha
    return alpha


cdef inline signed int _endgame_get_score_taker(unsigned int int_color, signed int alpha, signed int beta, unsigned int depth, unsigned int pas):
    global timer_timeout, measure_count, bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail, is_timer_enabled, rol, taker_sign, max_depth
    cdef:
        unsigned long long legal_moves_bits, move, count
        unsigned int i, is_game_end = 0, int_color_next = 1, x, y, reward
        signed int timeout, score, sign = -1
    # タイムアウト判定
    if is_timer_enabled:
        timeout = check_timeout()
        if timeout:
            return timeout
    # 探索ノード数カウント
    measure_count += 1
    # 合法手を取得
    legal_moves_bits = _get_legal_moves_bits(int_color, bb, wb, hb)
    # 前回パス and 打てる場所なし の場合ゲーム終了
    if pas and not legal_moves_bits:
        is_game_end = <unsigned int>1
    # 最大深さに到達 or ゲーム終了
    if not depth or is_game_end:
        if rol == BLACK_SHORTEST or rol == WHITE_SHORTEST:
            if is_game_end and <signed int>(bs * taker_sign) > <signed int>(ws * taker_sign):
                reward = (max_depth - (bs + ws)) * SHORTEST_REWARD
                if reward > SHORTEST_REWARD:
                    score = <signed int>((<signed int>bs - <signed int>ws) * taker_sign + <signed int>reward)
                    #print(depth, score, hex(bs), hex(ws))
                    _save_record(score, depth)
                    return score
        return <signed int>(<signed int>bs - <signed int>ws) * taker_sign
    # 次の手番
    if int_color:
        int_color_next = <unsigned int>0
    # パスの場合
    if not legal_moves_bits:
        return _endgame_get_score_taker(int_color_next, alpha, beta, depth, <unsigned int>1)
    # 最終1手
    if bs + ws == <unsigned int>(max_depth - 1):
        measure_count += 1
        count = _popcount(_get_flippable_discs_num(int_color, bb, wb, legal_moves_bits))
        if int_color:
            return <signed int>(<signed int>bs - <signed int>ws + <signed int>(1 + count*2)) * taker_sign
        else:
            return <signed int>(<signed int>bs - <signed int>ws - <signed int>(1 + count*2)) * taker_sign
    # 評価値を算出
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        _put_disc(int_color, move)
        score = _endgame_get_score_taker(int_color_next, alpha, beta, depth-1, <unsigned int>0)
        _undo()
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする
        if score > alpha:
            alpha = score
        if timer_timeout:
            return alpha
        if alpha >= beta:  # 枝刈り
            return alpha
    return alpha


cdef inline void _save_record(signed int score, unsigned int depth):
    global rec, rec_score, rec_depth, start_depth, rec_bb, rec_wb, rec_pbb, rec_pwb, rec_pbs, rec_pws, bb, wb, pbb, pwb, pbs, pws
    if rec and (score > rec_score):
        rec_depth = start_depth - depth
        rec_score = score
        rec_bb = bb
        rec_wb = wb
        for i in range(rec_depth):
            rec_pbb[i] = pbb[i]
            rec_pwb[i] = pwb[i]
            rec_pbs[i] = pbs[i]
            rec_pws[i] = pws[i]


# -------------------------------------------------- #
# Blank Methods
cdef inline signed int _blank_get_score(unsigned int int_color, signed int alpha, signed int beta, unsigned int depth, unsigned int pas):
    global timer_timeout, measure_count, bb, wb, hb, bs, ws, pbb, pwb, pbs, pws, fd, tail, tp_table, is_timer_enabled
    cdef:
        unsigned long long[64] next_moves_list
        unsigned long long legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, move, flippable_discs_num, b, w, bits, t_, rt, r_, rb, b_, lb, l_, lt, bf_t_ = 0, bf_rt = 0, bf_r_ = 0, bf_rb = 0, bf_b_ = 0, bf_lb = 0, bf_l_ = 0, bf_lt = 0, player, opponent, blank, horizontal, vertical, diagonal, tmp_h, tmp_v, tmp_d1, tmp_d2, legal_moves_bits_opponent, bits_count
        unsigned int i, int_color_next = 1, count = 0
        signed int[64] possibilities
        signed int null_window, timeout, sign = -1, score, upper, lower, score_max = NEGATIVE_INFINITY, alpha_ini = alpha
    # タイムアウト判定
    if is_timer_enabled:
        timeout = check_timeout()
        if timeout:
            return timeout
    # 探索ノード数カウント
    measure_count += 1
    # 置換表に結果が存在する場合、その値を返す
    key = (bb, wb, int_color)
    if depth >= TRANSPOSITION_TABLE_DEPTH:
        if key in tp_table:
            lower, upper = tp_table[key]
            if upper <= alpha:
                return upper
            if lower >= beta:
                return lower
            if upper == lower:
                return upper
            if lower > alpha:
                alpha = lower
            if upper < beta:
                beta = upper
    # 合法手を取得
    # {{{ -- _get_legal_moves_bits(int_color, bb, wb, hb) --
    player, opponent = wb, bb
    if int_color:
        player, opponent = bb, wb
    blank = ~(player | opponent | hb)
    horizontal = opponent & <unsigned long long>0x7E7E7E7E7E7E7E7E  # horizontal mask value
    vertical = opponent & <unsigned long long>0x00FFFFFFFFFFFF00    # vertical mask value
    diagonal = opponent & <unsigned long long>0x007E7E7E7E7E7E00    # diagonal mask value
    # left/right
    tmp_h = horizontal & ((player << 1) | (player >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    # top/bottom
    tmp_v = vertical & ((player << 8) | (player >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    # left-top/right-bottom
    tmp_d1 = diagonal & ((player << 9) | (player >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    # right-top/left-bottom
    tmp_d2 = diagonal & ((player << 7) | (player >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    legal_moves_bits =  blank & ((tmp_h << 1) | (tmp_h >> 1) | (tmp_v << 8) | (tmp_v >> 8) | (tmp_d1 << 9) | (tmp_d1 >> 9) | (tmp_d2 << 7) | (tmp_d2 >> 7))
    # -- _get_legal_moves_bits(int_color, bb, wb, hb) -- }}}
    # 次の手番
    if int_color:
        int_color_next = <unsigned int>0
        sign = <signed int>1
    # パスの場合
    if not legal_moves_bits:
        # 前回もパスの場合ゲーム終了
        if pas:
            # {{{ --- return _evaluate(int_color, <signed int>0, <signed int>0) * sign ---
            score = bs - ws
            if score > 0:    # 黒が勝った
                score += ww
            elif score < 0:  # 白が勝った
                score -= ww
            return score * sign
            # --- return _evaluate(int_color, <signed int>0, <signed int>0) * sign --- }}}
        return -_blank_get_score(int_color_next, -beta, -alpha, depth, <unsigned int>1)
    # 最大深さに到達
    if not depth:
        # 相手の着手可能数を取得
        # {{{ -- _get_legal_moves_bits(<unsigned int>0 if int_color else <unsigned int>1, bb, wb, hb) --
        player, opponent = opponent, player  # reversed for opponent
        blank = ~(player | opponent | hb)
        horizontal = opponent & <unsigned long long>0x7E7E7E7E7E7E7E7E  # horizontal mask value
        vertical = opponent & <unsigned long long>0x00FFFFFFFFFFFF00    # vertical mask value
        diagonal = opponent & <unsigned long long>0x007E7E7E7E7E7E00    # diagonal mask value
        # left/right
        tmp_h = horizontal & ((player << 1) | (player >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        # top/bottom
        tmp_v = vertical & ((player << 8) | (player >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        # left-top/right-bottom
        tmp_d1 = diagonal & ((player << 9) | (player >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        # right-top/left-bottom
        tmp_d2 = diagonal & ((player << 7) | (player >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        legal_moves_bits_opponent =  blank & ((tmp_h << 1) | (tmp_h >> 1) | (tmp_v << 8) | (tmp_v >> 8) | (tmp_d1 << 9) | (tmp_d1 >> 9) | (tmp_d2 << 7) | (tmp_d2 >> 7))
        # -- _get_legal_moves_bits((<unsigned int>0 if int_color else <unsigned int>1, bb, wb, hb) -- }}}
        if int_color:
            legal_moves_b_bits = legal_moves_bits
            legal_moves_w_bits = legal_moves_bits_opponent
        else:
            legal_moves_b_bits = legal_moves_bits_opponent
            legal_moves_w_bits = legal_moves_bits
        if legal_moves_b_bits:
            # {{{ -- _popcount --
            bits = legal_moves_b_bits
            bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
            bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
            bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
            bits = bits + (bits >> <unsigned int>8)
            bits = bits + (bits >> <unsigned int>16)
            legal_moves_b_bits = (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
            # -- _popcount -- }}}
        if legal_moves_w_bits:
            # {{{ -- _popcount --
            bits = legal_moves_w_bits
            bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
            bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
            bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
            bits = bits + (bits >> <unsigned int>8)
            bits = bits + (bits >> <unsigned int>16)
            legal_moves_w_bits = (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
            # -- _popcount -- }}}
        # 評価値を返す
        # {{{ --- return _evaluate(int_color, <signed int>legal_moves_b_bits, <signed int>legal_moves_w_bits) * sign ---
        # 勝敗が決まっている場合
        if not legal_moves_b_bits and not legal_moves_w_bits:
            score = bs - ws
            if score > 0:    # 黒が勝った
                score += ww
            elif score < 0:  # 白が勝った
                score -= ww
            return score * sign
        # 勝敗が決まっていない場合
        score = _get_t() + _get_p(<signed int>legal_moves_b_bits, <signed int>legal_moves_w_bits) + _get_e() + _get_b()
        return score * sign
        # --- return _evaluate(int_color, <signed int>legal_moves_b_bits, <signed int>legal_moves_w_bits) * sign --- }}}
    # 合法手と着手可能数の格納
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        next_moves_list[count] = move
        b, w = bb, wb
        # ひっくり返せる石を取得
        # {{{ -- _get_flippable_discs_num --
        flippable_discs_num = 0
        t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & (move << <unsigned int>8)  # top
        rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & (move << <unsigned int>7)  # right-top
        r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & (move >> <unsigned int>1)  # right
        rb = <unsigned long long>0x007F7F7F7F7F7F7F & (move >> <unsigned int>9)  # right-bottom
        b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & (move >> <unsigned int>8)  # bottom
        lb = <unsigned long long>0x00FEFEFEFEFEFEFE & (move >> <unsigned int>7)  # left-bottom
        l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & (move << <unsigned int>1)  # left
        lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & (move << <unsigned int>9)  # left-top
        for _ in range(6):
            if t_ & opponent:
                bf_t_ |= t_
                t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)
            if rt & opponent:
                bf_rt |= rt
                rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)
            if r_ & opponent:
                bf_r_ |= r_
                r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)
            if rb & opponent:
                bf_rb |= rb
                rb = <unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)
            if b_ & opponent:
                bf_b_ |= b_
                b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)
            if lb & opponent:
                bf_lb |= lb
                lb = <unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)
            if l_ & opponent:
                bf_l_ |= l_
                l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)
            if lt & opponent:
                bf_lt |= lt
                lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)
        if t_ & player:
            flippable_discs_num |= bf_t_
        if rt & player:
            flippable_discs_num |= bf_rt
        if r_ & player:
            flippable_discs_num |= bf_r_
        if rb & player:
            flippable_discs_num |= bf_rb
        if b_ & player:
            flippable_discs_num |= bf_b_
        if lb & player:
            flippable_discs_num |= bf_lb
        if l_ & player:
            flippable_discs_num |= bf_l_
        if lt & player:
            flippable_discs_num |= bf_lt
        # -- _get_flippable_discs_num -- }}}
        # 自分の石を置いて相手の石をひっくり返す
        if int_color:
            b ^= move | flippable_discs_num
            w ^= flippable_discs_num
        else:
            w ^= move | flippable_discs_num
            b ^= flippable_discs_num
        # 着手可能数を格納
        # {{{ -- _get_legal_moves_bits(int_color, b, w, hb) --
        player, opponent = w, b
        if int_color:
            player, opponent = b, w
        blank = ~(player | opponent | hb)
        horizontal = opponent & <unsigned long long>0x7E7E7E7E7E7E7E7E  # horizontal mask value
        vertical = opponent & <unsigned long long>0x00FFFFFFFFFFFF00    # vertical mask value
        diagonal = opponent & <unsigned long long>0x007E7E7E7E7E7E00    # diagonal mask value
        # left/right
        tmp_h = horizontal & ((player << 1) | (player >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
        # top/bottom
        tmp_v = vertical & ((player << 8) | (player >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
        # left-top/right-bottom
        tmp_d1 = diagonal & ((player << 9) | (player >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
        # right-top/left-bottom
        tmp_d2 = diagonal & ((player << 7) | (player >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
        bits =  blank & ((tmp_h << 1) | (tmp_h >> 1) | (tmp_v << 8) | (tmp_v >> 8) | (tmp_d1 << 9) | (tmp_d1 >> 9) | (tmp_d2 << 7) | (tmp_d2 >> 7))
        # -- _get_legal_moves_bits(int_color, b, w, hb) -- }}}
        # {{{ -- possibilities[count] = _popcount --
        bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
        bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
        bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
        bits = bits + (bits >> <unsigned int>8)
        bits = bits + (bits >> <unsigned int>16)
        possibilities[count] = -<signed int>((bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F)
        # -- _popcount -- }}}
        count += 1
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする
    # 着手可能数に応じて並び替え
    _sort_moves_by_possibility(count, next_moves_list, possibilities)
    # 次の手の探索
    for i in range(count):
        # 一手打つ
        # {{{ --- _put_disc(int_color, next_moves_list[i]) ---
        # ひっくり返せる石を取得
        # {{{ -- _get_flippable_discs_num --
        flippable_discs_num = 0
        bf_t_, bf_rt, bf_r_, bf_rb, bf_b_, bf_lb, bf_l_, bf_lt = 0, 0, 0, 0, 0, 0, 0, 0
        move = next_moves_list[i]
        player, opponent = wb, bb
        if int_color:
            player, opponent = bb, wb
        t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & (move << <unsigned int>8)  # top
        rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & (move << <unsigned int>7)  # right-top
        r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & (move >> <unsigned int>1)  # right
        rb = <unsigned long long>0x007F7F7F7F7F7F7F & (move >> <unsigned int>9)  # right-bottom
        b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & (move >> <unsigned int>8)  # bottom
        lb = <unsigned long long>0x00FEFEFEFEFEFEFE & (move >> <unsigned int>7)  # left-bottom
        l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & (move << <unsigned int>1)  # left
        lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & (move << <unsigned int>9)  # left-top
        for _ in range(6):
            if t_ & opponent:
                bf_t_ |= t_
                t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)
            if rt & opponent:
                bf_rt |= rt
                rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)
            if r_ & opponent:
                bf_r_ |= r_
                r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)
            if rb & opponent:
                bf_rb |= rb
                rb = <unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)
            if b_ & opponent:
                bf_b_ |= b_
                b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)
            if lb & opponent:
                bf_lb |= lb
                lb = <unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)
            if l_ & opponent:
                bf_l_ |= l_
                l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)
            if lt & opponent:
                bf_lt |= lt
                lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)
        if t_ & player:
            flippable_discs_num |= bf_t_
        if rt & player:
            flippable_discs_num |= bf_rt
        if r_ & player:
            flippable_discs_num |= bf_r_
        if rb & player:
            flippable_discs_num |= bf_rb
        if b_ & player:
            flippable_discs_num |= bf_b_
        if lb & player:
            flippable_discs_num |= bf_lb
        if l_ & player:
            flippable_discs_num |= bf_l_
        if lt & player:
            flippable_discs_num |= bf_lt
        fd = flippable_discs_num
        # -- _get_flippable_discs_num -- }}}
        # {{{ -- _popcount --
        bits = fd
        bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
        bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
        bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
        bits = bits + (bits >> <unsigned int>8)
        bits = bits + (bits >> <unsigned int>16)
        bits_count = (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
        # -- _popcount -- }}}
        # 打つ前の状態を格納
        pbb[tail] = bb
        pwb[tail] = wb
        pbs[tail] = bs
        pws[tail] = ws
        tail += 1
        # 自分の石を置いて相手の石をひっくり返す
        if int_color:
            bb ^= move | fd
            wb ^= fd
            bs += <unsigned int>1 + <unsigned int>bits_count
            ws -= <unsigned int>bits_count
        else:
            wb ^= move | fd
            bb ^= fd
            bs -= <unsigned int>bits_count
            ws += <unsigned int>1 + <unsigned int>bits_count
        # --- _put_disc(int_color, next_moves_list[i]) --- }}}
        # Null Window Search
        null_window = beta if not i else alpha + 1
        score = -_blank_get_score(int_color_next, -null_window, -alpha, depth-1, <unsigned int>0)
        if alpha < score:
            if i and score <= null_window:
                score = -_blank_get_score(int_color_next, -beta, -score, depth-1, <unsigned int>0)
            alpha = score
        # 手を戻す
        _undo()
        # タイムアウト判定
        if timer_timeout:
            return alpha
        # 最大値の更新
        if alpha > score_max:
            score_max = alpha
        # beta cut
        if score_max >= beta:
            if depth >= TRANSPOSITION_TABLE_DEPTH:
                tp_table[key] = (score_max, POSITIVE_INFINITY)
            return score_max
    if depth >= TRANSPOSITION_TABLE_DEPTH:
        # 置換表に結果を格納
        if score_max > alpha_ini:
            tp_table[key] = (score_max, score_max)
        else:
            tp_table[key] = (NEGATIVE_INFINITY, score_max)
    return score_max


cdef inline void _sort_moves_by_possibility(unsigned int count, unsigned long long[64] next_moves_list, signed int[64] possibilities):
    if count >= 2:
        if count <= BUCKET_SIZE:
            _bucket_sort(count, next_moves_list, possibilities)
        else:
            _merge_sort(count, next_moves_list, possibilities)


cdef inline void _bucket_sort(unsigned int count, unsigned long long[64] next_moves_list, signed int[64] possibilities):
    cdef:
        unsigned long long[POSSIBILITY_RANGE*BUCKET_SIZE] bucket
        unsigned int[POSSIBILITY_RANGE] possibility_count
        unsigned int i, j, k = 0, pos, index
    for i in range(POSSIBILITY_RANGE):
        possibility_count[i] = <unsigned int>0
    # バケツに入れる
    for i in range(count):
        pos = <unsigned int>(possibilities[i] + MAX_POSSIBILITY)
        index = pos * BUCKET_SIZE + possibility_count[pos]
        bucket[index] = next_moves_list[i]
        possibility_count[pos] += <unsigned int>1
    # バケツから取り出す
    k = count - 1
    for i in range(POSSIBILITY_RANGE):
        for j in range(possibility_count[i]):
            index = i * BUCKET_SIZE + j
            next_moves_list[k] = bucket[index]
            k -= 1


cdef inline void _merge_sort(unsigned int count, unsigned long long[64] next_moves_list, signed int[64] possibilities):
    cdef:
        unsigned long long[32] array_move1, array_move2
        unsigned int len1, len2, i
        signed int[32] array_p1, array_p2
    if count >= 2:
        len1 = <unsigned int>(count / 2)
        len2 = <unsigned int>(count - len1)
        for i in range(len1):
            array_move1[i] = next_moves_list[i]
            array_p1[i] = possibilities[i]
        for i in range(len2):
            array_move2[i] = next_moves_list[len1+i]
            array_p2[i] = possibilities[len1+i]
        _merge_sort(len1, array_move1, array_p1)
        _merge_sort(len2, array_move2, array_p2)
        _merge(len1, len2, array_move1, array_p1, array_move2, array_p2, next_moves_list, possibilities)


cdef inline void _merge(unsigned int len1, unsigned int len2, unsigned long long[32] array_move1, signed int[32] array_p1, unsigned long long[32] array_move2, signed int[32] array_p2, unsigned long long[64] next_moves_list, signed int[64] possibilities):
    cdef:
        unsigned int i = 0, j = 0
    while i < len1 or j < len2:
        if j >= len2 or (i < len1 and array_p1[i] >= array_p2[j]):
            next_moves_list[i+j] = array_move1[i]
            possibilities[i+j] = array_p1[i]
            i += 1
        else:
            next_moves_list[i+j] = array_move2[j]
            possibilities[i+j] = array_p2[j]
            j += 1


cdef inline signed int _set_t_table():
    global t_table, corner, c, a1, a2, b1, b2, b3, wx, o1, o2
    cdef:
        unsigned int row, col, bit8, mask
        signed int value
    t_table[0][0] = corner
    t_table[0][1] = c
    t_table[0][2] = a2
    t_table[0][3] = b3
    t_table[0][4] = b3
    t_table[0][5] = a2
    t_table[0][6] = c
    t_table[0][7] = corner
    t_table[1][0] = c
    t_table[1][1] = wx
    t_table[1][2] = o1
    t_table[1][3] = o2
    t_table[1][4] = o2
    t_table[1][5] = o1
    t_table[1][6] = wx
    t_table[1][7] = c
    t_table[2][0] = a2
    t_table[2][1] = o1
    t_table[2][2] = a1
    t_table[2][3] = b2
    t_table[2][4] = b2
    t_table[2][5] = a1
    t_table[2][6] = o1
    t_table[2][7] = a2
    t_table[3][0] = b3
    t_table[3][1] = o2
    t_table[3][2] = b2
    t_table[3][3] = b1
    t_table[3][4] = b1
    t_table[3][5] = b2
    t_table[3][6] = o2
    t_table[3][7] = b3
    t_table[4][0] = b3
    t_table[4][1] = o2
    t_table[4][2] = b2
    t_table[4][3] = b1
    t_table[4][4] = b1
    t_table[4][5] = b2
    t_table[4][6] = o2
    t_table[4][7] = b3
    t_table[5][0] = a2
    t_table[5][1] = o1
    t_table[5][2] = a1
    t_table[5][3] = b2
    t_table[5][4] = b2
    t_table[5][5] = a1
    t_table[5][6] = o1
    t_table[5][7] = a2
    t_table[6][0] = c
    t_table[6][1] = wx
    t_table[6][2] = o1
    t_table[6][3] = o2
    t_table[6][4] = o2
    t_table[6][5] = o1
    t_table[6][6] = wx
    t_table[6][7] = c
    t_table[7][0] = corner
    t_table[7][1] = c
    t_table[7][2] = a2
    t_table[7][3] = b3
    t_table[7][4] = b3
    t_table[7][5] = a2
    t_table[7][6] = c
    t_table[7][7] = corner
    # 事前計算
    for row in range(8):
        for bit8 in range(256):
            value = <signed int>0
            mask = <unsigned int>1 << 7
            for col in range(8):
                if mask & bit8:
                    value += t_table[row][col]
                mask >>= 1
            table_values[row][bit8] = value


cdef inline signed int _get_t():
    """テーブルによる評価値"""
    global bb, wb, table_values
    cdef:
        unsigned long long mask = 0x00000000000000FF, tb, tw
        unsigned int row, shift
        signed int score = 0
    for row in range(8):
        shift = (7 - row) * 8
        tb = (bb >> shift) & mask
        tw = (wb >> shift) & mask
        score += table_values[row][tb] - table_values[row][tw]
    return score


cdef inline signed int _get_p(signed int pos_b, signed int pos_w):
    """着手可能数による評価値"""
    global wp
    return (pos_b - pos_w) * wp


cdef inline signed int _get_e():
    """辺の確定石による評価値"""
    global bb, wb, we
    cdef:
        unsigned long long all_bitboard, bit_pos, lt, rt, lb, rb, b_t, w_t, b_b, w_b, b_l, w_l, b_r, w_r
        signed int score = 0
    all_bitboard = bb | wb
    bit_pos = <unsigned long long>0x8000000000000000
    lt = <unsigned long long>0x8000000000000000
    rt = <unsigned long long>0x0100000000000000
    lb = <unsigned long long>0x0000000000000080
    rb = <unsigned long long>0x0000000000000001
    # 四隅のどこかに石がある場合
    if (lt | rt | lb | rb) & all_bitboard:
        # 上辺
        b_t, w_t = 0, 0
        if (lt | rt) & all_bitboard:
            b_t = (<unsigned long long>0xFF00000000000000 & bb) >> 56
            w_t = (<unsigned long long>0xFF00000000000000 & wb) >> 56
        # 下辺
        b_b = <unsigned long long>0x00000000000000FF & bb
        w_b = <unsigned long long>0x00000000000000FF & wb
        # 左辺
        b_l, w_l = 0, 0
        if (lt | lb) & bb:
            if bb & <unsigned long long>0x8000000000000000:
                b_l += <unsigned long long>0x0000000000000080
            if bb & <unsigned long long>0x0080000000000000:
                b_l += <unsigned long long>0x0000000000000040
            if bb & <unsigned long long>0x0000800000000000:
                b_l += <unsigned long long>0x0000000000000020
            if bb & <unsigned long long>0x0000008000000000:
                b_l += <unsigned long long>0x0000000000000010
            if bb & <unsigned long long>0x0000000080000000:
                b_l += <unsigned long long>0x0000000000000008
            if bb & <unsigned long long>0x0000000000800000:
                b_l += <unsigned long long>0x0000000000000004
            if bb & <unsigned long long>0x0000000000008000:
                b_l += <unsigned long long>0x0000000000000002
            if bb & <unsigned long long>0x0000000000000080:
                b_l += <unsigned long long>0x0000000000000001
        if (lt | lb) & wb:
            if wb & <unsigned long long>0x8000000000000000:
                w_l += <unsigned long long>0x0000000000000080
            if wb & <unsigned long long>0x0080000000000000:
                w_l += <unsigned long long>0x0000000000000040
            if wb & <unsigned long long>0x0000800000000000:
                w_l += <unsigned long long>0x0000000000000020
            if wb & <unsigned long long>0x0000008000000000:
                w_l += <unsigned long long>0x0000000000000010
            if wb & <unsigned long long>0x0000000080000000:
                w_l += <unsigned long long>0x0000000000000008
            if wb & <unsigned long long>0x0000000000800000:
                w_l += <unsigned long long>0x0000000000000004
            if wb & <unsigned long long>0x0000000000008000:
                w_l += <unsigned long long>0x0000000000000002
            if wb & <unsigned long long>0x0000000000000080:
                w_l += <unsigned long long>0x0000000000000001
        # 右辺
        b_r, w_r = 0, 0
        if (rt | rb) & bb:
            if bb & <unsigned long long>0x0100000000000000:
                b_r += <unsigned long long>0x0000000000000080
            if bb & <unsigned long long>0x0001000000000000:
                b_r += <unsigned long long>0x0000000000000040
            if bb & <unsigned long long>0x0000010000000000:
                b_r += <unsigned long long>0x0000000000000020
            if bb & <unsigned long long>0x0000000100000000:
                b_r += <unsigned long long>0x0000000000000010
            if bb & <unsigned long long>0x0000000001000000:
                b_r += <unsigned long long>0x0000000000000008
            if bb & <unsigned long long>0x0000000000010000:
                b_r += <unsigned long long>0x0000000000000004
            if bb & <unsigned long long>0x0000000000000100:
                b_r += <unsigned long long>0x0000000000000002
            if bb & <unsigned long long>0x0000000000000001:
                b_r += <unsigned long long>0x0000000000000001
        if (rt | rb) & wb:
            if wb & <unsigned long long>0x0100000000000000:
                w_r += <unsigned long long>0x0000000000000080
            if wb & <unsigned long long>0x0001000000000000:
                w_r += <unsigned long long>0x0000000000000040
            if wb & <unsigned long long>0x0000010000000000:
                w_r += <unsigned long long>0x0000000000000020
            if wb & <unsigned long long>0x0000000100000000:
                w_r += <unsigned long long>0x0000000000000010
            if wb & <unsigned long long>0x0000000001000000:
                w_r += <unsigned long long>0x0000000000000008
            if wb & <unsigned long long>0x0000000000010000:
                w_r += <unsigned long long>0x0000000000000004
            if wb & <unsigned long long>0x0000000000000100:
                w_r += <unsigned long long>0x0000000000000002
            if wb & <unsigned long long>0x0000000000000001:
                w_r += <unsigned long long>0x0000000000000001
        score = ((edge_table8[b_t] - edge_table8[w_t]) + (edge_table8[b_b] - edge_table8[w_b]) + (edge_table8[b_l] - edge_table8[w_l]) + (edge_table8[b_r] - edge_table8[w_r])) * we
    return score


cdef inline signed int _get_b():
    """空きマスのパターンによる評価値"""
    global bb, wb, wb1, wb2, wb3
    cdef:
        unsigned long long[8] blanks
        unsigned long long blackwhite, blank, horizontal, vertical, diagonal, l_blank, r_blank, t_blank, b_blank, lt_blank, rt_blank, lb_blank, rb_blank, lt_x, rt_x, lb_x, rb_x, lt_r, lt_b, rt_l, rt_b, lb_t, lb_r, rb_t, rb_l, bits
        unsigned int i
        signed int score = 0, lt_r_sign = 1, lt_b_sign = 1, rt_l_sign = 1, rt_b_sign = 1, lb_t_sign = 1, lb_r_sign = 1, rb_t_sign = 1, rb_l_sign = 1
    black = bb
    white = wb
    blackwhite = black | white
    horizontal = blackwhite & <unsigned long long>0x7E7E7E7E7E7E7E7E  # 左右チェック用マスク
    vertical = blackwhite & <unsigned long long>0x00FFFFFFFFFFFF00    # 上下チェック用マスク
    diagonal = blackwhite & <unsigned long long>0x007E7E7E7E7E7E00    # 斜めチェック用マスク
    blank = ~blackwhite
    # 左方向に空がある(右方向が盤面の範囲内)
    l_blank = horizontal & ((horizontal << 1) & blank) >> 1
    # 右方向に空がある(左方向が盤面の範囲内)
    r_blank = horizontal & ((horizontal >> 1) & blank) << 1
    # 上方向に空がある(下方向が盤面の範囲内)
    t_blank = vertical & ((vertical << 8) & blank) >> 8
    # 下方向に空がある(上方向が盤面の範囲内)
    b_blank = vertical & ((vertical >> 8) & blank) << 8
    # 左上方向に空がある(右下方向が盤面の範囲内)
    lt_blank = diagonal & ((diagonal << 9) & blank) >> 9
    # 右上方向に空がある(左下方向が盤面の範囲内)
    rt_blank = diagonal & ((diagonal << 7) & blank) >> 7
    # 左下方向に空がある(右上方向が盤面の範囲内)
    lb_blank = diagonal & ((diagonal >> 7) & blank) << 7
    # 右下方向に空がある(左上方向が盤面の範囲内)
    rb_blank = diagonal & ((diagonal >> 9) & blank) << 9
    # wb1の計算
    blanks[0] = l_blank
    blanks[1] = r_blank
    blanks[2] = t_blank
    blanks[3] = b_blank
    blanks[4] = lt_blank
    blanks[5] = rt_blank
    blanks[6] = lb_blank
    blanks[7] = rb_blank
    for i in range(8):
        # black
        bits = blanks[i] & black
        if bits:
            # {{{ -- _popcount --
            bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
            bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
            bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
            bits = bits + (bits >> <unsigned int>8)
            bits = bits + (bits >> <unsigned int>16)
            score += <signed int>(bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
            # -- _popcount -- }}}
        # white
        bits = blanks[i] & white
        if bits:
            # -- {{{ _popcount --
            bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
            bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
            bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
            bits = bits + (bits >> <unsigned int>8)
            bits = bits + (bits >> <unsigned int>16)
            score -= <signed int>(bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
            # -- _popcount -- }}}
    score *= wb1
    # wb2の計算
    lt_x = lt_blank & <unsigned long long>0x0040000000000000  # 左上のX打ち
    if lt_x:
        if lt_x & black:
            score += wb2
        else:
            score -= wb2
    rt_x = rt_blank & <unsigned long long>0x0002000000000000  # 右上のX打ち
    if rt_x:
        if rt_x & black:
            score += wb2
        else:
            score -= wb2
    lb_x = lb_blank & <unsigned long long>0x0000000000004000  # 左下のX打ち
    if lb_x:
        if lb_x & black:
            score += wb2
        else:
            score -= wb2
    rb_x = rb_blank & <unsigned long long>0x0000000000000200  # 右下のX打ち
    if rb_x:
        if rb_x & black:
            score += wb2
        else:
            score -= wb2
    # wb3の計算
    lt_r = l_blank & <unsigned long long>0x4000000000000000
    lt_b = t_blank & <unsigned long long>0x0080000000000000
    rt_l = r_blank & <unsigned long long>0x0200000000000000
    rt_b = t_blank & <unsigned long long>0x0001000000000000
    lb_t = b_blank & <unsigned long long>0x0000000000008000
    lb_r = l_blank & <unsigned long long>0x0000000000000040
    rb_t = b_blank & <unsigned long long>0x0000000000000100
    rb_l = r_blank & <unsigned long long>0x0000000000000002
    if lt_r & white:
        lt_r_sign = -1
    if lt_b & white:
        lt_b_sign = -1
    if rt_l & white:
        rt_l_sign = -1
    if rt_b & white:
        rt_b_sign = -1
    if lb_t & white:
        lb_t_sign = -1
    if lb_r & white:
        lb_r_sign = -1
    if rb_t & white:
        rb_t_sign = -1
    if rb_l & white:
        rb_l_sign = -1
    for i in range(1, 5):
        lt_r >>= 1
        if lt_r & blank:
            score += wb3 * lt_r_sign
        lt_b >>= 8
        if lt_b & blank:
            score += wb3 * lt_b_sign
        rt_l <<= 1
        if rt_l & blank:
            score += wb3 * rt_l_sign
        rt_b >>= 8
        if rt_b & blank:
            score += wb3 * rt_b_sign
        lb_t <<= 8
        if lb_t & blank:
            score += wb3 * lb_t_sign
        lb_r >>= 1
        if lb_r & blank:
            score += wb3 * lb_r_sign
        rb_t <<= 8
        if rb_t & blank:
            score += wb3 * rb_t_sign
        rb_l <<= 1
        if rb_l & blank:
            score += wb3 * rb_l_sign
    return score


# -------------------------------------------------- #
# Search Common Methods
cdef inline measure(pid):
    if pid:
        if pid not in Measure.count:
            Measure.count[pid] = 0
        Measure.count[pid] += 1


cdef inline signed int timer(pid):
    if pid:
        if time.time() > Timer.deadline[pid]:
            Timer.timeout_flag[pid] = True  # タイムアウト発生
            return Timer.timeout_value[pid]
    return <signed int>0


cdef inline unsigned long long _put_disc_board_size8_64bit(board, unsigned int color, unsigned int x, unsigned int y):
    cdef:
        unsigned long long put, black_bitboard, white_bitboard, flippable_discs_num, flippable_discs_count
        unsigned int black_score, white_score
        signed int shift_size
    # 配置位置を整数に変換
    shift_size = (63-(y*8+x))
    put = <unsigned long long>1 << shift_size
    # ひっくり返せる石を取得
    black_bitboard = board._black_bitboard
    white_bitboard = board._white_bitboard
    black_score = board._black_score
    white_score = board._white_score
    flippable_discs_num = _get_flippable_discs_num(color, black_bitboard, white_bitboard, put)
    flippable_discs_count = _popcount(flippable_discs_num)
    # 打つ前の状態を格納
    board.prev += [(black_bitboard, white_bitboard, black_score, white_score)]
    # 自分の石を置いて相手の石をひっくり返す
    if color:
        black_bitboard ^= put | flippable_discs_num
        white_bitboard ^= flippable_discs_num
        black_score += <unsigned int>1 + <unsigned int>flippable_discs_count
        white_score -= <unsigned int>flippable_discs_count
    else:
        white_bitboard ^= put | flippable_discs_num
        black_bitboard ^= flippable_discs_num
        black_score -= <unsigned int>flippable_discs_count
        white_score += <unsigned int>1 + <unsigned int>flippable_discs_count
    board._black_bitboard = black_bitboard
    board._white_bitboard = white_bitboard
    board._black_score = black_score
    board._white_score = white_score
    board._flippable_discs_num = flippable_discs_num
    return flippable_discs_num


cdef inline _undo_board(board):
    (board._black_bitboard, board._white_bitboard, board._black_score, board._white_score) = board.prev.pop()


# -------------------------------------------------- #
# AlphaBeta Methods
cdef _alphabeta_get_score(alphabeta, color, board, alpha, beta, unsigned int depth, pid, unsigned int m, unsigned int t):
    cdef:
        unsigned int is_game_end
        signed int timeout
    # 前処理
    if m:
        measure(pid)
    if t:
        timeout = timer(pid)
        if timeout:
            return timeout
    # ゲーム終了 or 最大深さに到達
    legal_moves_b_bits = board.get_legal_moves_bits('black')
    legal_moves_w_bits = board.get_legal_moves_bits('white')
    is_game_end = <unsigned int>1 if not legal_moves_b_bits and not legal_moves_w_bits else <unsigned int>0
    if is_game_end or depth == <unsigned int>0:
        sign = 1 if color == 'black' else -1
        return alphabeta.evaluator.evaluate(color=color, board=board, possibility_b=board.get_bit_count(legal_moves_b_bits), possibility_w=board.get_bit_count(legal_moves_w_bits)) * sign  # noqa: E501
    # パスの場合
    legal_moves_bits = legal_moves_b_bits if color == 'black' else legal_moves_w_bits
    next_color = 'white' if color == 'black' else 'black'
    if not legal_moves_bits:
        return -_alphabeta_get_score(alphabeta, next_color, board, -beta, -alpha, depth, pid, m, t)
    # 評価値を算出
    cdef:
        unsigned int skip
    size = board.size
    mask = 1 << ((size**2)-1)
    for y in range(size):
        skip = <unsigned int>0
        for x in range(size):
            if legal_moves_bits & mask:
                board.put_disc(color, x, y)
                score = -_alphabeta_get_score(alphabeta, next_color, board, -beta, -alpha, depth-1, pid, m, t)
                board.undo()
                if Timer.is_timeout(pid):
                    return alpha
                alpha = max(alpha, score)  # 最大値を選択
                if alpha >= beta:  # 枝刈り
                    skip = <unsigned int>1
                    break
            mask >>= 1
        if skip:
            break
    return alpha


cdef double _alphabeta_get_score_size8_64bit(alphabeta, color, board, double alpha, double beta, unsigned int depth, pid, unsigned int m, unsigned int t):
    cdef:
        double score
        unsigned long long b, w, h, legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, mask
        unsigned int is_game_end, color_num, x, y
        signed int sign, timeout
    # 前処理
    if m:
        measure(pid)
    if t:
        timeout = timer(pid)
        if timeout:
            return timeout
    # ゲーム終了 or 最大深さに到達
    b = board._black_bitboard
    w = board._white_bitboard
    h = board._hole_bitboard
    legal_moves_b_bits = _get_legal_moves_bits(1, b, w, h)
    legal_moves_w_bits = _get_legal_moves_bits(0, b, w, h)
    is_game_end = <unsigned int>1 if not legal_moves_b_bits and not legal_moves_w_bits else <unsigned int>0
    if color == 'black':
        color_num = <unsigned int>1
        sign = <signed int>1
        legal_moves_bits = legal_moves_b_bits
        next_color = 'white'
    else:
        color_num = <unsigned int>0
        sign = <signed int>-1
        legal_moves_bits = legal_moves_w_bits
        next_color = 'black'
    if is_game_end or depth == <unsigned int>0:
        return alphabeta.evaluator.evaluate(color=color, board=board, possibility_b=_popcount(legal_moves_b_bits), possibility_w=_popcount(legal_moves_w_bits)) * sign  # noqa: E501
    # パスの場合
    if not legal_moves_bits:
        return -_alphabeta_get_score_size8_64bit(alphabeta, next_color, board, -beta, -alpha, depth, pid, m, t)
    # 評価値を算出
    mask = 1 << 63
    for y in range(8):
        for x in range(8):
            if legal_moves_bits & mask:
                _put_disc_board_size8_64bit(board, color_num, x, y)
                score = -_alphabeta_get_score_size8_64bit(alphabeta, next_color, board, -beta, -alpha, depth-1, pid, m, t)
                _undo_board(board)
                if score > alpha:
                    alpha = score
                if Timer.is_timeout(pid):
                    return alpha
                if alpha >= beta:  # 枝刈り
                    return alpha
            mask >>= 1
    return alpha


cdef inline tuple _alphabeta_next_move(str color, board, signed int param_min, signed int param_max, int depth, evaluator, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count, legal_moves_bit_list, legal_moves_x, legal_moves_y
    cdef:
        double alpha = param_min, beta = param_max
        unsigned long long b, w, h, legal_moves, mask = 0x8000000000000000
        unsigned int int_color = 0, x, y, index = 0
    measure_count = 0
    timer_timeout = <unsigned int>0
    if timer and pid:
        timer_deadline = Timer.deadline[pid]
        timer_timeout_value = Timer.timeout_value[pid]
    if measure and pid:
        if pid not in Measure.count:
            Measure.count[pid] = 0
        measure_count = Measure.count[pid]
    if color == 'black':
        int_color = <unsigned int>1
    b, w, h = board.get_bitboard_info()
    legal_moves = _get_legal_moves_bits(int_color, b, w, h)
    for y in range(8):
        for x in range(8):
            if legal_moves & mask:
                legal_moves_bit_list[index] = mask
                legal_moves_x[index] = x
                legal_moves_y[index] = y
                index += 1
            mask >>= 1
    best_move, _ = _alphabeta_get_best_move(int_color, board, index, legal_moves_bit_list, legal_moves_x, legal_moves_y, alpha, beta, depth, evaluator, timer)
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return best_move


cdef inline _alphabeta_get_best_move_wrap(str color, board, moves, double alpha, double beta, int depth, evaluator, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count
    cdef:
        unsigned long long[64] moves_bit_list
        unsigned long long put
        unsigned int[64] moves_x, moves_y
        unsigned int x, y, index = 0, int_color = 0
        signed int lshift
    measure_count = 0
    timer_timeout = <unsigned int>0
    if timer and pid:
        timer_deadline = Timer.deadline[pid]
        timer_timeout_value = Timer.timeout_value[pid]
    if measure and pid:
        if pid not in Measure.count:
            Measure.count[pid] = 0
        measure_count = Measure.count[pid]
    for x, y in moves:
        lshift = (63-(y*8+x))
        put = <unsigned long long>1 << lshift
        moves_bit_list[index] = put
        moves_x[index] = x
        moves_y[index] = y
        index += 1
    if color == 'black':
        int_color = <unsigned int>1
    best_move, scores = _alphabeta_get_best_move(int_color, board, index, moves_bit_list, moves_x, moves_y, alpha, beta, depth, evaluator, timer)
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return (best_move, scores)


cdef inline _alphabeta_get_best_move(unsigned int int_color, board, unsigned int index, unsigned long long[64] moves_bit_list, unsigned int[64] moves_x, unsigned int[64] moves_y, double alpha, double beta, int depth, evaluator, int timer):
    global timer_timeout, bb, wb, hb, bs, ws
    cdef:
        double score = alpha
        unsigned int int_color_next = 1, i, best = 64
    scores = {}
    # 手番
    if int_color:
        int_color_next = <unsigned int>0
    # ボード情報取得
    bb, wb, hb = board.get_bitboard_info()
    bs = board._black_score
    ws = board._white_score
    # ボード情報退避
    board_bb = bb
    board_wb = wb
    board_bs = bs
    board_ws = ws
    board_prev = [(item[0], item[1], item[2], item[3]) for item in board.prev]
    # 各手のスコア取得
    for i in range(index):
        _put_disc(int_color, moves_bit_list[i])
        score = -_alphabeta_get_score_evaluator(int_color_next, board, -beta, -alpha, depth-1, evaluator, timer, <unsigned int>0)
        _undo()
        scores[(moves_x[i], moves_y[i])] = score
        if timer_timeout:  # タイムアウト判定
            if best == 64:
                best = i
            break
        if score > alpha:  # 最善手を更新
            alpha = score
            best = i
    # ボードを元に戻す
    board._black_bitboard = board_bb
    board._white_bitboard = board_wb
    board._black_score = board_bs
    board._white_score = board_ws
    board.prev = [(item[0], item[1], item[2], item[3]) for item in board_prev]
    return (moves_x[best], moves_y[best]), scores


cdef inline double _alphabeta_get_score_evaluator(unsigned int int_color, board, double alpha, double beta, unsigned int depth, evaluator, int t, unsigned int pas):
    global timer_timeout, measure_count, bb, wb, hb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        double score
        unsigned long long legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, move
        unsigned int i, is_game_end = 0, int_color_next = 1, x, y
        signed int timeout, sign = -1
    # タイムアウト判定
    if t:
        timeout = check_timeout()
        if timeout:
            return timeout
    # 探索ノード数カウント
    measure_count += 1
    # 合法手を取得
    legal_moves_bits = _get_legal_moves_bits(int_color, bb, wb, hb)
    # 前回パス and 打てる場所なし の場合ゲーム終了
    if pas and not legal_moves_bits:
        is_game_end = <unsigned int>1
    # 最大深さに到達 or ゲーム終了
    if not depth or is_game_end:
        if int_color:
            legal_moves_b_bits = legal_moves_bits
            legal_moves_w_bits = _get_legal_moves_bits(<unsigned int>0, bb, wb, hb)
            sign = <signed int>1
            str_color = 'black'
        else:
            legal_moves_b_bits = _get_legal_moves_bits(<unsigned int>1, bb, wb, hb)
            legal_moves_w_bits = legal_moves_bits
            str_color = 'white'
        board._black_bitboard = bb
        board._white_bitboard = wb
        board._black_score = bs
        board._white_score = ws
        board._flippable_discs_num = fd
        board.prev = []
        for i in range(tail):
            board.prev += [(pbb[i], pwb[i], pbs[i], pws[i])]
        return evaluator.evaluate(str_color, board, _popcount(legal_moves_b_bits), _popcount(legal_moves_w_bits)) * sign
    # 次の手番
    if int_color:
        int_color_next = <unsigned int>0
    # パスの場合
    if not legal_moves_bits:
        return -_alphabeta_get_score_evaluator(int_color_next, board, -beta, -alpha, depth, evaluator, t, <unsigned int>1)
    # 評価値を算出
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        _put_disc(int_color, move)
        score = -_alphabeta_get_score_evaluator(int_color_next, board, -beta, -alpha, depth-1, evaluator, t, <unsigned int>0)
        _undo()
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする
        if score > alpha:
            alpha = score
        if timer_timeout:
            return alpha
        if alpha >= beta:  # 枝刈り
            return alpha
    return alpha


# -------------------------------------------------- #
# NegaScout Methods
cdef _negascout_get_score(func, negascout, color, board, alpha, beta, unsigned int depth, pid):
    cdef:
        unsigned int is_game_end
    # ゲーム終了 or 最大深さに到達
    legal_moves_b_bits = board.get_legal_moves_bits('black')
    legal_moves_w_bits = board.get_legal_moves_bits('white')
    is_game_end = <unsigned int>1 if not legal_moves_b_bits and not legal_moves_w_bits else <unsigned int>0
    sign = 1 if color == 'black' else -1
    if is_game_end or depth == <unsigned int>0:
        return negascout.evaluator.evaluate(color=color, board=board, possibility_b=board.get_bit_count(legal_moves_b_bits), possibility_w=board.get_bit_count(legal_moves_w_bits)) * sign  # noqa: E501
    # パスの場合
    legal_moves_bits = legal_moves_b_bits if color == 'black' else legal_moves_w_bits
    next_color = 'white' if color == 'black' else 'black'
    if not legal_moves_bits:
        return -func(func, negascout, next_color, board, -beta, -alpha, depth, pid=pid)
    # 着手可能数に応じて手を並び替え
    tmp = []
    size = board.size
    mask = 1 << ((size**2)-1)
    for y in range(size):
        for x in range(size):
            if legal_moves_bits & mask:
                board.put_disc(color, x, y)
                possibility_b = board.get_bit_count(board.get_legal_moves_bits('black'))
                possibility_w = board.get_bit_count(board.get_legal_moves_bits('white'))
                tmp += [((x, y), (possibility_b - possibility_w) * sign)]
                board.undo()
            mask >>= 1
    next_moves = [i[0] for i in sorted(tmp, reverse=True, key=lambda x:x[1])]
    # NegaScout法
    cdef:
        unsigned int index = 0
    tmp, null_window = None, beta
    for move in next_moves:
        if alpha < beta:
            board.put_disc(color, *move)
            tmp = -func(func, negascout, next_color, board, -null_window, -alpha, depth-1, pid=pid)
            board.undo()
            if alpha < tmp:
                if tmp <= null_window and index:
                    board.put_disc(color, *move)
                    alpha = -func(func, negascout, next_color, board, -beta, -tmp, depth-1, pid=pid)
                    board.undo()
                    if Timer.is_timeout(pid):
                        return alpha
                else:
                    alpha = tmp
            null_window = alpha + 1
        else:
            break
        index += <unsigned int>1
    return alpha


cdef _negascout_get_score_measure(func, negascout, color, board, alpha, beta, unsigned int depth, pid):
    measure(pid)
    return _negascout_get_score(func, negascout, color, board, alpha, beta, depth, pid)


cdef _negascout_get_score_timer(func, negascout, color, board, alpha, beta, unsigned int depth, pid):
    cdef:
        signed int timeout
    timeout = timer(pid)
    return timeout if timeout else _negascout_get_score(func, negascout, color, board, alpha, beta, depth, pid)


cdef _negascout_get_score_measure_timer(func, negascout, color, board, alpha, beta, unsigned int depth, pid):
    cdef:
        signed int timeout
    measure(pid)
    timeout = timer(pid)
    return timeout if timeout else _negascout_get_score(func, negascout, color, board, alpha, beta, depth, pid)


cdef double _negascout_get_score_measure_size8_64bit(func, negascout, color, board, double alpha, double beta, unsigned int depth, pid):
    measure(pid)
    return _negascout_get_score_size8_64bit(func, negascout, color, board, alpha, beta, depth, pid)


cdef double _negascout_get_score_timer_size8_64bit(func, negascout, color, board, double alpha, double beta, unsigned int depth, pid):
    cdef:
        signed int timeout
    timeout = timer(pid)
    return timeout if timeout else _negascout_get_score_size8_64bit(func, negascout, color, board, alpha, beta, depth, pid)


cdef double _negascout_get_score_measure_timer_size8_64bit(func, negascout, color, board, double alpha, double beta, unsigned int depth, pid):
    cdef:
        signed int timeout
    measure(pid)
    timeout = timer(pid)
    return timeout if timeout else _negascout_get_score_size8_64bit(func, negascout, color, board, alpha, beta, depth, pid)


cdef double _negascout_get_score_size8_64bit(func, negascout, color, board, double alpha, double beta, unsigned int depth, pid):
    cdef:
        double score, tmp, null_window
        unsigned long long b, w, h, legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, mask
        unsigned int[64] next_moves_x, next_moves_y
        unsigned int is_game_end, color_num, x, y, i, count, index = 0
        signed int[64] possibilities
        signed int sign
    # ゲーム終了 or 最大深さに到達
    b = board._black_bitboard
    w = board._white_bitboard
    h = board._hole_bitboard
    legal_moves_b_bits = _get_legal_moves_bits(<unsigned int>1, b, w, h)
    legal_moves_w_bits = _get_legal_moves_bits(<unsigned int>0, b, w, h)
    is_game_end = <unsigned int>1 if not legal_moves_b_bits and not legal_moves_w_bits else <unsigned int>0
    if color == 'black':
        color_num = <unsigned int>1
        sign = <signed int>1
        legal_moves_bits = legal_moves_b_bits
        next_color = 'white'
    else:
        color_num = <unsigned int>0
        sign = <signed int>-1
        legal_moves_bits = legal_moves_w_bits
        next_color = 'black'
    if is_game_end or depth == <unsigned int>0:
        return negascout.evaluator.evaluate(color=color, board=board, possibility_b=_popcount(legal_moves_b_bits), possibility_w=_popcount(legal_moves_w_bits)) * sign  # noqa: E501
    # パスの場合
    if not legal_moves_bits:
        return -func(func, negascout, next_color, board, -beta, -alpha, depth, pid)
    # 着手可能数に応じて手を並び替え
    count = 0
    mask = 1 << 63
    for y in range(8):
        for x in range(8):
            if legal_moves_bits & mask:
                next_moves_x[count] = x
                next_moves_y[count] = y
                possibilities[count] = _negascout_get_possibility_size8_64bit(board, color_num, x, y, sign)
                count += 1
            mask >>= 1
    _negascout_sort_moves_by_possibility(count, next_moves_x, next_moves_y, possibilities)
    # 次の手の探索
    null_window = beta
    for i in range(count):
        if alpha < beta:
            _put_disc_board_size8_64bit(board, color_num, next_moves_x[i], next_moves_y[i])
            tmp = -func(func, negascout, next_color, board, -null_window, -alpha, depth-1, pid)
            _undo_board(board)
            if alpha < tmp:
                if tmp <= null_window and index:
                    _put_disc_board_size8_64bit(board, color_num, next_moves_x[i], next_moves_y[i])
                    alpha = -func(func, negascout, next_color, board, -beta, -tmp, depth-1, pid)
                    _undo_board(board)
                    if Timer.is_timeout(pid):
                        return alpha
                else:
                    alpha = tmp
            null_window = alpha + 1
        else:
            return alpha
        index += <unsigned int>1
    return alpha


cdef inline signed int _negascout_get_possibility_size8_64bit(board, unsigned int color, unsigned int x, unsigned int y, signed int sign):
    cdef:
        unsigned long long put, black_bitboard, white_bitboard, hole_bitboard, flippable_discs_num
        signed int shift_size, possibility_b, possibility_w
    # 配置位置を整数に変換
    shift_size = (63-(y*8+x))
    put = <unsigned long long>1 << shift_size
    # ひっくり返せる石を取得
    black_bitboard = board._black_bitboard
    white_bitboard = board._white_bitboard
    hole_bitboard = board._hole_bitboard
    flippable_discs_num = _get_flippable_discs_num(color, black_bitboard, white_bitboard, put)
    # 自分の石を置いて相手の石をひっくり返す
    if color:
        black_bitboard ^= put | flippable_discs_num
        white_bitboard ^= flippable_discs_num
    else:
        white_bitboard ^= put | flippable_discs_num
        black_bitboard ^= flippable_discs_num
    possibility_b = <signed int>_popcount(_get_legal_moves_bits(<unsigned int>1, black_bitboard, white_bitboard, hole_bitboard))
    possibility_w = <signed int>_popcount(_get_legal_moves_bits(<unsigned int>0, black_bitboard, white_bitboard, hole_bitboard))
    return (possibility_b - possibility_w) * sign


cdef inline _negascout_sort_moves_by_possibility(unsigned int count, unsigned int *next_moves_x, unsigned int *next_moves_y, signed int *possibilities):
    cdef:
        unsigned int[64] array_x1, array_x2, array_y1, array_y2
        unsigned int len1, len2, i
        signed int[64] array_p1, array_p2
    # merge sort
    if count > 1:
        len1 = <unsigned int>(count / 2)
        len2 = <unsigned int>(count - len1)
        for i in range(len1):
            array_x1[i] = next_moves_x[i]
            array_y1[i] = next_moves_y[i]
            array_p1[i] = possibilities[i]
        for i in range(len2):
            array_x2[i] = next_moves_x[len1+i]
            array_y2[i] = next_moves_y[len1+i]
            array_p2[i] = possibilities[len1+i]
        _negascout_sort_moves_by_possibility(len1, array_x1, array_y1, array_p1)
        _negascout_sort_moves_by_possibility(len2, array_x2, array_y2, array_p2)
        _negascout_merge(len1, len2, array_x1, array_y1, array_p1, array_x2, array_y2, array_p2, next_moves_x, next_moves_y, possibilities)


cdef inline _negascout_merge(unsigned int len1, unsigned int len2, unsigned int *array_x1, unsigned int *array_y1, signed int *array_p1, unsigned int *array_x2, unsigned int *array_y2, signed int *array_p2, unsigned int *next_moves_x, unsigned int *next_moves_y, signed int *possibilities):
    cdef:
        unsigned int i = 0, j = 0

    while i < len1 or j < len2:
        # descending sort
        if j >= len2 or (i < len1 and array_p1[i] >= array_p2[j]):
            next_moves_x[i+j] = array_x1[i]
            next_moves_y[i+j] = array_y1[i]
            possibilities[i+j] = array_p1[i]
            i += 1
        else:
            next_moves_x[i+j] = array_x2[j]
            next_moves_y[i+j] = array_y2[j]
            possibilities[i+j] = array_p2[j]
            j += 1


cdef inline tuple _negascout_next_move(str color, board, signed int param_min, signed int param_max, int depth, evaluator, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count
    cdef:
        double alpha = param_min, beta = param_max
        unsigned int int_color = 0
    measure_count = 0
    timer_timeout = <unsigned int>0
    if timer and pid:
        timer_deadline = Timer.deadline[pid]
        timer_timeout_value = Timer.timeout_value[pid]
    if measure and pid:
        if pid not in Measure.count:
            Measure.count[pid] = 0
        measure_count = Measure.count[pid]
    if color == 'black':
        int_color = <unsigned int>1
    moves = board.get_legal_moves(color)  # 手の候補
    best_move, _ = _negascout_get_best_move(int_color, board, moves, alpha, beta, depth, evaluator, timer)
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return best_move


cdef inline _negascout_get_best_move_wrap(str color, board, moves, double alpha, double beta, int depth, evaluator, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count
    cdef:
        unsigned int int_color = 0
    measure_count = 0
    timer_timeout = <unsigned int>0
    if timer and pid:
        timer_deadline = Timer.deadline[pid]
        timer_timeout_value = Timer.timeout_value[pid]
    if measure and pid:
        if pid not in Measure.count:
            Measure.count[pid] = 0
        measure_count = Measure.count[pid]
    if color == 'black':
        int_color = <unsigned int>1
    best_move, scores = _negascout_get_best_move(int_color, board, moves, alpha, beta, depth, evaluator, timer)
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return (best_move, scores)


cdef inline _negascout_get_best_move(unsigned int int_color, board, moves, double alpha, double beta, int depth, evaluator, int timer):
    global timer_timeout, bb, wb, hb, bs, ws
    cdef:
        double score = alpha
        unsigned long long board_bb, board_wb
        unsigned int int_color_next = 1, board_bs, board_ws
    scores = {}
    # 手番
    if int_color:
        int_color_next = <unsigned int>0
    # ボード情報取得
    bb, wb, hb = board.get_bitboard_info()
    bs = board._black_score
    ws = board._white_score
    # ボード情報退避
    board_bb = bb
    board_wb = wb
    board_bs = bs
    board_ws = ws
    board_prev = [(item[0], item[1], item[2], item[3]) for item in board.prev]
    # 各手のスコア取得
    best_move = None
    for move in moves:
        _put_disc(int_color, <unsigned long long>1 << (63-(move[1]*8+move[0])))
        score = -_negascout_get_score_board(int_color_next, board, -beta, -alpha, depth-1, evaluator, timer, <unsigned int>0)
        _undo()
        scores[move] = score
        if timer_timeout:  # タイムアウト判定
            best_move = move if best_move is None else best_move
            break
        if score > alpha:  # 最善手を更新
            alpha = score
            best_move = move
    # ボードを元に戻す
    board._black_bitboard = board_bb
    board._white_bitboard = board_wb
    board._black_score = board_bs
    board._white_score = board_ws
    board.prev = [(item[0], item[1], item[2], item[3]) for item in board_prev]
    return best_move, scores


cdef inline double _negascout_get_score_board(unsigned int int_color, board, double alpha, double beta, unsigned int depth, evaluator, int t, unsigned int pas):
    global timer_timeout, measure_count, bb, wb, hb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        double score, tmp, null_window
        unsigned long long[64] next_moves_list
        unsigned long long legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, move
        unsigned int i, is_game_end = 0, int_color_next = 1, count = 0, index = 0
        signed int[64] possibilities
        signed int timeout, sign = -1
    # タイムアウト判定
    if t:
        timeout = check_timeout()
        if timeout:
            return timeout
    # 探索ノード数カウント
    measure_count += 1
    # 合法手を取得
    legal_moves_bits = _get_legal_moves_bits(int_color, bb, wb, hb)
    # 前回パス and 打てる場所なし の場合ゲーム終了
    if pas and not legal_moves_bits:
        is_game_end = <unsigned int>1
    # 最大深さに到達 or ゲーム終了
    if not depth or is_game_end:
        if int_color:
            legal_moves_b_bits = legal_moves_bits
            legal_moves_w_bits = _get_legal_moves_bits(<unsigned int>0, bb, wb, hb)
            sign = <signed int>1
            str_color = 'black'
        else:
            legal_moves_b_bits = _get_legal_moves_bits(<unsigned int>1, bb, wb, hb)
            legal_moves_w_bits = legal_moves_bits
            str_color = 'white'
        board._black_bitboard = bb
        board._white_bitboard = wb
        board._black_score = bs
        board._white_score = ws
        board._flippable_discs_num = fd
        board.prev = []
        for i in range(tail):
            board.prev += [(pbb[i], pwb[i], pbs[i], pws[i])]
        return evaluator.evaluate(str_color, board, _popcount(legal_moves_b_bits), _popcount(legal_moves_w_bits)) * sign
    # 次の手番
    if int_color:
        sign = <signed int>1
        int_color_next = <unsigned int>0
    # パスの場合
    if not legal_moves_bits:
        return -_negascout_get_score_board(int_color_next, board, -beta, -alpha, depth, evaluator, t, <unsigned int>1)
    # 着手可能数に応じて手を並び替え
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        next_moves_list[count] = move
        possibilities[count] = _negascout_get_possibility(int_color, bb, wb, move, sign)
        count += 1
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする
    _sort_moves_by_possibility(count, next_moves_list, possibilities)
    # 次の手の探索
    null_window = beta
    for i in range(count):
        if alpha < beta:
            _put_disc(int_color, next_moves_list[i])
            tmp = -_negascout_get_score_board(int_color_next, board, -null_window, -alpha, depth-1, evaluator, t, <unsigned int>0)
            _undo()
            if alpha < tmp:
                if tmp <= null_window and index:
                    _put_disc(int_color, next_moves_list[i])
                    alpha = -_negascout_get_score_board(int_color_next, board, -beta, -tmp, depth-1, evaluator, t, <unsigned int>0)
                    _undo()
                    if timer_timeout:
                        return alpha
                else:
                    alpha = tmp
            null_window = alpha + 1
        else:
            return alpha
        index += <unsigned int>1
    return alpha


cdef inline signed int _negascout_get_possibility(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long move, signed int sign):
    global hb
    cdef:
        unsigned long long flippable_discs_num
        signed int pb, pw
    # ひっくり返せる石を取得
    flippable_discs_num = _get_flippable_discs_num(int_color, b, w, move)
    # 自分の石を置いて相手の石をひっくり返す
    if int_color:
        b ^= move | flippable_discs_num
        w ^= flippable_discs_num
    else:
        w ^= move | flippable_discs_num
        b ^= flippable_discs_num
    pb = <signed int>_popcount(_get_legal_moves_bits(<unsigned int>1, b, w, hb))
    pw = <signed int>_popcount(_get_legal_moves_bits(<unsigned int>0, b, w, hb))
    return (pb - pw) * sign


# -------------------------------------------------- #
# Table Methods
cdef inline signed int _table_get_score_size8_64bit(table, board):
    cdef:
        unsigned long long b, w, mask = 0x8000000000000000
        unsigned int x, y
        signed int score = 0
    b = board._black_bitboard
    w = board._white_bitboard
    for y in range(8):
        for x in range(8):
            if b & mask:
                score += <signed int>table[y][x]
            elif w & mask:
                score -= <signed int>table[y][x]
            mask >>= 1
    return score


cdef inline signed int _table_get_score(table, board):
    cdef:
        unsigned int x, y, size
        signed int score
    board_info = board.get_board_info()
    size = board.size
    score = 0
    for y in range(size):
        for x in range(size):
            score += table[y][x] * board_info[y][x]
    return score


# -------------------------------------------------- #
# MonteCarlo Methods
cdef inline tuple _montecarlo_next_move(str color, board, unsigned int count, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count, legal_moves_bit_list, montecarlo_scores, bb, wb, hb, bs, ws
    cdef:
        unsigned long long b, w, h, legal_moves, mask = 0x8000000000000000
        unsigned int tbs, tws, int_color = 0, i, x, y, index = 0
        signed int max_score
    measure_count = 0
    timer_timeout = <unsigned int>0
    if timer and pid:
        timer_deadline = Timer.deadline[pid]
        timer_timeout_value = Timer.timeout_value[pid]
    if measure and pid:
        if pid not in Measure.count:
            Measure.count[pid] = 0
        measure_count = Measure.count[pid]
    if color == 'black':
        int_color = <unsigned int>1
    b, w, h = board.get_bitboard_info()
    tbs = board._black_score
    tws = board._white_score
    legal_moves = _get_legal_moves_bits(int_color, b, w, h)
    for y in range(8):
        for x in range(8):
            if legal_moves & mask:
                legal_moves_bit_list[index] = mask
                legal_moves_x[index] = x
                legal_moves_y[index] = y
                montecarlo_scores[index] = 0
                index += 1
            mask >>= 1
    # seed
    init_rand(<unsigned long>time.time())
    for j in range(count):
        for i in range(index):
            # ボード情報取得
            bb, wb, hb = b, w, h
            bs = tbs
            ws = tws
            montecarlo_scores[i] += _playout(int_color, legal_moves_bit_list[i])
            # 探索ノード数カウント
            measure_count += 1
        if timer and check_timeout():
            break
    max_score = montecarlo_scores[0]
    best_move = (legal_moves_x[0], legal_moves_y[0])
    for i in range(index):
        if montecarlo_scores[i] > max_score:
            max_score = montecarlo_scores[i]
            best_move = (legal_moves_x[i], legal_moves_y[i])
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return best_move


cdef inline signed int _playout(unsigned int int_color, unsigned long long move_bit):
    global bb, wb, hb, bs, ws
    cdef:
        unsigned long long random_put, legal_moves_bits, count
        unsigned int turn, x, y, pass_count = 0, random_index
        signed int ret
    # 1手打つ
    _put_disc_no_prev(int_color, move_bit)
    # 決着までランダムに打つ
    turn = int_color
    while True:
        # 次の手番
        turn = <unsigned int>0 if turn else <unsigned int>1
        # 合法手を取得
        legal_moves_bits = _get_legal_moves_bits(turn, bb, wb, hb)
        # 打てる場所なし
        if not legal_moves_bits:
            pass_count += 1
            if pass_count == 2:
                break
        # 打てる場所あり
        else:
            pass_count = 0
            # ランダムに手を選ぶ
            count = _popcount(legal_moves_bits)
            random_index = rand_int() % count + 1
            for _ in range(random_index):
                random_put = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
                legal_moves_bits ^= random_put                         # 一番右のONしているビットをOFFする
            # 1手打つ
            _put_disc_no_prev(turn, random_put)
    # 結果を返す
    ret = -2
    if (int_color and bs > ws) or (not int_color and ws > bs):
        ret = 2
    elif bs == ws:
        ret = 1
    return ret


cdef inline signed int _board_playout(str color, board, move):
    global bb, wb, hb, bs, ws
    cdef:
        unsigned long long random_put, legal_moves_bits
        unsigned int int_color = 0, turn, x, y, pass_count = 0, random_index
        signed int ret
    # ボード情報取得
    bb, wb, hb = board.get_bitboard_info()
    bs = board._black_score
    ws = board._white_score
    # 手番
    if color == 'black':
        int_color = <unsigned int>1
    # 1手打つ
    x, y = move
    _put_disc_no_prev(int_color, <unsigned long long>1 << (63-(y*8+x)))
    # 決着までランダムに打つ
    turn = int_color
    while True:
        # 次の手番
        turn = <unsigned int>0 if turn else <unsigned int>1
        # 合法手を取得
        legal_moves_bits = _get_legal_moves_bits(turn, bb, wb, hb)
        # 打てる場所なし
        if not legal_moves_bits:
            pass_count += 1
            if pass_count == 2:
                break
        # 打てる場所あり
        else:
            pass_count = 0
            # ランダムに手を選ぶ
            count = _popcount(legal_moves_bits)
            random_index = rand() % count + 1
            for _ in range(random_index):
                random_put = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
                legal_moves_bits ^= random_put                         # 一番右のONしているビットをOFFする
            # 1手打つ
            _put_disc_no_prev(turn, random_put)
    # 結果を返す
    ret = -2
    if (int_color and bs > ws) or (not int_color and ws > bs):
        ret = 2
    elif bs == ws:
        ret = 1
    return ret


# -------------------------------------------------- #
# BitBoard Methods
cdef inline unsigned long long _get_legal_moves_bits(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long h):
    cdef:
        unsigned long long player = w, opponent = b
    if int_color:
        player = b
        opponent = w
    cdef:
        unsigned long long blank = ~(player | opponent | h)
        unsigned long long horizontal = opponent & <unsigned long long>0x7E7E7E7E7E7E7E7E  # horizontal mask value
        unsigned long long vertical = opponent & <unsigned long long>0x00FFFFFFFFFFFF00    # vertical mask value
        unsigned long long diagonal = opponent & <unsigned long long>0x007E7E7E7E7E7E00    # diagonal mask value
        unsigned long long tmp_h, tmp_v, tmp_d1, tmp_d2
    # left/right
    tmp_h = horizontal & ((player << 1) | (player >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    tmp_h |= horizontal & ((tmp_h << 1) | (tmp_h >> 1))
    # top/bottom
    tmp_v = vertical & ((player << 8) | (player >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    tmp_v |= vertical & ((tmp_v << 8) | (tmp_v >> 8))
    # left-top/right-bottom
    tmp_d1 = diagonal & ((player << 9) | (player >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    tmp_d1 |= diagonal & ((tmp_d1 << 9) | (tmp_d1 >> 9))
    # right-top/left-bottom
    tmp_d2 = diagonal & ((player << 7) | (player >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    tmp_d2 |= diagonal & ((tmp_d2 << 7) | (tmp_d2 >> 7))
    return blank & ((tmp_h << 1) | (tmp_h >> 1) | (tmp_v << 8) | (tmp_v >> 8) | (tmp_d1 << 9) | (tmp_d1 >> 9) | (tmp_d2 << 7) | (tmp_d2 >> 7))


cdef inline unsigned long long _popcount(unsigned long long bits):
    bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
    bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
    bits = bits + (bits >> <unsigned int>8)
    bits = bits + (bits >> <unsigned int>16)
    return (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F


cdef inline void _put_disc(unsigned int int_color, unsigned long long move):
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        unsigned long long count
        signed int lshift
    # ひっくり返せる石を取得
    fd = _get_flippable_discs_num(int_color, bb, wb, move)
    count = _popcount(fd)
    # 打つ前の状態を格納
    pbb[tail] = bb
    pwb[tail] = wb
    pbs[tail] = bs
    pws[tail] = ws
    tail += 1
    # 自分の石を置いて相手の石をひっくり返す
    if int_color:
        bb ^= move | fd
        wb ^= fd
        bs += <unsigned int>1 + <unsigned int>count
        ws -= <unsigned int>count
    else:
        wb ^= move | fd
        bb ^= fd
        bs -= <unsigned int>count
        ws += <unsigned int>1 + <unsigned int>count


cdef inline void _put_disc_no_prev(unsigned int int_color, unsigned long long move):
    global bb, wb, bs, ws, fd
    cdef:
        unsigned long long count
        signed int lshift
    # ひっくり返せる石を取得
    fd = _get_flippable_discs_num(int_color, bb, wb, move)
    count = _popcount(fd)
    # 自分の石を置いて相手の石をひっくり返す
    if int_color:
        bb ^= move | fd
        wb ^= fd
        bs += <unsigned int>1 + <unsigned int>count
        ws -= <unsigned int>count
    else:
        wb ^= move | fd
        bb ^= fd
        bs -= <unsigned int>count
        ws += <unsigned int>1 + <unsigned int>count


cdef inline unsigned long long _get_flippable_discs_num(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long move):
    cdef:
        unsigned long long t_, rt, r_, rb, b_, lb, l_, lt, m_t_, m_rt, m_r_, m_rb, m_b_, m_lb, m_l_, m_lt, player = w, opponent = b, flippable_discs_num = 0
        unsigned int x, other = 0
    if int_color:
        player = b
        opponent = w
    # x座標を取得
    x = <unsigned int>(move % <unsigned int>0xFF)
    # ひっくり返せるディスクを求める
    if x >= <unsigned int>0x40:
        # (1)a1, b1, a2, b2
        if move >= <unsigned long long>0x0001000000000000:
            # 右、右下、下
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            m_rb = <unsigned long long>0x007F7F7F7F7F7F7F & opponent
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            rb = m_rb & (move >> <unsigned int>9)  # right-bottom
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            for _ in range(5):
                r_ |= m_r_ & (r_ >> <unsigned int>1)
                rb |= m_rb & (rb >> <unsigned int>9)
                b_ |= m_b_ & (b_ >> <unsigned int>8)
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
            if (<unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)) & player:
                flippable_discs_num |= rb
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
        # (4)a7, b7, a8, b8
        elif move <= <unsigned long long>0x0000000000008000:
            # 上、右上、右
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            m_rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & opponent
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            t_ = m_t_ & (move << <unsigned int>8)  # top
            rt = m_rt & (move << <unsigned int>7)  # right-top
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            for _ in range(5):
                t_ |= m_t_ & (t_ << <unsigned int>8)
                rt |= m_rt & (rt << <unsigned int>7)
                r_ |= m_r_ & (r_ >> <unsigned int>1)
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
            if (<unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)) & player:
                flippable_discs_num |= rt
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
        # (8)a3-b3, a4-b4, a5-b5, a6-b6
        elif move <= <unsigned long long>0x0000800000000000 and move >= <unsigned long long>0x0000000000400000:
            # 上、右上、右、右下、下
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            m_rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & opponent
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            m_rb = <unsigned long long>0x007F7F7F7F7F7F7F & opponent
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            t_ = m_t_ & (move << <unsigned int>8)  # top
            rt = m_rt & (move << <unsigned int>7)  # right-top
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            rb = m_rb & (move >> <unsigned int>9)  # right-bottom
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            for _ in range(5):
                r_ |= m_r_ & (r_ >> <unsigned int>1)
            for _ in range(3):
                t_ |= m_t_ & (t_ << <unsigned int>8)
                rt |= m_rt & (rt << <unsigned int>7)
                rb |= m_rb & (rb >> <unsigned int>9)
                b_ |= m_b_ & (b_ >> <unsigned int>8)
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
            if (<unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)) & player:
                flippable_discs_num |= rt
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
            if (<unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)) & player:
                flippable_discs_num |= rb
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
        else:
            other = 1
    elif x <= <unsigned int>0x02:
        # (2)g1, h1, g2, h2
        if move >= <unsigned long long>0x0001000000000000:
            # 下、左下、左
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            m_lb = <unsigned long long>0x00FEFEFEFEFEFEFE & opponent
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            lb = m_lb & (move >> <unsigned int>7)  # left-bottom
            l_ = m_l_ & (move << <unsigned int>1)  # left
            for _ in range(5):
                b_ |= m_b_ & (b_ >> <unsigned int>8)
                lb |= m_lb & (lb >> <unsigned int>7)
                l_ |= m_l_ & (l_ << <unsigned int>1)
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
            if (<unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)) & player:
                flippable_discs_num |= lb
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
        # (3)g7, h7, g8, h8
        elif move <= <unsigned long long>0x0000000000008000:
            # 左、左上、上
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            m_lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & opponent
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            l_ = m_l_ & (move << <unsigned int>1)  # left
            lt = m_lt & (move << <unsigned int>9)  # left-top
            t_ = m_t_ & (move << <unsigned int>8)  # top
            for _ in range(5):
                l_ |= m_l_ & (l_ << <unsigned int>1)
                lt |= m_lt & (lt << <unsigned int>9)
                t_ |= m_t_ & (t_ << <unsigned int>8)
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
            if (<unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)) & player:
                flippable_discs_num |= lt
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
        # (6)g3-h3, g4-h4, g5-h5, g6-h6
        elif move <= <unsigned long long>0x00000200000000000 and move >= <unsigned long long>0x0000000000010000:
            # 下、左下、左、左上、上
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            m_lb = <unsigned long long>0x00FEFEFEFEFEFEFE & opponent
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            m_lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & opponent
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            lb = m_lb & (move >> <unsigned int>7)  # left-bottom
            l_ = m_l_ & (move << <unsigned int>1)  # left
            lt = m_lt & (move << <unsigned int>9)  # left-top
            t_ = m_t_ & (move << <unsigned int>8)  # top
            for _ in range(5):
                l_ |= m_l_ & (l_ << <unsigned int>1)
            for _ in range(3):
                b_ |= m_b_ & (b_ >> <unsigned int>8)
                lb |= m_lb & (lb >> <unsigned int>7)
                lt |= m_lt & (lt << <unsigned int>9)
                t_ |= m_t_ & (t_ << <unsigned int>8)
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
            if (<unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)) & player:
                flippable_discs_num |= lb
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
            if (<unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)) & player:
                flippable_discs_num |= lt
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
        else:
            other = 1
    elif x <= <unsigned int>0x20 and x >= <unsigned int>0x04:
        # (5)c1-f1, c2-f2
        if move >= <unsigned long long>0x0004000000000000:
            # 右、右下、下、左下、左
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            m_rb = <unsigned long long>0x007F7F7F7F7F7F7F & opponent
            m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
            m_lb = <unsigned long long>0x00FEFEFEFEFEFEFE & opponent
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            rb = m_rb & (move >> <unsigned int>9)  # right-bottom
            b_ = m_b_ & (move >> <unsigned int>8)  # bottom
            lb = m_lb & (move >> <unsigned int>7)  # left-bottom
            l_ = m_l_ & (move << <unsigned int>1)  # left
            for _ in range(5):
                b_ |= m_b_ & (b_ >> <unsigned int>8)
            for _ in range(3):
                r_ |= m_r_ & (r_ >> <unsigned int>1)
                rb |= m_rb & (rb >> <unsigned int>9)
                lb |= m_lb & (lb >> <unsigned int>7)
                l_ |= m_l_ & (l_ << <unsigned int>1)
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
            if (<unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)) & player:
                flippable_discs_num |= rb
            if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
                flippable_discs_num |= b_
            if (<unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)) & player:
                flippable_discs_num |= lb
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
        # (7)c7-f7, c8-f8
        elif move <= <unsigned long long>0x0000000000002000:
            # 左、左上、上、右上、右
            m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
            m_lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & opponent
            m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
            m_rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & opponent
            m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
            l_ = m_l_ & (move << <unsigned int>1)  # left
            lt = m_lt & (move << <unsigned int>9)  # left-top
            t_ = m_t_ & (move << <unsigned int>8)  # top
            rt = m_rt & (move << <unsigned int>7)  # right-top
            r_ = m_r_ & (move >> <unsigned int>1)  # right
            for _ in range(5):
                t_ |= m_t_ & (t_ << <unsigned int>8)
            for _ in range(3):
                l_ |= m_l_ & (l_ << <unsigned int>1)
                lt |= m_lt & (lt << <unsigned int>9)
                rt |= m_rt & (rt << <unsigned int>7)
                r_ |= m_r_ & (r_ >> <unsigned int>1)
            if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
                flippable_discs_num |= l_
            if (<unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)) & player:
                flippable_discs_num |= lt
            if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
                flippable_discs_num |= t_
            if (<unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)) & player:
                flippable_discs_num |= rt
            if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
                flippable_discs_num |= r_
        else:
            other = 1
    else:
        other = 1
    if other:
        m_t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & opponent
        m_rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & opponent
        m_r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & opponent
        m_rb = <unsigned long long>0x007F7F7F7F7F7F7F & opponent
        m_b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & opponent
        m_lb = <unsigned long long>0x00FEFEFEFEFEFEFE & opponent
        m_l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & opponent
        m_lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & opponent
        t_ = m_t_ & (move << <unsigned int>8)  # top
        rt = m_rt & (move << <unsigned int>7)  # right-top
        r_ = m_r_ & (move >> <unsigned int>1)  # right
        rb = m_rb & (move >> <unsigned int>9)  # right-bottom
        b_ = m_b_ & (move >> <unsigned int>8)  # bottom
        lb = m_lb & (move >> <unsigned int>7)  # left-bottom
        l_ = m_l_ & (move << <unsigned int>1)  # left
        lt = m_lt & (move << <unsigned int>9)  # left-top
        for _ in range(3):
            t_ |= m_t_ & (t_ << <unsigned int>8)
            rt |= m_rt & (rt << <unsigned int>7)
            r_ |= m_r_ & (r_ >> <unsigned int>1)
            rb |= m_rb & (rb >> <unsigned int>9)
            b_ |= m_b_ & (b_ >> <unsigned int>8)
            lb |= m_lb & (lb >> <unsigned int>7)
            l_ |= m_l_ & (l_ << <unsigned int>1)
            lt |= m_lt & (lt << <unsigned int>9)
        if (<unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)) & player:
            flippable_discs_num |= t_
        if (<unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)) & player:
            flippable_discs_num |= rt
        if (<unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)) & player:
            flippable_discs_num |= r_
        if (<unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)) & player:
            flippable_discs_num |= rb
        if (<unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)) & player:
            flippable_discs_num |= b_
        if (<unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)) & player:
            flippable_discs_num |= lb
        if (<unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)) & player:
            flippable_discs_num |= l_
        if (<unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)) & player:
            flippable_discs_num |= lt
    return flippable_discs_num


cdef inline void _undo():
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, tail
    tail -= 1
    bb = pbb[tail]
    wb = pwb[tail]
    bs = pbs[tail]
    ws = pws[tail]


# -------------------------------------------------- #
# Timeout Methods
cdef inline signed int check_timeout():
    global timer_deadline, timer_timeout, timer_timeout_value
    if time.time() > timer_deadline:
        timer_timeout = <unsigned int>1
        return timer_timeout_value
    return <signed int>0


# -------------------------------------------------- #
# rand_int Methods
cdef unsigned long set_s(unsigned long s):
    s = (s * 1812433253) + 1
    s ^= s << 13
    s ^= s >> 17
    return s


cdef init_rand(unsigned long s):
    while True:
        s = set_s(s)
        tx = 123464980 ^ s
        s = set_s(s)
        ty = 3447902351 ^ s
        s = set_s(s)
        tz = 2859490775 ^ s
        s = set_s(s)
        tw = 47621719 ^ s
        if not ((tx == 0) and (ty == 0) and (tz == 0) and (tw == 0)):
            break


cdef unsigned long rand_int():
    global tx, ty, tz, tw
    cdef:
        unsigned long tt
    tt = tx ^ (tx << 11)
    tx = ty
    ty = tz
    tz = tw
    tw = (tw ^ (tw >> 19)) ^ (tt ^ (tt>>8))
    return tw


# =========================================== #
# EvaluatorMethods
def evaluate_tpw(t, params, color, board, possibility_b, possibility_w):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _evaluate_tpw_size8_64bit(t.table.table, params, color, board, possibility_b, possibility_w)
    return _evaluate_tpw(t, params, color, board, possibility_b, possibility_w)


cdef inline signed int _evaluate_tpw_size8_64bit(table, params, color, board, possibility_b, possibility_w):
    cdef:
        unsigned long long t_mask = 0x8000000000000000, b_bitboard, w_bitboard, all_bitboard, bit_pos, lt, rt, lb, rb, b_t, w_t, b_b, w_b, b_l, w_l, b_r, w_r
        unsigned int x, y
        signed int wp = params[0], ww = params[1], score_w = 0, score_t = 0, score_p = 0
    b_bitboard, w_bitboard, h_bitboard = board.get_bitboard_info()
    # 勝敗が決まっている場合
    if not possibility_b and not possibility_w:
        score_w = board._black_score - board._white_score
        if score_w > 0:    # 黒が勝った
            score_w += ww
        elif score_w < 0:  # 白が勝った
            score_w -= ww
        return score_w
    # テーブルによるスコア
    for y in range(8):
        for x in range(8):
            if b_bitboard & t_mask:
                score_t += <signed int>table[y][x]
            elif w_bitboard & t_mask:
                score_t -= <signed int>table[y][x]
            t_mask >>= 1
    # 着手可能数によるスコア
    score_p = (possibility_b - possibility_w) * wp
    return score_t + score_p


cdef inline signed int _evaluate_tpw(t, params, color, board, possibility_b, possibility_w):
    if not possibility_b and not possibility_w:  # 勝敗が決まっている場合
        ret = board._black_score - board._white_score
        if ret > 0:    # 黒が勝った
            ret += params[1]
        elif ret < 0:  # 白が勝った
            ret -= params[1]
        return ret
    return t.get_score(None, board, None, None) + (possibility_b - possibility_w) * params[0]


def evaluate_tpwe(t, table, params, color, board, possibility_b, possibility_w):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _evaluate_tpwe_size8_64bit(table, params, color, board, possibility_b, possibility_w)
    return _evaluate_tpwe(t, params, color, board, possibility_b, possibility_w)


cdef inline signed int _evaluate_tpwe_size8_64bit(table, params, color, board, possibility_b, possibility_w):
    cdef:
        unsigned long long t_mask = 0x8000000000000000, b_bitboard, w_bitboard, all_bitboard, bit_pos, lt, rt, lb, rb, b_t, w_t, b_b, w_b, b_l, w_l, b_r, w_r
        unsigned int i, x, y
        signed int wp = params[0], ww = params[1], we = params[2], score_w = 0, score_t = 0, score_p = 0, score_e = 0, lt_sign, lb_sign, rt_sign, rb_sign
    b_bitboard, w_bitboard, h_bitboard = board.get_bitboard_info()
    # 勝敗が決まっている場合
    if not possibility_b and not possibility_w:
        score_w = board._black_score - board._white_score
        if score_w > 0:    # 黒が勝った
            score_w += ww
        elif score_w < 0:  # 白が勝った
            score_w -= ww
        return score_w
    # テーブルによるスコア
    for y in range(8):
        for x in range(8):
            if b_bitboard & t_mask:
                score_t += <signed int>table[y][x]
            elif w_bitboard & t_mask:
                score_t -= <signed int>table[y][x]
            t_mask >>= 1
    # 着手可能数によるスコア
    score_p = (possibility_b - possibility_w) * wp
    # 辺のパターンによるスコア
    all_bitboard = b_bitboard | w_bitboard
    bit_pos = <unsigned long long>0x8000000000000000
    lt = <unsigned long long>0x8000000000000000
    rt = <unsigned long long>0x0100000000000000
    lb = <unsigned long long>0x0000000000000080
    rb = <unsigned long long>0x0000000000000001
    # 四隅のどこかに石がある場合
    if (lt | rt | lb | rb) & all_bitboard:
        # 上辺
        b_t, w_t = 0, 0
        if (lt | rt) & all_bitboard:
            b_t = (<unsigned long long>0xFF00000000000000 & b_bitboard) >> 56
            w_t = (<unsigned long long>0xFF00000000000000 & w_bitboard) >> 56
        # 下辺
        b_b = <unsigned long long>0x00000000000000FF & b_bitboard
        w_b = <unsigned long long>0x00000000000000FF & w_bitboard
        # 左辺
        b_l, w_l = 0, 0
        if (lt | lb) & b_bitboard:
            if b_bitboard & <unsigned long long>0x8000000000000000:
                b_l += <unsigned long long>0x0000000000000080
            if b_bitboard & <unsigned long long>0x0080000000000000:
                b_l += <unsigned long long>0x0000000000000040
            if b_bitboard & <unsigned long long>0x0000800000000000:
                b_l += <unsigned long long>0x0000000000000020
            if b_bitboard & <unsigned long long>0x0000008000000000:
                b_l += <unsigned long long>0x0000000000000010
            if b_bitboard & <unsigned long long>0x0000000080000000:
                b_l += <unsigned long long>0x0000000000000008
            if b_bitboard & <unsigned long long>0x0000000000800000:
                b_l += <unsigned long long>0x0000000000000004
            if b_bitboard & <unsigned long long>0x0000000000008000:
                b_l += <unsigned long long>0x0000000000000002
            if b_bitboard & <unsigned long long>0x0000000000000080:
                b_l += <unsigned long long>0x0000000000000001
        if (lt | lb) & w_bitboard:
            if w_bitboard & <unsigned long long>0x8000000000000000:
                w_l += <unsigned long long>0x0000000000000080
            if w_bitboard & <unsigned long long>0x0080000000000000:
                w_l += <unsigned long long>0x0000000000000040
            if w_bitboard & <unsigned long long>0x0000800000000000:
                w_l += <unsigned long long>0x0000000000000020
            if w_bitboard & <unsigned long long>0x0000008000000000:
                w_l += <unsigned long long>0x0000000000000010
            if w_bitboard & <unsigned long long>0x0000000080000000:
                w_l += <unsigned long long>0x0000000000000008
            if w_bitboard & <unsigned long long>0x0000000000800000:
                w_l += <unsigned long long>0x0000000000000004
            if w_bitboard & <unsigned long long>0x0000000000008000:
                w_l += <unsigned long long>0x0000000000000002
            if w_bitboard & <unsigned long long>0x0000000000000080:
                w_l += <unsigned long long>0x0000000000000001
        # 右辺
        b_r, w_r = 0, 0
        if (rt | rb) & b_bitboard:
            if b_bitboard & <unsigned long long>0x0100000000000000:
                b_r += <unsigned long long>0x0000000000000080
            if b_bitboard & <unsigned long long>0x0001000000000000:
                b_r += <unsigned long long>0x0000000000000040
            if b_bitboard & <unsigned long long>0x0000010000000000:
                b_r += <unsigned long long>0x0000000000000020
            if b_bitboard & <unsigned long long>0x0000000100000000:
                b_r += <unsigned long long>0x0000000000000010
            if b_bitboard & <unsigned long long>0x0000000001000000:
                b_r += <unsigned long long>0x0000000000000008
            if b_bitboard & <unsigned long long>0x0000000000010000:
                b_r += <unsigned long long>0x0000000000000004
            if b_bitboard & <unsigned long long>0x0000000000000100:
                b_r += <unsigned long long>0x0000000000000002
            if b_bitboard & <unsigned long long>0x0000000000000001:
                b_r += <unsigned long long>0x0000000000000001
        if (rt | rb) & w_bitboard:
            if w_bitboard & <unsigned long long>0x0100000000000000:
                w_r += <unsigned long long>0x0000000000000080
            if w_bitboard & <unsigned long long>0x0001000000000000:
                w_r += <unsigned long long>0x0000000000000040
            if w_bitboard & <unsigned long long>0x0000010000000000:
                w_r += <unsigned long long>0x0000000000000020
            if w_bitboard & <unsigned long long>0x0000000100000000:
                w_r += <unsigned long long>0x0000000000000010
            if w_bitboard & <unsigned long long>0x0000000001000000:
                w_r += <unsigned long long>0x0000000000000008
            if w_bitboard & <unsigned long long>0x0000000000010000:
                w_r += <unsigned long long>0x0000000000000004
            if w_bitboard & <unsigned long long>0x0000000000000100:
                w_r += <unsigned long long>0x0000000000000002
            if w_bitboard & <unsigned long long>0x0000000000000001:
                w_r += <unsigned long long>0x0000000000000001
        score_e = ((edge_table8[b_t] - edge_table8[w_t]) + (edge_table8[b_b] - edge_table8[w_b]) + (edge_table8[b_l] - edge_table8[w_l]) + (edge_table8[b_r] - edge_table8[w_r])) * we
    return score_t + score_p + score_e


cdef inline signed int _evaluate_tpwe(t, params, color, board, possibility_b, possibility_w):
    cdef:
        unsigned int i
        signed int wp = params[0], ww = params[1], we = params[2], score_w = 0, score_t = 0, score_p = 0, score_e = 0, lt_sign, lb_sign, rt_sign, rb_sign
    # 勝敗が決まっている場合
    if not possibility_b and not possibility_w:
        score_w = board._black_score - board._white_score
        if score_w > 0:    # 黒が勝った
            score_w += ww
        elif score_w < 0:  # 白が勝った
            score_w -= ww
        return score_w
    score_t = t.get_score(None, board, None, None)  # テーブルによるスコア
    score_p = (possibility_b - possibility_w) * wp  # 着手可能数によるスコア
    # 辺のパターンによるスコア
    size = board.size
    b_bitboard, w_bitboard, h_bitboard = board.get_bitboard_info()
    all_bitboard = b_bitboard | w_bitboard
    bit_pos = 1 << (size * size - 1)
    lt = bit_pos
    rt = bit_pos >> size-1
    lb = bit_pos >> size*(size-1)
    rb = bit_pos >> size*size-1
    # 四隅のどこかに石がある場合
    if (lt | rt | lb | rb) & all_bitboard:
        # 左上
        lt_board = b_bitboard
        lt_sign = 1
        if lt & w_bitboard:
            lt_board = w_bitboard
            lt_sign = -1
        lt_r, lt_b = lt & lt_board, lt & lt_board
        # 右上
        rt_board = b_bitboard
        rt_sign = 1
        if rt & w_bitboard:
            rt_board = w_bitboard
            rt_sign = -1
        rt_l, rt_b = rt & rt_board, rt & rt_board
        # 左下
        lb_board = b_bitboard
        lb_sign = 1
        if lb & w_bitboard:
            lb_board = w_bitboard
            lb_sign = -1
        lb_r, lb_t = lb & lb_board, lb & lb_board
        # 右下
        rb_board = b_bitboard
        rb_sign = 1
        if rb & w_bitboard:
            rb_board = w_bitboard
            rb_sign = -1
        rb_l, rb_t = rb & rb_board, rb & rb_board
        # 確定石の連続数(2個～7個まで)をカウント
        for i in range(<unsigned int>(size-2)):
            # 左上:右方向
            lt_r >>= 1
            lt_r &= lt_board
            if lt_r & lt_board:
                score_e += we * lt_sign
            # 左上:下方向
            lt_b >>= size
            lt_b &= lt_board
            if lt_b & lt_board:
                score_e += we * lt_sign
            # 右上:左方向
            rt_l <<= 1
            rt_l &= rt_board
            if rt_l & rt_board:
                score_e += we * rt_sign
            # 右上:下方向
            rt_b >>= size
            rt_b &= rt_board
            if rt_b & rt_board:
                score_e += we * rt_sign
            # 左下:右方向
            lb_r >>= 1
            lb_r &= lb_board
            if lb_r & lb_board:
                score_e += we * lb_sign
            # 左下:上方向
            lb_t <<= size
            lb_t &= lb_board
            if lb_t & lb_board:
                score_e += we * lb_sign
            # 右下:左方向
            rb_l <<= 1
            rb_l &= rb_board
            if rb_l & rb_board:
                score_e += we * rb_sign
            # 右下:上方向
            rb_t <<= size
            rb_t &= rb_board
            if rb_t & rb_board:
                score_e += we * rb_sign
        # 辺が同じ色で埋まっている場合はさらに加算
        top = int(''.join(['1'] * size + ['0'] * (size*(size-1))), 2)
        if lt_board & top == top:
            score_e += we * lt_sign
        left = int(''.join((['1'] + ['0'] * (size-1)) * size), 2)
        if lt_board & left == left:
            score_e += we * lt_sign
        right = int(''.join((['0'] * (size-1) + ['1']) * size), 2)
        if rb_board & right == right:
            score_e += we * rb_sign
        bottom = int(''.join(['0'] * (size*(size-1)) + ['1'] * size), 2)
        if rb_board & bottom == bottom:
            score_e += we * rb_sign
    return score_t + score_p + score_e


# =========================================== #
# ScorerMethods
def get_blank_score(board, w1, w2, w3):
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        return _get_blank_score_size8_64bit(board, w1, w2, w3)
    return _get_blank_score(board, w1, w2, w3)


cdef inline signed int _get_blank_score_size8_64bit(board, signed int w1, signed int w2, signed int w3):
    cdef:
        unsigned long long black, white, hole, blackwhite, not_blackwhite, horizontal, vertical, diagonal, l_blank, r_blank, t_blank, b_blank, lt_blank, rt_blank, lb_blank, rb_blank, lt_x, rt_x, lb_x, rb_x, lt_r, lt_b, rt_l, rt_b, lb_t, lb_r, rb_t, rb_l
        signed int score = 0, lt_r_sign = 1, lt_b_sign = 1, rt_l_sign = 1, rt_b_sign = 1, lb_t_sign = 1, lb_r_sign = 1, rb_t_sign = 1, rb_l_sign = 1
    black, white, hole = board.get_bitboard_info()
    blackwhite = (black | white) & ~hole
    horizontal = blackwhite & <unsigned long long>0x7E7E7E7E7E7E7E7E  # 左右チェック用マスク
    vertical = blackwhite & <unsigned long long>0x00FFFFFFFFFFFF00    # 上下チェック用マスク
    diagonal = blackwhite & <unsigned long long>0x007E7E7E7E7E7E00    # 斜めチェック用マスク
    not_blackwhite = ~blackwhite
    # 左方向に空がある(右方向が盤面の範囲内)
    l_blank = horizontal & ((horizontal << 1) & not_blackwhite) >> 1
    # 右方向に空がある(左方向が盤面の範囲内)
    r_blank = horizontal & ((horizontal >> 1) & not_blackwhite) << 1
    # 上方向に空がある(下方向が盤面の範囲内)
    t_blank = vertical & ((vertical << 8) & not_blackwhite) >> 8
    # 下方向に空がある(上方向が盤面の範囲内)
    b_blank = vertical & ((vertical >> 8) & not_blackwhite) << 8
    # 左上方向に空がある(右下方向が盤面の範囲内)
    lt_blank = diagonal & ((diagonal << 9) & not_blackwhite) >> 9
    # 右上方向に空がある(左下方向が盤面の範囲内)
    rt_blank = diagonal & ((diagonal << 7) & not_blackwhite) >> 7
    # 左下方向に空がある(右上方向が盤面の範囲内)
    lb_blank = diagonal & ((diagonal >> 7) & not_blackwhite) << 7
    # 右下方向に空がある(左上方向が盤面の範囲内)
    rb_blank = diagonal & ((diagonal >> 9) & not_blackwhite) << 9
    # w1の計算
    score += w1 * (<signed int>_popcount(l_blank & black) - <signed int>_popcount(l_blank & white))
    score += w1 * (<signed int>_popcount(r_blank & black) - <signed int>_popcount(r_blank & white))
    score += w1 * (<signed int>_popcount(t_blank & black) - <signed int>_popcount(t_blank & white))
    score += w1 * (<signed int>_popcount(b_blank & black) - <signed int>_popcount(b_blank & white))
    score += w1 * (<signed int>_popcount(lt_blank & black) - <signed int>_popcount(lt_blank & white))
    score += w1 * (<signed int>_popcount(rt_blank & black) - <signed int>_popcount(rt_blank & white))
    score += w1 * (<signed int>_popcount(lb_blank & black) - <signed int>_popcount(lb_blank & white))
    score += w1 * (<signed int>_popcount(rb_blank & black) - <signed int>_popcount(rb_blank & white))
    # w2の計算
    lt_x = lt_blank & <unsigned long long>0x0040000000000000  # 左上のX打ち
    if lt_x:
        if lt_x & black:
            score += w2
        else:
            score -= w2
    rt_x = rt_blank & <unsigned long long>0x0002000000000000  # 右上のX打ち
    if rt_x:
        if rt_x & black:
            score += w2
        else:
            score -= w2
    lb_x = lb_blank & <unsigned long long>0x0000000000004000  # 左下のX打ち
    if lb_x:
        if lb_x & black:
            score += w2
        else:
            score -= w2
    rb_x = rb_blank & <unsigned long long>0x0000000000000200  # 右下のX打ち
    if rb_x:
        if rb_x & black:
            score += w2
        else:
            score -= w2
    # w3の計算
    lt_r = l_blank & <unsigned long long>0x4000000000000000
    lt_b = t_blank & <unsigned long long>0x0080000000000000
    rt_l = r_blank & <unsigned long long>0x0200000000000000
    rt_b = t_blank & <unsigned long long>0x0001000000000000
    lb_t = b_blank & <unsigned long long>0x0000000000008000
    lb_r = l_blank & <unsigned long long>0x0000000000000040
    rb_t = b_blank & <unsigned long long>0x0000000000000100
    rb_l = r_blank & <unsigned long long>0x0000000000000002
    if lt_r & white:
        lt_r_sign = -1
    if lt_b & white:
        lt_b_sign = -1
    if rt_l & white:
        rt_l_sign = -1
    if rt_b & white:
        rt_b_sign = -1
    if lb_t & white:
        lb_t_sign = -1
    if lb_r & white:
        lb_r_sign = -1
    if rb_t & white:
        rb_t_sign = -1
    if rb_l & white:
        rb_l_sign = -1
    for i in range(1, 5):
        lt_r >>= 1
        if lt_r & not_blackwhite:
            score += w3 * lt_r_sign
        lt_b >>= 8
        if lt_b & not_blackwhite:
            score += w3 * lt_b_sign
        rt_l <<= 1
        if rt_l & not_blackwhite:
            score += w3 * rt_l_sign
        rt_b >>= 8
        if rt_b & not_blackwhite:
            score += w3 * rt_b_sign
        lb_t <<= 8
        if lb_t & not_blackwhite:
            score += w3 * lb_t_sign
        lb_r >>= 1
        if lb_r & not_blackwhite:
            score += w3 * lb_r_sign
        rb_t <<= 8
        if rb_t & not_blackwhite:
            score += w3 * rb_t_sign
        rb_l <<= 1
        if rb_l & not_blackwhite:
            score += w3 * rb_l_sign
    return score


cdef inline signed int _get_blank_score(board, signed int w1, signed int w2, signed int w3):
    cdef:
        signed int[26][26] board_info
        signed int i, x, y, value, j, dx, dy, next_x1, next_y1, next_x2, next_y2, d, dx_abs, dy_abs, k, next_x3, next_y3, score = 0, size = board.size
        signed int size_x_size = size * size
    board_info_tmp = board.get_board_info()
    for y in range(size):
        for x in range(size):
            board_info[x][y] = board_info_tmp[x][y]
    for y in range(size):
        for x in range(size):
            i = y * size + x
            # 自分または相手の石が存在する
            if board_info[x][y]:
                value = 0
                for j in range(8):
                    dx, dy = directions_x[j], directions_y[j]
                    next_x1, next_y1 = x + dx, y + dy
                    next_x2, next_y2 = x - dx, y - dy
                    if 0 <= next_x1 < size and 0 <= next_y1 < size and 0 <= next_x2 < size and 0 <= next_y2 < size:
                        # 空きマスに面している(ただし反対側が盤面の範囲内)
                        if not board_info[next_x1][next_y1]:
                            value += w1
                            # 隅に接している場合
                            d = dy * size + dx
                            if i+d == 0 or i+d == size-1 or i+d == size_x_size-8 or i+d == size_x_size-1:
                                if abs(dx) + abs(dy) == 2:
                                    value += w2  # X打ち(チェック方向が斜め)の場合
                                else:
                                    for k in range(1, 5):
                                        next_x3, next_y3 = x - k * dx, y - k * dy
                                        if not board_info[next_x3][next_y3]:
                                            value += w3  # 隅の反対の縦横方向に空きマスがある場合
                score += value * board_info[x][y]
    return score


# =========================================== #
# BitBoardMethods
def get_legal_moves(color, size, b, w, h, mask):
    if size == 8 and sys.maxsize == MAXSIZE64:
        return _get_legal_moves_size8_64bit(color, b, w, h)
    return _get_legal_moves(color, size, b, w, h, mask)


def get_legal_moves_bits(color, size, b, w, h, mask):
    if size == 8 and sys.maxsize == MAXSIZE64:
        return _get_legal_moves_bits(color == 'black', b, w, h)
    return _get_legal_moves_bits_sizable(color, size, b, w, h, mask)


def get_bit_count(size, bits):
    if size == 8 and sys.maxsize == MAXSIZE64:
        return _popcount(bits)
    return _get_bit_count(size, bits)


def get_flippable_discs(color, size, black_bitboard, white_bitboard, x, y, mask):
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_flippable_discs_size8_64bit(color == 'black', black_bitboard, white_bitboard, x, y)
        return _get_flippable_discs_size8(color, black_bitboard, white_bitboard, x, y)
    return _get_flippable_discs_sizable(color, size, black_bitboard, white_bitboard, x, y, mask)


def put_disc(board, color, x, y):
    size = board.size
    if size == 8 and sys.maxsize == MAXSIZE64:
        return _put_disc_board_size8_64bit(board, color == 'black', x, y)
    return _put_disc_board_sizable(size, board, color, x, y)


def get_board_info(size, b, w):
    if size == 8:
        if sys.maxsize == MAXSIZE64:
            return _get_board_info_size8_64bit(b, w)
        return _get_board_info_size8(b, w)
    return _get_board_info_sizable(size, b, w)


def undo(board):
    _undo_board(board)


cdef inline _get_legal_moves_size8_64bit(str color, unsigned long long b, unsigned long long w, unsigned long long h):
    cdef:
        unsigned long long legal_moves, mask = 0x8000000000000000
        unsigned int x, y
    legal_moves = _get_legal_moves_bits(color == 'black', b, w, h)
    ret = []
    for y in range(8):
        for x in range(8):
            if legal_moves & mask:
                ret += [(x, y)]
            mask >>= 1
    return ret


cdef _get_legal_moves(color, size, b, w, h, mask):
    legal_moves_bits = _get_legal_moves_bits_sizable(color, size, b, w, h, mask)
    # 石が置ける場所を格納
    ret = []
    check = 1 << (size * size - 1)
    for y in range(size):
        for x in range(size):
            # 石が置ける場合
            if legal_moves_bits & check:
                ret += [(x, y)]
            check >>= 1
    return ret


cdef _get_legal_moves_bits_sizable(color, size, b, w, h, mask):
    # 前準備
    player, opponent = (b, w) if color == 'black' else (w, b)  # プレイヤーと相手を決定
    legal_moves_bits = 0                                       # 石が置ける場所
    horizontal = opponent & mask.h                             # 水平方向のチェック値
    vertical = opponent & mask.v                               # 垂直方向のチェック値
    diagonal = opponent & mask.d                               # 斜め方向のチェック値
    blank = ~(player | opponent | h)                           # 空きマス位置
    # 置ける場所を探す
    legal_moves_bits |= _get_legal_moves_lshift(size, horizontal, player, blank, 1)     # 左方向
    legal_moves_bits |= _get_legal_moves_rshift(size, horizontal, player, blank, 1)     # 右方向
    legal_moves_bits |= _get_legal_moves_lshift(size, vertical, player, blank, size)    # 上方向
    legal_moves_bits |= _get_legal_moves_rshift(size, vertical, player, blank, size)    # 下方向
    legal_moves_bits |= _get_legal_moves_lshift(size, diagonal, player, blank, size+1)  # 左斜め上方向
    legal_moves_bits |= _get_legal_moves_lshift(size, diagonal, player, blank, size-1)  # 右斜め上方向
    legal_moves_bits |= _get_legal_moves_rshift(size, diagonal, player, blank, size-1)  # 左斜め下方向
    legal_moves_bits |= _get_legal_moves_rshift(size, diagonal, player, blank, size+1)  # 右斜め下方向
    return legal_moves_bits


cdef _get_legal_moves_lshift(size, mask, player, blank, shift_size):
    """左シフトで石が置ける場所を取得"""
    tmp = mask & (player << shift_size)
    for _ in range(size-3):
        tmp |= mask & (tmp << shift_size)
    return blank & (tmp << shift_size)


cdef _get_legal_moves_rshift(size, mask, player, blank, shift_size):
    """右シフトで石が置ける場所を取得"""
    tmp = mask & (player >> shift_size)
    for _ in range(size-3):
        tmp |= mask & (tmp >> shift_size)
    return blank & (tmp >> shift_size)


cdef _get_bit_count(size, bits):
    count = 0
    mask = 1 << ((size**2)-1)
    for y in range(size):
        for x in range(size):
            if bits & mask:
                count += 1
            mask >>= 1
    return count


cdef inline _get_flippable_discs_size8_64bit(unsigned int color, unsigned long long black_bitboard, unsigned long long white_bitboard, unsigned int x, unsigned int y):
    cdef:
        unsigned long long move = <unsigned long long>1 << (63-(y*8+x)), flippable_discs = 0, mask = 0x8000000000000000
    ret = []
    flippable_discs = _get_flippable_discs_num(color, black_bitboard, white_bitboard, move)
    for y in range(8):
        for x in range(8):
            if flippable_discs & mask:
                ret += [(x, y)]
            mask >>= 1
    return ret


cdef _get_flippable_discs_size8(color, black_bitboard, white_bitboard, unsigned int x, unsigned int y):
    player, opponent = (black_bitboard, white_bitboard) if color == 'black' else (white_bitboard, black_bitboard)
    player |= 0x10000000000000000    # 32bit以下でもシフトできるよう対策
    opponent |= 0x10000000000000000
    cdef:
        unsigned int p0 = (player >> 32) & 0xFFFFFFFF    # プレイヤー石(上位)
        unsigned int p1 = player & 0xFFFFFFFF            # プレイヤー石(下位)
        unsigned int o0 = (opponent >> 32) & 0xFFFFFFFF  # 相手石(上位)
        unsigned int o1 = opponent & 0xFFFFFFFF          # 相手石(上位)
        unsigned int put0 = 0                            # 石を置く場所(上位)
        unsigned int put1 = 0                            # 石を置く場所(下位)
        unsigned int flippable_discs0 = 0                # ひっくり返せる場所(上位)
        unsigned int flippable_discs1 = 0                # ひっくり返せる場所(下位)
        unsigned int direction, next0, next1, buff0, buff1, mask0 = 0x80000000, mask1 = 0x80000000
    # 石を置く場所
    if y < 4:
        put0 = 1 << (31-(y*8+x))
    else:
        put1 = 1 << (31-((y-4)*8+x))
    # 8方向を順番にチェック
    for direction in range(8):
        buff0, buff1 = 0, 0
        next0, next1 = _get_next_put_size8(put0, put1, direction)
        # 相手の石が存在する限り位置を記憶
        while (next0 & o0) or (next1 & o1):
            buff0 |= next0
            buff1 |= next1
            next0, next1 = _get_next_put_size8(next0, next1, direction)
        # 自分の石で囲まれている場合は結果を格納する
        if (next0 & p0) or (next1 & p1):
            flippable_discs0 |= buff0
            flippable_discs1 |= buff1
    # 配列に変換
    ret = []
    for y in range(8):
        # ビットボード上位32bit
        if y < 4:
            for x in range(8):
                if flippable_discs0 & mask0:
                    ret += [(x, y)]
                mask0 >>= 1
        # ビットボード下位32bit
        else:
            for x in range(8):
                if flippable_discs1 & mask1:
                    ret += [(x, y)]
                mask1 >>= 1
    return ret


cdef _get_next_put_size8(unsigned int put0, unsigned int put1, unsigned int direction):
    """指定位置から指定方向に1マス分移動した場所を返す(ボードサイズ8限定)
    """
    cdef:
        unsigned int upper, lower
    if direction == 0:     # 上
        upper = 0xFFFFFFFF & ((put0 << 8) | (put1 >> 24))
        lower = 0xFFFFFF00 & (put1 << 8)
    elif direction == 1:  # 右上
        upper = 0x7F7F7F7F & ((put0 << 7) | (put1 >> 25))
        lower = 0x7F7F7F00 & (put1 << 7)
    elif direction == 2:   # 右
        upper = 0x7F7F7F7F & (put0 >> 1)
        lower = 0x7F7F7F7F & (put1 >> 1)
    elif direction == 3:  # 右下
        upper = 0x007F7F7F & (put0 >> 9)
        lower = 0x7F7F7F7F & ((put1 >> 9) | (put0 << 23))
    elif direction == 4:   # 下
        upper = 0x00FFFFFF & (put0 >> 8)
        lower = 0xFFFFFFFF & ((put1 >> 8) | (put0 << 24))
    elif direction == 5:  # 左下
        upper = 0x00FEFEFE & (put0 >> 7)
        lower = 0xFEFEFEFE & ((put1 >> 7) | (put0 << 25))
    elif direction == 6:   # 左
        upper = 0xFEFEFEFE & (put0 << 1)
        lower = 0xFEFEFEFE & (put1 << 1)
    elif direction == 7:  # 左上
        upper = 0xFEFEFEFE & ((put0 << 9) | (put1 >> 23))
        lower = 0xFEFEFE00 & (put1 << 9)
    else:
        upper, lower = 0, 0
    return upper, lower


cdef _get_flippable_discs_sizable(color, size, black_bitboard, white_bitboard, x, y, mask):
    ret = []
    flippable_discs = 0
    player, opponent = (black_bitboard, white_bitboard) if color == 'black' else (white_bitboard, black_bitboard)
    # 石を置く場所
    put = 1 << ((size*size-1)-(y*size+x))
    # 8方向を順番にチェック
    for direction in ('U', 'UR', 'R', 'BR', 'B', 'BL', 'L', 'UL'):
        tmp = 0
        check = _get_next_put(size, put, direction, mask)
        # 相手の石が存在する限り位置を記憶
        while check & opponent:
            tmp |= check
            check = _get_next_put(size, check, direction, mask)
        # 自分の石で囲まれている場合は結果を格納する
        if check & player:
            flippable_discs |= tmp
    # 配列に変換
    check = 1 << (size*size-1)
    for y in range(size):
        for x in range(size):
            if flippable_discs & check:
                ret += [(x, y)]
            check >>= 1
    return ret


cdef _get_next_put(size, put, direction, mask):
    """指定位置から指定方向に1マス分移動した場所を返す(ボードサイズ8以外)"""
    if direction == 'U':     # 上
        return (put << size) & mask.u
    elif direction == 'UR':  # 右上
        return (put << (size-1)) & mask.ur
    elif direction == 'R':   # 右
        return (put >> 1) & mask.r
    elif direction == 'BR':  # 右下
        return (put >> (size+1)) & mask.br
    elif direction == 'B':   # 下
        return (put >> size) & mask.b
    elif direction == 'BL':  # 左下
        return (put >> (size-1)) & mask.bl
    elif direction == 'L':   # 左
        return (put << 1) & mask.l
    elif direction == 'UL':  # 左上
        return (put << (size+1)) & mask.ul
    else:
        return 0


cdef inline _put_disc_board_sizable(size, board, color, unsigned int x, unsigned int y):
    cdef:
        unsigned int tmp_x, tmp_y
    # 配置位置を整数に変換
    shift_size = ((size*size-1)-(y*size+x))
    if shift_size < 0 or shift_size > size**2-1:
        return 0
    put = 1 << ((size*size-1)-(y*size+x))
    # 反転位置を整数に変換
    flippable_discs = board.get_flippable_discs(color, x, y)
    flippable_discs_num = 0
    for tmp_x, tmp_y in flippable_discs:
        flippable_discs_num |= 1 << ((size*size-1)-(tmp_y*size+tmp_x))
    # 打つ前の状態を格納
    board.prev += [(board._black_bitboard, board._white_bitboard, board._black_score, board._white_score)]
    # 自分の石を置いて相手の石をひっくり返す
    if color == 'black':
        board._black_bitboard ^= put | flippable_discs_num
        board._white_bitboard ^= flippable_discs_num
        board._black_score += 1 + len(flippable_discs)
        board._white_score -= len(flippable_discs)
    else:
        board._white_bitboard ^= put | flippable_discs_num
        board._black_bitboard ^= flippable_discs_num
        board._black_score -= len(flippable_discs)
        board._white_score += 1 + len(flippable_discs)
    board._flippable_discs_num = flippable_discs_num
    return flippable_discs_num


cdef inline _get_board_info_size8_64bit(unsigned long long b, unsigned long long w):
    cdef:
        unsigned long long mask = 0x8000000000000000
        unsigned int x, y
        signed int[8][8] board_info
    for y in range(8):
        for x in range(8):
            if b & mask:
                board_info[y][x] = 1
            elif w & mask:
                board_info[y][x] = -1
            else:
                board_info[y][x] = 0
            mask >>= 1
    return board_info


cdef _get_board_info_size8(b, w):
    cdef:
        unsigned int x, y, b0 = ((0x10000000000000000 | b) >> 32) & 0xFFFFFFFF, b1 = b & 0xFFFFFFFF, w0 = ((0x10000000000000000 | w) >> 32) & 0xFFFFFFFF, w1 = w & 0x00000000FFFFFFFF, mask0 = 0x80000000, mask1 = 0x80000000
    board_info = []
    for y in range(8):
        tmp = []
        # ビットボード上位32bit
        if y < 4:
            for x in range(8):
                if b0 & mask0:
                    tmp += [1]
                elif w0 & mask0:
                    tmp += [-1]
                else:
                    tmp += [0]
                mask0 >>= 1
        # ビットボード下位32bit
        else:
            for x in range(8):
                if b1 & mask1:
                    tmp += [1]
                elif w1 & mask1:
                    tmp += [-1]
                else:
                    tmp += [0]
                mask1 >>= 1
        board_info += [tmp]
    return board_info


cdef _get_board_info_sizable(size, b, w):
    board_info = []
    mask = 1 << (size * size - 1)
    for y in range(size):
        tmp = []
        for x in range(size):
            if b & mask:
                tmp += [1]
            elif w & mask:
                tmp += [-1]
            else:
                tmp += [0]
            mask >>= 1
        board_info += [tmp]
    return board_info


cdef class CythonBitBoard():
    cdef readonly size
    cdef public _black_score, _white_score, prev, _green_bitboard, _black_bitboard, _white_bitboard, _hole_bitboard, _ini_green, _ini_black, _ini_white, _mask, _flippable_discs_num

    def __init__(self, hole=0x0, ini_black=None, ini_white=None):
        self.size = 8
        self.prev = []
        self._green_bitboard = 0
        self._black_bitboard = 0
        self._white_bitboard = 0
        # 初期配置
        size = self.size
        center = size // 2
        self._ini_black = 1 << ((size*size-1)-(size*(center-1)+center))
        self._ini_black |= 1 << ((size*size-1)-(size*center+(center-1)))
        self._ini_white = 1 << ((size*size-1)-(size*(center-1)+(center-1)))
        self._ini_white |= 1 << ((size*size-1)-(size*center+center))
        if ini_black is not None:
            self._ini_black = ini_black
        if ini_white is not None:
            self._ini_white = ini_white
        self._ini_green = self._ini_black & self._ini_white
        self._ini_black &= ~self._ini_green
        self._ini_white &= ~self._ini_green
        self._green_bitboard |= self._ini_green
        self._black_bitboard |= self._ini_black
        self._white_bitboard |= self._ini_white
        self._hole_bitboard = hole
        # 置ける場所の検出用マスク
        BitMask = namedtuple('BitMask', 'h v d u ur r br b bl l ul')
        self._mask = BitMask(
            int(''.join((['0'] + ['1'] * (size-2) + ['0']) * size), 2),                                      # 水平方向のマスク値
            int(''.join(['0'] * size + ['1'] * size * (size-2) + ['0'] * size), 2),                          # 垂直方向のマスク値
            int(''.join(['0'] * size + (['0'] + (['1'] * (size-2)) + ['0']) * (size-2) + ['0'] * size), 2),  # 斜め方向のマスク値
            int(''.join(['1'] * size * (size-1) + ['0'] * size), 2),                                         # 上方向のマスク値
            int(''.join((['0'] + ['1'] * (size-1)) * (size-1) + ['0'] * size), 2),                           # 右上方向のマスク値
            int(''.join((['0'] + ['1'] * (size-1)) * size), 2),                                              # 右方向のマスク値
            int(''.join(['0'] * size + (['0'] + ['1'] * (size-1)) * (size-1)), 2),                           # 右下方向のマスク値
            int(''.join(['0'] * size + ['1'] * size * (size-1)), 2),                                         # 下方向のマスク値
            int(''.join(['0'] * size + (['1'] * (size-1) + ['0']) * (size-1)), 2),                           # 左下方向のマスク値
            int(''.join((['1'] * (size-1) + ['0']) * size), 2),                                              # 左方向のマスク値
            int(''.join((['1'] * (size-1) + ['0']) * (size-1) + ['0'] * size), 2)                            # 左上方向のマスク値
        )
        # 穴をあける
        self._green_bitboard &= ~self._hole_bitboard
        self._black_bitboard &= ~self._hole_bitboard
        self._white_bitboard &= ~self._hole_bitboard
        self.update_score()

    def _is_invalid_size(self, size):
        return not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0)

    def __str__(self):
        header = '   ' + ' '.join([chr(97 + i) for i in range(8)]) + '\n'
        board = [['□' for _ in range(8)] for _ in range(8)]
        mask = 1 << 63
        for y in range(8):
            for x in range(8):
                if self._hole_bitboard & mask:
                    board[y][x] = '　'
                elif self._black_bitboard & mask:
                    board[y][x] = '〇'
                elif self._white_bitboard & mask:
                    board[y][x] = '●'
                elif self._green_bitboard & mask:
                    board[y][x] = '◎'
                mask >>= 1
        body = ''
        for num, row in enumerate(board, 1):
            body += f'{num:2d}' + ''.join([value for value in row]) + '\n'
        return header + body

    def get_legal_moves(self, str color):
        return _get_legal_moves_size8_64bit(color, self._black_bitboard, self._white_bitboard, self._hole_bitboard)

    def get_legal_moves_bits(self, str color):
        return _get_legal_moves_bits(color == 'black', self._black_bitboard, self._white_bitboard, self._hole_bitboard)

    def get_flippable_discs(self, str color, x, y):
        return _get_flippable_discs_size8_64bit(color == 'black', self._black_bitboard, self._white_bitboard, x, y)

    def put_disc(self, str color, x, y):
        return _put_disc_board_size8_64bit(self, color == 'black', x, y)

    def update_score(self):
        self._black_score, self._white_score = 0, 0
        mask = 1 << 63
        for y in range(8):
            for x in range(8):
                if self._black_bitboard & mask:
                    self._black_score += 1
                elif self._white_bitboard & mask:
                    self._white_score += 1
                mask >>= 1

    def get_board_info(self):
        return _get_board_info_size8_64bit(self._black_bitboard, self._white_bitboard)

    def get_board_line_info(self, player, black='*', white='O', hole='_', empty='-'):
        board_line_info = ''
        # board
        size = self.size
        mask = 1 << (size * size - 1)
        for y in range(size):
            for x in range(size):
                if self._black_bitboard & mask:
                    board_line_info += black
                elif self._white_bitboard & mask:
                    board_line_info += white
                elif self._hole_bitboard & mask:
                    board_line_info += hole
                else:
                    board_line_info += empty
                mask >>= 1
        # player
        if player == 'black':
            board_line_info += black
        elif player == 'white':
            board_line_info += white
        else:
            board_line_info += empty
        return board_line_info

    def get_bit_count(self, bits):
        return _popcount(bits)

    def get_bitboard_info(self):
        return self._black_bitboard, self._white_bitboard, self._hole_bitboard

    def undo(self):
        (self._black_bitboard, self._white_bitboard, self._black_score, self._white_score) = self.prev.pop()

    def get_remain(self):
        size = self.size
        mask = 1 << (size * size - 1)
        remain = size * size
        hole = self._hole_bitboard
        green = self._green_bitboard
        black = self._black_bitboard
        white = self._white_bitboard
        not_blank = hole | green | black | white
        return remain - self.get_bit_count(not_blank)
