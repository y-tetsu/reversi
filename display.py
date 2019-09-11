#!/usr/bin/env python
"""
表示の管理
"""

import time
import abc


class AbstractDisplay(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def progress(self, board, black, white):
        pass

    @abc.abstractmethod
    def turn(self, player, possibles):
        pass

    @abc.abstractmethod
    def move(self, player, possibles):
        pass

    @abc.abstractmethod
    def foul(self, player):
        pass

    @abc.abstractmethod
    def win(self, player):
        pass

    @abc.abstractmethod
    def draw(self):
        pass


class ConsoleDisplay(AbstractDisplay):
    """
    コンソールへの表示
    """
    def progress(self, board, black, white):
        """
        ゲームの進行の表示(スコア、ボード状態)
        """
        score_b = str(black) + ":" + str(board.num[black.stone])
        score_w = str(white) + ":" + str(board.num[white.stone])

        print(score_b, score_w)
        print(board)

    def turn(self, player, possibles):
        """
        手番の表示
        """
        time.sleep(1)
        print(player, "の番です")

        for index, value in enumerate(possibles, 1):
            coordinate = (chr(value[0] + 97), str(value[1] + 1))
            print(f'{index:2d}:', coordinate)

    def move(self, player, possibles):
        """
        手の表示
        """
        x = chr(player.move[0] + 97)
        y = str(player.move[1] + 1)

        print((x, y), "に置きました\n")
        time.sleep(1)

    def foul(self, player):
        """
        反則プレイヤーの表示
        """
        print(player, "の反則")

    def win(self, player):
        """
        勝ちプレイヤーの表示
        """
        print(player, "の勝ちです")

    def draw(self):
        """
        引き分けの表示
        """
        print("引き分けです")


class NoneDisplay(AbstractDisplay):
    """
    表示なし
    """
    def progress(self, board, black, white):
        pass

    def turn(self, player, possibles):
        pass

    def move(self, player, possibles):
        pass

    def foul(self, player):
        pass

    def win(self, player):
        pass

    def draw(self):
        pass


class WindowDisplay(AbstractDisplay):
    """
    GUIへの表示
    """
    def __init__(self, window):
        self.window = window

    def progress(self, board, black, white):
        """
        ゲームの進行の表示(スコア)
        """
        black_num = self.window.black_stonenum
        self.window.canvas.itemconfigure(black_num, text=str(board.num[black.stone]))

        white_num = self.window.white_stonenum
        self.window.canvas.itemconfigure(white_num, text=str(board.num[white.stone]))

    def turn(self, player, possibles):
        """
        手番の表示
        """
        time.sleep(1)

        # 手の表示を消す
        black_move = self.window.black_move
        self.window.canvas.itemconfigure(black_move, text='')

        white_move = self.window.white_move
        self.window.canvas.itemconfigure(white_move, text='')

        # 手番を表示
        if player.stone == self.window.black:
            black_turn = self.window.black_turn
            self.window.canvas.itemconfigure(black_turn, text="手番です")
        elif player.stone == self.window.white:
            white_turn = self.window.white_turn
            self.window.canvas.itemconfigure(white_turn, text="手番です")

        # 候補を表示
        self.window.enable_moves(possibles)

    def move(self, player, possibles):
        """
        手の表示
        """
        x = chr(player.move[0] + 97)
        y = str(player.move[1] + 1)

        time.sleep(0.5)

        # 手番を消す
        black_turn = self.window.black_turn
        self.window.canvas.itemconfigure(black_turn, text="")

        white_turn = self.window.white_turn
        self.window.canvas.itemconfigure(white_turn, text="")

        # 手を表示
        if player.stone == self.window.black:
            black_move = self.window.black_move
            self.window.canvas.itemconfigure(black_move, text=f'({x}, {y}) に置きました')

        elif player.stone == self.window.white:
            white_move = self.window.white_move
            self.window.canvas.itemconfigure(white_move, text=f'({x}, {y}) に置きました')

        # 石を置く表示
        self.window.disable_moves(possibles)
        self.window.enable_move(*player.move)
        self.window.put_stone(player.stone, *player.move)
        time.sleep(0.5)
        self.window.turn_stone(player.stone, player.captures)
        self.window.disable_move(*player.move)

    def foul(self, player):
        """
        反則プレイヤーの表示
        """
        if player.stone == self.window.black:
            black_winlose = self.window.black_winlose
            self.window.canvas.itemconfigure(black_winlose, text='反則')
        elif player.stone == self.window.white:
            white_winlose = self.window.white_winlose
            self.window.canvas.itemconfigure(white_winlose, text='反則')

    def win(self, player):
        """
        勝ちプレイヤーの表示
        """
        if player.stone == self.window.black:
            black_winlose = self.window.black_winlose
            self.window.canvas.itemconfigure(black_winlose, text='勝ち')
            white_winlose = self.window.white_winlose
            self.window.canvas.itemconfigure(white_winlose, text='負け')
        elif player.stone == self.window.white:
            white_winlose = self.window.white_winlose
            self.window.canvas.itemconfigure(white_winlose, text='勝ち')
            black_winlose = self.window.black_winlose
            self.window.canvas.itemconfigure(black_winlose, text='負け')

    def draw(self):
        """
        引き分けの表示
        """
        black_winlose = self.window.black_winlose
        self.window.canvas.itemconfigure(black_winlose, text='引き分け')
        white_winlose = self.window.white_winlose
        self.window.canvas.itemconfigure(white_winlose, text='引き分け')


if __name__ == '__main__':
    from board import Board
    from player import Player
    import strategies

    board8x8 = Board()
    black = Player(board8x8.black, "Random", strategies.Random())
    white = Player(board8x8.white, "User", strategies.ConsoleUserInput())

    display = ConsoleDisplay()
    display.progress(board8x8, black, white)

    possibles = board8x8.get_possibles(black.stone)
    display.turn(black, possibles)

    black.put_stone(board8x8)
    display.move(black, possibles)
    display.progress(board8x8, black, white)

    display.foul(black)
    display.win(black)
    display.draw()
