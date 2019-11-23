#!/usr/bin/env python
"""
ビットボードの情報取得処理
"""

def get_board_info(size, b, w):
    """
    ボードの情報(黒:1、白:-1、空き:0)を返す
    """
    if size == 8:
        return _get_board_info_size8(b, w)

    return _get_board_info(size, b, w)


cdef _get_board_info_size8(b, w):
    """
    ボードの情報(サイズ8限定)
    """
    cdef:
        unsigned int x, y
        unsigned int b0 = (b >> 32)& 0xFFFFFFFF
        unsigned int b1 = b & 0xFFFFFFFF
        unsigned int w0 = (w >> 32) & 0xFFFFFFFF
        unsigned int w1 = w & 0xFFFFFFFF
        unsigned int mask1 = 0x80000000
        unsigned int mask2 = 0x80000000

    board_info = []

    for y in range(8):
        tmp = []

        # ビットボード上位32bit
        if y < 4:
            for x in range(8):
                if b0 & mask1:
                    tmp.append(1)
                elif w0 & mask1:
                    tmp.append(-1)
                else:
                    tmp.append(0)
                mask1 >>= 1
        # ビットボード下位32bit
        else:
            for x in range(8):
                if b1 & mask2:
                    tmp.append(1)
                elif w1 & mask2:
                    tmp.append(-1)
                else:
                    tmp.append(0)
                mask2 >>= 1

        board_info.append(tmp)

    return board_info


cdef _get_board_info(size, b, w):
    """
    ボードの情報(サイズ8以外)
    """
    board_info = []
    mask = 1 << (size * size - 1)

    for y in range(size):
        tmp = []

        for x in range(size):
            if b & mask:
                tmp.append(1)
            elif w & mask:
                tmp.append(-1)
            else:
                tmp.append(0)
            mask >>= 1

        board_info.append(tmp)

    return board_info
