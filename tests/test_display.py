"""Tests of display.py
"""

import os
import unittest
from test.support import captured_stdout

from reversi.board import Board
from reversi.player import Player
from reversi.display import AbstractDisplay, ConsoleDisplay, NoneDisplay, WindowDisplay
from reversi.strategies import ConsoleUserInput


class TestDisplay(unittest.TestCase):
    """display
    """
    tmp = None

    def setUp(self):
        self.tmp = os.system
        os.system = lambda x: False

    def tearDown(self):
        os.system = self.tmp

    def test_console_display(self):
        board8x8 = Board()

        class Test():
            def next_move(self, disc, board):
                return (3, 2)

        black_player = Player('black', 'Test', Test())
        white_player = Player('white', 'User', ConsoleUserInput())

        display = ConsoleDisplay()
        self.assertEqual(display.sleep_time_turn, 1)
        self.assertEqual(display.sleep_time_move, 1)

        display = ConsoleDisplay(sleep_time_turn=0.001, sleep_time_move=0.001)
        self.assertEqual(display.sleep_time_turn, 0.001)
        self.assertEqual(display.sleep_time_move, 0.001)

        with captured_stdout() as stdout:
            display.progress(board8x8, black_player, white_player)
            legal_moves = board8x8.get_legal_moves('black')
            display.turn(black_player, legal_moves)
            black_player.put_disc(board8x8)
            display.move(black_player, legal_moves)
            display.progress(board8x8, black_player, white_player)
            display.foul(black_player)
            display.win(black_player)
            display.draw()

            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines[0], "〇Test:2 ●User:2")
            self.assertEqual(lines[1], "   a b c d e f g h")
            self.assertEqual(lines[2], " 1□□□□□□□□")
            self.assertEqual(lines[3], " 2□□□□□□□□")
            self.assertEqual(lines[4], " 3□□□□□□□□")
            self.assertEqual(lines[5], " 4□□□●〇□□□")
            self.assertEqual(lines[6], " 5□□□〇●□□□")
            self.assertEqual(lines[7], " 6□□□□□□□□")
            self.assertEqual(lines[8], " 7□□□□□□□□")
            self.assertEqual(lines[9], " 8□□□□□□□□")
            self.assertEqual(lines[10], "")
            self.assertEqual(lines[11], "〇Test's turn")
            self.assertEqual(lines[12], " 1: ('d', '3')")
            self.assertEqual(lines[13], " 2: ('c', '4')")
            self.assertEqual(lines[14], " 3: ('f', '5')")
            self.assertEqual(lines[15], " 4: ('e', '6')")
            self.assertEqual(lines[16], "putted on ('d', '3')")
            self.assertEqual(lines[17], "")
            self.assertEqual(lines[18], "〇Test:4 ●User:1")
            self.assertEqual(lines[19], "   a b c d e f g h")
            self.assertEqual(lines[20], " 1□□□□□□□□")
            self.assertEqual(lines[21], " 2□□□□□□□□")
            self.assertEqual(lines[22], " 3□□□〇□□□□")
            self.assertEqual(lines[23], " 4□□□〇〇□□□")
            self.assertEqual(lines[24], " 5□□□〇●□□□")
            self.assertEqual(lines[25], " 6□□□□□□□□")
            self.assertEqual(lines[26], " 7□□□□□□□□")
            self.assertEqual(lines[27], " 8□□□□□□□□")
            self.assertEqual(lines[28], "")
            self.assertEqual(lines[29], "〇Test foul")
            self.assertEqual(lines[30], "〇Test win")
            self.assertEqual(lines[31], "draw")

    def test_none_display(self):
        board8x8 = Board()

        class Test():
            def next_move(self, disc, board):
                return (3, 2)

        black_player = Player('black', 'Test', Test())
        white_player = Player('white', 'User', ConsoleUserInput())

        display = NoneDisplay()

        with captured_stdout() as stdout:
            display.progress(board8x8, black_player, white_player)
            legal_moves = board8x8.get_legal_moves('black')
            display.turn(black_player, legal_moves)
            black_player.put_disc(board8x8)
            display.move(black_player, legal_moves)
            display.progress(board8x8, black_player, white_player)
            display.foul(black_player)
            display.win(black_player)
            display.draw()
            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines, [])

    def test_window_display(self):
        class TestInfo:
            def set_text(self, color, text1, text2):
                print('set_text', color, text1, text2)

            def set_turn_text_on(self, color):
                print('set_turn_text_on', color)

            def set_turn_text_off(self, color):
                print('set_turn_text_off', color)

            def set_move_text_on(self, color, x, y):
                print('set_move_text_on', color, x, y)

            def set_move_text_off(self, color):
                print('set_move_text_off', color)

            def set_foul_text_on(self, player):
                print('set_foul_text_on', player)

            def set_win_text_on(self, player):
                print('set_win_text_on', player)

            def set_lose_text_on(self, player):
                print('set_lose_text_on', player)

            def set_draw_text_on(self, player):
                print('set_draw_text_on', player)

        class TestBoard:
            def enable_move(self, x, y):
                print('enable_move', x, y)

            def disable_move(self, x, y):
                print('disable_move', x, y)

            def enable_moves(self, legal_moves):
                print('enable_moves', legal_moves)

            def disable_moves(self, legal_moves):
                print('disable_moves', legal_moves)

            def put_disc(self, color, x, y):
                print('put_disc', color, x, y)

            def turn_disc(self, color, captures):
                print('turn_disc', color, captures)

        class TestWindow:
            info = TestInfo()
            board = TestBoard()

        display = WindowDisplay(TestWindow())

        # init
        self.assertIsInstance(display.info, TestInfo)
        self.assertIsInstance(display.board, TestBoard)
        self.assertEqual(display.sleep_time_turn, 0.3)
        self.assertEqual(display.sleep_time_move, 0.3)
        self.assertIsNone(display.pre_move)

        display = WindowDisplay(TestWindow(), sleep_time_turn=0.001, sleep_time_move=0.001)
        self.assertEqual(display.sleep_time_turn, 0.001)
        self.assertEqual(display.sleep_time_move, 0.001)

        # progress
        with captured_stdout() as stdout:
            display.progress(Board(), None, None)
            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines, ['set_text black score 2', 'set_text white score 2'])

        # turn
        with captured_stdout() as stdout:
            display.turn(Player('black', 'TestPlayer', None), Board().get_legal_moves('black'))
            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines, ['set_turn_text_on black', 'enable_moves [(3, 2), (2, 3), (5, 4), (4, 5)]'])

        # move
        player = Player('black', 'TestPlayer', None)
        player.move = (5, 4)
        player.captures = [(4, 4)]
        legal_moves = Board().get_legal_moves('black')
        display.pre_move = (0, 0)
        with captured_stdout() as stdout:
            display.move(player, legal_moves)
            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines, [
                'set_turn_text_off black',
                'set_move_text_off black',
                'set_turn_text_off white',
                'set_move_text_off white',
                'disable_moves [(3, 2), (2, 3), (5, 4), (4, 5)]',
                'disable_move 0 0',
                'enable_move 5 4',
                'put_disc black 5 4',
                'set_move_text_on black f 5',
                'turn_disc black [(4, 4)]',
            ])

        # foul
        with captured_stdout() as stdout:
            display.foul(Player('black', 'TestPlayer', None))
            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines, ['set_foul_text_on black'])

        # win
        with captured_stdout() as stdout:
            display.win(Player('black', 'TestPlayer', None))
            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines, ['set_win_text_on black', 'set_lose_text_on white'])

        with captured_stdout() as stdout:
            display.win(Player('white', 'TestPlayer', None))
            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines, ['set_win_text_on white', 'set_lose_text_on black'])

        # draw
        with captured_stdout() as stdout:
            display.draw()
            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines, ['set_draw_text_on black', 'set_draw_text_on white'])

    def test_abstract_display(self):
        AbstractDisplay.progress("self", "board", "black_player", "white_player")
        AbstractDisplay.turn("self", "player", "legal_moves")
        AbstractDisplay.move("self", "player", "legal_moves")
        AbstractDisplay.foul("self", "player")
        AbstractDisplay.win("self", "player")
        AbstractDisplay.draw("self")
