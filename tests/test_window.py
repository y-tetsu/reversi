"""Tests of window.py
"""

import unittest
import tkinter as tk
import threading

import reversi
from reversi import Window


class TestWindow(unittest.TestCase):
    """window
    """
    def test_window_const(self):
        self.assertEqual('reversi', reversi.window.WINDOW_TITLE)
        self.assertEqual(1320, reversi.window.WINDOW_WIDTH)
        self.assertEqual(660, reversi.window.WINDOW_HEIGHT)
        self.assertEqual('slategray', reversi.window.COLOR_SLATEGRAY)
        self.assertEqual('black', reversi.window.COLOR_BLACK)
        self.assertEqual('white', reversi.window.COLOR_WHITE)
        self.assertEqual('lightpink', reversi.window.COLOR_LIGHTPINK)
        self.assertEqual('gold', reversi.window.COLOR_GOLD)
        self.assertEqual('khaki2', reversi.window.COLOR_KHAKI)
        self.assertEqual('tomato', reversi.window.COLOR_TOMATO)
        self.assertEqual(reversi.window.WINDOW_WIDTH//7, reversi.window.INFO_OFFSET_X['black'])
        self.assertEqual(reversi.window.WINDOW_WIDTH-(reversi.window.WINDOW_WIDTH//7), reversi.window.INFO_OFFSET_X['white'])
        self.assertEqual(80, reversi.window.INFO_OFFSET_Y['name'])
        self.assertEqual(250, reversi.window.INFO_OFFSET_Y['score'])
        self.assertEqual(400, reversi.window.INFO_OFFSET_Y['winlose'])
        self.assertEqual(500, reversi.window.INFO_OFFSET_Y['turn'])
        self.assertEqual(600, reversi.window.INFO_OFFSET_Y['move'])
        self.assertEqual(reversi.window.COLOR_BLACK, reversi.window.INFO_COLOR['name']['black'])
        self.assertEqual(reversi.window.COLOR_WHITE, reversi.window.INFO_COLOR['name']['white'])
        self.assertEqual(reversi.window.COLOR_BLACK, reversi.window.INFO_COLOR['score']['black'])
        self.assertEqual(reversi.window.COLOR_WHITE, reversi.window.INFO_COLOR['score']['white'])
        self.assertEqual(reversi.window.COLOR_BLACK, reversi.window.INFO_COLOR['winlose']['black'])
        self.assertEqual(reversi.window.COLOR_WHITE, reversi.window.INFO_COLOR['winlose']['white'])
        self.assertEqual(reversi.window.COLOR_LIGHTPINK, reversi.window.INFO_COLOR['turn']['black'])
        self.assertEqual(reversi.window.COLOR_LIGHTPINK, reversi.window.INFO_COLOR['turn']['white'])
        self.assertEqual(reversi.window.COLOR_BLACK, reversi.window.INFO_COLOR['move']['black'])
        self.assertEqual(reversi.window.COLOR_WHITE, reversi.window.INFO_COLOR['move']['white'])
        self.assertEqual(32, reversi.window.INFO_FONT_SIZE['name'])
        self.assertEqual(140, reversi.window.INFO_FONT_SIZE['score'])
        self.assertEqual(32, reversi.window.INFO_FONT_SIZE['winlose'])
        self.assertEqual(32, reversi.window.INFO_FONT_SIZE['turn'])
        self.assertEqual(32, reversi.window.INFO_FONT_SIZE['move'])
        self.assertEqual(reversi.window.WINDOW_WIDTH//2, reversi.window.START_OFFSET_X)
        self.assertEqual(610, reversi.window.START_OFFSET_Y)
        self.assertEqual(32, reversi.window.START_FONT_SIZE)
        self.assertEqual(20, reversi.window.ASSIST_OFFSET_X)
        self.assertEqual(40, reversi.window.ASSIST_OFFSET_Y)
        self.assertEqual(12, reversi.window.ASSIST_FONT_SIZE)
        self.assertEqual(20, reversi.window.CPUTIME_OFFSET_X)
        self.assertEqual(20, reversi.window.CPUTIME_OFFSET_Y)
        self.assertEqual(12, reversi.window.CPUTIME_FONT_SIZE)
        self.assertEqual(1290, reversi.window.SLOWMODE_OFFSET_X)
        self.assertEqual(20, reversi.window.SLOWMODE_OFFSET_Y)
        self.assertEqual(12, reversi.window.SLOWMODE_FONT_SIZE)
        self.assertEqual(15, reversi.window.SQUAREHEADER_OFFSET_XY)
        self.assertEqual(20, reversi.window.SQUAREHEADER_FONT_SIZE)
        self.assertEqual(40, reversi.window.SQUARE_OFFSET_Y)
        self.assertEqual(120, reversi.window.SQUARE_BOTTOM_MARGIN)
        self.assertEqual(0.8, reversi.window.OVAL_SIZE_RATIO)
        self.assertEqual(10, reversi.window.TURNOVAL_SIZE_DIVISOR)
        self.assertEqual([('white', 'turnwhite'), ('turnwhite', 'black')], reversi.window.TURN_BLACK_PATTERN)
        self.assertEqual([('black', 'turnblack'), ('turnblack', 'white')], reversi.window.TURN_WHITE_PATTERN)
        self.assertEqual(0.1, reversi.window.TURN_DISC_WAIT)
        self.assertEqual(['ON', 'OFF'], reversi.window.ASSIST_MENU)
        self.assertEqual(['English', 'Japanese'], reversi.window.LANGUAGE_MENU)
        self.assertEqual(['OK'], reversi.window.CANCEL_MENU)
        self.assertEqual(['Set'], reversi.window.CPUTIME_MENU)
        self.assertEqual(reversi.strategies.common.cputime.CPU_TIME, reversi.window.CPU_TIME)
        self.assertEqual(['Set'], reversi.window.EXTRA_MENU)
        self.assertEqual('●', reversi.window.DISC_MARK)
        self.assertEqual(8, reversi.window.DEFAULT_BOARD_SIZE)
        self.assertEqual('2', reversi.window.DEFAULT_BLACK_NUM)
        self.assertEqual('2', reversi.window.DEFAULT_WHITE_NUM)

        class TestPlayer:
            player = {
                'black': 'TEST_BLACK',
                'white': 'TEST_WHITE',
            }
        self.assertEqual('●TEST_BLACK', reversi.window.DEFAULT_INFO_TEXT['name']['black'](TestPlayer()))
        self.assertEqual('●TEST_WHITE', reversi.window.DEFAULT_INFO_TEXT['name']['white'](TestPlayer()))
        self.assertEqual('2', reversi.window.DEFAULT_INFO_TEXT['score']['black'](TestPlayer()))
        self.assertEqual('2', reversi.window.DEFAULT_INFO_TEXT['score']['white'](TestPlayer()))
        self.assertEqual('', reversi.window.DEFAULT_INFO_TEXT['winlose']['black'](TestPlayer()))
        self.assertEqual('', reversi.window.DEFAULT_INFO_TEXT['winlose']['white'](TestPlayer()))
        self.assertEqual('', reversi.window.DEFAULT_INFO_TEXT['turn']['black'](TestPlayer()))
        self.assertEqual('', reversi.window.DEFAULT_INFO_TEXT['turn']['white'](TestPlayer()))
        self.assertEqual('', reversi.window.DEFAULT_INFO_TEXT['move']['black'](TestPlayer()))
        self.assertEqual('', reversi.window.DEFAULT_INFO_TEXT['move']['white'](TestPlayer()))
        self.assertEqual('CPU_TIME', reversi.window.CPUTIME_DIALOG_TITLE)
        self.assertEqual(230, reversi.window.CPUTIME_DIALOG_WIDTH)
        self.assertEqual(90, reversi.window.CPUTIME_DIALOG_HEIGHT)
        self.assertEqual('Extra', reversi.window.EXTRA_DIALOG_TITLE)
        self.assertEqual(700, reversi.window.EXTRA_DIALOG_WIDTH)
        self.assertEqual(90, reversi.window.EXTRA_DIALOG_HEIGHT)
        self.assertEqual('Click to start', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['START_TEXT'])
        self.assertEqual('Your turn', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['TURN_ON'])
        self.assertEqual('', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['TURN_OFF'])
        self.assertEqual('', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['MOVE_ON'])
        self.assertEqual('', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['MOVE_OFF'])
        self.assertEqual('Foul', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['FOUL_ON'])
        self.assertEqual('Win', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['WIN_ON'])
        self.assertEqual('Lose', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['LOSE_ON'])
        self.assertEqual('Draw', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['DRAW_ON'])
        self.assertEqual('Please set CPU wait time.', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['CPU_WAIT_TEXT'])
        self.assertEqual('(sec)', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['CPU_SECOND_TEXT'])
        self.assertEqual('Set', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['CPU_SETTING_TEXT'])
        self.assertEqual('Please add extra player by loading registration file.', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['EXTRA_PLAYER_TEXT'])
        self.assertEqual('Registration file', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['EXTRA_FILE_TEXT'])
        self.assertEqual('Reference', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['EXTRA_REF_TEXT'])
        self.assertEqual('Load', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[0]]['EXTRA_LOAD_TEXT'])
        self.assertEqual('クリックでスタート', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['START_TEXT'])
        self.assertEqual('手番です', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['TURN_ON'])
        self.assertEqual('', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['TURN_OFF'])
        self.assertEqual(' に置きました', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['MOVE_ON'])
        self.assertEqual('', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['MOVE_OFF'])
        self.assertEqual('反則', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['FOUL_ON'])
        self.assertEqual('勝ち', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['WIN_ON'])
        self.assertEqual('負け', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['LOSE_ON'])
        self.assertEqual('引き分け', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['DRAW_ON'])
        self.assertEqual('CPUの持ち時間を設定してください', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['CPU_WAIT_TEXT'])
        self.assertEqual('(秒)', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['CPU_SECOND_TEXT'])
        self.assertEqual('設定', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['CPU_SETTING_TEXT'])
        self.assertEqual('登録ファイルを読み込むとプレイヤーを追加できます', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['EXTRA_PLAYER_TEXT'])
        self.assertEqual('登録ファイル', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['EXTRA_FILE_TEXT'])
        self.assertEqual('参照', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['EXTRA_REF_TEXT'])
        self.assertEqual('読み込む', reversi.window.TEXTS[reversi.window.LANGUAGE_MENU[1]]['EXTRA_LOAD_TEXT'])

    def test_window_init(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)

        self.assertEqual(window.root, root)
        self.assertEqual(window.size, reversi.window.DEFAULT_BOARD_SIZE)
        self.assertEqual(window.player['black'], 'Easy1')
        self.assertEqual(window.player['white'], 'Easy2')
        self.assertEqual(window.assist, 'OFF')
        self.assertEqual(window.language, 'English')
        self.assertEqual(window.cancel, 'OK')
        self.assertEqual(window.cputime, reversi.window.CPU_TIME)
        self.assertEqual(window.extra_file, '')
        self.assertIsInstance(window.menu, reversi.window.Menu)
        self.assertIsInstance(window.canvas, tk.Canvas)
        self.assertEqual(window.canvas['width'], str(reversi.window.WINDOW_WIDTH))
        self.assertEqual(window.canvas['height'], str(reversi.window.WINDOW_HEIGHT))
        self.assertEqual(window.canvas['bg'], str(reversi.window.COLOR_SLATEGRAY))

    def test_window_init_screen(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)
        window.init_screen()
        # board
        self.assertEqual(window.board.size, reversi.window.DEFAULT_BOARD_SIZE)
        self.assertEqual(window.board.cputime, reversi.window.CPU_TIME)
        self.assertEqual(window.board.assist, reversi.window.ASSIST_MENU[1])
        self.assertEqual(window.board._squares, [[None for _ in range(window.board.size)] for _ in range(window.board.size)])
        self.assertEqual(window.board._xlines, [6, 10, 14, 18, 22, 26, 30, 38, 40])
        self.assertEqual(window.board._ylines, [4, 8, 12, 16, 20, 24, 28, 36, 39])
        self.assertEqual(window.board.move, None)
        self.assertEqual(window.board.event.is_set(), False)
        # info
        self.assertEqual(window.info.player, {'black': b[0], 'white': w[0]})
        self.assertEqual(window.info.language, reversi.window.LANGUAGE_MENU[0])
        # start
        self.assertEqual(window.start.language, reversi.window.LANGUAGE_MENU[0])
        self.assertEqual(window.start.event.is_set(), False)

    def test_window_set_state(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)
        window.init_screen()

        class TestState:
            def __init__(self):
                self.state = None

            def set_state(self, state):
                self.state = state

        window.start = TestState()
        window.menu = TestState()

        window.set_state('Normal')
        self.assertEqual(window.start.state, 'Normal')
        self.assertEqual(window.menu.state, 'Normal')

        window.set_state('Disable')
        self.assertEqual(window.start.state, 'Disable')
        self.assertEqual(window.menu.state, 'Disable')

    def test_window_menu_init(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)
        self.assertIsInstance(window.menu.window, Window)
        self.assertEqual(window.menu.size, reversi.window.DEFAULT_BOARD_SIZE)
        self.assertEqual(window.menu.black_player, b[0])
        self.assertEqual(window.menu.white_player, w[0])
        self.assertEqual(window.menu.assist, reversi.window.ASSIST_MENU[1])
        self.assertEqual(window.menu.language, reversi.window.LANGUAGE_MENU[0])
        self.assertEqual(window.menu.cancel, reversi.window.CANCEL_MENU[0])
        self.assertIsInstance(window.menu.event, threading.Event)
        self.assertEqual(window.menu.menu_items['size'], range(reversi.board.MIN_BOARD_SIZE, reversi.board.MAX_BOARD_SIZE + 1, 2))
        self.assertEqual(window.menu.menu_items['black'], b)
        self.assertEqual(window.menu.menu_items['white'], w)
        self.assertEqual(window.menu.menu_items['cputime'], reversi.window.CPUTIME_MENU)
        self.assertEqual(window.menu.menu_items['extra'], reversi.window.EXTRA_MENU)
        self.assertEqual(window.menu.menu_items['assist'], reversi.window.ASSIST_MENU)
        self.assertEqual(window.menu.menu_items['language'], reversi.window.LANGUAGE_MENU)
        self.assertEqual(window.menu.menu_items['cancel'], reversi.window.CANCEL_MENU)

    def test_window_menu_create_menu_items(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)
        for item in ['size', 'black', 'white', 'cputime', 'extra', 'assist', 'language', 'cancel']:
            self.assertIsInstance(window.menu.menus[item], tk.Menu)

    def test_window_command(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)

        # size
        test_size = 12
        command = window.menu._command('size', test_size)

        self.assertFalse(window.menu.event.is_set())
        self.assertEqual(window.menu.size, reversi.window.DEFAULT_BOARD_SIZE)

        command()

        self.assertTrue(window.menu.event.is_set())
        self.assertEqual(window.menu.size, test_size)
        window.menu.event.clear()

        # black
        test_black_player = 'Hard1'
        command = window.menu._command('black', test_black_player)

        self.assertFalse(window.menu.event.is_set())
        self.assertEqual(window.menu.black_player, b[0])

        command()

        self.assertTrue(window.menu.event.is_set())
        self.assertEqual(window.menu.black_player, test_black_player)
        window.menu.event.clear()

        # white
        test_white_player = 'Hard2'
        command = window.menu._command('white', test_white_player)

        self.assertFalse(window.menu.event.is_set())
        self.assertEqual(window.menu.white_player, w[0])

        command()

        self.assertTrue(window.menu.event.is_set())
        self.assertEqual(window.menu.white_player, test_white_player)
        window.menu.event.clear()

        # cputime
        command = window.menu._command('cputime', '')

        self.assertFalse(window.menu.event.is_set())

        command()

        self.assertTrue(window.menu.event.is_set())
        window.menu.event.clear()

        # extra
        command = window.menu._command('extra', '')

        self.assertFalse(window.menu.event.is_set())

        command()

        self.assertTrue(window.menu.event.is_set())
        window.menu.event.clear()

        # assist
        test_assist = 'ON'
        command = window.menu._command('assist', test_assist)

        self.assertFalse(window.menu.event.is_set())
        self.assertEqual(window.menu.assist, reversi.window.ASSIST_MENU[1])

        command()

        self.assertTrue(window.menu.event.is_set())
        self.assertEqual(window.menu.assist, test_assist)
        window.menu.event.clear()

        # language
        test_language = 'JAPANESE'
        command = window.menu._command('language', test_language)

        self.assertFalse(window.menu.event.is_set())
        self.assertEqual(window.menu.language, reversi.window.LANGUAGE_MENU[0])

        command()

        self.assertTrue(window.menu.event.is_set())
        self.assertEqual(window.menu.language, test_language)
        window.menu.event.clear()

        # cancel
        test_cancel = 'TEST_ON'
        command = window.menu._command('cancel', test_cancel)

        self.assertFalse(window.menu.event.is_set())
        self.assertEqual(window.menu.cancel, 'OK')

        command()

        self.assertTrue(window.menu.event.is_set())
        self.assertEqual(window.menu.cancel, test_cancel)
        window.menu.event.clear()
