"""Tests of app.py
"""

import unittest
from test.support import captured_stdout
import os

from reversi import Reversi, Reversic, Window, ErrorMessage
from reversi.strategies import WindowUserInput, ConsoleUserInput


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

        def demo_animation_true():
            return True

        def demo_animation_false():
            return False

        app = Reversi()
        app.window = TestWindow()

        # event is_set True and demo_anumation_true
        app.window.start.event.is_set = lambda: True
        app._demo_animation = demo_animation_true
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

    def test_reversi_demo_animaion(self):
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

        app = Reversi()
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

    # for Reversic
    def test_reversic_init(self):
        app = Reversic()
        self.assertEqual(app.board_size, 8)
        self.assertEqual(app.player_names, {'black': 'User1', 'white': 'User2'})
        self.assertEqual(app.state, app.START)
        self.assertTrue('User1' in app.players_info['black'])
        self.assertIsInstance(app.players_info['black']['User1'], ConsoleUserInput)
        self.assertTrue('User2' in app.players_info['white'])
        self.assertIsInstance(app.players_info['white']['User2'], ConsoleUserInput)
