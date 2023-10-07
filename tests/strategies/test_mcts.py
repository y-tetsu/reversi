"""Tests of mcts.py
"""

import unittest
import os

from reversi import C as c
from reversi.board import BitBoard
from reversi.strategies import Mcts, Node
from reversi.strategies.common import Measure
from reversi.strategies.mcts import argmax


class TestMcts(unittest.TestCase):
    """Mcts
    """
    def test_mcts_next_move(self):
        board = BitBoard(ini_black=0x90, ini_white=0x4B)
        mcts = Mcts(count=10)
        move = mcts.next_move('black', board)
        self.assertEqual(move, (2, 7))

    def test_mcts_next_move_before_remain(self):
        board = BitBoard()
        mcts = Mcts(count=10, remain=59)
        move = mcts.next_move('black', board)
        self.assertTrue(move in [(2, 3), (3, 2), (4, 5), (5, 4)])

    def test_mcts_performance(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)

        mcts = Mcts(count=10000000)
        key = mcts.__class__.__name__ + str(os.getpid())
        Measure.count[key] = 0

        mcts.next_move('white', board)

        print()
        print(key)
        print(' count(1800) :', Measure.count[key])
        print(' min         :', Measure.elp_time[key]['min'], '(s)')
        print(' max         :', Measure.elp_time[key]['max'], '(s)')
        print(' ave         :', Measure.elp_time[key]['ave'], '(s)')

    def test_node_init(self):
        color = c.black
        size = 6
        b, w, h = 1, 2, 8
        board = BitBoard(size, h, b, w)
        excount = 10
        legal_moves = [(3, 5)]
        total, count = 0, 0
        node = Node(color, board)

        self.assertEqual(node.color, color)
        self.assertEqual(node.board.size, size)
        self.assertEqual(node.board.get_bitboard_info(), (b, w, h))
        self.assertEqual(node.excount, excount)
        self.assertEqual(node.legal_moves, legal_moves)
        self.assertIsNone(node.legal_moves_o)
        self.assertEqual(node.total, total)
        self.assertEqual(node.count, count)
        self.assertIsNone(node.child_nodes)

    def test_node_copy_board(self):
        board = BitBoard()
        node = Node(c.black, board)
        new_board = node.copy_board(board)

        self.assertNotEqual(board, new_board)
        self.assertEqual(board.size, new_board.size)
        self.assertEqual(board.get_bitboard_info(), new_board.get_bitboard_info())

    def test_node_board_has_legal_moves(self):
        board = BitBoard()
        node = Node(c.black, board)
        self.assertTrue(node.board_has_legal_moves())

        board = BitBoard(ini_black=1, ini_white=2)
        node = Node(c.black, board)
        self.assertTrue(node.board_has_legal_moves())

        board = BitBoard(ini_black=2, ini_white=1)
        node = Node(c.black, board)
        self.assertTrue(node.board_has_legal_moves())

        board = BitBoard(ini_black=0xFFFFFFFF00000000, ini_white=0x00000000FFFFFFFF)
        node = Node(c.black, board)
        self.assertFalse(node.board_has_legal_moves())

    def test_node_get_winlose(self):
        board = BitBoard()
        node = Node(c.black, board)
        self.assertIsNone(node.get_winlose())

        board = BitBoard(ini_black=0xFFFFFFFF00000000, ini_white=0x00000000FFFFFFFF)
        node = Node(c.black, board)
        self.assertEqual(node.get_winlose(), 'draw')

        board = BitBoard(ini_black=0xFFFFFFFFF0000000, ini_white=0x000000000FFFFFFF)
        node = Node(c.black, board)
        self.assertEqual(node.get_winlose(), 'win')

        board = BitBoard(ini_black=0xFFFFFFFFF0000000, ini_white=0x000000000FFFFFFF)
        node = Node(c.white, board)
        self.assertEqual(node.get_winlose(), 'lose')

        board = BitBoard(ini_black=0xFFFFFFF000000000, ini_white=0x0000000FFFFFFFFF)
        node = Node(c.white, board)
        self.assertEqual(node.get_winlose(), 'win')

        board = BitBoard(ini_black=0xFFFFFFF000000000, ini_white=0x0000000FFFFFFFFF)
        node = Node(c.black, board)
        self.assertEqual(node.get_winlose(), 'lose')

    def test_node_expand(self):
        # has move
        board = BitBoard()
        node = Node(c.black, board)
        node.expand()
        expected = (
            (0x0000101810000000, 0x0000000008000000, 0x0000000000000000),
            (0x0000003810000000, 0x0000000008000000, 0x0000000000000000),
            (0x000000081C000000, 0x0000001000000000, 0x0000000000000000),
            (0x0000000818080000, 0x0000001000000000, 0x0000000000000000),
        )
        for num, child in enumerate(node.child_nodes):
            self.assertEqual(child.color, c.white)
            self.assertEqual(child.board.get_bitboard_info(), expected[num])
        # black pass
        board = BitBoard(ini_black=0x302, ini_white=1)
        node = Node(c.black, board)
        node.expand()
        expected = (
            (0x0000000000000302, 0x0000000000000001, 0x0000000000000000),
        )
        for num, child in enumerate(node.child_nodes):
            self.assertEqual(child.color, c.white)
            self.assertEqual(child.board.get_bitboard_info(), expected[num])
        # white pass
        board = BitBoard(ini_black=1, ini_white=0x302)
        node = Node(c.white, board)
        node.expand()
        expected = (
            (0x0000000000000001, 0x0000000000000302, 0x0000000000000000),
        )
        for num, child in enumerate(node.child_nodes):
            self.assertEqual(child.color, c.black)
            self.assertEqual(child.board.get_bitboard_info(), expected[num])
            # print([f'0x{i:016X}' for i in child.board.get_bitboard_info()])

    def test_node_argmax(self):
        self.assertEqual(argmax([0, 1, 1, 3, 3, 2, 3]), 3)

    def test_node_get_max_ucb1_child_node(self):
        # has 0-count nodes
        board = BitBoard()
        node = Node(c.black, board)
        node.expand()
        next_node = node.get_max_ucb1_child_node()
        self.assertEqual(next_node.board.get_bitboard_info(), (0x0000101810000000, 0x0000000008000000, 0x0000000000000000))
        # has no 0-count nodes and not pass
        for num, child in enumerate(node.child_nodes, 1):
            child.total = num ** 4
            child.count = num ** 3
        next_node = node.get_max_ucb1_child_node()
        self.assertEqual(next_node.total, 1)
        self.assertEqual(next_node.count, 1)
        # has no 0-count nodes and pass
        board = BitBoard()
        node = Node(c.white, board)
        node.board = BitBoard(ini_black=1, ini_white=0x302)
        node.expand()
        next_node = node.get_max_ucb1_child_node()
        for num, child in enumerate(node.child_nodes, 1):
            child.total = 3
            child.count = 2
        next_node = node.get_max_ucb1_child_node()
        self.assertEqual(next_node.total, 3)
        self.assertEqual(next_node.count, 2)

    def test_node_evaluate(self):
        excount = 10
        # game end win
        board = BitBoard(ini_black=0xFFFFFFFFF0000000, ini_white=0x000000000FFFFFFF)
        node = Node(c.black, board)
        value = node.evaluate()
        self.assertEqual(value, 1)
        self.assertEqual(node.total, 1)
        self.assertEqual(node.count, 1)
        # game end lose
        board = BitBoard(ini_black=0xFFFFFFF000000000, ini_white=0x0000000FFFFFFFFF)
        node = Node(c.black, board)
        value = node.evaluate()
        self.assertEqual(value, -1)
        self.assertEqual(node.total, -1)
        self.assertEqual(node.count, 1)
        # game end draw
        board = BitBoard(ini_black=0xFFFFFFFF00000000, ini_white=0x00000000FFFFFFFF)
        node = Node(c.black, board)
        value = node.evaluate()
        self.assertEqual(value, 0.5)
        self.assertEqual(node.total, 0.5)
        self.assertEqual(node.count, 1)
        # has no child nodes without pass
        board = BitBoard(ini_black=0x1, ini_white=0x2)
        node = Node(c.black, board)
        value = node.evaluate()
        self.assertEqual(value, 1)
        self.assertEqual(node.total, 1)
        self.assertEqual(node.count, 1)
        # has no child nodes with pass without expand
        board = BitBoard(ini_black=0x1, ini_white=0x2)
        node = Node(c.white, board)
        node.count = excount - 2
        value = node.evaluate()
        self.assertEqual(value, -1)
        self.assertEqual(node.total, -1)
        self.assertEqual(node.count, excount - 1)
        self.assertIsNone(node.child_nodes)
        # has no child nodes without pass with expand
        board = BitBoard(ini_black=0x1, ini_white=0xA)
        node = Node(c.black, board)
        node.count = excount - 1
        value = node.evaluate()
        self.assertEqual(value, 1)
        self.assertEqual(node.total, 1)
        self.assertEqual(node.count, excount)
        expected = (
            (0x0000000000000007, 0x0000000000000008, 0x0000000000000000),
        )
        for num, child in enumerate(node.child_nodes):
            self.assertEqual(child.board.get_bitboard_info(), expected[num])
        # has child nodes
        value = node.evaluate()
        self.assertEqual(value, 1)
        self.assertEqual(node.total, 2)
        self.assertEqual(node.count, excount + 1)
        self.assertEqual(node.child_nodes[0].total, -1)
        self.assertEqual(node.child_nodes[0].count, 1)
