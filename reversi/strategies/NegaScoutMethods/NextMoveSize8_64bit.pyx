#cython: language_level=3, profile=False, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""Next Move(Size8,64bit) of NegaScout
"""

import time

from reversi.strategies.common import Timer, Measure


cdef:
    unsigned long long measure_count
    double timer_deadline
    unsigned int timer_timeout
    signed int timer_timeout_value
    unsigned long long bb
    unsigned long long wb
    unsigned long long hb
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
    best_move, _ = _get_best_move(int_color, board, moves, alpha, beta, depth, evaluator, timer)
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return best_move


cdef inline _get_best_move_wrap(str color, board, moves, double alpha, double beta, int depth, evaluator, str pid, int timer, int measure):
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
    best_move, scores = _get_best_move(int_color, board, moves, alpha, beta, depth, evaluator, timer)
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return (best_move, scores)


cdef inline _get_best_move(unsigned int int_color, board, moves, double alpha, double beta, int depth, evaluator, int timer):
    global timer_timeout, bb, wb, hb, bs, ws
    cdef:
        double score = alpha
        unsigned int int_color_next = 1, board_bs, board_ws
        unsigned long long board_bb, board_wb
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
        score = -_get_score(int_color_next, board, -beta, -alpha, depth-1, evaluator, timer, <unsigned int>0)
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
    global timer_timeout, measure_count, bb, wb, hb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        double score, tmp, null_window
        unsigned long long legal_moves_b_bits, legal_moves_w_bits, legal_moves_bits, move
        unsigned int i, is_game_end = 0, int_color_next = 1, count = 0, index = 0
        signed int timeout, sign = -1
        unsigned long long[64] next_moves_list
        signed int[64] possibilities
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
        return -_get_score(int_color_next, board, -beta, -alpha, depth, evaluator, t, <unsigned int>1)
    # 着手可能数に応じて手を並び替え
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        next_moves_list[count] = move
        possibilities[count] = _get_possibility(int_color, bb, wb, move, sign)
        count += 1
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする
    _sort_moves_by_possibility(count, next_moves_list, possibilities)
    # 次の手の探索
    null_window = beta
    for i in range(count):
        if alpha < beta:
            _put_disc(int_color, next_moves_list[i])
            tmp = -_get_score(int_color_next, board, -null_window, -alpha, depth-1, evaluator, t, <unsigned int>0)
            _undo()
            if alpha < tmp:
                if tmp <= null_window and index:
                    _put_disc(int_color, next_moves_list[i])
                    alpha = -_get_score(int_color_next, board, -beta, -tmp, depth-1, evaluator, t, <unsigned int>0)
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


cdef inline signed int _get_possibility(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long move, signed int sign):
    """_get_possibility
    """
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


cdef inline void _sort_moves_by_possibility(unsigned int count, unsigned long long[64] next_moves_list, signed int[64] possibilities):
    """_sort_moves_by_possibility
    """
    cdef:
        unsigned int len1, len2, i
        unsigned long long[64] array_move1
        unsigned long long[64] array_move2
        signed int[64] array_p1
        signed int[64] array_p2
    if count > 1:
        len1 = <unsigned int>(count / 2)
        len2 = <unsigned int>(count - len1)
        for i in range(len1):
            array_move1[i] = next_moves_list[i]
            array_p1[i] = possibilities[i]
        for i in range(len2):
            array_move2[i] = next_moves_list[len1+i]
            array_p2[i] = possibilities[len1+i]
        _sort_moves_by_possibility(len1, array_move1, array_p1)
        _sort_moves_by_possibility(len2, array_move2, array_p2)
        _merge(len1, len2, array_move1, array_p1, array_move2, array_p2, next_moves_list, possibilities)


cdef inline void _merge(unsigned int len1, unsigned int len2, unsigned long long[64] array_move1, signed int[64] array_p1, unsigned long long[64] array_move2, signed int[64] array_p2, unsigned long long[64] next_moves_list, signed int[64] possibilities):
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


cdef inline unsigned long long _get_legal_moves_bits(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long h):
    """_get_legal_moves_bits
    """
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
    """_popcount
    """
    bits = bits - ((bits >> <unsigned int>1) & <unsigned long long>0x5555555555555555)
    bits = (bits & <unsigned long long>0x3333333333333333) + ((bits >> <unsigned int>2) & <unsigned long long>0x3333333333333333)
    bits = (bits + (bits >> <unsigned int>4)) & <unsigned long long>0x0F0F0F0F0F0F0F0F
    bits = bits + (bits >> <unsigned int>8)
    bits = bits + (bits >> <unsigned int>16)
    return (bits + (bits >> <unsigned int>32)) & <unsigned long long>0x000000000000007F


cdef inline void _put_disc(unsigned int int_color, unsigned long long move):
    """_put_disc
    """
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail
    cdef:
        unsigned long long count
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


cdef inline unsigned long long _get_flippable_discs_num(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long move):
    """_get_flippable_discs_num
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
