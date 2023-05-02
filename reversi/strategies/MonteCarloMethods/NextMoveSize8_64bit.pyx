#cython: language_level=3, profile=False, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
"""Next Move(Size8,64bit) of MonteCarlo strategy
"""

import time

from reversi.strategies.common import Timer, Measure


cdef extern from "xorshift.h":
    void init_rand(unsigned long s)
    unsigned long rand_int()


cdef:
    unsigned long long measure_count
    unsigned long long[64] legal_moves_bit_list
    unsigned int[64] legal_moves_x
    unsigned int[64] legal_moves_y
    unsigned long long bb
    unsigned long long wb
    unsigned long long hb
    unsigned long long fd
    unsigned int bs
    unsigned int ws
    double timer_deadline
    unsigned int timer_timeout
    signed int timer_timeout_value
    signed int[64] scores


def next_move(color, board, count, pid, timer, measure):
    """next_move
    """
    if pid is None:
        timer, measure = False, False
    return _next_move(color, board, count, pid, timer, measure)


cdef inline tuple _next_move(str color, board, unsigned int count, str pid, int timer, int measure):
    global timer_deadline, timer_timeout, timer_timeout_value, measure_count, legal_moves_bit_list, scores, bb, wb, hb, bs, ws
    cdef:
        unsigned long long b, w, h
        unsigned int tbs
        unsigned int tws
        unsigned int int_color = 0
        unsigned int i, x, y, index = 0
        unsigned long long legal_moves, mask = 0x8000000000000000
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
                scores[index] = 0
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
            scores[i] += _playout(int_color, legal_moves_bit_list[i])
            # 探索ノード数カウント
            measure_count += 1
        if timer and check_timeout():
            break
    max_score = scores[0];
    best_move = (legal_moves_x[0], legal_moves_y[0])
    for i in range(index):
        if scores[i] > max_score:
            max_score = scores[i]
            best_move = (legal_moves_x[i], legal_moves_y[i])
    if measure and pid:
        Measure.count[pid] = measure_count
    if timer and pid and timer_timeout:
        Timer.timeout_flag[pid] = True  # タイムアウト発生
    return best_move


cdef inline signed int _playout(unsigned int int_color, unsigned long long move_bit):
    global bb, wb, hb, bs, ws
    cdef:
        unsigned int turn
        unsigned int x, y, pass_count = 0, random_index
        unsigned long long random_put, legal_moves_bits, count
        signed int ret
    # 1手打つ
    _put_disc(int_color, move_bit)
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
            _put_disc(turn, random_put)
    # 結果を返す
    ret = -2
    if (int_color and bs > ws) or (not int_color and ws > bs):
        ret = 2
    elif bs == ws:
        ret = 1
    return ret


cdef inline signed int check_timeout():
    """check_timeout
    """
    global timer_deadline, timer_timeout, timer_timeout_value
    if time.time() > timer_deadline:
        timer_timeout = <unsigned int>1
        return timer_timeout_value
    return <signed int>0


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
    """_get_flippable_discs_size8_64bit
    """
    cdef:
        unsigned long long t_, rt, r_, rb, b_, lb, l_, lt
        unsigned long long m_t_, m_rt, m_r_, m_rb, m_b_, m_lb, m_l_, m_lt
        unsigned long long player = w, opponent = b, flippable_discs_num = 0
    if int_color:
        player = b
        opponent = w
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
    for _ in range(5):
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