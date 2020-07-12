"""
ビットボードの情報取得処理
"""


def get_board_info(size, b, w):
    """
    ボードの情報(黒:1、白:-1、空き:0)を返す
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
