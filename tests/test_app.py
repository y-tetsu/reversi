"""Tests of app.py
"""

import unittest
from test.support import captured_stdin, captured_stdout
import os

from reversi import Reversi, Reversic, Window, ErrorMessage, MIN_BOARD_SIZE, MAX_BOARD_SIZE
from reversi.strategies import AbstractStrategy, WindowUserInput, ConsoleUserInput


class TestErrMsg:
    def show(self, message):
        print(message)


class TestApp(unittest.TestCase):
    """app
    """
    def setUp(self):
        with open('./not_json.json', 'w') as wf:
            wf.write('This is not a json file.\n')

        with open('./extra_file.json', 'w') as wf:
            wf.write('{\n')
            wf.write('    "name": "EXTERNAL",\n')
            wf.write('    "cmd": "cmd external",\n')
            wf.write('    "timeouttime": 10\n')
            wf.write('}\n')

    def tearDown(self):
        os.remove('./not_json.json')
        os.remove('./extra_file.json')

    # for Reversi
    def test_reversi_init(self):
        app = Reversi()
        self.assertEqual(app.state, app.INIT)
        self.assertIsInstance(app.window, Window)
        self.assertTrue('User1' in app.players_info)
        self.assertIsInstance(app.players_info['User1'], WindowUserInput)
        self.assertTrue('User2' in app.players_info)
        self.assertIsInstance(app.players_info['User2'], WindowUserInput)
        self.assertIsInstance(app.err_msg, ErrorMessage)
        self.assertEqual(app.turn_disc_wait, 0.1)
        self.assertEqual(app.sleep_time_play, 1.5)
        self.assertEqual(app.sleep_time_end, 0.01)
        self.assertEqual(app.sleep_time_turn, 0.3)
        self.assertEqual(app.sleep_time_move, 0.3)

    def test_reversi_keyword_arg(self):
        app = Reversi(turn_disc_wait=0.001, sleep_time_play=0.002, sleep_time_end=0.003, sleep_time_turn=0.004, sleep_time_move=0.005)
        self.assertEqual(app.turn_disc_wait, 0.001)
        self.assertEqual(app.sleep_time_play, 0.002)
        self.assertEqual(app.sleep_time_end, 0.003)
        self.assertEqual(app.sleep_time_turn, 0.004)
        self.assertEqual(app.sleep_time_move, 0.005)

    def test_reversi_state(self):
        app = Reversi()
        app.state = 'INIT'
        self.assertEqual(app.state, app.INIT)
        self.assertEqual(app.game, app._Reversi__init)

        app.state = 'DEMO'
        self.assertEqual(app.state, app.DEMO)
        self.assertEqual(app.game, app._Reversi__demo)

        app.state = 'PLAY'
        self.assertEqual(app.state, app.PLAY)
        self.assertEqual(app.game, app._Reversi__play)

        app.state = 'END'
        self.assertEqual(app.state, app.END)
        self.assertEqual(app.game, app._Reversi__end)

        app.state = 'REINIT'
        self.assertEqual(app.state, app.REINIT)
        self.assertEqual(app.game, app._Reversi__reinit)

        app.state = 'UNDEFINED'
        self.assertEqual(app.state, 'UNDEFINED')
        self.assertEqual(app.game, app._Reversi__reinit)

    def test_reversi_gameloop(self):
        def test_game():
            print('test_game')
            return True

        app = Reversi()
        app.game = test_game
        with captured_stdout() as stdout:
            app.gameloop()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'test_game')

    def test_reversi_start(self):
        def test_game_start():
            print('test_game_start')

        def test_window_start():
            print('test_window_start')

        app = Reversi()
        app.game_start = test_game_start
        app.window_start = test_window_start
        with captured_stdout() as stdout:
            app.start()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'test_game_start')
        self.assertEqual(lines[1], 'test_window_start')

    def test_reversi_game_start(self):
        def test_thread_start(game_thread):
            print(game_thread.daemon)

        app = Reversi()
        app._thread_start = test_thread_start
        with captured_stdout() as stdout:
            app.game_start()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'True')

    def test_reversi_thread_start(self):
        class TestThreadStart:
            def start(self):
                print('thread.start()')

        app = Reversi()
        with captured_stdout() as stdout:
            app._thread_start(TestThreadStart())

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'thread.start()')

    def test_reversi_window_start(self):
        class TestWindow:
            def __init__(self):
                class Root:
                    def deiconify(self):
                        print('deiconify')

                    def mainloop(self):
                        print('mainloop')

                self.root = Root()

        app = Reversi()
        app.window = TestWindow()
        with captured_stdout() as stdout:
            app.window_start()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'deiconify')
        self.assertEqual(lines[1], 'mainloop')

    def test_reversi__init(self):
        class TestWindow:
            def __init__(self):
                self.extra_file = None

            def init_screen(self):
                print('init_screen')

            def set_state(self, state):
                print(state)

        def _load_extra_file(extra_file):
            print(extra_file)

        # no extra_file
        app = Reversi()
        app.window = TestWindow()
        app._load_extra_file = _load_extra_file
        with captured_stdout() as stdout:
            app._Reversi__init()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'init_screen')
        self.assertEqual(lines[1], 'normal')
        with self.assertRaises(IndexError):
            print(lines[2])
        self.assertEqual(app.state, Reversi.DEMO)

        # extra_file
        app = Reversi()
        app.window = TestWindow()
        app.window.extra_file = 'extra_file'
        app._load_extra_file = _load_extra_file
        with captured_stdout() as stdout:
            app._Reversi__init()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'init_screen')
        self.assertEqual(lines[1], 'normal')
        self.assertEqual(lines[2], 'extra_file')
        self.assertEqual(app.window.extra_file, '')
        self.assertEqual(app.state, Reversi.DEMO)

    def test_reversi_load_extra_file_no_file_error(self):
        app = Reversi()
        app.err_msg = TestErrMsg()
        with captured_stdout() as stdout:
            app._load_extra_file('./no_file')

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], '指定された登録ファイルが見つかりませんでした')

    def test_reversi_load_extra_file_format_error(self):
        app = Reversi()
        app.err_msg = TestErrMsg()
        with captured_stdout() as stdout:
            app._load_extra_file('./not_json.json')

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'フォーマットエラーのため登録ファイルが読み込めませんでした')

    def test_reversi_load_extra_file(self):
        app = Reversi()
        app._load_extra_file('./extra_file.json')

        self.assertEqual(app.players_info['EXTERNAL'].cmd, 'cmd external')
        self.assertEqual(app.players_info['EXTERNAL'].timeouttime, 10)

    def test_reversi__demo(self):
        class TestWindow:
            def __init__(self):
                class Start:
                    def __init__(self):
                        class Event:
                            def __init__(self):
                                self.is_set = None

                            def clear(self):
                                print('clear')

                        self.event = Event()
                self.start = Start()

        def demo_animation_false():
            return False

        app = Reversi()
        app.window = TestWindow()

        # event is_set True and demo_anumation_true
        app.window.start.event.is_set = lambda: True
        with captured_stdout() as stdout:
            app._Reversi__demo()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'clear')
        self.assertEqual(app.state, Reversi.PLAY)

        # event is_set False and demo_anumation_false
        app.window.start.event.is_set = lambda: False
        app._demo_animation = demo_animation_false
        with captured_stdout() as stdout:
            app._Reversi__demo()

        lines = stdout.getvalue().splitlines()
        with self.assertRaises(IndexError):
            print(lines[0])
        self.assertEqual(app.state, Reversi.INIT)

    def test_reversi_demo_animation(self):
        class TestWindow:
            def __init__(self):
                class Board:
                    def __init__(self):
                        self.size = 8

                    def remove_disc(self, color, x, y):
                        print('remove_disc', color, x, y)

                    def put_disc(self, color, x, y):
                        print('put_disc', color, x, y)

                self.board = Board()

        app = Reversi(turn_disc_wait=0.001)
        app.window = TestWindow()

        # setting_changed Falase
        app._setting_changed = lambda: False
        with captured_stdout() as stdout:
            ret = app._demo_animation()

        lines = stdout.getvalue().splitlines()

        self.assertEqual(lines[0], 'remove_disc black 4 3')
        self.assertEqual(lines[1], 'put_disc turnblack 4 3')
        self.assertEqual(lines[2], 'remove_disc turnblack 4 3')
        self.assertEqual(lines[3], 'put_disc white 4 3')
        self.assertEqual(lines[4], 'remove_disc white 4 3')
        self.assertEqual(lines[5], 'put_disc turnwhite 4 3')
        self.assertEqual(lines[6], 'remove_disc turnwhite 4 3')
        self.assertEqual(lines[7], 'put_disc black 4 3')
        self.assertEqual(lines[8], 'remove_disc black 3 4')
        self.assertEqual(lines[9], 'put_disc turnblack 3 4')
        self.assertEqual(lines[10], 'remove_disc turnblack 3 4')
        self.assertEqual(lines[11], 'put_disc white 3 4')
        self.assertEqual(lines[12], 'remove_disc white 3 4')
        self.assertEqual(lines[13], 'put_disc turnwhite 3 4')
        self.assertEqual(lines[14], 'remove_disc turnwhite 3 4')
        self.assertEqual(lines[15], 'put_disc black 3 4')
        self.assertEqual(lines[16], 'remove_disc white 3 3')
        self.assertEqual(lines[17], 'put_disc turnwhite 3 3')
        self.assertEqual(lines[18], 'remove_disc turnwhite 3 3')
        self.assertEqual(lines[19], 'put_disc black 3 3')
        self.assertEqual(lines[20], 'remove_disc black 3 3')
        self.assertEqual(lines[21], 'put_disc turnblack 3 3')
        self.assertEqual(lines[22], 'remove_disc turnblack 3 3')
        self.assertEqual(lines[23], 'put_disc white 3 3')
        self.assertEqual(lines[24], 'remove_disc white 4 4')
        self.assertEqual(lines[25], 'put_disc turnwhite 4 4')
        self.assertEqual(lines[26], 'remove_disc turnwhite 4 4')
        self.assertEqual(lines[27], 'put_disc black 4 4')
        self.assertEqual(lines[28], 'remove_disc black 4 4')
        self.assertEqual(lines[29], 'put_disc turnblack 4 4')
        self.assertEqual(lines[30], 'remove_disc turnblack 4 4')
        self.assertEqual(lines[31], 'put_disc white 4 4')

        with self.assertRaises(IndexError):
            print(lines[32])

        self.assertEqual(ret, True)

        # setting_changed True
        app._setting_changed = lambda: True
        with captured_stdout() as stdout:
            ret = app._demo_animation()

        lines = stdout.getvalue().splitlines()

        with self.assertRaises(IndexError):
            print(lines[0])

        self.assertEqual(ret, False)

    def test_reversi__play(self):
        class TestWindow:
            def __init__(self):
                class Board:
                    def __init__(self):
                        self.size = 4

                    def enable_moves(self, moves):
                        print('enable_moves', moves)

                    def disable_moves(self, moves):
                        print('disable_moves', moves)

                    def enable_move(self, x, y):
                        print('enable_move', x, y)

                    def disable_move(self, x, y):
                        print('disable_move', x, y)

                    def put_disc(self, color, x, y):
                        print('put_disc', color, x, y)

                    def turn_disc(self, color, captures):
                        print('put_disc', color, captures)

                class Menu:
                    def __init__(self):
                        class Event:
                            def is_set(self):
                                return False

                        self.event = Event()

                class Info:
                    def set_text(self, color, text, score):
                        print('set_text', color, text, score)

                    def set_turn_text_on(self, color):
                        print('set_turn_text_on', color)

                    def set_turn_text_off(self, color):
                        print('set_turn_text_off', color)

                    def set_move_text_on(self, color, x, y):
                        print('set_move_text_on', color, x, y)

                    def set_move_text_off(self, color):
                        print('set_move_text_off', color)

                    def set_win_text_on(self, color):
                        print('set_win_text_on', color)

                    def set_lose_text_on(self, color):
                        print('set_lose_text_on', color)

                self.board = Board()
                self.menu = Menu()
                self.player = {'black': 'WhiteWin', 'white': 'WhiteWin'}
                self.cputime = 0.1
                self.info = Info()

            def set_state(self, state):
                print(state)

        class WhiteWin(AbstractStrategy):
            def next_move(self, color, board):
                depth = board._black_score + board._white_score - 4
                move = None
                if depth == 0:
                    move = (1, 0)
                elif depth == 1:
                    move = (0, 0)
                elif depth == 2:
                    move = (0, 1)
                elif depth == 3:
                    move = (2, 0)
                elif depth == 4:
                    move = (3, 0)
                elif depth == 5:
                    move = (0, 2)
                elif depth == 6:
                    move = (0, 3)
                elif depth == 7:
                    move = (3, 2)
                elif depth == 8:
                    move = (2, 3)

                return move

        app = Reversi(sleep_time_play=0.001, sleep_time_turn=0.001, sleep_time_move=0.001)
        app.window = TestWindow()
        app.players_info = {'WhiteWin': WhiteWin()}

        with captured_stdout() as stdout:
            app._Reversi__play()

        lines = stdout.getvalue().splitlines()

        self.assertEqual(lines[0], 'disable')
        self.assertEqual(lines[1], 'set_text black score 2')
        self.assertEqual(lines[2], 'set_text white score 2')
        self.assertEqual(lines[3], 'set_turn_text_on black')
        self.assertEqual(lines[4], 'enable_moves [(1, 0), (0, 1), (3, 2), (2, 3)]')
        self.assertEqual(lines[5], 'set_turn_text_off black')
        self.assertEqual(lines[6], 'set_move_text_off black')
        self.assertEqual(lines[7], 'set_turn_text_off white')
        self.assertEqual(lines[8], 'set_move_text_off white')
        self.assertEqual(lines[9], 'disable_moves [(1, 0), (0, 1), (3, 2), (2, 3)]')
        self.assertEqual(lines[10], 'enable_move 1 0')
        self.assertEqual(lines[11], 'put_disc black 1 0')
        self.assertEqual(lines[12], 'set_move_text_on black b 1')
        self.assertEqual(lines[13], 'put_disc black [(1, 1)]')
        self.assertEqual(lines[14], 'set_text black score 4')
        self.assertEqual(lines[15], 'set_text white score 1')
        self.assertEqual(lines[16], 'set_turn_text_on white')
        self.assertEqual(lines[17], 'enable_moves [(0, 0), (2, 0), (0, 2)]')
        self.assertEqual(lines[18], 'set_turn_text_off black')
        self.assertEqual(lines[19], 'set_move_text_off black')
        self.assertEqual(lines[20], 'set_turn_text_off white')
        self.assertEqual(lines[21], 'set_move_text_off white')
        self.assertEqual(lines[22], 'disable_moves [(0, 0), (2, 0), (0, 2)]')
        self.assertEqual(lines[23], 'disable_move 1 0')
        self.assertEqual(lines[24], 'enable_move 0 0')
        self.assertEqual(lines[25], 'put_disc white 0 0')
        self.assertEqual(lines[26], 'set_move_text_on white a 1')
        self.assertEqual(lines[27], 'put_disc white [(1, 1)]')
        self.assertEqual(lines[28], 'set_text black score 3')
        self.assertEqual(lines[29], 'set_text white score 3')
        self.assertEqual(lines[30], 'set_turn_text_on black')
        self.assertEqual(lines[31], 'enable_moves [(0, 1), (3, 2), (2, 3)]')
        self.assertEqual(lines[32], 'set_turn_text_off black')
        self.assertEqual(lines[33], 'set_move_text_off black')
        self.assertEqual(lines[34], 'set_turn_text_off white')
        self.assertEqual(lines[35], 'set_move_text_off white')
        self.assertEqual(lines[36], 'disable_moves [(0, 1), (3, 2), (2, 3)]')
        self.assertEqual(lines[37], 'disable_move 0 0')
        self.assertEqual(lines[38], 'enable_move 0 1')
        self.assertEqual(lines[39], 'put_disc black 0 1')
        self.assertEqual(lines[40], 'set_move_text_on black a 2')
        self.assertEqual(lines[41], 'put_disc black [(1, 1)]')
        self.assertEqual(lines[42], 'set_text black score 5')
        self.assertEqual(lines[43], 'set_text white score 2')
        self.assertEqual(lines[44], 'set_turn_text_on white')
        self.assertEqual(lines[45], 'enable_moves [(2, 0), (0, 2)]')
        self.assertEqual(lines[46], 'set_turn_text_off black')
        self.assertEqual(lines[47], 'set_move_text_off black')
        self.assertEqual(lines[48], 'set_turn_text_off white')
        self.assertEqual(lines[49], 'set_move_text_off white')
        self.assertEqual(lines[50], 'disable_moves [(2, 0), (0, 2)]')
        self.assertEqual(lines[51], 'disable_move 0 1')
        self.assertEqual(lines[52], 'enable_move 2 0')
        self.assertEqual(lines[53], 'put_disc white 2 0')
        self.assertEqual(lines[54], 'set_move_text_on white c 1')
        self.assertEqual(lines[55], 'put_disc white [(1, 0), (2, 1)]')
        self.assertEqual(lines[56], 'set_text black score 3')
        self.assertEqual(lines[57], 'set_text white score 5')
        self.assertEqual(lines[58], 'set_turn_text_on black')
        self.assertEqual(lines[59], 'enable_moves [(3, 0), (3, 1), (3, 2), (3, 3)]')
        self.assertEqual(lines[60], 'set_turn_text_off black')
        self.assertEqual(lines[61], 'set_move_text_off black')
        self.assertEqual(lines[62], 'set_turn_text_off white')
        self.assertEqual(lines[63], 'set_move_text_off white')
        self.assertEqual(lines[64], 'disable_moves [(3, 0), (3, 1), (3, 2), (3, 3)]')
        self.assertEqual(lines[65], 'disable_move 2 0')
        self.assertEqual(lines[66], 'enable_move 3 0')
        self.assertEqual(lines[67], 'put_disc black 3 0')
        self.assertEqual(lines[68], 'set_move_text_on black d 1')
        self.assertEqual(lines[69], 'put_disc black [(2, 1)]')
        self.assertEqual(lines[70], 'set_text black score 5')
        self.assertEqual(lines[71], 'set_text white score 4')
        self.assertEqual(lines[72], 'set_turn_text_on white')
        self.assertEqual(lines[73], 'enable_moves [(0, 2), (3, 2), (1, 3)]')
        self.assertEqual(lines[74], 'set_turn_text_off black')
        self.assertEqual(lines[75], 'set_move_text_off black')
        self.assertEqual(lines[76], 'set_turn_text_off white')
        self.assertEqual(lines[77], 'set_move_text_off white')
        self.assertEqual(lines[78], 'disable_moves [(0, 2), (3, 2), (1, 3)]')
        self.assertEqual(lines[79], 'disable_move 3 0')
        self.assertEqual(lines[80], 'enable_move 0 2')
        self.assertEqual(lines[81], 'put_disc white 0 2')
        self.assertEqual(lines[82], 'set_move_text_on white a 3')
        self.assertEqual(lines[83], 'put_disc white [(0, 1), (1, 1), (1, 2)]')
        self.assertEqual(lines[84], 'set_text black score 2')
        self.assertEqual(lines[85], 'set_text white score 8')
        self.assertEqual(lines[86], 'set_turn_text_on black')
        self.assertEqual(lines[87], 'enable_moves [(0, 3), (2, 3)]')
        self.assertEqual(lines[88], 'set_turn_text_off black')
        self.assertEqual(lines[89], 'set_move_text_off black')
        self.assertEqual(lines[90], 'set_turn_text_off white')
        self.assertEqual(lines[91], 'set_move_text_off white')
        self.assertEqual(lines[92], 'disable_moves [(0, 3), (2, 3)]')
        self.assertEqual(lines[93], 'disable_move 0 2')
        self.assertEqual(lines[94], 'enable_move 0 3')
        self.assertEqual(lines[95], 'put_disc black 0 3')
        self.assertEqual(lines[96], 'set_move_text_on black a 4')
        self.assertEqual(lines[97], 'put_disc black [(1, 2)]')
        self.assertEqual(lines[98], 'set_text black score 4')
        self.assertEqual(lines[99], 'set_text white score 7')
        self.assertEqual(lines[100], 'set_turn_text_on white')
        self.assertEqual(lines[101], 'enable_moves [(3, 1), (3, 2), (1, 3), (2, 3)]')
        self.assertEqual(lines[102], 'set_turn_text_off black')
        self.assertEqual(lines[103], 'set_move_text_off black')
        self.assertEqual(lines[104], 'set_turn_text_off white')
        self.assertEqual(lines[105], 'set_move_text_off white')
        self.assertEqual(lines[106], 'disable_moves [(3, 1), (3, 2), (1, 3), (2, 3)]')
        self.assertEqual(lines[107], 'disable_move 0 3')
        self.assertEqual(lines[108], 'enable_move 3 2')
        self.assertEqual(lines[109], 'put_disc white 3 2')
        self.assertEqual(lines[110], 'set_move_text_on white d 3')
        self.assertEqual(lines[111], 'put_disc white [(2, 1)]')
        self.assertEqual(lines[112], 'set_text black score 3')
        self.assertEqual(lines[113], 'set_text white score 9')
        self.assertEqual(lines[114], 'set_turn_text_on white')
        self.assertEqual(lines[115], 'enable_moves [(1, 3), (2, 3)]')
        self.assertEqual(lines[116], 'set_turn_text_off black')
        self.assertEqual(lines[117], 'set_move_text_off black')
        self.assertEqual(lines[118], 'set_turn_text_off white')
        self.assertEqual(lines[119], 'set_move_text_off white')
        self.assertEqual(lines[120], 'disable_moves [(1, 3), (2, 3)]')
        self.assertEqual(lines[121], 'disable_move 3 2')
        self.assertEqual(lines[122], 'enable_move 2 3')
        self.assertEqual(lines[123], 'put_disc white 2 3')
        self.assertEqual(lines[124], 'set_move_text_on white c 4')
        self.assertEqual(lines[125], 'put_disc white [(1, 2)]')
        self.assertEqual(lines[126], 'set_text black score 2')
        self.assertEqual(lines[127], 'set_text white score 11')
        self.assertEqual(lines[128], 'set_win_text_on white')
        self.assertEqual(lines[129], 'set_lose_text_on black')

        with self.assertRaises(IndexError):
            print(lines[131])

        self.assertEqual(app.state, Reversi.END)

    def test_reversi__end(self):
        class TestWindow:
            def __init__(self):
                class Start:
                    def __init__(self):
                        class Event:
                            def is_set(self):
                                return True

                            def clear(self):
                                print('clear')

                        self.event = Event()

                self.start = Start()

            def set_state(self, state):
                print(state)

        app = Reversi()
        app.window = TestWindow()

        # REINIT
        app._setting_changed = lambda: False

        with captured_stdout() as stdout:
            app._Reversi__end()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'normal')
        self.assertEqual(lines[1], 'clear')

        with self.assertRaises(IndexError):
            print(lines[2])

        self.assertEqual(app.state, Reversi.REINIT)

        # INIT
        app.window.start.event.is_set = lambda: False
        app._setting_changed = lambda: True

        with captured_stdout() as stdout:
            app._Reversi__end()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'normal')

        with self.assertRaises(IndexError):
            print(lines[1])

        self.assertEqual(app.state, Reversi.INIT)

    def test_reversi__reinit(self):
        class TestWindow:
            def init_screen(self):
                print('init_screen')

        app = Reversi()
        app.window = TestWindow()

        with captured_stdout() as stdout:
            app._Reversi__reinit()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'init_screen')

        with self.assertRaises(IndexError):
            print(lines[1])

        self.assertEqual(app.state, Reversi.PLAY)

    def test_reversi_setting_changed(self):
        class TestWindow:
            def __init__(self):
                class Menu:
                    def __init__(self):
                        class Event:
                            def is_set(self):
                                return False

                            def clear(self):
                                print('clear')

                        self.event = Event()
                        self.size = 8
                        self.black_player = 'BLACK2'
                        self.white_player = 'WHITE2'
                        self.assist = True
                        self.language = 'Japanese'

                self.menu = Menu()

                self.size = 4
                self.player = {'black': 'BLACK', 'white': 'WHITE'}
                self.assist = False
                self.language = 'English'

        app = Reversi()
        app.window = TestWindow()

        # return False
        with captured_stdout() as stdout:
            ret = app._setting_changed()

        lines = stdout.getvalue().splitlines()

        with self.assertRaises(IndexError):
            print(lines[0])

        self.assertEqual(app.window.size, 4)
        self.assertEqual(app.window.player['black'], 'BLACK')
        self.assertEqual(app.window.player['white'], 'WHITE')
        self.assertEqual(app.window.assist, False)
        self.assertEqual(app.window.language, 'English')
        self.assertEqual(ret, False)

        # return True
        app.window.menu.event.is_set = lambda: True

        with captured_stdout() as stdout:
            ret = app._setting_changed()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'clear')

        with self.assertRaises(IndexError):
            print(lines[1])

        self.assertEqual(app.window.size, 8)
        self.assertEqual(app.window.player['black'], 'BLACK2')
        self.assertEqual(app.window.player['white'], 'WHITE2')
        self.assertEqual(app.window.assist, True)
        self.assertEqual(app.window.language, 'Japanese')
        self.assertEqual(ret, True)

    # for Reversic
    def test_reversic_init(self):
        app = Reversic()
        self.assertEqual(app.board_type, 'Square-8')
        self.assertEqual(app.player_names, {'black': 'User1', 'white': 'User2'})
        self.assertEqual(app.state, app.START)
        self.assertTrue('User1' in app.players_info['black'])
        self.assertIsInstance(app.players_info['black']['User1'], ConsoleUserInput)
        self.assertTrue('User2' in app.players_info['white'])
        self.assertIsInstance(app.players_info['white']['User2'], ConsoleUserInput)
        self.assertEqual(app.sleep_time_play, 2)
        self.assertEqual(app.sleep_time_turn, 1)
        self.assertEqual(app.sleep_time_move, 1)

    def test_reversic_keyword_arg(self):
        app = Reversic(sleep_time_play=0.001, sleep_time_turn=0.002, sleep_time_move=0.003)
        self.assertEqual(app.sleep_time_play, 0.001)
        self.assertEqual(app.sleep_time_turn, 0.002)
        self.assertEqual(app.sleep_time_move, 0.003)

    def test_reversic_state(self):
        app = Reversic()
        app.state = 'START'
        self.assertEqual(app.state, app.START)
        self.assertEqual(app.game, app._Reversic__start)

        app.state = 'MENU'
        self.assertEqual(app.state, app.MENU)
        self.assertEqual(app.game, app._Reversic__menu)

        app.state = 'PLAY'
        self.assertEqual(app.state, app.PLAY)
        self.assertEqual(app.game, app._Reversic__play)

        app.state = 'ANOTHER'
        self.assertEqual(app.state, 'ANOTHER')
        self.assertEqual(app.game, app._Reversic__play)

    def test_reversic_start(self):
        def test_game():
            x = 0

            def _test_game():
                nonlocal x
                print('test_game', x)
                if x > 1:
                    return True
                x += 1
                return False

            return _test_game

        app = Reversic()
        app.game = test_game()
        with captured_stdout() as stdout:
            app.start()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'test_game 0')
        self.assertEqual(lines[1], 'test_game 1')
        self.assertEqual(lines[2], 'test_game 2')
        with self.assertRaises(IndexError):
            print(lines[3])

    def test_reversic__start(self):
        app = Reversic()
        with captured_stdout() as stdout:
            app._Reversic__start()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], '')
        self.assertEqual(lines[1], '=============================')
        self.assertEqual(lines[2], 'BoardType   = Square-8')
        self.assertEqual(lines[3], 'BlackPlayer = User1')
        self.assertEqual(lines[4], 'WhitePlayer = User2')
        self.assertEqual(lines[5], '=============================')
        self.assertEqual(lines[6], '')
        with self.assertRaises(IndexError):
            print(lines[7])

        self.assertEqual(app.state, Reversic.MENU)

    def test_reversic__menu(self):
        app = Reversic()
        app.players_info = {'black': 'BLACK', 'white': 'WHITE'}
        app._get_board_size = lambda: 26
        app._get_player = lambda x: x

        # play
        app.state = None
        with captured_stdout() as stdout:
            with captured_stdin() as stdin:
                stdin.write('\n')
                stdin.seek(0)
                app._Reversic__menu()

        lines = stdout.getvalue().splitlines()

        def check_header(self, lines):
            self.assertEqual(lines[0], 'press any key')
            self.assertEqual(lines[1], '-----------------------------')
            self.assertEqual(lines[2], ' enter  : start game')
            self.assertEqual(lines[3], ' t      : change board type')
            self.assertEqual(lines[4], ' b      : change black player')
            self.assertEqual(lines[5], ' w      : change white player')
            self.assertEqual(lines[6], ' q      : quit')
            self.assertEqual(lines[7], '-----------------------------')

        check_header(self, lines)
        self.assertEqual(lines[8], '>> ')
        with self.assertRaises(IndexError):
            print(lines[9])

        self.assertEqual(app.state, Reversic.PLAY)

        # black
        app.state = None
        with captured_stdout() as stdout:
            with captured_stdin() as stdin:
                stdin.write('b')
                stdin.seek(0)
                app._Reversic__menu()

        lines = stdout.getvalue().splitlines()
        check_header(self, lines)
        self.assertEqual(lines[8], '>> ')
        with self.assertRaises(IndexError):
            print(lines[9])

        self.assertEqual(app.player_names['black'], 'BLACK')
        self.assertEqual(app.state, Reversic.START)

        # white
        app.state = None
        with captured_stdout() as stdout:
            with captured_stdin() as stdin:
                stdin.write('w')
                stdin.seek(0)
                app._Reversic__menu()

        lines = stdout.getvalue().splitlines()
        check_header(self, lines)
        self.assertEqual(lines[8], '>> ')
        with self.assertRaises(IndexError):
            print(lines[9])

        self.assertEqual(app.player_names['white'], 'WHITE')
        self.assertEqual(app.state, Reversic.START)

        # invalid keyword & quit
        app.state = None
        ret = False
        with captured_stdout() as stdout:
            with captured_stdin() as stdin:
                stdin.write('invalid keyword\nq')
                stdin.seek(0)
                ret = app._Reversic__menu()

        lines = stdout.getvalue().splitlines()
        check_header(self, lines)
        self.assertEqual(lines[8], '>> >> See you!')
        with self.assertRaises(IndexError):
            print(lines[9])

        self.assertTrue(ret)
        self.assertIsNone(app.state)

    def test_reversic_get_board_type(self):
        app = Reversic()

        # normal pattern
        for i, _ in enumerate(Reversic.BOARDS.keys()):
            with captured_stdout() as stdout:
                with captured_stdin() as stdin:
                    stdin.write(str(i+1))
                    stdin.seek(0)
                    ret = app._get_board_type()

            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines[0], 'select board type')
            self.assertEqual(lines[1], '-----------------------------')
            self.assertEqual(lines[2], '  1 : X')
            self.assertEqual(lines[3], '  2 : x')
            self.assertEqual(lines[4], '  3 : Square-8')
            self.assertEqual(lines[5], '  4 : Square-6')
            self.assertEqual(lines[6], '  5 : Square-4')
            self.assertEqual(lines[7], '  6 : Octagon')
            self.assertEqual(lines[8], '  7 : Diamond')
            self.assertEqual(lines[9], '  8 : Clover')
            self.assertEqual(lines[10], '  9 : Cross')
            self.assertEqual(lines[11], ' 10 : Plus')
            self.assertEqual(lines[12], ' 11 : Drone')
            self.assertEqual(lines[13], ' 12 : Kazaguruma')
            self.assertEqual(lines[14], ' 13 : Manji')
            self.assertEqual(lines[15], ' 14 : Rectangle')
            self.assertEqual(lines[16], ' 15 : T')
            self.assertEqual(lines[17], ' 16 : Torus')
            self.assertEqual(lines[18], ' 17 : Two')
            self.assertEqual(lines[19], ' 18 : Equal')
            self.assertEqual(lines[20], ' 19 : Xhole')
            self.assertEqual(lines[21], '-----------------------------')
            self.assertEqual(lines[22], '>> ')
            with self.assertRaises(IndexError):
                print(lines[23])

            self.assertEqual(ret, list(Reversic.BOARDS.keys())[i])

    def test_reversic_get_player(self):
        app = Reversic()
        test_players = {'Test1': None, 'Test2': None}

        # normal pattern
        for i in range(1, 3):
            with captured_stdout() as stdout:
                with captured_stdin() as stdin:
                    stdin.write(str(i))
                    stdin.seek(0)
                    ret = app._get_player(test_players)

            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines[0], 'select number for player')
            self.assertEqual(lines[1], '-----------------------------')
            self.assertEqual(lines[2], '  1 : Test1')
            self.assertEqual(lines[3], '  2 : Test2')
            self.assertEqual(lines[4], '-----------------------------')
            self.assertEqual(lines[5], '>> ')
            with self.assertRaises(IndexError):
                print(lines[6])

            self.assertEqual(ret, list(test_players.keys())[i-1])

        # illegal pattern
        for i in range(0, 4, 3):
            with captured_stdout() as stdout:
                with captured_stdin() as stdin:
                    stdin.write(str(i) + '\n' + str(1))
                    stdin.seek(0)
                    ret = app._get_player(test_players)

            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines[0], 'select number for player')
            self.assertEqual(lines[1], '-----------------------------')
            self.assertEqual(lines[2], '  1 : Test1')
            self.assertEqual(lines[3], '  2 : Test2')
            self.assertEqual(lines[4], '-----------------------------')
            self.assertEqual(lines[5], '>> >> ')
            with self.assertRaises(IndexError):
                print(lines[6])

            self.assertEqual(ret, 'Test1')

        with captured_stdout() as stdout:
            with captured_stdin() as stdin:
                stdin.write('a\n08\n１\nあ\n' + str(2))
                stdin.seek(0)
                ret = app._get_player(test_players)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'select number for player')
        self.assertEqual(lines[1], '-----------------------------')
        self.assertEqual(lines[2], '  1 : Test1')
        self.assertEqual(lines[3], '  2 : Test2')
        self.assertEqual(lines[4], '-----------------------------')
        self.assertEqual(lines[5], '>> >> >> >> >> ')
        with self.assertRaises(IndexError):
            print(lines[6])

        self.assertEqual(ret, 'Test2')

    def test_reversic__play(self):
        class BlackFoul(AbstractStrategy):
            def next_move(self, color, board):
                depth = board._black_score + board._white_score - 4
                move = None
                if depth == 0:
                    move = (0, 0)

                return move

        app = Reversic({'BLACK_FOUL': BlackFoul()}, sleep_time_play=0.001, sleep_time_turn=0.001, sleep_time_move=0.001)
        app.player_names = {'black': 'BLACK_FOUL', 'white': 'BLACK_FOUL'}
        app.board_type = 'X'
        app.state = None
        with captured_stdout() as stdout:
            app._Reversic__play()

        lines = stdout.getvalue().splitlines()
        expected = """
〇BLACK_FOUL:2 ●BLACK_FOUL:2
   a b c d e f g h
 1□□　　　　□□
 2□□□　　□□□
 3　　□□□□　　
 4　　　●〇　　　
 5　　　〇●　　　
 6　　□□□□　　
 7□□□　　□□□
 8□□　　　　□□

〇BLACK_FOUL's turn
 1: ('d', '3')
 2: ('e', '6')
putted on ('a', '1')

〇BLACK_FOUL:3 ●BLACK_FOUL:2
   a b c d e f g h
 1〇□　　　　□□
 2□□□　　□□□
 3　　□□□□　　
 4　　　●〇　　　
 5　　　〇●　　　
 6　　□□□□　　
 7□□□　　□□□
 8□□　　　　□□

〇BLACK_FOUL foul
●BLACK_FOUL win
""".split('\n')[1:-1]

        self.assertEqual(lines, expected)
        self.assertEqual(app.state, Reversic.START)
