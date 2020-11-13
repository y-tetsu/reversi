"""Tests of external.py
"""

import unittest
from test.support import captured_stdout
import os

import reversi
from reversi.strategies.external import External
from reversi.board import BitBoard


def error_message(message):
    print(message)


def mainloop_check(message):
    print('mainloop_check')


class MainLoop:
    def mainloop(self):
        print('mainloop')


class TestExternal(unittest.TestCase):
    """external
    """
    def setUp(self):
        self.board1 = BitBoard()
        self.board2 = BitBoard()
        self.osname = os.name

        with open('./exit1.py', 'w') as wf:
            wf.write("import sys\n")
            wf.write("print('Error : exit(9)', file=sys.stderr)\n")
            wf.write("exit(9)\n")

        with open('./unexpected1.py', 'w') as wf:
            wf.write("print('unexpected1', end='')\n")

        with open('./unexpected2.py', 'w') as wf:
            wf.write("print('a b', end='')\n")

        with open('./topleft.py', 'w') as wf:
            wf.write("""import sys


BLANK, BLACK, WHITE = 0, 1, -1


def get_message():
    lines = sys.stdin.read().split('\\n')
    color = BLACK if int(lines.pop(0)) == 1 else WHITE
    size = int(lines.pop(0))
    board = [[int(i) for i in line.split()] for line in lines]

    return (color, size, board)


def get_legal_moves(color, size, board):
    legal_moves = {}

    for y in range(size):
        for x in range(size):
            reversibles = get_reversibles(color, size, board, x, y)

            if reversibles:
                legal_moves[(x, y)] = reversibles

    return legal_moves


def get_reversibles(color, size, board, x, y):
    # (-1,  1) (0,  1) (1,  1)
    # (-1,  0)         (1,  0)
    # (-1, -1) (0, -1) (1, -1)
    directions = [
        (-1,  1), (0,  1), (1,  1),
        (-1,  0),          (1,  0),
        (-1, -1), (0, -1), (1, -1)
    ]
    ret = []

    if in_range(size, x, y) and board[y][x] == BLANK:
        for direction in directions:
            tmp = get_reversibles_in_direction(color, size, board, x, y, direction)

            if tmp:
                ret += tmp

    return ret


def get_reversibles_in_direction(color, size, board, x, y, direction):
    ret = []
    next_x, next_y = x, y
    dx, dy = direction

    while True:
        next_x, next_y = next_x + dx, next_y + dy

        if in_range(size, next_x, next_y):
            next_value = board[next_y][next_x]

            if next_value != BLANK:
                if next_value == color:
                    return ret

                ret += [(next_x, next_y)]
            else:
                break
        else:
            break

    return []


def in_range(size, x, y):
    if 0 <= x < size and 0 <= y < size:
        return True

    return False


if __name__ == '__main__':
    # Get STDIN
    color, size, board = get_message()
    print(color, file=sys.stderr)
    print(size, file=sys.stderr)
    print(board, file=sys.stderr)

    # Get Legal Moves
    legal_moves = list(get_legal_moves(color, size, board).keys())
    print(legal_moves, file=sys.stderr)

    # Get top left edge
    x, y = legal_moves[0]

    # Output STDOUT
    print(x, y)
""")

        self.board2.put_disc('black', 3, 2)
        self.board2.put_disc('white', 2, 4)
        self.board2.put_disc('black', 5, 5)
        self.board2.put_disc('white', 4, 2)
        self.board2.put_disc('black', 5, 2)
        self.board2.put_disc('white', 5, 4)
        self.board2.put_disc('black', 4, 5)
        self.board2.put_disc('white', 5, 6)
        self.board2.put_disc('black', 4, 6)

    def tearDown(self):
        os.remove('./exit1.py')
        os.remove('./unexpected1.py')
        os.remove('./unexpected2.py')
        os.remove('./topleft.py')

    def test_external_init(self):
        external = External()
        self.assertEqual(external.cmd, None)
        self.assertEqual(external.timeouttime, reversi.strategies.external.TIMEOUT_TIME)

    def test_external_next_move_no_cmd_error(self):
        external = External()
        external.error_message = error_message

        move = None
        with captured_stdout() as stdout:
            move = external.next_move('black', self.board1)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "コマンドが設定されていません。")
        self.assertEqual(move, (self.board1.size//2-1, self.board1.size//2-1))

    def test_external_next_move_cmd_timeout_error(self):
        external = External('more')
        external.timeouttime = 0
        external.error_message = error_message

        move = None
        with captured_stdout() as stdout:
            move = external.next_move('black', self.board1)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "コマンドがタイムアウトしました。")
        self.assertEqual(move, (self.board1.size//2-1, self.board1.size//2-1))

    def test_external_next_move_cmd_illegal_finish_error(self):
        cmd = 'py -3.7 ./exit1.py' if self.osname == 'nt' else 'python ./exit1.py'
        external = External(cmd)
        external.error_message = error_message

        move = None
        with captured_stdout() as stdout:
            move = external.next_move('black', self.board1)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "プロセスが異常終了しました。終了ステータス(9)")
        self.assertEqual(lines[1], "(標準エラー出力)")
        self.assertEqual(lines[2], "Error : exit(9)")
        self.assertEqual(move, (self.board1.size//2-1, self.board1.size//2-1))

    def test_external_next_move_cmd_unexpected_output1_error(self):
        cmd = 'py -3.7 ./unexpected1.py' if self.osname == 'nt' else 'python ./unexpected1.py'
        external = External(cmd)
        external.error_message = error_message

        move = None
        with captured_stdout() as stdout:
            move = external.next_move('black', self.board1)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "プログラムからの戻り値が想定外でした(1)。戻り値(unexpected1)")
        self.assertEqual(move, (self.board1.size//2-1, self.board1.size//2-1))

    def test_external_next_move_cmd_unexpected_output2_error(self):
        cmd = 'py -3.7 ./unexpected2.py' if self.osname == 'nt' else 'python ./unexpected2.py'
        external = External(cmd)
        external.error_message = error_message

        move = None
        with captured_stdout() as stdout:
            move = external.next_move('black', self.board1)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "プログラムからの戻り値が想定外でした(2)。戻り値(a b)")
        self.assertEqual(move, (self.board1.size//2-1, self.board1.size//2-1))

    def test_external_next_move(self):
        cmd = 'py -3.7 ./topleft.py' if self.osname == 'nt' else 'python ./topleft.py'
        external = External(cmd)
        external.error_message = error_message

        self.assertEqual(external.next_move('white', self.board2), (2, 1))

    def test_external_error_message(self):
        external = External()
        external._mainloop = mainloop_check

        with captured_stdout() as stdout:
            external.error_message('test')

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "mainloop_check")

    def test_external_mainloop(self):
        external = External()

        with captured_stdout() as stdout:
            external._mainloop(MainLoop())

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "mainloop")
