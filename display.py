#!/usr/bin/env python
"""
表示の管理
"""

import abc
from board import Board


class AbstractDisplay(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def start(self, board, black, white):
        pass

    @abc.abstractmethod
    def turn(self, player, possibles):
        pass

    @abc.abstractmethod
    def move(self, player, captures, board):
        pass

    @abc.abstractmethod
    def win(self, name):
        pass

    @abc.abstractmethod
    def draw(self):
        pass


class ConsoleDisplay(AbstractDisplay):
    """
    コンソールへの表示
    """
    def start(self, board, black, white):
        """
        開始時の表示
        """
        score_b = "〇:" + str(board.black_num) + " " + black.name
        score_w = "●:" + str(board.white_num) + " " + white.name

        print(score_b, score_w)
        print(board)

    def turn(self, player, possibles):
        """
        手番の表示
        """
        if player.stone == Board.BLACK:
            print("〇" + player.name, "の番です")
        else:
            print("●" + player.name, "の番です")

        for index, value in enumerate(possibles, 1):
            coordinate = (chr(value[0] + 97), str(value[1] + 1))
            print(f'{index:2d}:', coordinate)

    def move(self, player, captures, board, black, white):
        """
        手の表示
        """
        x = chr(player.move[0] + 97)
        y = str(player.move[1] + 1)

        print((x, y), "に置きました(" + str(len(captures)) + "個取得)\n")
        self.start(board, black, white)

    def win(self, player):
        """
        勝ちプレイヤーの表示
        """
        if player.stone == Board.BLACK:
            print("〇" + player.name, "の勝ちです")
        else:
            print("●" + player.name, "の勝ちです")

    def draw(self):
        """
        引き分けの表示
        """
        print("引き分けです")


class NoneDisplay(AbstractDisplay):
    """
    表示なし
    """
    def start(self, board, black, white):
        pass

    def turn(self, player, possibles):
        pass

    def move(self, player, captures, board, black, white):
        pass

    def win(self, player):
        pass

    def draw(self):
        pass


if __name__ == '__main__':
    from board import Board
    from player import Player
    import strategies

    board = Board()
    black = Player(Board.BLACK, "Random", strategies.Random())
    white = Player(Board.WHITE, "User", strategies.ConsoleUserInput())

    display = ConsoleDisplay()
    display.start(board, black, white)

    possibles = board.get_possibles(black.stone)
    display.turn(black, possibles)

    captures = black.put_stone(board)
    display.move(black, captures, board, black, white)

    display.win(black)
    display.draw()
