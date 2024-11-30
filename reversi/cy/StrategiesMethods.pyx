#cython: language_level=3, profile=False, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""Cython Strategies Methods
"""

import time

from reversi.strategies.common import Timer, Measure
from reversi.recorder import Recorder


DEF BEST_MATCH = 0
DEF BLACK_MAX = 1
DEF WHITE_MAX = 2
DEF BLACK_SHORTEST = 3
DEF WHITE_SHORTEST = 4

DEF SHORTEST_REWARD = 10000


cdef:
    unsigned long long measure_count
    unsigned long long bb
    unsigned long long wb
    unsigned long long rec_bb
    unsigned long long rec_wb
    unsigned long long hb
    unsigned long long fd
    unsigned long long[64] pbb
    unsigned long long[64] pwb
    unsigned long long[64] rec_pbb
    unsigned long long[64] rec_pwb
    unsigned int rol
    unsigned int rec
    unsigned int rec_depth
    unsigned int bs
    unsigned int ws
    unsigned int max_depth
    unsigned int start_depth
    unsigned int[64] pbs
    unsigned int[64] pws
    unsigned int[64] rec_pbs
    unsigned int[64] rec_pws
    unsigned int tail
    unsigned int is_timer_enabled
    double timer_deadline
    double rec_score
    unsigned int timer_timeout
    signed int timer_timeout_value
    signed int taker_sign


def endgame_next_move(color, board, depth, pid, timer, measure, role):
    """endgame_next_move
    """
    if pid is None:
        timer, measure = False, False
    return _next_move(color, board, depth, pid, timer, measure, role)


def endgame_get_best_move(color, board, moves, alpha, beta, depth, pid, timer, measure, role, recorder):
    """get_best_move
    """
    if pid is None:
        timer, measure = False, False
    return _get_best_move_wrap(color, board, moves, alpha, beta, depth, pid, timer, measure, role, recorder)


cdef inline tuple _next_move(str color, board, int depth, str pid, int timer, int measure, str role):
    global is_timer_enabled, timer_deadline, timer_timeout, timer_timeout_value, measure_count, bb, wb, hb, bs, ws, max_depth
    cdef:
        double alpha = -10000000, beta = 10000000
        unsigned int int_color = 0
        unsigned int x, y, i, index = 0
        unsigned long long legal_moves, mask = 0x8000000000000000
        unsigned long long[64] legal_moves_bit_list
        unsigned int[64] legal_moves_x
        unsigned int[64] legal_moves_y
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
    # 役割
    beta = _set_role(role, beta)
    # 最大深さ調整
    if depth > <int>(max_depth - (bs + ws)):
        depth =  <int>max_depth - (bs + ws)
    # 棋譜初期化(無効)
    _init_recorder(<unsigned int>0, depth)
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
    best_move, scores = _get_best_move(int_color, index, legal_moves_bit_list, legal_moves_x, legal_moves_y, alpha, beta, depth)
    # タイマーとメジャー格納
    if measure and pid:
        Measure.count[pid] = measure_count
    if is_timer_enabled and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return best_move


cdef inline _get_best_move_wrap(str color, board, moves, double alpha, double beta, int depth, str pid, int timer, int measure, str role, int recorder):
    global is_timer_enabled, timer_deadline, timer_timeout, timer_timeout_value, measure_count, bb, wb, hb, bs, ws, max_depth, rec, rec_depth, rec_bb, rec_wb, rec_pbb, rec_pbs, rec_pwb, rec_pws
    cdef:
        unsigned long long[64] moves_bit_list
        unsigned int[64] moves_x
        unsigned int[64] moves_y
        unsigned int x, y, i, index = 0, int_color = 0
        unsigned long long put
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
    # 役割
    beta = _set_role(role, beta)
    # 最大深さ調整
    if depth > <int>(max_depth - (bs + ws)):
        depth =  <int>max_depth - (bs + ws)
    # 棋譜初期化
    _init_recorder(recorder, depth)
    # 最善手を取得
    for x, y in moves:
        lshift = (63-(y*8+x))
        put = <unsigned long long>1 << lshift
        moves_bit_list[index] = put
        moves_x[index] = x
        moves_y[index] = y
        index += 1
    best_move, scores = _get_best_move(int_color, index, moves_bit_list, moves_x, moves_y, alpha, beta, depth)
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


cdef inline void _init_recorder(unsigned int recorder, unsigned int  depth):
    global rec, rec_score, rec_depth, start_depth, rec_bb, rec_wb, rec_pbb, rec_pwb, rec_pbs, rec_pws
    cdef:
        unsigned int i
    rec = recorder
    rec_score = <double>0
    rec_depth = <unsigned int>0
    rec_bb = <unsigned long long>0
    rec_wb = <unsigned long long>0
    for i in range(64):
        rec_pbb[i] = <unsigned long long>0
        rec_pwb[i] = <unsigned long long>0
        rec_pbs[i] = <unsigned int>0
        rec_pws[i] = <unsigned int>0
    start_depth = depth


cdef inline double _set_role(str role, double beta):
    global rol, hb, max_depth, taker_sign
    rol = BEST_MATCH
    max_depth = <unsigned int>64 - <unsigned int>_popcount(hb)
    if role != 'best_match':
        # TODO : MUCH_TAKER:確定石の場所を記憶し、相手が確定石に置く手を後回しにする
        if role == 'black_max':
            beta = <double>max_depth
            rol = BLACK_MAX
            taker_sign = <signed int>1
        elif role == 'white_max':
            beta = <double>max_depth
            rol = WHITE_MAX
            taker_sign = <signed int>-1
        elif role == 'black_shortest':
            beta = <double>SHORTEST_REWARD * 64
            rol = BLACK_SHORTEST
            taker_sign = <signed int>1
        elif role == 'white_shortest':
            beta = <double>SHORTEST_REWARD * 64
            rol = WHITE_SHORTEST
            taker_sign = <signed int>-1
    return beta


cdef inline _get_best_move(unsigned int int_color, unsigned int index, unsigned long long[64] moves_bit_list, unsigned int[64] moves_x, unsigned int[64] moves_y, double alpha, double beta, int depth):
    global timer_timeout, rol
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
        if rol == BEST_MATCH:
            score = -_get_score(int_color_next, -beta, -alpha, depth-1, <unsigned int>0)
        else:
            score = _get_score_taker(int_color_next, alpha, beta, depth-1, <unsigned int>0)
        _undo()
        scores[(moves_x[i], moves_y[i])] = score
        #print(moves_x[i], moves_y[i], score)
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


cdef inline double _get_score(unsigned int int_color, double alpha, double beta, unsigned int depth, unsigned int pas):
    """_get_score
    """
    global timer_timeout, measure_count, bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail, is_timer_enabled, max_depth
    cdef:
        signed int timeout
        double score
        unsigned long long legal_moves_bits, move, count
        unsigned int i, is_game_end = 0, int_color_next = 1, x, y
        signed int sign = -1
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
        return <double>((<double>bs - <double>ws) * <double>sign)
    # 次の手番
    if int_color:
        int_color_next = <unsigned int>0
    # パスの場合
    if not legal_moves_bits:
        return -_get_score(int_color_next, -beta, -alpha, depth, <unsigned int>1)
    # 最終1手
    if bs + ws == <unsigned int>(max_depth - 1):
        measure_count += 1
        count = _popcount(_get_flippable_discs_num(int_color, bb, wb, legal_moves_bits))
        if rol == BEST_MATCH:
            if int_color:
                return <double>(<double>bs - <double>ws + <double>(1 + count*2))
            else:
                return <double>-(<double>bs - <double>ws - <double>(1 + count*2))
    # 評価値を算出
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        _put_disc(int_color, move)
        score = -_get_score(int_color_next, -beta, -alpha, depth-1, <unsigned int>0)
        _undo()
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする
        if score > alpha:
            alpha = score
        if timer_timeout:
            return alpha
        if alpha >= beta:  # 枝刈り
            return alpha
    return alpha


cdef inline double _get_score_taker(unsigned int int_color, double alpha, double beta, unsigned int depth, unsigned int pas):
    """_get_score_taker
    """
    global timer_timeout, measure_count, bb, wb, bs, ws, pbb, pwb, pbs, pws, fd, tail, is_timer_enabled, rol, taker_sign, max_depth
    cdef:
        signed int timeout
        double score
        unsigned long long legal_moves_bits, move, count
        unsigned int i, is_game_end = 0, int_color_next = 1, x, y, reward
        signed int sign = -1
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
                    score = <double>((<double>bs - <double>ws) * taker_sign + <double>reward)
                    #print(depth, score, hex(bs), hex(ws))
                    _save_record(score, depth)
                    return score
        return <double>(<double>bs - <double>ws) * taker_sign
    # 次の手番
    if int_color:
        int_color_next = <unsigned int>0
    # パスの場合
    if not legal_moves_bits:
        return _get_score_taker(int_color_next, alpha, beta, depth, <unsigned int>1)
    # 最終1手
    if bs + ws == <unsigned int>(max_depth - 1):
        measure_count += 1
        count = _popcount(_get_flippable_discs_num(int_color, bb, wb, legal_moves_bits))
        if int_color:
            return <double>(<double>bs - <double>ws + <double>(1 + count*2)) * taker_sign
        else:
            return <double>(<double>bs - <double>ws - <double>(1 + count*2)) * taker_sign
    # 評価値を算出
    while (legal_moves_bits):
        move = legal_moves_bits & (~legal_moves_bits+1)  # 一番右のONしているビットのみ取り出す
        _put_disc(int_color, move)
        score = _get_score_taker(int_color_next, alpha, beta, depth-1, <unsigned int>0)
        _undo()
        legal_moves_bits ^= move  # 一番右のONしているビットをOFFする
        if score > alpha:
            alpha = score
        if timer_timeout:
            return alpha
        if alpha >= beta:  # 枝刈り
            return alpha
    return alpha


cdef inline void _save_record(double score, unsigned int depth):
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


cdef inline unsigned long long _get_flippable_discs_num(unsigned int int_color, unsigned long long b, unsigned long long w, unsigned long long move):
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned long long t_, rt, r_, rb, b_, lb, l_, lt
        unsigned long long m_t_, m_rt, m_r_, m_rb, m_b_, m_lb, m_l_, m_lt
        unsigned long long player = w, opponent = b, flippable_discs_num = 0
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
            other = 1;
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
            other = 1;
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
            other = 1;
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
    """_undo
    """
    global bb, wb, bs, ws, pbb, pwb, pbs, pws, tail
    tail -= 1
    bb = pbb[tail]
    wb = pwb[tail]
    bs = pbs[tail]
    ws = pws[tail]
