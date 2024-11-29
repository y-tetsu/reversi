"""Tests of game.py
"""

import unittest
from test.support import captured_stdout

from reversi.game import Game
from reversi.board import Board, PyListBoard, PyBitBoard, BitBoardMethods
from reversi.player import Player
from reversi.display import NoneDisplay
from reversi.strategies.common import AbstractStrategy


class TestGame(unittest.TestCase):
    """game
    """
    def test_game_init(self):
        class Black(AbstractStrategy):
            def next_move(self, color, board):
                return (0, 0)

        class White(AbstractStrategy):
            def next_move(self, color, board):
                return (0, 0)

        black = Player('black', 'Black', Black())
        white = Player('white', 'White', White())
        game = Game(black, white)
        self.assertIsInstance(game.black_player.strategy, Black)
        self.assertIsInstance(game.white_player.strategy, White)
        self.assertIsInstance(game.board, BitBoardMethods.cy.CyBoard8_64bit.CythonBitBoard)
        self.assertEqual(game.players, [black, white])
        self.assertEqual(game.black_player, game.players[0])
        self.assertEqual(game.white_player, game.players[1])
        self.assertIsInstance(game.display, NoneDisplay)
        self.assertEqual(game.cancel, None)
        self.assertEqual(game.result, [])

    def test_game(self):
        class TestDisplay:
            def progress(self, board, black_player, white_player):
                print('display.progress', '\n' + str(board), black_player, white_player)

            def turn(self, player, legal_moves):
                print('display.turn', player, legal_moves)

            def move(self, player, legal_moves):
                print('display.move', player.move, legal_moves)

            def foul(self, player):
                print('display.foul', player)

            def win(self, player):
                print('display.win', player)

            def draw(self):
                print('display.draw')

        class TopLeft(AbstractStrategy):
            def next_move(self, color, board):
                return board.get_legal_moves(color)[0]

        class BottomRight(AbstractStrategy):
            def next_move(self, color, board):
                return board.get_legal_moves(color)[-1]

        class Foul(AbstractStrategy):
            def next_move(self, color, board):
                return (board.size//2, board.size//2)

        class TestCancel:
            class TestEvent:
                def is_set(self):
                    print('cancel-event is set')
                    return True
            event = TestEvent()

        p1 = Player('black', 'TopLeft', TopLeft())
        p2 = Player('white', 'BottomRight', BottomRight())
        p3 = Player('white', 'TopLeft', TopLeft())
        p4 = Player('black', 'Foul', Foul())
        p5 = Player('white', 'Foul', Foul())

        # init
        game1 = Game(p1, p2, Board(4), TestDisplay())
        self.assertIsInstance(game1.board, PyBitBoard)
        self.assertIsInstance(game1.black_player.strategy, TopLeft)
        self.assertIsInstance(game1.white_player.strategy, BottomRight)
        self.assertEqual(game1.black_player, game1.players[0])
        self.assertEqual(game1.white_player, game1.players[1])
        self.assertEqual(game1.cancel, None)
        self.assertEqual(game1.result, [])

        game2 = Game(p1, p3, Board(4), TestDisplay())
        self.assertIsInstance(game2.board, PyBitBoard)
        self.assertIsInstance(game2.black_player.strategy, TopLeft)
        self.assertIsInstance(game2.white_player.strategy, TopLeft)
        self.assertEqual(game2.black_player, game2.players[0])
        self.assertEqual(game2.white_player, game2.players[1])
        self.assertEqual(game2.cancel, None)
        self.assertEqual(game2.result, [])

        game3 = Game(p1, p2, Board(4), TestDisplay(), 'white', TestCancel())
        self.assertIsInstance(game3.board, PyBitBoard)
        self.assertIsInstance(game3.black_player.strategy, TopLeft)
        self.assertIsInstance(game3.white_player.strategy, BottomRight)
        self.assertEqual(game3.black_player, game3.players[1])
        self.assertEqual(game3.white_player, game3.players[0])
        self.assertTrue(game3.cancel, TestCancel)
        self.assertEqual(game3.result, [])

        game4 = Game(p4, p2, PyListBoard(4), TestDisplay())
        self.assertIsInstance(game4.board, PyListBoard)
        self.assertIsInstance(game4.black_player.strategy, Foul)
        self.assertIsInstance(game4.white_player.strategy, BottomRight)
        self.assertEqual(game4.black_player, game4.players[0])
        self.assertEqual(game4.white_player, game4.players[1])
        self.assertEqual(game4.cancel, None)
        self.assertEqual(game4.result, [])

        game5 = Game(p1, p5, PyListBoard(4), TestDisplay())
        self.assertIsInstance(game5.board, PyListBoard)
        self.assertIsInstance(game5.black_player.strategy, TopLeft)
        self.assertIsInstance(game5.white_player.strategy, Foul)
        self.assertEqual(game5.black_player, game5.players[0])
        self.assertEqual(game5.white_player, game5.players[1])
        self.assertEqual(game5.cancel, None)
        self.assertEqual(game5.result, [])

        # play-black-win
        with captured_stdout() as stdout:
            game1.play()

            lines = stdout.getvalue().splitlines()
            output_ret = [
                'display.progress ',
                '   a b c d',
                ' 1□□□□',
                ' 2□●〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn 〇TopLeft [(1, 0), (0, 1), (3, 2), (2, 3)]',
                'display.move (1, 0) [(1, 0), (0, 1), (3, 2), (2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇□□',
                ' 2□〇〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn ●BottomRight [(0, 0), (2, 0), (0, 2)]',
                'display.move (0, 2) [(0, 0), (2, 0), (0, 2)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇□□',
                ' 2□〇〇□',
                ' 3●●●□',
                ' 4□□□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn 〇TopLeft [(0, 3), (1, 3), (2, 3), (3, 3)]',
                'display.move (0, 3) [(0, 3), (1, 3), (2, 3), (3, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇□□',
                ' 2□〇〇□',
                ' 3●〇●□',
                ' 4〇□□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn ●BottomRight [(0, 0), (2, 0)]',
                'display.move (2, 0) [(0, 0), (2, 0)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇●□',
                ' 2□●●□',
                ' 3●〇●□',
                ' 4〇□□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn 〇TopLeft [(3, 0), (0, 1), (3, 2)]',
                'display.move (3, 0) [(3, 0), (0, 1), (3, 2)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇〇〇',
                ' 2□●〇□',
                ' 3●〇●□',
                ' 4〇□□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn ●BottomRight [(3, 1), (1, 3)]',
                'display.move (1, 3) [(3, 1), (1, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇〇〇',
                ' 2□●〇□',
                ' 3●●●□',
                ' 4〇●□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn 〇TopLeft [(0, 1), (2, 3)]',
                'display.move (0, 1) [(0, 1), (2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇〇〇',
                ' 2〇〇〇□',
                ' 3〇●●□',
                ' 4〇●□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn ●BottomRight [(0, 0)]',
                'display.move (0, 0) [(0, 0)]',
                'display.progress ',
                '   a b c d',
                ' 1●〇〇〇',
                ' 2〇●〇□',
                ' 3〇●●□',
                ' 4〇●□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn 〇TopLeft [(3, 2), (2, 3)]',
                'display.move (3, 2) [(3, 2), (2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●〇〇〇',
                ' 2〇●〇□',
                ' 3〇〇〇〇',
                ' 4〇●□□',
                ' 〇TopLeft ●BottomRight',
                'display.turn ●BottomRight [(3, 1), (3, 3)]',
                'display.move (3, 3) [(3, 1), (3, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●〇〇〇',
                ' 2〇●〇□',
                ' 3〇〇●〇',
                ' 4〇●□●',
                ' 〇TopLeft ●BottomRight',
                'display.turn 〇TopLeft [(2, 3)]',
                'display.move (2, 3) [(2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●〇〇〇',
                ' 2〇●〇□',
                ' 3〇〇〇〇',
                ' 4〇〇〇●',
                ' 〇TopLeft ●BottomRight',
                'display.turn ●BottomRight [(3, 1)]',
                'display.move (3, 1) [(3, 1)]',
                'display.progress ',
                '   a b c d',
                ' 1●〇〇〇',
                ' 2〇●●●',
                ' 3〇〇〇●',
                ' 4〇〇〇●',
                ' 〇TopLeft ●BottomRight',
                'display.win 〇TopLeft',
            ]
            self.assertEqual(lines, output_ret)
            self.assertEqual(game1.result.winlose, Game.BLACK_WIN)
            self.assertEqual(game1.result.black_name, 'TopLeft')
            self.assertEqual(game1.result.white_name, 'BottomRight')
            self.assertEqual(game1.result.black_num, 10)
            self.assertEqual(game1.result.white_num, 6)

        # play-white-win
        with captured_stdout() as stdout:
            game2.play()

            lines = stdout.getvalue().splitlines()
            output_ret = [
                'display.progress ',
                '   a b c d',
                ' 1□□□□',
                ' 2□●〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn 〇TopLeft [(1, 0), (0, 1), (3, 2), (2, 3)]',
                'display.move (1, 0) [(1, 0), (0, 1), (3, 2), (2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇□□',
                ' 2□〇〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn ●TopLeft [(0, 0), (2, 0), (0, 2)]',
                'display.move (0, 0) [(0, 0), (2, 0), (0, 2)]',
                'display.progress ',
                '   a b c d',
                ' 1●〇□□',
                ' 2□●〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn 〇TopLeft [(0, 1), (3, 2), (2, 3)]',
                'display.move (0, 1) [(0, 1), (3, 2), (2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●〇□□',
                ' 2〇〇〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn ●TopLeft [(2, 0), (0, 2)]',
                'display.move (2, 0) [(2, 0), (0, 2)]',
                'display.progress ',
                '   a b c d',
                ' 1●●●□',
                ' 2〇〇●□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn 〇TopLeft [(3, 0), (3, 1), (3, 2), (3, 3)]',
                'display.move (3, 0) [(3, 0), (3, 1), (3, 2), (3, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●●●〇',
                ' 2〇〇〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn ●TopLeft [(0, 2), (3, 2), (1, 3)]',
                'display.move (0, 2) [(0, 2), (3, 2), (1, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●●●〇',
                ' 2●●〇□',
                ' 3●●●□',
                ' 4□□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn 〇TopLeft [(0, 3), (2, 3)]',
                'display.move (0, 3) [(0, 3), (2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●●●〇',
                ' 2●●〇□',
                ' 3●〇●□',
                ' 4〇□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn ●TopLeft [(3, 1), (3, 2), (1, 3), (2, 3)]',
                'display.move (3, 1) [(3, 1), (3, 2), (1, 3), (2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●●●〇',
                ' 2●●●●',
                ' 3●〇●□',
                ' 4〇□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn 〇TopLeft [(3, 2)]',
                'display.move (3, 2) [(3, 2)]',
                'display.progress ',
                '   a b c d',
                ' 1●●●〇',
                ' 2●●●〇',
                ' 3●〇〇〇',
                ' 4〇□□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn ●TopLeft [(1, 3), (2, 3), (3, 3)]',
                'display.move (1, 3) [(1, 3), (2, 3), (3, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●●●〇',
                ' 2●●●〇',
                ' 3●●〇〇',
                ' 4〇●□□',
                ' 〇TopLeft ●TopLeft',
                'display.turn 〇TopLeft [(2, 3)]',
                'display.move (2, 3) [(2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●●●〇',
                ' 2●●●〇',
                ' 3●●〇〇',
                ' 4〇〇〇□',
                ' 〇TopLeft ●TopLeft',
                'display.turn ●TopLeft [(3, 3)]',
                'display.move (3, 3) [(3, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1●●●〇',
                ' 2●●●〇',
                ' 3●●●〇',
                ' 4〇〇〇●',
                ' 〇TopLeft ●TopLeft',
                'display.win ●TopLeft',
            ]
            self.assertEqual(lines, output_ret)
            self.assertEqual(game2.result.winlose, Game.WHITE_WIN)
            self.assertEqual(game2.result.black_name, 'TopLeft')
            self.assertEqual(game2.result.white_name, 'TopLeft')
            self.assertEqual(game2.result.black_num, 6)
            self.assertEqual(game2.result.white_num, 10)

        # play-cancel-draw
        with captured_stdout() as stdout:
            game3.play()

            lines = stdout.getvalue().splitlines()
            output_ret = [
                'display.progress ',
                '   a b c d',
                ' 1□□□□',
                ' 2□●〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●BottomRight',
                'cancel-event is set',
                'display.draw',
            ]
            self.assertEqual(lines, output_ret)
            self.assertEqual(game3.result.winlose, Game.DRAW)
            self.assertEqual(game3.result.black_name, 'TopLeft')
            self.assertEqual(game3.result.white_name, 'BottomRight')
            self.assertEqual(game3.result.black_num, 2)
            self.assertEqual(game3.result.white_num, 2)

        # play-black-foul
        with captured_stdout() as stdout:
            game4.play()

            lines = stdout.getvalue().splitlines()
            output_ret = [
                'display.progress ',
                '   a b c d',
                ' 1□□□□',
                ' 2□●〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇Foul ●BottomRight',
                'display.turn 〇Foul [(1, 0), (0, 1), (3, 2), (2, 3)]',
                'display.move (2, 2) [(1, 0), (0, 1), (3, 2), (2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1□□□□',
                ' 2□●〇□',
                ' 3□〇〇□',
                ' 4□□□□',
                ' 〇Foul ●BottomRight',
                'display.foul 〇Foul',
                'display.win ●BottomRight',
            ]
            self.assertEqual(lines, output_ret)
            self.assertEqual(game4.result.winlose, Game.WHITE_WIN)
            self.assertEqual(game4.result.black_name, 'Foul')
            self.assertEqual(game4.result.white_name, 'BottomRight')
            self.assertEqual(game4.result.black_num, 3)
            self.assertEqual(game4.result.white_num, 1)

        # play-white-foul
        with captured_stdout() as stdout:
            game5.play()

            lines = stdout.getvalue().splitlines()
            output_ret = [
                'display.progress ',
                '   a b c d',
                ' 1□□□□',
                ' 2□●〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●Foul',
                'display.turn 〇TopLeft [(1, 0), (0, 1), (3, 2), (2, 3)]',
                'display.move (1, 0) [(1, 0), (0, 1), (3, 2), (2, 3)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇□□',
                ' 2□〇〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●Foul',
                'display.turn ●Foul [(0, 0), (2, 0), (0, 2)]',
                'display.move (2, 2) [(0, 0), (2, 0), (0, 2)]',
                'display.progress ',
                '   a b c d',
                ' 1□〇□□',
                ' 2□〇〇□',
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇TopLeft ●Foul',
                'display.foul ●Foul',
                'display.win 〇TopLeft',
            ]
            self.assertEqual(lines, output_ret)
            self.assertEqual(game5.result.winlose, Game.BLACK_WIN)
            self.assertEqual(game5.result.black_name, 'TopLeft')
            self.assertEqual(game5.result.white_name, 'Foul')
            self.assertEqual(game5.result.black_num, 4)
            self.assertEqual(game5.result.white_num, 1)

    def test_game_players_setup(self):
        class SetUp(AbstractStrategy):
            def init(self):
                self.info = None

            def setup(self, board):
                self.info = board.get_board_info()

            def next_move(self, color, board):
                return board.get_legal_moves(color)[0]

        p1 = Player('black', 'setup1', SetUp())
        p2 = Player('white', 'setup2', SetUp())
        board = Board(6)
        expected = board.get_board_info()

        game = Game(p1, p2, board, NoneDisplay())
        game.play()

        self.assertEqual(p1.strategy.info, expected)
        self.assertEqual(p2.strategy.info, expected)

        board = Board(8)
        expected = board.get_board_info()

        game = Game(p1, p2, board, NoneDisplay())
        game.play()

        self.assertEqual(p1.strategy.info, expected)
        self.assertEqual(p2.strategy.info, expected)

    def test_game_players_teardown(self):
        class TearDown(AbstractStrategy):
            def init(self):
                self.info = None
                self.result = None

            def teardown(self, board, result):
                self.info = board.get_board_info()
                self.result = result

            def next_move(self, color, board):
                return board.get_legal_moves(color)[0]

        p1 = Player('black', 'setup1', TearDown())
        p2 = Player('white', 'setup2', TearDown())
        board = Board(6)

        game = Game(p1, p2, board, NoneDisplay())
        game.play()
        expected_board = board.get_board_info()
        expected_result = game.result

        self.assertEqual(p1.strategy.info, expected_board)
        self.assertEqual(p1.strategy.result, expected_result)
        self.assertEqual(p2.strategy.info, expected_board)
        self.assertEqual(p2.strategy.result, expected_result)

        board = Board(8)

        game = Game(p1, p2, board, NoneDisplay())
        game.play()
        expected_board = board.get_board_info()
        expected_result = game.result

        self.assertEqual(p1.strategy.info, expected_board)
        self.assertEqual(p1.strategy.result, expected_result)
        self.assertEqual(p2.strategy.info, expected_board)
        self.assertEqual(p2.strategy.result, expected_result)
