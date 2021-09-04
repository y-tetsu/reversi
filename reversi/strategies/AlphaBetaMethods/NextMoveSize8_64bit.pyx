#cython: language_level=3, profile=True, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""Next Move(Size8,64bit) of AlphaBeta strategy
"""

import time

from reversi.strategies.common import Timer, Measure


def next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure):
    """next_move
    """
    return _next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure)


cdef inline tuple _next_move(str color, board, signed int param_min, signed int param_max, int depth, evaluator, str pid, int timer, int measure):
    cdef:
        tuple move, best_move = None
        str next_color
        double alpha = param_min, beta = param_max, score = param_min
    moves = board.get_legal_moves(color)
    for move in moves:
        board.put_disc(color, *move)
        next_color = 'white' if color == 'black' else 'black'
        if timer:
            if measure:  # タイマーあり:メジャーあり
                score = -_get_score_timer_measure(_get_score_timer_measure, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
                board.undo()
            else:        # タイマーあり:メジャーなし
                score = -_get_score_timer(_get_score_timer, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
                board.undo()
            if Timer.is_timeout(pid):  # タイムアウト判定
                best_move = move if best_move is None else best_move
                break
        elif measure:    # タイマーなし:メジャーあり
            score = -_get_score_measure(_get_score_measure, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
            board.undo()
        else:            # タイマーなし:メジャーなし
            score = -_get_score(_get_score, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
            board.undo()
        if score > alpha:  # 最善手を更新
            alpha = score
            best_move = move
    return best_move


cdef inline double _get_score_measure(func, str color, board, double alpha, double beta, unsigned int depth, evaluator, str pid):
    """_get_score_measure
    """
    measure(pid)
    return _get_score(func, color, board, alpha, beta, depth, evaluator, pid)


cdef inline double _get_score_timer(func, str color, board, double alpha, double beta, unsigned int depth, evaluator, str pid):
    """_get_score_timer
    """
    cdef:
        signed int timeout
    timeout = timer(pid)
    return timeout if timeout else _get_score(func, color, board, alpha, beta, depth, evaluator, pid)


cdef inline double _get_score_timer_measure(func, str color, board, double alpha, double beta, unsigned int depth, evaluator, str pid):
    """_get_score_timer_measure
    """
    cdef:
        signed int timeout
    measure(pid)
    timeout = timer(pid)
    return timeout if timeout else _get_score(func, color, board, alpha, beta, depth, evaluator, pid)


cdef inline measure(str pid):
    """measure
    """
    if pid:
        if pid not in Measure.count:
            Measure.count[pid] = 0
        Measure.count[pid] += 1


cdef inline signed int timer(str pid):
    """timer
    """
    if pid:
        if time.time() > Timer.deadline[pid]:
            Timer.timeout_flag[pid] = True  # タイムアウト発生
            return Timer.timeout_value[pid]

    return <signed int>0


cdef inline double _get_score(func, str color, board, double alpha, double beta, unsigned int depth, evaluator, str pid):
    """_get_score
    """
    cdef:
        double score
        unsigned long long b, w, legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, mask
        unsigned int is_game_end, color_num, x, y
        signed int sign

    # ゲーム終了 or 最大深さに到達
    b = board._black_bitboard
    w = board._white_bitboard
    legal_moves_b_bits = _get_legal_moves_bits(1, b, w)
    legal_moves_w_bits = _get_legal_moves_bits(0, b, w)
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
        return evaluator.evaluate(color=color, board=board, possibility_b=_get_bit_count(legal_moves_b_bits), possibility_w=_get_bit_count(legal_moves_w_bits)) * sign  # noqa: E501

    # パスの場合
    if not legal_moves_bits:
        return -func(func, next_color, board, -beta, -alpha, depth, evaluator, pid)

    # 評価値を算出
    mask = 1 << 63
    for y in range(8):
        for x in range(8):
            if legal_moves_bits & mask:
                _put_disc(board, color_num, x, y)
                score = -func(func, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
                _undo(board)

                if score > alpha:
                    alpha = score

                if Timer.is_timeout(pid):
                    return alpha

                if alpha >= beta:  # 枝刈り
                    return alpha

            mask >>= 1

    return alpha


cdef inline unsigned long long _get_legal_moves_bits(unsigned int color, unsigned long long b, unsigned long long w):
    """_get_legal_moves_bits
    """
    cdef:
        unsigned long long player, opponent

    if color:
        player = b
        opponent = w
    else:
        player = w
        opponent = b

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


cdef inline unsigned long long _get_bit_count(unsigned long long bits):
    """_get_bit_count
    """
    bits = (bits & <unsigned long long>0x5555555555555555) + (bits >> <unsigned int>1 & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + (bits >> <unsigned int>2 & <unsigned long long>0x3333333333333333)
    bits = (bits & <unsigned long long>0x0F0F0F0F0F0F0F0F) + (bits >> <unsigned int>4 & <unsigned long long>0x0F0F0F0F0F0F0F0F)
    bits = (bits & <unsigned long long>0x00FF00FF00FF00FF) + (bits >> <unsigned int>8 & <unsigned long long>0x00FF00FF00FF00FF)
    bits = (bits & <unsigned long long>0x0000FFFF0000FFFF) + (bits >> <unsigned int>16 & <unsigned long long>0x0000FFFF0000FFFF)

    return (bits & <unsigned long long>0x00000000FFFFFFFF) + (bits >> <unsigned int>32 & <unsigned long long>0x00000000FFFFFFFF)


cdef inline unsigned long long _put_disc(board, unsigned int color, unsigned int x, unsigned int y):
    """_put_disc
    """
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
    flippable_discs_num = _get_flippable_discs_num(color, black_bitboard, white_bitboard, shift_size)
    flippable_discs_count = _get_bit_count(flippable_discs_num)

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


cdef inline unsigned long long _get_flippable_discs_num(unsigned int color, unsigned long long black_bitboard, unsigned long long white_bitboard, unsigned int shift_size):
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned int direction1, direction2
        unsigned long long buff, next_put
        unsigned long long move = 0
        unsigned long long player, opponent, flippable_discs_num = 0

    if color:
        player = black_bitboard
        opponent = white_bitboard
    else:
        player = white_bitboard
        opponent = black_bitboard

    move = <unsigned long long>1 << shift_size

    for direction1 in range(8):
        buff = 0
        next_put = _get_next_put(move, direction1)

        # get discs of consecutive opponents
        for direction2 in range(8):
            if next_put & opponent:
                buff |= next_put
                next_put = _get_next_put(next_put, direction1)
            else:
                break

        # store result if surrounded by own disc
        if next_put & player:
            flippable_discs_num |= buff

    return flippable_discs_num


cdef inline unsigned long long _get_next_put(unsigned long long put, unsigned int direction):
    """_get_next_put
    """
    cdef:
        unsigned long long next_put

    if direction == 0:
        next_put = <unsigned long long>0xFFFFFFFFFFFFFF00 & (put << <unsigned int>8)  # top
    elif direction == 1:
        next_put = <unsigned long long>0x7F7F7F7F7F7F7F00 & (put << <unsigned int>7)  # right-top
    elif direction == 2:
        next_put = <unsigned long long>0x7F7F7F7F7F7F7F7F & (put >> <unsigned int>1)  # right
    elif direction == 3:
        next_put = <unsigned long long>0x007F7F7F7F7F7F7F & (put >> <unsigned int>9)  # right-bottom
    elif direction == 4:
        next_put = <unsigned long long>0x00FFFFFFFFFFFFFF & (put >> <unsigned int>8)  # bottom
    elif direction == 5:
        next_put = <unsigned long long>0x00FEFEFEFEFEFEFE & (put >> <unsigned int>7)  # left-bottom
    elif direction == 6:
        next_put = <unsigned long long>0xFEFEFEFEFEFEFEFE & (put << <unsigned int>1)  # left
    elif direction == 7:
        next_put = <unsigned long long>0xFEFEFEFEFEFEFE00 & (put << <unsigned int>9)  # left-top
    else:
        next_put = <unsigned long long>0                                              # unexpected

    return next_put


cdef inline _undo(board):
    """_undo
    """
    (board._black_bitboard, board._white_bitboard, board._black_score, board._white_score) = board.prev.pop()
