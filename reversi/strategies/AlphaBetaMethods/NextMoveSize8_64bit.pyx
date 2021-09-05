#cython: language_level=3, profile=True, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""Next Move(Size8,64bit) of AlphaBeta strategy
"""

import time
from copy import deepcopy

from reversi.strategies.common import Timer, Measure


cdef:
    unsigned int[64] legal_moves_x
    unsigned int[64] legal_moves_y
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


def next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure):
    """next_move
    """
    return _next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure)


def get_best_move(color, board, moves, alpha, beta, depth, evaluator, pid, timer, measure):
    """get_best_move
    """
    return _get_best_move_wrap(color, board, moves, alpha, beta, depth, evaluator, pid, timer, measure)


cdef inline tuple _next_move(str color, board, signed int param_min, signed int param_max, int depth, evaluator, str pid, int timer, int measure):
    global legal_moves_x, legal_moves_y
    cdef:
        double alpha = param_min, beta = param_max
        unsigned int index
        unsigned long long b, w
    b, w = board.get_bitboard_info()
    index = _get_legal_moves(color, b, w)
    best_move, _ = _get_best_move(color, board, index, legal_moves_x, legal_moves_y, alpha, beta, depth, evaluator, pid, timer, measure)
    return best_move


cdef inline _get_best_move_wrap(str color, board, moves, double alpha, double beta, int depth, evaluator, str pid, int timer, int measure):
    cdef:
        unsigned int[64] moves_x
        unsigned int[64] moves_y
        unsigned int x, y, index = 0
    for x, y in moves:
        moves_x[index] = x
        moves_y[index] = y
        index += 1
    return _get_best_move(color, board, index, moves_x, moves_y, alpha, beta, depth, evaluator, pid, timer, measure)


cdef inline _get_best_move(str color, board, unsigned int index, unsigned int[64] moves_x, unsigned int[64] moves_y, double alpha, double beta, int depth, evaluator, str pid, int timer, int measure):
    global bb, wb
    cdef:
        str next_color
        double score = alpha
        unsigned int i, best = 64
    scores = {}
    bb, wb = board.get_bitboard_info()
    # ボード情報退避
    board_bb = board._black_bitboard
    board_wb = board._white_bitboard
    board_bs = board._black_score
    board_ws = board._white_score
    board_prev = deepcopy(board.prev)
    # 各手のスコア取得
    for i in range(index):
        _put_disc(1 if color == 'black' else 0, moves_x[i], moves_y[i])
        next_color = 'white' if color == 'black' else 'black'
        if timer:
            if measure:  # タイマーあり:メジャーあり
                score = -_get_score_timer_measure(_get_score_timer_measure, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
                _undo()
            else:        # タイマーあり:メジャーなし
                score = -_get_score_timer(_get_score_timer, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
                _undo()
            scores[(moves_x[i], moves_y[i])] = score
            if Timer.is_timeout(pid):  # タイムアウト判定
                if best == 64:
                    best = i
                break
        elif measure:    # タイマーなし:メジャーあり
            score = -_get_score_measure(_get_score_measure, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
            _undo()
            scores[(moves_x[i], moves_y[i])] = score
        else:            # タイマーなし:メジャーなし
            score = -_get_score(_get_score, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
            _undo()
            scores[(moves_x[i], moves_y[i])] = score
        if score > alpha:  # 最善手を更新
            alpha = score
            best = i
    # ボードを元に戻す
    board._black_bitboard = board_bb
    board._white_bitboard = board_wb
    board._black_score = board_bs
    board._white_score = board_ws
    board.prev = deepcopy(board_prev)
    return (moves_x[best], moves_y[best]), scores


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
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        double score
        unsigned long long legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, mask
        unsigned int is_game_end, color_num, x, y
        signed int sign
    # ゲーム終了 or 最大深さに到達
    legal_moves_b_bits = _get_legal_moves_bits(1, bb, wb)
    legal_moves_w_bits = _get_legal_moves_bits(0, bb, wb)
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
        board._black_bitboard = bb
        board._white_bitboard = wb
        board._black_score = bs
        board._white_score = ws
        board._flippable_discs_num = fd
        board.prev = []
        for i in range(tail):
            board.prev += [(pbb[i], pwb[i], pbs[i], pws[i])]
        return evaluator.evaluate(color=color, board=board, possibility_b=_get_bit_count(legal_moves_b_bits), possibility_w=_get_bit_count(legal_moves_w_bits)) * sign  # noqa: E501
    # パスの場合
    if not legal_moves_bits:
        return -func(func, next_color, board, -beta, -alpha, depth, evaluator, pid)
    # 評価値を算出
    mask = 1 << 63
    for y in range(8):
        for x in range(8):
            if legal_moves_bits & mask:
                _put_disc(color_num, x, y)
                score = -func(func, next_color, board, -beta, -alpha, depth-1, evaluator, pid)
                _undo()
                if score > alpha:
                    alpha = score
                if Timer.is_timeout(pid):
                    return alpha
                if alpha >= beta:  # 枝刈り
                    return alpha
            mask >>= 1
    return alpha


cdef inline unsigned int _get_legal_moves(str color, unsigned long long b, unsigned long long w):
    """_get_legal_moves
    """
    global legal_moves_x, legal_moves_y
    cdef:
        unsigned int x, y, index = 0
        unsigned long long legal_moves, mask = 0x8000000000000000
    legal_moves = _get_legal_moves_bits(1 if color == 'black' else 0, b, w)
    for y in range(8):
        for x in range(8):
            if legal_moves & mask:
                legal_moves_x[index] = x
                legal_moves_y[index] = y
                index += 1
            mask >>= 1
    return index


cdef inline unsigned long long _get_legal_moves_bits(unsigned int color, unsigned long long b, unsigned long long w):
    """_get_legal_moves_bits
    """
    cdef:
        unsigned long long player = w, opponent = b
    if color:
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


cdef inline unsigned long long _get_bit_count(unsigned long long bits):
    """_get_bit_count
    """
    bits = (bits & <unsigned long long>0x5555555555555555) + (bits >> <unsigned int>1 & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + (bits >> <unsigned int>2 & <unsigned long long>0x3333333333333333)
    bits = (bits & <unsigned long long>0x0F0F0F0F0F0F0F0F) + (bits >> <unsigned int>4 & <unsigned long long>0x0F0F0F0F0F0F0F0F)
    bits = (bits & <unsigned long long>0x00FF00FF00FF00FF) + (bits >> <unsigned int>8 & <unsigned long long>0x00FF00FF00FF00FF)
    bits = (bits & <unsigned long long>0x0000FFFF0000FFFF) + (bits >> <unsigned int>16 & <unsigned long long>0x0000FFFF0000FFFF)
    return (bits & <unsigned long long>0x00000000FFFFFFFF) + (bits >> <unsigned int>32 & <unsigned long long>0x00000000FFFFFFFF)


cdef inline void _put_disc(unsigned int color, unsigned int x, unsigned int y):
    """_put_disc
    """
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        unsigned long long put, count
        signed int lshift
    # 配置位置を整数に変換
    lshift = (63-(y*8+x))
    put = <unsigned long long>1 << lshift
    # ひっくり返せる石を取得
    fd = _get_flippable_discs_num(color, bb, wb, lshift)
    count = _get_bit_count(fd)
    # 打つ前の状態を格納
    pbb[tail] = bb
    pwb[tail] = wb
    pbs[tail] = bs
    pws[tail] = ws
    tail += 1
    # 自分の石を置いて相手の石をひっくり返す
    if color:
        bb ^= put | fd
        wb ^= fd
        bs += <unsigned int>1 + <unsigned int>count
        ws -= <unsigned int>count
    else:
        wb ^= put | fd
        bb ^= fd
        bs -= <unsigned int>count
        ws += <unsigned int>1 + <unsigned int>count


cdef inline unsigned long long _get_flippable_discs_num(unsigned int color, unsigned long long b, unsigned long long w, unsigned int lshift):
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned int d1, d2
        unsigned long long buff, next_put
        unsigned long long move = 0
        unsigned long long player, opponent, flippable_discs_num = 0
    if color:
        player = b
        opponent = w
    else:
        player = w
        opponent = b
    move = <unsigned long long>1 << lshift
    for d1 in range(8):
        buff = 0
        next_put = _get_next_put(move, d1)
        # get discs of consecutive opponents
        for d2 in range(8):
            if next_put & opponent:
                buff |= next_put
                next_put = _get_next_put(next_put, d1)
            else:
                break
        # store result if surrounded by own disc
        if next_put & player:
            flippable_discs_num |= buff
    return flippable_discs_num


cdef inline unsigned long long _get_next_put(unsigned long long put, unsigned int d):
    """_get_next_put
    """
    cdef:
        unsigned long long next_put
    if d == 0:
        next_put = <unsigned long long>0xFFFFFFFFFFFFFF00 & (put << <unsigned int>8)  # top
    elif d == 1:
        next_put = <unsigned long long>0x7F7F7F7F7F7F7F00 & (put << <unsigned int>7)  # right-top
    elif d == 2:
        next_put = <unsigned long long>0x7F7F7F7F7F7F7F7F & (put >> <unsigned int>1)  # right
    elif d == 3:
        next_put = <unsigned long long>0x007F7F7F7F7F7F7F & (put >> <unsigned int>9)  # right-bottom
    elif d == 4:
        next_put = <unsigned long long>0x00FFFFFFFFFFFFFF & (put >> <unsigned int>8)  # bottom
    elif d == 5:
        next_put = <unsigned long long>0x00FEFEFEFEFEFEFE & (put >> <unsigned int>7)  # left-bottom
    elif d == 6:
        next_put = <unsigned long long>0xFEFEFEFEFEFEFEFE & (put << <unsigned int>1)  # left
    elif d == 7:
        next_put = <unsigned long long>0xFEFEFEFEFEFEFE00 & (put << <unsigned int>9)  # left-top
    else:
        next_put = <unsigned long long>0                                              # unexpected
    return next_put


cdef inline void _undo():
    """_undo
    """
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, tail
    bb = pbb[tail-1]
    wb = pwb[tail-1]
    bs = pbs[tail-1]
    ws = pws[tail-1]
    tail -= 1
