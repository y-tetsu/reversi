"""Tests of window.py
"""

import unittest
import tkinter as tk
import threading
import importlib

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
    def setUp(self):
        importlib.reload(tk)

    def test_window_const(self):
        self.assertEqual('reversi', reversi.window.WINDOW_TITLE)
        self.assertEqual(1320, reversi.window.WINDOW_WIDTH)
        self.assertEqual(660, reversi.window.WINDOW_HEIGHT)
        self.assertEqual('slategray', reversi.window.COLOR_BACKGROUND)
        self.assertEqual('black', reversi.window.COLOR_PLAYER1)
        self.assertEqual('white', reversi.window.COLOR_PLAYER2)
        self.assertEqual('white', reversi.window.COLOR_CPUTIME_LABEL)
        self.assertEqual('white', reversi.window.COLOR_ASSIST_LABEL)
        self.assertEqual('white', reversi.window.COLOR_CELL_NUMBER)
        self.assertEqual('white', reversi.window.COLOR_CELL_LINE)
        self.assertEqual('white', reversi.window.COLOR_CELL_MARK)
        self.assertEqual('lightpink', reversi.window.COLOR_TURN_MESSAGE)
        self.assertEqual('gold', reversi.window.COLOR_START_MESSAGE1)
        self.assertEqual('tomato', reversi.window.COLOR_START_MESSAGE2)
        self.assertEqual('khaki2', reversi.window.COLOR_MOVE_HIGHLIGHT1)
        self.assertEqual('tomato', reversi.window.COLOR_MOVE_HIGHLIGHT2)
        self.assertEqual('tomato', reversi.window.COLOR_REC_LABEL)
        self.assertEqual('tomato', reversi.window.COLOR_LOWSPEED_LABEL)
        self.assertEqual(reversi.window.WINDOW_WIDTH//7, reversi.window.INFO_OFFSET_X['black'])
        self.assertEqual(reversi.window.WINDOW_WIDTH-(reversi.window.WINDOW_WIDTH//7), reversi.window.INFO_OFFSET_X['white'])
        self.assertEqual(80, reversi.window.INFO_OFFSET_Y['name'])
        self.assertEqual(250, reversi.window.INFO_OFFSET_Y['score'])
        self.assertEqual(400, reversi.window.INFO_OFFSET_Y['winlose'])
        self.assertEqual(500, reversi.window.INFO_OFFSET_Y['turn'])
        self.assertEqual(600, reversi.window.INFO_OFFSET_Y['move'])
        self.assertEqual(reversi.window.COLOR_PLAYER1, reversi.window.INFO_COLOR['name']['black'])
        self.assertEqual(reversi.window.COLOR_PLAYER2, reversi.window.INFO_COLOR['name']['white'])
        self.assertEqual(reversi.window.COLOR_PLAYER1, reversi.window.INFO_COLOR['score']['black'])
        self.assertEqual(reversi.window.COLOR_PLAYER2, reversi.window.INFO_COLOR['score']['white'])
        self.assertEqual(reversi.window.COLOR_PLAYER1, reversi.window.INFO_COLOR['winlose']['black'])
        self.assertEqual(reversi.window.COLOR_PLAYER2, reversi.window.INFO_COLOR['winlose']['white'])
        self.assertEqual(reversi.window.COLOR_TURN_MESSAGE, reversi.window.INFO_COLOR['turn']['black'])
        self.assertEqual(reversi.window.COLOR_TURN_MESSAGE, reversi.window.INFO_COLOR['turn']['white'])
        self.assertEqual(reversi.window.COLOR_PLAYER1, reversi.window.INFO_COLOR['move']['black'])
        self.assertEqual(reversi.window.COLOR_PLAYER2, reversi.window.INFO_COLOR['move']['white'])
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
        self.assertEqual(1270, reversi.window.RECORD_OFFSET_X)
        self.assertEqual(40, reversi.window.RECORD_OFFSET_Y)
        self.assertEqual(12, reversi.window.RECORD_FONT_SIZE)
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
        self.assertEqual(['ON', 'OFF'], reversi.window.RECORD_MENU)
        self.assertEqual(['English', 'Japanese'], reversi.window.LANGUAGE_MENU)
        self.assertEqual(['OK'], reversi.window.CANCEL_MENU)
        self.assertEqual(['Set'], reversi.window.CPUTIME_MENU)
        self.assertEqual(reversi.strategies.CPU_TIME, reversi.window.CPU_TIME)
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
        self.assertEqual(window.canvas['width'], str(reversi.window.CANVAS_WIDTH))
        self.assertEqual(window.canvas['height'], str(reversi.window.CANVAS_HEIGHT))
        self.assertEqual(window.canvas['bg'], str(reversi.window.COLOR_BACKGROUND))

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
        self.assertEqual(window.board.record, reversi.window.RECORD_MENU[0])
        self.assertEqual(window.board._squares, [[None for _ in range(window.board.size)] for _ in range(window.board.size)])
        self.assertEqual(window.board._xlines, [7, 11, 15, 19, 23, 27, 31, 39, 41])
        self.assertEqual(window.board._ylines, [5, 9, 13, 17, 21, 25, 29, 37, 40])
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
        self.assertEqual(window.menu.record, reversi.window.RECORD_MENU[0])
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
        self.assertEqual(window.menu.menu_items['record'], reversi.window.RECORD_MENU)
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

        # record
        test_record = 'OFF'
        command = window.menu._command('record', test_record)

        self.assertFalse(window.menu.event.is_set())
        self.assertEqual(window.menu.record, reversi.window.RECORD_MENU[0])

        command()

        self.assertTrue(window.menu.event.is_set())
        self.assertEqual(window.menu.record, test_record)
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
        reversi.cy.IMPORTED = False
        test_size = 4
        test_cputime = 5.0
        test_assist = 'ON'
        test_record = 'ON'
        test_xlines = [
            ((408, 40, 908, 40), {'fill': 'white'}),
            ((408, 165, 908, 165), {'fill': 'white'}),
            ((408, 290, 908, 290), {'fill': 'white'}),
            ((408, 415, 908, 415), {'fill': 'white'}),
            ((408, 540, 908, 540), {'fill': 'white'}),
        ]
        test_ylines = [
            ((408, 40, 408, 540), {'fill': 'white'}),
            ((533, 40, 533, 540), {'fill': 'white'}),
            ((658, 40, 658, 540), {'fill': 'white'}),
            ((783, 40, 783, 540), {'fill': 'white'}),
            ((908, 40, 908, 540), {'fill': 'white'}),
        ]
        test_canvas_created_text = [
            ((20, 20), {'anchor': 'w', 'fill': 'white', 'font': ('', 12), 'text': 'CPU_TIME(5.0s)'}),
            ((20, 40), {'anchor': 'w', 'fill': 'white', 'font': ('', 12), 'text': 'Assist On'}),
            ((1270, 40), {'anchor': 'w', 'fill': 'tomato', 'font': ('', 12), 'text': 'REC'}),
            ((1290, 20), {'text': '■', 'font': ('', 12), 'anchor': 'w', 'fill': 'tomato'}),
            ((393, 102), {'fill': 'white', 'font': ('', 20), 'text': '1'}),
            ((470, 25), {'fill': 'white', 'font': ('', 20), 'text': 'a'}),
            ((393, 227), {'fill': 'white', 'font': ('', 20), 'text': '2'}),
            ((595, 25), {'fill': 'white', 'font': ('', 20), 'text': 'b'}),
            ((393, 352), {'fill': 'white', 'font': ('', 20), 'text': '3'}),
            ((720, 25), {'fill': 'white', 'font': ('', 20), 'text': 'c'}),
            ((393, 477), {'fill': 'white', 'font': ('', 20), 'text': '4'}),
            ((845, 25), {'fill': 'white', 'font': ('', 20), 'text': 'd'}),
        ]
        test_canvas_created_oval = [
            ((670.0, 177.0, 770.0, 277.0), {'fill': 'black', 'outline': 'black', 'tag': 'black_c2'}),
            ((545.0, 302.0, 645.0, 402.0), {'fill': 'black', 'outline': 'black', 'tag': 'black_b3'}),
            ((545.0, 177.0, 645.0, 277.0), {'fill': 'white', 'outline': 'white', 'tag': 'white_b2'}),
            ((670.0, 302.0, 770.0, 402.0), {'fill': 'white', 'outline': 'white', 'tag': 'white_c3'}),
        ]
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist, test_record)
        self.assertEqual(screenboard.size, test_size)
        self.assertEqual(screenboard.cputime, test_cputime)
        self.assertEqual(screenboard.assist, test_assist)
        self.assertEqual(screenboard.record, test_record)
        self.assertEqual(screenboard.canvas.created_text, test_canvas_created_text)
        self.assertEqual(screenboard.canvas.created_oval, test_canvas_created_oval)
        self.assertEqual(screenboard._squares, [[None for _ in range(test_size)] for _ in range(test_size)])
        self.assertEqual(screenboard._xlines, test_xlines)
        self.assertEqual(screenboard._ylines, test_ylines)
        self.assertIsNone(screenboard.move)
        self.assertFalse(screenboard.event.is_set())
        reversi.BitBoardMethods.CYTHON = False

    def test_window_screenboard_draw_squares(self):
        test_size = 26
        test_cputime = 5.0
        test_assist = 'ON'
        test_record = 'ON'
        test_square_y_ini = 40
        test_square_w = 19
        test_square_x_ini = 411
        test_oval_w1 = 15
        test_oval_w2 = 1
        test_xlines = [
            ((411, 40, 905, 40), {'fill': 'white'}),
            ((411, 59, 905, 59), {'fill': 'white'}),
            ((411, 78, 905, 78), {'fill': 'white'}),
            ((411, 97, 905, 97), {'fill': 'white'}),
            ((411, 116, 905, 116), {'fill': 'white'}),
            ((411, 135, 905, 135), {'fill': 'white'}),
            ((411, 154, 905, 154), {'fill': 'white'}),
            ((411, 173, 905, 173), {'fill': 'white'}),
            ((411, 192, 905, 192), {'fill': 'white'}),
            ((411, 211, 905, 211), {'fill': 'white'}),
            ((411, 230, 905, 230), {'fill': 'white'}),
            ((411, 249, 905, 249), {'fill': 'white'}),
            ((411, 268, 905, 268), {'fill': 'white'}),
            ((411, 287, 905, 287), {'fill': 'white'}),
            ((411, 306, 905, 306), {'fill': 'white'}),
            ((411, 325, 905, 325), {'fill': 'white'}),
            ((411, 344, 905, 344), {'fill': 'white'}),
            ((411, 363, 905, 363), {'fill': 'white'}),
            ((411, 382, 905, 382), {'fill': 'white'}),
            ((411, 401, 905, 401), {'fill': 'white'}),
            ((411, 420, 905, 420), {'fill': 'white'}),
            ((411, 439, 905, 439), {'fill': 'white'}),
            ((411, 458, 905, 458), {'fill': 'white'}),
            ((411, 477, 905, 477), {'fill': 'white'}),
            ((411, 496, 905, 496), {'fill': 'white'}),
            ((411, 515, 905, 515), {'fill': 'white'}),
            ((411, 534, 905, 534), {'fill': 'white'}),
        ]
        test_ylines = [
            ((411, 40, 411, 534), {'fill': 'white'}),
            ((430, 40, 430, 534), {'fill': 'white'}),
            ((449, 40, 449, 534), {'fill': 'white'}),
            ((468, 40, 468, 534), {'fill': 'white'}),
            ((487, 40, 487, 534), {'fill': 'white'}),
            ((506, 40, 506, 534), {'fill': 'white'}),
            ((525, 40, 525, 534), {'fill': 'white'}),
            ((544, 40, 544, 534), {'fill': 'white'}),
            ((563, 40, 563, 534), {'fill': 'white'}),
            ((582, 40, 582, 534), {'fill': 'white'}),
            ((601, 40, 601, 534), {'fill': 'white'}),
            ((620, 40, 620, 534), {'fill': 'white'}),
            ((639, 40, 639, 534), {'fill': 'white'}),
            ((658, 40, 658, 534), {'fill': 'white'}),
            ((677, 40, 677, 534), {'fill': 'white'}),
            ((696, 40, 696, 534), {'fill': 'white'}),
            ((715, 40, 715, 534), {'fill': 'white'}),
            ((734, 40, 734, 534), {'fill': 'white'}),
            ((753, 40, 753, 534), {'fill': 'white'}),
            ((772, 40, 772, 534), {'fill': 'white'}),
            ((791, 40, 791, 534), {'fill': 'white'}),
            ((810, 40, 810, 534), {'fill': 'white'}),
            ((829, 40, 829, 534), {'fill': 'white'}),
            ((848, 40, 848, 534), {'fill': 'white'}),
            ((867, 40, 867, 534), {'fill': 'white'}),
            ((886, 40, 886, 534), {'fill': 'white'}),
            ((905, 40, 905, 534), {'fill': 'white'}),
        ]
        test_canvas_created_text = [
            ((20, 20), {'anchor': 'w', 'fill': 'white', 'font': ('', 12), 'text': 'CPU_TIME(5.0s)'}),
            ((20, 40), {'anchor': 'w', 'fill': 'white', 'font': ('', 12), 'text': 'Assist On'}),
            ((1270, 40), {'anchor': 'w', 'fill': 'tomato', 'font': ('', 12), 'text': 'REC'}),
            ((396, 49), {'fill': 'white', 'font': ('', 20), 'text': '1'}),
            ((420, 25), {'fill': 'white', 'font': ('', 20), 'text': 'a'}),
            ((396, 68), {'fill': 'white', 'font': ('', 20), 'text': '2'}),
            ((439, 25), {'fill': 'white', 'font': ('', 20), 'text': 'b'}),
            ((396, 87), {'fill': 'white', 'font': ('', 20), 'text': '3'}),
            ((458, 25), {'fill': 'white', 'font': ('', 20), 'text': 'c'}),
            ((396, 106), {'fill': 'white', 'font': ('', 20), 'text': '4'}),
            ((477, 25), {'fill': 'white', 'font': ('', 20), 'text': 'd'}),
            ((396, 125), {'fill': 'white', 'font': ('', 20), 'text': '5'}),
            ((496, 25), {'fill': 'white', 'font': ('', 20), 'text': 'e'}),
            ((396, 144), {'fill': 'white', 'font': ('', 20), 'text': '6'}),
            ((515, 25), {'fill': 'white', 'font': ('', 20), 'text': 'f'}),
            ((396, 163), {'fill': 'white', 'font': ('', 20), 'text': '7'}),
            ((534, 25), {'fill': 'white', 'font': ('', 20), 'text': 'g'}),
            ((396, 182), {'fill': 'white', 'font': ('', 20), 'text': '8'}),
            ((553, 25), {'fill': 'white', 'font': ('', 20), 'text': 'h'}),
            ((396, 201), {'fill': 'white', 'font': ('', 20), 'text': '9'}),
            ((572, 25), {'fill': 'white', 'font': ('', 20), 'text': 'i'}),
            ((396, 220), {'fill': 'white', 'font': ('', 20), 'text': '10'}),
            ((591, 25), {'fill': 'white', 'font': ('', 20), 'text': 'j'}),
            ((396, 239), {'fill': 'white', 'font': ('', 20), 'text': '11'}),
            ((610, 25), {'fill': 'white', 'font': ('', 20), 'text': 'k'}),
            ((396, 258), {'fill': 'white', 'font': ('', 20), 'text': '12'}),
            ((629, 25), {'fill': 'white', 'font': ('', 20), 'text': 'l'}),
            ((396, 277), {'fill': 'white', 'font': ('', 20), 'text': '13'}),
            ((648, 25), {'fill': 'white', 'font': ('', 20), 'text': 'm'}),
            ((396, 296), {'fill': 'white', 'font': ('', 20), 'text': '14'}),
            ((667, 25), {'fill': 'white', 'font': ('', 20), 'text': 'n'}),
            ((396, 315), {'fill': 'white', 'font': ('', 20), 'text': '15'}),
            ((686, 25), {'fill': 'white', 'font': ('', 20), 'text': 'o'}),
            ((396, 334), {'fill': 'white', 'font': ('', 20), 'text': '16'}),
            ((705, 25), {'fill': 'white', 'font': ('', 20), 'text': 'p'}),
            ((396, 353), {'fill': 'white', 'font': ('', 20), 'text': '17'}),
            ((724, 25), {'fill': 'white', 'font': ('', 20), 'text': 'q'}),
            ((396, 372), {'fill': 'white', 'font': ('', 20), 'text': '18'}),
            ((743, 25), {'fill': 'white', 'font': ('', 20), 'text': 'r'}),
            ((396, 391), {'fill': 'white', 'font': ('', 20), 'text': '19'}),
            ((762, 25), {'fill': 'white', 'font': ('', 20), 'text': 's'}),
            ((396, 410), {'fill': 'white', 'font': ('', 20), 'text': '20'}),
            ((781, 25), {'fill': 'white', 'font': ('', 20), 'text': 't'}),
            ((396, 429), {'fill': 'white', 'font': ('', 20), 'text': '21'}),
            ((800, 25), {'fill': 'white', 'font': ('', 20), 'text': 'u'}),
            ((396, 448), {'fill': 'white', 'font': ('', 20), 'text': '22'}),
            ((819, 25), {'fill': 'white', 'font': ('', 20), 'text': 'v'}),
            ((396, 467), {'fill': 'white', 'font': ('', 20), 'text': '23'}),
            ((838, 25), {'fill': 'white', 'font': ('', 20), 'text': 'w'}),
            ((396, 486), {'fill': 'white', 'font': ('', 20), 'text': '24'}),
            ((857, 25), {'fill': 'white', 'font': ('', 20), 'text': 'x'}),
            ((396, 505), {'fill': 'white', 'font': ('', 20), 'text': '25'}),
            ((876, 25), {'fill': 'white', 'font': ('', 20), 'text': 'y'}),
            ((396, 524), {'fill': 'white', 'font': ('', 20), 'text': '26'}),
            ((895, 25), {'fill': 'white', 'font': ('', 20), 'text': 'z'}),
        ]
        test_canvas_created_oval = [
            ((619, 248, 621, 250), {'fill': 'white', 'outline': 'white', 'tag': 'mark'}),
            ((619, 324, 621, 326), {'fill': 'white', 'outline': 'white', 'tag': 'mark'}),
            ((695, 248, 697, 250), {'fill': 'white', 'outline': 'white', 'tag': 'mark'}),
            ((695, 324, 697, 326), {'fill': 'white', 'outline': 'white', 'tag': 'mark'}),
            ((659.5, 269.5, 674.5, 284.5), {'fill': 'black', 'outline': 'black', 'tag': 'black_n13'}),
            ((640.5, 288.5, 655.5, 303.5), {'fill': 'black', 'outline': 'black', 'tag': 'black_m14'}),
            ((640.5, 269.5, 655.5, 284.5), {'fill': 'white', 'outline': 'white', 'tag': 'white_m13'}),
            ((659.5, 288.5, 674.5, 303.5), {'fill': 'white', 'outline': 'white', 'tag': 'white_n14'}),
        ]
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist, test_record)
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
        test_record = 'ON'
        test_canvas_created_oval = [
            ((545.0, 177.0, 645.0, 277.0), {'fill': 'black', 'outline': 'black', 'tag': 'black_b2'}),
            ((545.0, 302.0, 645.0, 402.0), {'fill': 'white', 'outline': 'white', 'tag': 'white_b3'}),
        ]
        test_canvas_created_rectangle = [
            ((583, 177.0, 595, 277.0), {'fill': 'white', 'outline': 'white', 'tag': 'turnblack1_b2'}),
            ((595, 177.0, 607, 277.0), {'fill': 'black', 'outline': 'black', 'tag': 'turnblack2_b2'}),
            ((583, 302.0, 595, 402.0), {'fill': 'black', 'outline': 'black', 'tag': 'turnwhite1_b3'}),
            ((595, 302.0, 607, 402.0), {'fill': 'white', 'outline': 'white', 'tag': 'turnwhite2_b3'}),
        ]
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist, test_record)
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
        test_record = 'ON'
        test_canvas_created_oval = [
            ((545.0, 302.0, 645.0, 402.0), {'fill': 'white', 'outline': 'white', 'tag': 'white_b3'}),
        ]
        test_canvas_created_rectangle = [
            ((583, 177.0, 595, 277.0), {'fill': 'white', 'outline': 'white', 'tag': 'turnblack1_b2'}),
            ((595, 177.0, 607, 277.0), {'fill': 'black', 'outline': 'black', 'tag': 'turnblack2_b2'}),
        ]
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist, test_record)
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
        test_record = 'ON'
        test_x = 2
        test_y = 3
        test_coordinate = (565, 257)
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist, test_record)
        self.assertEqual(screenboard._get_coordinate(test_x, test_y), test_coordinate)

    def test_window_screenboard_get_label(self):
        test_size = 8
        test_cputime = 5.0
        test_assist = 'ON'
        test_record = 'ON'
        test_name = 'black'
        test_x = 2
        test_y = 4
        test_label = 'black_c5'
        screenboard = reversi.window.ScreenBoard(TestCanvas(), test_size, test_cputime, test_assist, test_record)
        self.assertEqual(screenboard._get_label(test_name, test_x, test_y), test_label)
