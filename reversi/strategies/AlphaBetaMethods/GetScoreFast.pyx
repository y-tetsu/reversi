#cython: language_level=3
"""Get Score of AlphaBeta strategy
"""

import sys
import time

from reversi.strategies.common import Timer, Measure


MAXSIZE64 = 2**63 - 1


def get_score(alphabeta, color, board, alpha, beta, depth, pid):
    """get_score
    """
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        pass

    return _get_score(_get_score, alphabeta, color, board, alpha, beta, depth, pid)


def get_score_measure(alphabeta, color, board, alpha, beta, depth, pid):
    """get_score_measure
    """
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        pass

    return _get_score_measure(_get_score_measure, alphabeta, color, board, alpha, beta, depth, pid)


def get_score_timer(alphabeta, color, board, alpha, beta, depth, pid):
    """get_score_timer
    """
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        pass

    return _get_score_timer(_get_score_timer, alphabeta, color, board, alpha, beta, depth, pid)


def get_score_measure_timer(alphabeta, color, board, alpha, beta, depth, pid):
    """get_score_measure_timer
    """
    if board.size == 8 and sys.maxsize == MAXSIZE64 and hasattr(board, '_black_bitboard'):
        pass

    return _get_score_measure_timer(_get_score_measure_timer, alphabeta, color, board, alpha, beta, depth, pid)


cdef signed int _get_score(func, alphabeta, color, board, signed int alpha, signed int beta, unsigned int depth, pid):
    """_get_score
    """
    cdef:
        unsigned int is_game_end
        signed int sign

    # ゲーム終了 or 最大深さに到達
    legal_moves_b_bits = board.get_legal_moves_bits('black')
    legal_moves_w_bits = board.get_legal_moves_bits('white')
    is_game_end = 1 if not legal_moves_b_bits and not legal_moves_w_bits else 0
    if is_game_end or depth <= 0:
        sign = 1 if color == 'black' else -1
        return alphabeta.evaluator.evaluate(color=color, board=board, possibility_b=board.get_bit_count(legal_moves_b_bits), possibility_w=board.get_bit_count(legal_moves_w_bits)) * sign  # noqa: E501

    # パスの場合
    legal_moves_bits = legal_moves_b_bits if color == 'black' else legal_moves_w_bits
    next_color = 'white' if color == 'black' else 'black'
    if not legal_moves_bits:
        return -func(func, alphabeta, next_color, board, -beta, -alpha, depth, pid)

    # 評価値を算出
    cdef:
        unsigned int size, skip, y, x
    size = board.size
    mask = 1 << ((size**2)-1)
    for y in range(size):
        skip = <unsigned int>0
        for x in range(size):
            if legal_moves_bits & mask:
                board.put_disc(color, x, y)
                score = -func(func, alphabeta, next_color, board, -beta, -alpha, depth-1, pid)
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


cdef signed int _get_score_measure(func, alphabeta, color, board, alpha, beta, unsigned int depth, pid):
    """_get_score_measure
    """
    measure(pid)

    return _get_score(func, alphabeta, color, board, alpha, beta, depth, pid)


cdef signed int _get_score_timer(func, alphabeta, color, board, alpha, beta, unsigned int depth, pid):
    """_get_score_timer
    """
    cdef:
        signed int timeout
    timeout = timer(pid)

    return timeout if timeout else _get_score(func, alphabeta, color, board, alpha, beta, depth, pid)


cdef signed int _get_score_measure_timer(func, alphabeta, color, board, alpha, beta, unsigned int depth, pid):
    """_get_score_measure_timer
    """
    cdef:
        signed int timeout
    measure(pid)
    timeout = timer(pid)

    return timeout if timeout else _get_score(func, alphabeta, color, board, alpha, beta, depth, pid)


cdef inline measure(pid):
    """measure
    """
    if pid:
        if pid not in Measure.count:
            Measure.count[pid] = 0
        Measure.count[pid] += 1


cdef inline signed int timer(pid):
    """timer
    """
    if pid:
        if time.time() > Timer.deadline[pid]:
            Timer.timeout_flag[pid] = True  # タイムアウト発生
            return Timer.timeout_value[pid]

    return <signed int>0
