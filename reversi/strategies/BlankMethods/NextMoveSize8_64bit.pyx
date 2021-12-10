#cython: language_level=3, profile=True, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""Next Move(Size8,64bit) of Blank strategy
"""

import time

from reversi.strategies.common import Timer, Measure


DEF MAX_POSSIBILITY = 40  # 着手可能数の最大(想定)
DEF POSSIBILITY_RANGE = MAX_POSSIBILITY * 2 + 1
DEF BUCKET_SIZE = MAX_POSSIBILITY
cdef:
    unsigned long long measure_count
    unsigned long long bb
    unsigned long long wb
    unsigned long long fd
    unsigned long long[64] pbb
    unsigned long long[64] pwb
    unsigned int bs
    unsigned int ws
    unsigned int[64] pbs
    unsigned int[64] pws
    unsigned int tail
    double timer_deadline
    unsigned int timer_timeout
    signed int timer_timeout_value
    signed int corner, c, a1, a2, b1, b2, b3, wx, o1, o2, wp, ww, we, wb1, wb2, wb3
    signed int[8][8] t_table= [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    signed int[8][256] table_values= [
        [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ],
    ]
    signed int[256] edge_table8 = [
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 4,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 5,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 4,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 6,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 4,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 3,
        0, 0, 0, 1, 0, 0, 0, 2,
        0, 0, 0, 1, 0, 0, 0, 5,
        1, 1, 1, 2, 1, 1, 1, 3,
        1, 1, 1, 2, 1, 1, 1, 4,
        1, 1, 1, 2, 1, 1, 1, 3,
        1, 1, 1, 2, 1, 1, 1, 5,
        2, 2, 2, 3, 2, 2, 2, 4,
        2, 2, 2, 3, 2, 2, 2, 5,
        3, 3, 3, 4, 3, 3, 3, 5,
        4, 4, 4, 5, 5, 5, 6, 13
    ]

def next_move(color, board, params, depth, pid, timer, measure):
    """next_move
    """
    if pid is None:
        timer, measure = False, False
    return _next_move(color, board, params, depth, pid, timer, measure)


def get_best_move(color, board, params, moves, alpha, beta, depth, pid, timer, measure):
    """get_best_move
    """
    if pid is None:
        timer, measure = False, False
    return _get_best_move_wrap(color, board, params, moves, alpha, beta, depth, pid, timer, measure)


cdef inline tuple _next_move(str color, board, params, int depth, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count, bb, wb, bs, ws, corner, c, a1, a2, b1, b2, b3, wx, o1, o2, wp, ww, we, wb1, wb2, wb3
    cdef:
        double alpha = -10000000, beta = 10000000
        unsigned int int_color = 0
        unsigned int x, y, index = 0
        unsigned long long legal_moves, mask = 0x8000000000000000
        unsigned long long[64] legal_moves_bit_list
        unsigned int[64] legal_moves_x
        unsigned int[64] legal_moves_y
    # タイマーとメジャー準備
    measure_count = 0
    timer_timeout = <unsigned int>0
    if timer and pid:
        timer_deadline = Timer.deadline[pid]
        timer_timeout_value = Timer.timeout_value[pid]
    if measure and pid:
        if pid not in Measure.count:
            Measure.count[pid] = <unsigned int>0
        measure_count = Measure.count[pid]
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
    # 次の手番
    if color == 'black':
        int_color = <unsigned int>1
    # ボード情報取得
    bb, wb = board.get_bitboard_info()
    bs = board._black_score
    ws = board._white_score
    # 最大深さ調整
    if depth > <int>(64 - (bs + ws)):
        depth =  <int>64 - (bs + ws)
    # 最善手を取得
    legal_moves = _get_legal_moves_bits(int_color, bb, wb)
    for y in range(8):
        for x in range(8):
            if legal_moves & mask:
                legal_moves_bit_list[index] = mask
                legal_moves_x[index] = x
                legal_moves_y[index] = y
                index += 1
            mask >>= 1
    best_move, scores = _get_best_move(int_color, index, legal_moves_bit_list, legal_moves_x, legal_moves_y, alpha, beta, depth, timer)
    # タイマーとメジャー格納
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return best_move


cdef inline _get_best_move_wrap(str color, board, params, moves, double alpha, double beta, int depth, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count, bb, wb, bs, ws, corner, c, a1, a2, b1, b2, b3, wx, o1, o2, wp, ww, we, wb1, wb2, wb3
    cdef:
        unsigned long long[64] moves_bit_list
        unsigned int[64] moves_x
        unsigned int[64] moves_y
        unsigned int x, y, index = 0, int_color = 0
        unsigned long long put
        signed int lshift
    # タイマーとメジャー準備
    measure_count = 0
    timer_timeout = <unsigned int>0
    if timer and pid:
        timer_deadline = Timer.deadline[pid]
        timer_timeout_value = Timer.timeout_value[pid]
    if measure and pid:
        if pid not in Measure.count:
            Measure.count[pid] = <unsigned int>0
        measure_count = Measure.count[pid]
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
    # 次の手番
    if color == 'black':
        int_color = <unsigned int>1
    # ボード情報取得
    bb, wb = board.get_bitboard_info()
    bs = board._black_score
    ws = board._white_score
    # 最大深さ調整
    if depth > <int>(64 - (bs + ws)):
        depth =  <int>64 - (bs + ws)
    # 最善手を取得
    for x, y in moves:
        lshift = (63-(y*8+x))
        put = <unsigned long long>1 << lshift
        moves_bit_list[index] = put
        moves_x[index] = x
        moves_y[index] = y
        index += 1
    best_move, scores = _get_best_move(int_color, index, moves_bit_list, moves_x, moves_y, alpha, beta, depth, timer)
    # タイマーとメジャー格納
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return (best_move, scores)


cdef inline _get_best_move(unsigned int int_color, unsigned int index, unsigned long long[64] moves_bit_list, unsigned int[64] moves_x, unsigned int[64] moves_y, double alpha, double beta, int depth, int timer):
    global timer_timeout
    cdef:
        double score = alpha
        unsigned int int_color_next = 1, i, best = 64
    scores = {}
    # 手番
    if int_color:
        int_color_next = <unsigned int>0
    # 各手のスコア取得
    for i in range(index):
        _put_disc(int_color, moves_bit_list[i])
        score = -_get_score(int_color_next, -beta, -alpha, depth-1, timer, <unsigned int>0)
        _undo()
        scores[(moves_x[i], moves_y[i])] = score
        if timer_timeout:
            if best == 64:
                best = i
            break
        if score > alpha:  # 最善手を更新
            alpha = score
            best = i
    return (moves_x[best], moves_y[best]), scores


cdef inline signed int check_timeout():
    """check_timeout
    """
    global timer_deadline, timer_timeout, timer_timeout_value
    if time.time() > timer_deadline:
        timer_timeout = <unsigned int>1
        return timer_timeout_value
    return <signed int>0


cdef inline double _get_score(unsigned int int_color, double alpha, double beta, unsigned int depth, int t, unsigned int pas):
    """_get_score
    """
    global timer_timeout, measure_count, bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        double tmp, null_window
        unsigned long long legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, move
        unsigned int i, int_color_next = 1, count = 0, index = 0
        signed int timeout, sign = -1
        unsigned long long[64] next_moves_list
        signed int[64] possibilities
        unsigned long long flippable_discs_num, b, w, bits
        unsigned long long t_, rt, r_, rb, b_, lb, l_, lt
        unsigned long long bf_t_ = 0, bf_rt = 0, bf_r_ = 0, bf_rb = 0, bf_b_ = 0, bf_lb = 0, bf_l_ = 0, bf_lt = 0
        unsigned long long player, opponent
        unsigned long long blank, horizontal, vertical, diagonal, tmp_h, tmp_v, tmp_d1, tmp_d2
        unsigned long long legal_moves_bits_opponent
        signed int score
        unsigned long long bits_count
    # タイムアウト判定
    if t:
        timeout = check_timeout()
        if timeout:
            return timeout

    # 探索ノード数カウント
    measure_count += 1

    # 合法手を取得
    # -- _get_legal_moves_bits(int_color, bb, wb) --
    player, opponent = wb, bb
    if int_color:
        player, opponent = bb, wb
    blank = ~(player | opponent)
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
    # -- _get_legal_moves_bits(int_color, bb, wb) --

    # 次の手番
    if int_color:
        int_color_next = <unsigned int>0
        sign = <signed int>1

    # パスの場合
    if not legal_moves_bits:
        # 前回もパスの場合ゲーム終了
        if pas:
            # --- return _evaluate(int_color, <signed int>0, <signed int>0) * sign ---
            score = bs - ws
            if score > 0:    # 黒が勝った
                score += ww
            elif score < 0:  # 白が勝った
                score -= ww
            return score * sign
            # --- return _evaluate(int_color, <signed int>0, <signed int>0) * sign ---

        return -_get_score(int_color_next, -beta, -alpha, depth, t, <unsigned int>1)

    # 最大深さに到達
    if not depth:
        # 相手の着手可能数を取得
        # -- _get_legal_moves_bits(<unsigned int>0 if int_color else <unsigned int>1, bb, wb) --
        player, opponent = opponent, player  # reversed for opponent
        blank = ~(player | opponent)
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
        # -- _get_legal_moves_bits((<unsigned int>0 if int_color else <unsigned int>1, bb, wb) --

        if int_color:
            legal_moves_b_bits = legal_moves_bits
            legal_moves_w_bits = legal_moves_bits_opponent
        else:
            legal_moves_b_bits = legal_moves_bits_opponent
            legal_moves_w_bits = legal_moves_bits

        if legal_moves_b_bits:
            # -- _popcount --
            bits = legal_moves_b_bits
            bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
            bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
            bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
            bits = bits + (bits >> <unsigned int>8)
            bits = bits + (bits >> <unsigned int>16)
            legal_moves_b_bits = (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
            # -- _popcount --

        if legal_moves_b_bits:
            # -- _popcount --
            bits = legal_moves_w_bits
            bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
            bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
            bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
            bits = bits + (bits >> <unsigned int>8)
            bits = bits + (bits >> <unsigned int>16)
            legal_moves_w_bits = (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
            # -- _popcount --

        # 評価値を返す
        # --- return _evaluate(int_color, <signed int>legal_moves_b_bits, <signed int>legal_moves_w_bits) * sign ---
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
        # --- return _evaluate(int_color, <signed int>legal_moves_b_bits, <signed int>legal_moves_w_bits) * sign ---

    # 着手可能数に応じて手を並び替え
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        next_moves_list[count] = move

        # ひっくり返せる石を取得
        b, w = bb, wb

        # -- _get_flippable_discs_num --
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
        # -- _get_flippable_discs_num --

        # 自分の石を置いて相手の石をひっくり返す
        if int_color:
            b ^= move | flippable_discs_num
            w ^= flippable_discs_num
        else:
            w ^= move | flippable_discs_num
            b ^= flippable_discs_num

        # -- _get_legal_moves_bits(int_color, b, w) --
        player, opponent = w, b
        if int_color:
            player, opponent = b, w
        blank = ~(player | opponent)
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
        # -- _get_legal_moves_bits(int_color, b, w) --

        # -- _popcount --
        bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
        bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
        bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
        bits = bits + (bits >> <unsigned int>8)
        bits = bits + (bits >> <unsigned int>16)
        possibilities[count] = -<signed int>((bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F)
        # -- _popcount --

        count += 1
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする

    # 着手可能数に応じて並び替え
    _sort_moves_by_possibility(count, next_moves_list, possibilities)

    # 次の手の探索
    null_window = beta
    for i in range(count):
        if alpha < beta:
            # 一手打つ
            # --- _put_disc(int_color, next_moves_list[i]) ---
            # ひっくり返せる石を取得
            # -- _get_flippable_discs_num --
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
            # -- _get_flippable_discs_num --
            # -- _popcount --
            bits = fd
            bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
            bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
            bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
            bits = bits + (bits >> <unsigned int>8)
            bits = bits + (bits >> <unsigned int>16)
            bits_count = (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
            # -- _popcount --
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
            # --- _put_disc(int_color, next_moves_list[i]) ---
            tmp = -_get_score(int_color_next, -null_window, -alpha, depth-1, t, <unsigned int>0)
            if alpha < tmp:
                if tmp <= null_window and index:
                    alpha = -_get_score(int_color_next, -beta, -tmp, depth-1, t, <unsigned int>0)
                    _undo()
                    if timer_timeout:
                        return alpha
                else:
                    _undo()
                    alpha = tmp
            else:
                _undo()
            null_window = alpha + 1
        else:
            return alpha
        index += <unsigned int>1
    return alpha


cdef inline void _sort_moves_by_possibility(unsigned int count, unsigned long long[64] next_moves_list, signed int[64] possibilities):
    """_sort_moves_by_possibility
    """
    if count >= 2:
        if count <= BUCKET_SIZE:
            _bucket_sort(count, next_moves_list, possibilities)
        else:
            _merge_sort(count, next_moves_list, possibilities)


cdef inline void _bucket_sort(unsigned int count, unsigned long long[64] next_moves_list, signed int[64] possibilities):
    """_bucket_sort
    """
    cdef:
        unsigned int i, j, k = 0, pos, index
        unsigned long long[POSSIBILITY_RANGE*BUCKET_SIZE] bucket
        unsigned int[POSSIBILITY_RANGE] possibility_count
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
    """_merge_sort
    """
    cdef:
        unsigned int len1, len2, i
        unsigned long long[32] array_move1
        unsigned long long[32] array_move2
        signed int[32] array_p1
        signed int[32] array_p2
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
    """_merge
    """
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


cdef inline unsigned long long _get_legal_moves_bits(unsigned int int_color, unsigned long long b, unsigned long long w):
    """_get_legal_moves_bits
    """
    cdef:
        unsigned long long player = w, opponent = b
    if int_color:
        player = b
        opponent = w
    cdef:
        unsigned long long blank = ~(player | opponent)
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


cdef inline void _put_disc(unsigned int int_color, unsigned long long move):
    """_put_disc
    """
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        unsigned long long count, bits
        unsigned long long t_, rt, r_, rb, b_, lb, l_, lt
        unsigned long long bf_t_ = 0, bf_rt = 0, bf_r_ = 0, bf_rb = 0, bf_b_ = 0, bf_lb = 0, bf_l_ = 0, bf_lt = 0
        unsigned long long player, opponent, flippable_discs_num = 0
    # ひっくり返せる石を取得
    # -- _get_flippable_discs_num --
    player = wb
    opponent = bb
    if int_color:
        player = bb
        opponent = wb
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
    # -- _get_flippable_discs_num --
    # -- _popcount --
    bits = fd
    bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
    bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
    bits = bits + (bits >> <unsigned int>8)
    bits = bits + (bits >> <unsigned int>16)
    count = (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
    # -- _popcount --
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


cdef inline void _undo():
    """_undo
    """
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, tail
    tail -= 1
    bb = pbb[tail]
    wb = pwb[tail]
    bs = pbs[tail]
    ws = pws[tail]


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
    """テーブルによる評価値
    """
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
    """着手可能数による評価値
    """
    global wp
    return (pos_b - pos_w) * wp


cdef inline signed int _get_e():
    """辺の確定石による評価値
    """
    global bb, wb, we
    cdef:
        signed int score = 0
        unsigned long long all_bitboard, bit_pos, lt, rt, lb, rb, b_t, w_t, b_b, w_b, b_l, w_l, b_r, w_r
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
    """空きマスのパターンによる評価値
    """
    global bb, wb, wb1, wb2, wb3
    cdef:
        signed int score = 0
        unsigned long long blackwhite, blank
        unsigned long long horizontal, vertical, diagonal
        unsigned long long l_blank, r_blank, t_blank, b_blank, lt_blank, rt_blank, lb_blank, rb_blank
        unsigned long long lt_x, rt_x, lb_x, rb_x
        unsigned long long lt_r, lt_b, rt_l, rt_b, lb_t, lb_r, rb_t, rb_l
        signed int lt_r_sign = 1, lt_b_sign = 1, rt_l_sign = 1, rt_b_sign = 1, lb_t_sign = 1, lb_r_sign = 1, rb_t_sign = 1, rb_l_sign = 1
        unsigned int i;
        unsigned long long[8] blanks;
        unsigned long long bits;
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
            # -- _popcount --
            bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
            bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
            bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
            bits = bits + (bits >> <unsigned int>8)
            bits = bits + (bits >> <unsigned int>16)
            score += <signed int>(bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
            # -- _popcount --
        # white
        bits = blanks[i] & white
        if bits:
            # -- _popcount --
            bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
            bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
            bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
            bits = bits + (bits >> <unsigned int>8)
            bits = bits + (bits >> <unsigned int>16)
            score -= <signed int>(bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F
            # -- _popcount --
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


#cdef inline unsigned long long _popcount(unsigned long long bits):
#    """_popcount
#    """
#    bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
#    bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
#    bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
#    bits = bits + (bits >> <unsigned int>8)
#    bits = bits + (bits >> <unsigned int>16)
#    return (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F


#cdef inline unsigned long long _get_flippable_discs_num(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long move):
#    """_get_flippable_discs_num
#    """
#    cdef:
#        unsigned long long t_, rt, r_, rb, b_, lb, l_, lt
#        unsigned long long bf_t_ = 0, bf_rt = 0, bf_r_ = 0, bf_rb = 0, bf_b_ = 0, bf_lb = 0, bf_l_ = 0, bf_lt = 0
#        unsigned long long player = w, opponent = b, flippable_discs_num = 0
#    if int_color:
#        player = b
#        opponent = w
#    t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & (move << <unsigned int>8)  # top
#    rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & (move << <unsigned int>7)  # right-top
#    r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & (move >> <unsigned int>1)  # right
#    rb = <unsigned long long>0x007F7F7F7F7F7F7F & (move >> <unsigned int>9)  # right-bottom
#    b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & (move >> <unsigned int>8)  # bottom
#    lb = <unsigned long long>0x00FEFEFEFEFEFEFE & (move >> <unsigned int>7)  # left-bottom
#    l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & (move << <unsigned int>1)  # left
#    lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & (move << <unsigned int>9)  # left-top
#    for _ in range(6):
#        if t_ & opponent:
#            bf_t_ |= t_
#            t_ = <unsigned long long>0xFFFFFFFFFFFFFF00 & (t_ << <unsigned int>8)
#        if rt & opponent:
#            bf_rt |= rt
#            rt = <unsigned long long>0x7F7F7F7F7F7F7F00 & (rt << <unsigned int>7)
#        if r_ & opponent:
#            bf_r_ |= r_
#            r_ = <unsigned long long>0x7F7F7F7F7F7F7F7F & (r_ >> <unsigned int>1)
#        if rb & opponent:
#            bf_rb |= rb
#            rb = <unsigned long long>0x007F7F7F7F7F7F7F & (rb >> <unsigned int>9)
#        if b_ & opponent:
#            bf_b_ |= b_
#            b_ = <unsigned long long>0x00FFFFFFFFFFFFFF & (b_ >> <unsigned int>8)
#        if lb & opponent:
#            bf_lb |= lb
#            lb = <unsigned long long>0x00FEFEFEFEFEFEFE & (lb >> <unsigned int>7)
#        if l_ & opponent:
#            bf_l_ |= l_
#            l_ = <unsigned long long>0xFEFEFEFEFEFEFEFE & (l_ << <unsigned int>1)
#        if lt & opponent:
#            bf_lt |= lt
#            lt = <unsigned long long>0xFEFEFEFEFEFEFE00 & (lt << <unsigned int>9)
#    if t_ & player:
#        flippable_discs_num |= bf_t_
#    if rt & player:
#        flippable_discs_num |= bf_rt
#    if r_ & player:
#        flippable_discs_num |= bf_r_
#    if rb & player:
#        flippable_discs_num |= bf_rb
#    if b_ & player:
#        flippable_discs_num |= bf_b_
#    if lb & player:
#        flippable_discs_num |= bf_lb
#    if l_ & player:
#        flippable_discs_num |= bf_l_
#    if lt & player:
#        flippable_discs_num |= bf_lt
#    return flippable_discs_num


#cdef inline signed int _evaluate(unsigned int int_color, signed int pos_b,  signed int pos_w):
#    """_evaluate
#    """
#    global bs, ws, ww
#    cdef:
#        signed int score
#    # 勝敗が決まっている場合
#    if not pos_b and not pos_w:
#        score = bs - ws
#        if score > 0:    # 黒が勝った
#            score += ww
#        elif score < 0:  # 白が勝った
#            score -= ww
#        return score
#    # 勝敗が決まっていない場合
#    score = _get_t() + _get_p(pos_b, pos_w) + _get_e() + _get_b()
#    return score
