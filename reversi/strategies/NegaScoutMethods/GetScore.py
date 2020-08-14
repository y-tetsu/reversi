"""Get Score of NegaScout strategy
"""

import time

from reversi.strategies.common import Timer, Measure


def get_score(negascout, color, board, alpha, beta, depth, pid):
    """get_score
    """
    return _get_score(_get_score, negascout, color, board, alpha, beta, depth, pid)


def get_score_measure(negascout, color, board, alpha, beta, depth, pid):
    """get_score_measure
    """
    return _get_score_measure(_get_score_measure, negascout, color, board, alpha, beta, depth, pid)


def get_score_timer(negascout, color, board, alpha, beta, depth, pid):
    """get_score_timer
    """
    return _get_score_timer(_get_score_timer, negascout, color, board, alpha, beta, depth, pid)


def get_score_measure_timer(negascout, color, board, alpha, beta, depth, pid):
    """get_score_measure_timer
    """
    return _get_score_measure_timer(_get_score_measure_timer, negascout, color, board, alpha, beta, depth, pid)


def _get_score_measure(func, negascout, color, board, alpha, beta, depth, pid):
    """_get_score_measure
    """
    measure(pid)

    return _get_score(func, negascout, color, board, alpha, beta, depth, pid)


def _get_score_timer(func, negascout, color, board, alpha, beta, depth, pid):
    """_get_score_timer
    """
    timeout = timer(pid)

    return timeout if timeout else _get_score(func, negascout, color, board, alpha, beta, depth, pid)


def _get_score_measure_timer(func, negascout, color, board, alpha, beta, depth, pid):
    """_get_score_measure_timer
    """
    measure(pid)
    timeout = timer(pid)

    return timeout if timeout else _get_score(func, negascout, color, board, alpha, beta, depth, pid)


def _get_score(func, negascout, color, board, alpha, beta, depth, pid):
    """_get_score
    """
    # ゲーム終了 or 最大深さに到達
    legal_moves_b_bits = board.get_legal_moves_bits('black')
    legal_moves_w_bits = board.get_legal_moves_bits('white')
    is_game_end = True if not legal_moves_b_bits and not legal_moves_w_bits else False
    if is_game_end or depth <= 0:
        sign = 1 if color == 'black' else -1
        return negascout.evaluator.evaluate(color=color, board=board, possibility_b=board.get_bit_count(legal_moves_b_bits), possibility_w=board.get_bit_count(legal_moves_w_bits)) * sign  # noqa: E501

    # パスの場合
    legal_moves_bits = legal_moves_b_bits if color == 'black' else legal_moves_w_bits
    next_color = 'white' if color == 'black' else 'black'

    if not legal_moves_bits:
        return -func(func, negascout, next_color, board, -beta, -alpha, depth, pid=pid)

    # NegaScout法
    tmp, null_window, index = None, beta, 0
    size = board.size
    mask = 1 << ((size**2)-1)
    for y in range(size):
        skip = False
        for x in range(size):
            if legal_moves_bits & mask:
                if alpha < beta:
                    board.put_disc(color, x, y)
                    tmp = -func(func, negascout, next_color, board, -null_window, -alpha, depth-1, pid=pid)
                    board.undo()

                    if alpha < tmp:
                        if tmp <= null_window and index:
                            board.put_disc(color, x, y)
                            alpha = -func(func, negascout, next_color, board, -beta, -tmp, depth-1, pid=pid)
                            board.undo()

                            if Timer.is_timeout(pid):
                                return alpha
                        else:
                            alpha = tmp

                    null_window = alpha + 1
                else:
                    skip = True
                    break

                index += 1

            mask >>= 1

        if skip:
            break

    return alpha


def measure(pid):
    """measure
    """
    if pid:
        if pid not in Measure.count:
            Measure.count[pid] = 0
        Measure.count[pid] += 1


def timer(pid):
    """timer
    """
    if pid:
        if time.time() > Timer.deadline[pid]:
            Timer.timeout_flag[pid] = True  # タイムアウト発生
            return Timer.timeout_value[pid]

    return None
