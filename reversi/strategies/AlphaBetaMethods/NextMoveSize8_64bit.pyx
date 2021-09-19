#cython: language_level=3, profile=False, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""Next Move(Size8,64bit) of AlphaBeta strategy
"""

import time

from reversi.strategies.common import Timer, Measure


cdef:
    unsigned long long measure_count
    unsigned long long[64] legal_moves_bit_list
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
    double timer_deadline
    unsigned int timer_timeout
    signed int timer_timeout_value


def next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure):
    """next_move
    """
    if pid is None:
        timer, measure = False, False
    return _next_move(color, board, param_min, param_max, depth, evaluator, pid, timer, measure)


def get_best_move(color, board, moves, alpha, beta, depth, evaluator, pid, timer, measure):
    """get_best_move
    """
    if pid is None:
        timer, measure = False, False
    return _get_best_move_wrap(color, board, moves, alpha, beta, depth, evaluator, pid, timer, measure)


cdef inline tuple _next_move(str color, board, signed int param_min, signed int param_max, int depth, evaluator, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count, legal_moves_bit_list, legal_moves_x, legal_moves_y
    cdef:
        double alpha = param_min, beta = param_max
        unsigned long long b, w
        unsigned int int_color = 0
        unsigned int x, y, index = 0
        unsigned long long legal_moves, mask = 0x8000000000000000
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
    b, w = board.get_bitboard_info()
    legal_moves = _get_legal_moves_bits(int_color, b, w)
    for y in range(8):
        for x in range(8):
            if legal_moves & mask:
                legal_moves_bit_list[index] = mask
                legal_moves_x[index] = x
                legal_moves_y[index] = y
                index += 1
            mask >>= 1
    best_move, _ = _get_best_move(int_color, board, index, legal_moves_bit_list, legal_moves_x, legal_moves_y, alpha, beta, depth, evaluator, timer)
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return best_move


cdef inline _get_best_move_wrap(str color, board, moves, double alpha, double beta, int depth, evaluator, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count
    cdef:
        unsigned long long[64] moves_bit_list
        unsigned int[64] moves_x
        unsigned int[64] moves_y
        unsigned int x, y, index = 0, int_color = 0
        unsigned long long put
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
    best_move, scores = _get_best_move(int_color, board, index, moves_bit_list, moves_x, moves_y, alpha, beta, depth, evaluator, timer)
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return (best_move, scores)


cdef inline _get_best_move(unsigned int int_color, board, unsigned int index, unsigned long long[64] moves_bit_list, unsigned int[64] moves_x, unsigned int[64] moves_y, double alpha, double beta, int depth, evaluator, int timer):
    global timer_timeout, bb, wb, bs, ws
    cdef:
        double score = alpha
        unsigned int int_color_next = 1, i, best = 64
    scores = {}
    # 手番
    if int_color:
        int_color_next = <unsigned int>0
    # ボード情報取得
    bb, wb = board.get_bitboard_info()
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
        score = -_get_score(int_color_next, board, -beta, -alpha, depth-1, evaluator, timer, <unsigned int>0)
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


cdef inline signed int check_timeout():
    """check_timeout
    """
    global timer_deadline, timer_timeout, timer_timeout_value
    if time.time() > timer_deadline:
        timer_timeout = <unsigned int>1
        return timer_timeout_value
    return <signed int>0


cdef inline double _get_score(unsigned int int_color, board, double alpha, double beta, unsigned int depth, evaluator, int t, unsigned int pas):
    """_get_score
    """
    global timer_timeout, measure_count, bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        signed int timeout
        double score
        unsigned long long legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, move
        unsigned int i, is_game_end = 0, int_color_next = 1, x, y
        signed int sign = -1
    # タイムアウト判定
    if t:
        timeout = check_timeout()
        if timeout:
            return timeout
    # 探索ノード数カウント
    measure_count += 1
    # 合法手を取得
    legal_moves_bits = _get_legal_moves_bits(int_color, bb, wb)
    # 前回パス and 打てる場所なし の場合ゲーム終了
    if pas and not legal_moves_bits:
        is_game_end = <unsigned int>1
    # 最大深さに到達 or ゲーム終了
    if not depth or is_game_end:
        if int_color:
            legal_moves_b_bits = legal_moves_bits
            legal_moves_w_bits = _get_legal_moves_bits(<unsigned int>0, bb, wb)
            sign = <signed int>1
            str_color = 'black'
        else:
            legal_moves_b_bits = _get_legal_moves_bits(<unsigned int>1, bb, wb)
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
        return evaluator.evaluate(str_color, board, _get_bit_count(legal_moves_b_bits), _get_bit_count(legal_moves_w_bits)) * sign
    # 次の手番
    if int_color:
        int_color_next = <unsigned int>0
    # パスの場合
    if not legal_moves_bits:
        return -_get_score(int_color_next, board, -beta, -alpha, depth, evaluator, t, <unsigned int>1)
    # 評価値を算出
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        _put_disc(int_color, move)
        score = -_get_score(int_color_next, board, -beta, -alpha, depth-1, evaluator, t, <unsigned int>0)
        _undo()
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする
        if score > alpha:
            alpha = score
        if timer_timeout:
            return alpha
        if alpha >= beta:  # 枝刈り
            return alpha
    return alpha


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


cdef inline unsigned long long _get_bit_count(unsigned long long bits):
    """_get_bit_count
    """
    bits = bits - (bits >> <unsigned int>1 & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + (bits >> <unsigned int>2 & <unsigned long long>0x3333333333333333)
    bits = (bits & <unsigned long long>0x0F0F0F0F0F0F0F0F) + (bits >> <unsigned int>4 & <unsigned long long>0x0F0F0F0F0F0F0F0F)
    bits = (bits & <unsigned long long>0x00FF00FF00FF00FF) + (bits >> <unsigned int>8 & <unsigned long long>0x00FF00FF00FF00FF)
    bits = (bits & <unsigned long long>0x0000FFFF0000FFFF) + (bits >> <unsigned int>16 & <unsigned long long>0x0000FFFF0000FFFF)
    return (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F


cdef inline void _put_disc(unsigned int int_color, unsigned long long move):
    """_put_disc
    """
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        unsigned long long count
        signed int lshift
    # ひっくり返せる石を取得
    fd = _get_flippable_discs_num(int_color, bb, wb, move)
    count = _get_bit_count(fd)
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


cdef inline unsigned long long _get_flippable_discs_num(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long move):
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned long long t_, rt, r_, rb, b_, lb, l_, lt
        unsigned long long bf_t_ = 0, bf_rt = 0, bf_r_ = 0, bf_rb = 0, bf_b_ = 0, bf_lb = 0, bf_l_ = 0, bf_lt = 0
        unsigned long long player = w, opponent = b, flippable_discs_num = 0
    if int_color:
        player = b
        opponent = w
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
    return flippable_discs_num


cdef inline void _undo():
    """_undo
    """
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, tail
    tail -= 1
    bb = pbb[tail]
    wb = pwb[tail]
    bs = pbs[tail]
    ws = pws[tail]
