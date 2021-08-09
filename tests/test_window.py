"""Tests of window.py
"""

import unittest
import tkinter as tk
import threading

import reversi
from reversi import Window


class TestCanvas:
    def __init__(self):
        self.created_text = []
        self.created_oval = []
        self.created_rectangle = []

    def create_text(self, *args, **kwargs):
        self.created_text.append((args, kwargs))

    def create_line(self, *args, **kwargs):
        return (args, kwargs)

    def create_oval(self, *args, **kwargs):
        self.created_oval.append((args, kwargs))

    def create_rectangle(self, *args, **kwargs):
        self.created_rectangle.append((args, kwargs))

    def delete(self, *args, **kwargs):
        self.created_oval = [i for i in self.created_oval if i[1]['tag'] != args[0]]
        self.created_rectangle = [i for i in self.created_rectangle if i[1]['tag'] != args[0]]


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
        window = Window(root=tk.Tk(), black_players=['b'], white_players=['w'])
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
        self.assertIsNone(window.menu.cputimedialog)
        self.assertIsNone(window.menu.extradialog)
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
        window = Window(root=tk.Tk(), black_players=['b'], white_players=['w'])
        for item in ['size', 'black', 'white', 'cputime', 'extra', 'assist', 'language', 'cancel']:
            self.assertIsInstance(window.menu.menus[item], tk.Menu)

    def test_window_menu_command(self):
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

        self.assertIsInstance(window.menu.cputimedialog, reversi.window.CpuTimeDialog)
        window.menu.cputimedialog.dialog.destroy()

        # extra
        command = window.menu._command('extra', '')

        self.assertFalse(window.menu.event.is_set())

        command()

        self.assertTrue(window.menu.event.is_set())
        window.menu.event.clear()

        self.assertIsInstance(window.menu.extradialog, reversi.window.ExtraDialog)
        window.menu.extradialog.dialog.destroy()

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

    def test_window_menu_set_state(self):
        window = Window(root=tk.Tk(), black_players=['b'], white_players=['w'])

        # initial
        expected = ['normal' for _ in window.menu.menu_items.keys()]
        result = []
        for name in window.menu.menu_items.keys():
            index = window.menu.index(name.title())
            result.append(window.menu.entrycget(index, 'state'))
        self.assertEqual(result, expected)

        # disable
        window.menu.set_state('disable')
        expected = ['disabled' for _ in window.menu.menu_items.keys()]
        expected[-1] = 'normal'
        result = []
        for name in window.menu.menu_items.keys():
            index = window.menu.index(name.title())
            result.append(window.menu.entrycget(index, 'state'))
        self.assertEqual(result, expected)

        # normal
        window.menu.set_state('normal')
        expected = ['normal' for _ in window.menu.menu_items.keys()]
        expected[-1] = 'disabled'
        result = []
        for name in window.menu.menu_items.keys():
            index = window.menu.index(name.title())
            result.append(window.menu.entrycget(index, 'state'))
        self.assertEqual(result, expected)

    def test_window_cputimedialog_init(self):
        window = Window(root=tk.Tk(), black_players=['b'], white_players=['w'])
        event = 'event'
        language = 'Japanese'
        cputimedialog = reversi.window.CpuTimeDialog(window, event, language)
        self.assertEqual(cputimedialog.window, window)
        self.assertEqual(cputimedialog.event, event)
        self.assertEqual(cputimedialog.dialog.master, window.root)
        self.assertEqual(cputimedialog.parameter.get(), str(window.cputime))
        self.assertEqual(cputimedialog.label1['text'], reversi.window.TEXTS[language]['CPU_WAIT_TEXT'])
        self.assertEqual(cputimedialog.entry['textvariable'], str(cputimedialog.parameter))
        self.assertEqual(cputimedialog.label2['text'], reversi.window.TEXTS[language]['CPU_SECOND_TEXT'])
        self.assertEqual(cputimedialog.button['text'], reversi.window.TEXTS[language]['CPU_SETTING_TEXT'])
        cputimedialog.dialog.destroy()

    def test_window_cputimedialog_set_parameter(self):
        window = Window(root=tk.Tk(), black_players=['b'], white_players=['w'])
        cputimedialog = reversi.window.CpuTimeDialog(window, threading.Event(), 'Japanese')
        # NOT MATCH
        new_cputime = -1.0
        cputimedialog.parameter.set(new_cputime)
        cputimedialog.button.invoke()
        self.assertNotEqual(window.cputime, new_cputime)
        # IS ZERO
        new_cputime = 00.0
        cputimedialog.parameter.set(new_cputime)
        cputimedialog.button.invoke()
        self.assertNotEqual(window.cputime, new_cputime)
        # OK
        new_cputime = 1.0
        cputimedialog.parameter.set(new_cputime)
        cputimedialog.button.invoke()
        self.assertEqual(window.cputime, new_cputime)
        self.assertTrue(cputimedialog.event.is_set())

    def test_window_extradialog_init(self):
        window = Window(root=tk.Tk(), black_players=['b'], white_players=['w'])
        event = 'event'
        language = 'Japanese'
        extradialog = reversi.window.ExtraDialog(window, event, language)
        self.assertEqual(extradialog.window, window)
        self.assertEqual(extradialog.event, event)
        self.assertEqual(extradialog.dialog.master, window.root)
        self.assertEqual(extradialog.extra_file.get(), str(window.extra_file))
        self.assertEqual(extradialog.label1['text'], reversi.window.TEXTS[language]['EXTRA_PLAYER_TEXT'])
        self.assertEqual(extradialog.label2['text'], reversi.window.TEXTS[language]['EXTRA_FILE_TEXT'])
        self.assertEqual(extradialog.entry['textvariable'], str(extradialog.extra_file))
        self.assertEqual(extradialog.button1['text'], reversi.window.TEXTS[language]['EXTRA_REF_TEXT'])
        self.assertEqual(extradialog.button2['text'], reversi.window.TEXTS[language]['EXTRA_LOAD_TEXT'])
        extradialog.dialog.destroy()

    def test_window_extradialog_select_extra_file(self):
        import os
        test_filetypes = None
        test_initialdir = None
        extra_file_ok = 'extra_file_ok'

        def test_askopenfilename_ok(filetypes, initialdir):
            nonlocal test_filetypes, test_initialdir, extra_file_ok
            test_filetypes = filetypes
            test_initialdir = initialdir
            return extra_file_ok

        def test_askopenfilename_ng(filetypes, initialdir):
            return False

        window = Window(root=tk.Tk(), black_players=['b'], white_players=['w'])
        extradialog = reversi.window.ExtraDialog(window, threading.Event(), 'Japanese')
        # OK
        extradialog.askopenfilename = test_askopenfilename_ok
        extradialog.button1.invoke()
        self.assertEqual(test_filetypes, [("", "*.json")])
        self.assertEqual(test_initialdir, os.path.abspath(os.path.dirname('./extra/')))
        self.assertEqual(extradialog.extra_file.get(), extra_file_ok)
        # NG
        extradialog.askopenfilename = test_askopenfilename_ng
        extradialog.button1.invoke()
        self.assertEqual(extradialog.extra_file.get(), extra_file_ok)
        extradialog.dialog.destroy()

    def test_window_extradialog_set_parameter(self):
        new_extra_file = 'new_extra_file'
        window = Window(root=tk.Tk(), black_players=['b'], white_players=['w'])
        extradialog = reversi.window.ExtraDialog(window, threading.Event(), 'Japanese')
        extradialog.extra_file.set(new_extra_file)
        extradialog.button2.invoke()
        self.assertEqual(window.extra_file, new_extra_file)
        self.assertTrue(extradialog.event.is_set())

    def test_window_screenboard_init(self):
        reversi.BitBoardMethods.SLOW_MODE1 = True
        test_size = 4
        test_cputime = 5.0
        test_assist = 'ON'
        test_xlines = [
            ((410, 40, 910, 40), {'fill': 'white'}),
            ((410, 165, 910, 165), {'fill': 'white'}),
            ((410, 290, 910, 290), {'fill': 'white'}),
            ((410, 415, 910, 415), {'fill': 'white'}),
            ((410, 540, 910, 540), {'fill': 'white'}),
        ]
        test_ylines = [
            ((410, 40, 410, 540), {'fill': 'white'}),
            ((535, 40, 535, 540), {'fill': 'white'}),
            ((660, 40, 660, 540), {'fill': 'white'}),
            ((785, 40, 785, 540), {'fill': 'white'}),
            ((910, 40, 910, 540), {'fill': 'white'}),
        ]
        test_canvas_created_text = [
            ((20, 20), {'anchor': 'w', 'fill': 'white', 'font': ('', 12), 'text': 'CPU_TIME(5.0s)'}),
            ((20, 40), {'anchor': 'w', 'fill': 'white', 'font': ('', 12), 'text': 'Assist On'}),
            ((1290, 20), {'text': '■', 'font': ('', 12), 'anchor': 'w', 'fill': 'tomato'}),
            ((395, 102), {'fill': 'white', 'font': ('', 20), 'text': '1'}),
            ((472, 25), {'fill': 'white', 'font': ('', 20), 'text': 'a'}),
            ((395, 227), {'fill': 'white', 'font': ('', 20), 'text': '2'}),
            ((597, 25), {'fill': 'white', 'font': ('', 20), 'text': 'b'}),
            ((395, 352), {'fill': 'white', 'font': ('', 20), 'text': '3'}),
            ((722, 25), {'fill': 'white', 'font': ('', 20), 'text': 'c'}),
            ((395, 477), {'fill': 'white', 'font': ('', 20), 'text': '4'}),
            ((847, 25), {'fill': 'white', 'font': ('', 20), 'text': 'd'}),
        ]
        test_canvas_created_oval = [
            ((672.0, 177.0, 772.0, 277.0), {'fill': 'black', 'outline': 'black', 'tag': 'black_c2'}),
            ((547.0, 302.0, 647.0, 402.0), {'fill': 'black', 'outline': 'black', 'tag': 'black_b3'}),
            ((547.0, 177.0, 647.0, 277.0), {'fill': 'white', 'outline': 'white', 'tag': 'white_b2'}),
            ((672.0, 302.0, 772.0, 402.0), {'fill': 'white', 'outline': 'white', 'tag': 'white_c3'}),
        ]
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist)
        self.assertEqual(screenboard.size, test_size)
        self.assertEqual(screenboard.cputime, test_cputime)
        self.assertEqual(screenboard.assist, test_assist)
        self.assertEqual(screenboard.canvas.created_text, test_canvas_created_text)
        self.assertEqual(screenboard.canvas.created_oval, test_canvas_created_oval)
        self.assertEqual(screenboard._squares, [[None for _ in range(test_size)] for _ in range(test_size)])
        self.assertEqual(screenboard._xlines, test_xlines)
        self.assertEqual(screenboard._ylines, test_ylines)
        self.assertIsNone(screenboard.move)
        self.assertFalse(screenboard.event.is_set())
        reversi.BitBoardMethods.SLOW_MODE1 = False

    def test_window_screenboard_draw_squares(self):
        test_size = 26
        test_cputime = 5.0
        test_assist = 'ON'
        test_square_y_ini = 40
        test_square_w = 19
        test_square_x_ini = 413
        test_oval_w1 = 15
        test_oval_w2 = 1
        test_xlines = [
            ((413, 40, 907, 40), {'fill': 'white'}),
            ((413, 59, 907, 59), {'fill': 'white'}),
            ((413, 78, 907, 78), {'fill': 'white'}),
            ((413, 97, 907, 97), {'fill': 'white'}),
            ((413, 116, 907, 116), {'fill': 'white'}),
            ((413, 135, 907, 135), {'fill': 'white'}),
            ((413, 154, 907, 154), {'fill': 'white'}),
            ((413, 173, 907, 173), {'fill': 'white'}),
            ((413, 192, 907, 192), {'fill': 'white'}),
            ((413, 211, 907, 211), {'fill': 'white'}),
            ((413, 230, 907, 230), {'fill': 'white'}),
            ((413, 249, 907, 249), {'fill': 'white'}),
            ((413, 268, 907, 268), {'fill': 'white'}),
            ((413, 287, 907, 287), {'fill': 'white'}),
            ((413, 306, 907, 306), {'fill': 'white'}),
            ((413, 325, 907, 325), {'fill': 'white'}),
            ((413, 344, 907, 344), {'fill': 'white'}),
            ((413, 363, 907, 363), {'fill': 'white'}),
            ((413, 382, 907, 382), {'fill': 'white'}),
            ((413, 401, 907, 401), {'fill': 'white'}),
            ((413, 420, 907, 420), {'fill': 'white'}),
            ((413, 439, 907, 439), {'fill': 'white'}),
            ((413, 458, 907, 458), {'fill': 'white'}),
            ((413, 477, 907, 477), {'fill': 'white'}),
            ((413, 496, 907, 496), {'fill': 'white'}),
            ((413, 515, 907, 515), {'fill': 'white'}),
            ((413, 534, 907, 534), {'fill': 'white'}),
        ]
        test_ylines = [
            ((413, 40, 413, 534), {'fill': 'white'}),
            ((432, 40, 432, 534), {'fill': 'white'}),
            ((451, 40, 451, 534), {'fill': 'white'}),
            ((470, 40, 470, 534), {'fill': 'white'}),
            ((489, 40, 489, 534), {'fill': 'white'}),
            ((508, 40, 508, 534), {'fill': 'white'}),
            ((527, 40, 527, 534), {'fill': 'white'}),
            ((546, 40, 546, 534), {'fill': 'white'}),
            ((565, 40, 565, 534), {'fill': 'white'}),
            ((584, 40, 584, 534), {'fill': 'white'}),
            ((603, 40, 603, 534), {'fill': 'white'}),
            ((622, 40, 622, 534), {'fill': 'white'}),
            ((641, 40, 641, 534), {'fill': 'white'}),
            ((660, 40, 660, 534), {'fill': 'white'}),
            ((679, 40, 679, 534), {'fill': 'white'}),
            ((698, 40, 698, 534), {'fill': 'white'}),
            ((717, 40, 717, 534), {'fill': 'white'}),
            ((736, 40, 736, 534), {'fill': 'white'}),
            ((755, 40, 755, 534), {'fill': 'white'}),
            ((774, 40, 774, 534), {'fill': 'white'}),
            ((793, 40, 793, 534), {'fill': 'white'}),
            ((812, 40, 812, 534), {'fill': 'white'}),
            ((831, 40, 831, 534), {'fill': 'white'}),
            ((850, 40, 850, 534), {'fill': 'white'}),
            ((869, 40, 869, 534), {'fill': 'white'}),
            ((888, 40, 888, 534), {'fill': 'white'}),
            ((907, 40, 907, 534), {'fill': 'white'}),
        ]
        test_canvas_created_text = [
            ((20, 20), {'anchor': 'w', 'fill': 'white', 'font': ('', 12), 'text': 'CPU_TIME(5.0s)'}),
            ((20, 40), {'anchor': 'w', 'fill': 'white', 'font': ('', 12), 'text': 'Assist On'}),
            ((398, 49), {'fill': 'white', 'font': ('', 20), 'text': '1'}),
            ((422, 25), {'fill': 'white', 'font': ('', 20), 'text': 'a'}),
            ((398, 68), {'fill': 'white', 'font': ('', 20), 'text': '2'}),
            ((441, 25), {'fill': 'white', 'font': ('', 20), 'text': 'b'}),
            ((398, 87), {'fill': 'white', 'font': ('', 20), 'text': '3'}),
            ((460, 25), {'fill': 'white', 'font': ('', 20), 'text': 'c'}),
            ((398, 106), {'fill': 'white', 'font': ('', 20), 'text': '4'}),
            ((479, 25), {'fill': 'white', 'font': ('', 20), 'text': 'd'}),
            ((398, 125), {'fill': 'white', 'font': ('', 20), 'text': '5'}),
            ((498, 25), {'fill': 'white', 'font': ('', 20), 'text': 'e'}),
            ((398, 144), {'fill': 'white', 'font': ('', 20), 'text': '6'}),
            ((517, 25), {'fill': 'white', 'font': ('', 20), 'text': 'f'}),
            ((398, 163), {'fill': 'white', 'font': ('', 20), 'text': '7'}),
            ((536, 25), {'fill': 'white', 'font': ('', 20), 'text': 'g'}),
            ((398, 182), {'fill': 'white', 'font': ('', 20), 'text': '8'}),
            ((555, 25), {'fill': 'white', 'font': ('', 20), 'text': 'h'}),
            ((398, 201), {'fill': 'white', 'font': ('', 20), 'text': '9'}),
            ((574, 25), {'fill': 'white', 'font': ('', 20), 'text': 'i'}),
            ((398, 220), {'fill': 'white', 'font': ('', 20), 'text': '10'}),
            ((593, 25), {'fill': 'white', 'font': ('', 20), 'text': 'j'}),
            ((398, 239), {'fill': 'white', 'font': ('', 20), 'text': '11'}),
            ((612, 25), {'fill': 'white', 'font': ('', 20), 'text': 'k'}),
            ((398, 258), {'fill': 'white', 'font': ('', 20), 'text': '12'}),
            ((631, 25), {'fill': 'white', 'font': ('', 20), 'text': 'l'}),
            ((398, 277), {'fill': 'white', 'font': ('', 20), 'text': '13'}),
            ((650, 25), {'fill': 'white', 'font': ('', 20), 'text': 'm'}),
            ((398, 296), {'fill': 'white', 'font': ('', 20), 'text': '14'}),
            ((669, 25), {'fill': 'white', 'font': ('', 20), 'text': 'n'}),
            ((398, 315), {'fill': 'white', 'font': ('', 20), 'text': '15'}),
            ((688, 25), {'fill': 'white', 'font': ('', 20), 'text': 'o'}),
            ((398, 334), {'fill': 'white', 'font': ('', 20), 'text': '16'}),
            ((707, 25), {'fill': 'white', 'font': ('', 20), 'text': 'p'}),
            ((398, 353), {'fill': 'white', 'font': ('', 20), 'text': '17'}),
            ((726, 25), {'fill': 'white', 'font': ('', 20), 'text': 'q'}),
            ((398, 372), {'fill': 'white', 'font': ('', 20), 'text': '18'}),
            ((745, 25), {'fill': 'white', 'font': ('', 20), 'text': 'r'}),
            ((398, 391), {'fill': 'white', 'font': ('', 20), 'text': '19'}),
            ((764, 25), {'fill': 'white', 'font': ('', 20), 'text': 's'}),
            ((398, 410), {'fill': 'white', 'font': ('', 20), 'text': '20'}),
            ((783, 25), {'fill': 'white', 'font': ('', 20), 'text': 't'}),
            ((398, 429), {'fill': 'white', 'font': ('', 20), 'text': '21'}),
            ((802, 25), {'fill': 'white', 'font': ('', 20), 'text': 'u'}),
            ((398, 448), {'fill': 'white', 'font': ('', 20), 'text': '22'}),
            ((821, 25), {'fill': 'white', 'font': ('', 20), 'text': 'v'}),
            ((398, 467), {'fill': 'white', 'font': ('', 20), 'text': '23'}),
            ((840, 25), {'fill': 'white', 'font': ('', 20), 'text': 'w'}),
            ((398, 486), {'fill': 'white', 'font': ('', 20), 'text': '24'}),
            ((859, 25), {'fill': 'white', 'font': ('', 20), 'text': 'x'}),
            ((398, 505), {'fill': 'white', 'font': ('', 20), 'text': '25'}),
            ((878, 25), {'fill': 'white', 'font': ('', 20), 'text': 'y'}),
            ((398, 524), {'fill': 'white', 'font': ('', 20), 'text': '26'}),
            ((897, 25), {'fill': 'white', 'font': ('', 20), 'text': 'z'}),
        ]
        test_canvas_created_oval = [
            ((621, 248, 623, 250), {'fill': 'white', 'outline': 'white', 'tag': 'mark'}),
            ((621, 324, 623, 326), {'fill': 'white', 'outline': 'white', 'tag': 'mark'}),
            ((697, 248, 699, 250), {'fill': 'white', 'outline': 'white', 'tag': 'mark'}),
            ((697, 324, 699, 326), {'fill': 'white', 'outline': 'white', 'tag': 'mark'}),
            ((661.5, 269.5, 676.5, 284.5), {'fill': 'black', 'outline': 'black', 'tag': 'black_n13'}),
            ((642.5, 288.5, 657.5, 303.5), {'fill': 'black', 'outline': 'black', 'tag': 'black_m14'}),
            ((642.5, 269.5, 657.5, 284.5), {'fill': 'white', 'outline': 'white', 'tag': 'white_m13'}),
            ((661.5, 288.5, 676.5, 303.5), {'fill': 'white', 'outline': 'white', 'tag': 'white_n14'}),
        ]
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist)
        self.assertEqual(screenboard._squares, [[None for _ in range(test_size)] for _ in range(test_size)])
        self.assertEqual(screenboard.square_y_ini, test_square_y_ini)
        self.assertEqual(screenboard.square_w, test_square_w)
        self.assertEqual(screenboard.square_x_ini, test_square_x_ini)
        self.assertEqual(screenboard.oval_w1, test_oval_w1)
        self.assertEqual(screenboard.oval_w2, test_oval_w2)
        self.assertEqual(screenboard.canvas.created_text, test_canvas_created_text)
        self.assertEqual(screenboard.canvas.created_oval, test_canvas_created_oval)
        self.assertEqual(screenboard._xlines, test_xlines)
        self.assertEqual(screenboard._ylines, test_ylines)

    def test_window_screenboard_put_disc(self):
        test_size = 4
        test_cputime = 5.0
        test_assist = 'ON'
        test_canvas_created_oval = [
            ((547.0, 177.0, 647.0, 277.0), {'fill': 'black', 'outline': 'black', 'tag': 'black_b2'}),
            ((547.0, 302.0, 647.0, 402.0), {'fill': 'white', 'outline': 'white', 'tag': 'white_b3'}),
        ]
        test_canvas_created_rectangle = [
            ((585, 177.0, 597, 277.0), {'fill': 'white', 'outline': 'white', 'tag': 'turnblack1_b2'}),
            ((597, 177.0, 609, 277.0), {'fill': 'black', 'outline': 'black', 'tag': 'turnblack2_b2'}),
            ((585, 302.0, 597, 402.0), {'fill': 'black', 'outline': 'black', 'tag': 'turnwhite1_b3'}),
            ((597, 302.0, 609, 402.0), {'fill': 'white', 'outline': 'white', 'tag': 'turnwhite2_b3'}),
        ]
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist)
        screenboard.canvas.created_oval = []
        screenboard.put_disc('black', 1, 1)
        screenboard.put_disc('white', 1, 2)
        self.assertEqual(screenboard.canvas.created_oval, test_canvas_created_oval)
        screenboard.put_disc('turnblack', 1, 1)
        screenboard.put_disc('turnwhite', 1, 2)
        self.assertEqual(screenboard.canvas.created_rectangle, test_canvas_created_rectangle)

    def test_window_screenboard_remove_disc(self):
        test_size = 4
        test_cputime = 5.0
        test_assist = 'ON'
        test_canvas_created_oval = [
            ((547.0, 302.0, 647.0, 402.0), {'fill': 'white', 'outline': 'white', 'tag': 'white_b3'}),
        ]
        test_canvas_created_rectangle = [
            ((585, 177.0, 597, 277.0), {'fill': 'white', 'outline': 'white', 'tag': 'turnblack1_b2'}),
            ((597, 177.0, 609, 277.0), {'fill': 'black', 'outline': 'black', 'tag': 'turnblack2_b2'}),
        ]
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist)
        screenboard.canvas.created_oval = []
        screenboard.put_disc('black', 1, 1)
        screenboard.put_disc('white', 1, 2)
        screenboard.remove_disc('black', 1, 1)
        screenboard.remove_disc('black', 1, 2)
        self.assertEqual(screenboard.canvas.created_oval, test_canvas_created_oval)
        screenboard.put_disc('turnblack', 1, 1)
        screenboard.put_disc('turnwhite', 1, 2)
        screenboard.remove_disc('turnwhite', 1, 1)
        screenboard.remove_disc('turnwhite', 1, 2)
        self.assertEqual(screenboard.canvas.created_rectangle, test_canvas_created_rectangle)

    def test_window_screenboard_get_coordinate(self):
        test_size = 8
        test_cputime = 5.0
        test_assist = 'ON'
        test_x = 2
        test_y = 3
        test_coordinate = (567, 257)
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist)
        self.assertEqual(screenboard._get_coordinate(test_x, test_y), test_coordinate)
