"""Tests of game.py
"""

import unittest
from test.support import captured_stdout

from reversi.game import Game
from reversi.board import Board
from reversi.player import Player
from reversi.strategies.common import AbstractStrategy


class TestGame(unittest.TestCase):
    """game
    """
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
                return list(board.get_legal_moves(color).keys())[0]

        class BottomRight(AbstractStrategy):
            def next_move(self, color, board):
                return list(board.get_legal_moves(color).keys())[-1]

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
        game1 = Game(Board(4), p1, p2, TestDisplay())
        self.assertTrue(isinstance(game1.board, Board))
        self.assertTrue(isinstance(game1.black_player.strategy, TopLeft))
        self.assertTrue(isinstance(game1.white_player.strategy, BottomRight))
        self.assertEqual(game1.black_player, game1.players[0])
        self.assertEqual(game1.white_player, game1.players[1])
        self.assertEqual(game1.cancel, None)
        self.assertEqual(game1.result, [])

        game2 = Game(Board(4), p1, p3, TestDisplay())
        self.assertTrue(isinstance(game2.board, Board))
        self.assertTrue(isinstance(game2.black_player.strategy, TopLeft))
        self.assertTrue(isinstance(game2.white_player.strategy, TopLeft))
        self.assertEqual(game2.black_player, game2.players[0])
        self.assertEqual(game2.white_player, game2.players[1])
        self.assertEqual(game2.cancel, None)
        self.assertEqual(game2.result, [])

        game3 = Game(Board(4), p1, p2, TestDisplay(), 'white', TestCancel())
        self.assertTrue(isinstance(game3.board, Board))
        self.assertTrue(isinstance(game3.black_player.strategy, TopLeft))
        self.assertTrue(isinstance(game3.white_player.strategy, BottomRight))
        self.assertEqual(game3.black_player, game3.players[1])
        self.assertEqual(game3.white_player, game3.players[0])
        self.assertTrue(isinstance(game3.cancel, TestCancel))
        self.assertEqual(game3.result, [])

        game4 = Game(Board(4), p4, p2, TestDisplay())
        self.assertTrue(isinstance(game4.board, Board))
        self.assertTrue(isinstance(game4.black_player.strategy, Foul))
        self.assertTrue(isinstance(game4.white_player.strategy, BottomRight))
        self.assertEqual(game4.black_player, game4.players[0])
        self.assertEqual(game4.white_player, game4.players[1])
        self.assertEqual(game4.cancel, None)
        self.assertEqual(game4.result, [])

        game5 = Game(Board(4), p1, p5, TestDisplay())
        self.assertTrue(isinstance(game5.board, Board))
        self.assertTrue(isinstance(game5.black_player.strategy, TopLeft))
        self.assertTrue(isinstance(game5.white_player.strategy, Foul))
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
                ' 3□〇●□',
                ' 4□□□□',
                ' 〇Foul ●BottomRight',
                'display.foul 〇Foul',
                'display.win ●BottomRight',
            ]
            self.assertEqual(lines, output_ret)
            self.assertEqual(game4.result.winlose, Game.WHITE_WIN)
            self.assertEqual(game4.result.black_name, 'Foul')
            self.assertEqual(game4.result.white_name, 'BottomRight')
            self.assertEqual(game4.result.black_num, 2)
            self.assertEqual(game4.result.white_num, 2)

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
