#!/usr/bin/env python
"""
表示の管理
"""

import time
import abc


PLAYER_COLORS = ('black', 'white')


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
        score_b = str(black) + ":" + str(board.score[black.stone])
        score_w = str(white) + ":" + str(board.score[white.stone])

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
        for color, stone in zip(PLAYER_COLORS, (black.stone, white.stone)):
            self.window.info.set_text(color, 'score', str(board.score[stone]))

    def turn(self, player, possibles):
        """
        手番の表示
        """
        for color in PLAYER_COLORS:
            self.window.info.set_text(color, 'move', '')  # 打った手の表示を消す

        color = 'black' if player.stone == self.window.black else 'white'
        self.window.info.set_text(color, 'turn', '手番です')  # 手番の表示
        self.window.enable_moves(possibles)  # 打てる候補を表示
        time.sleep(0.3)

    def move(self, player, possibles):
        """
        手の表示
        """
        x = chr(player.move[0] + 97)
        y = str(player.move[1] + 1)

        for color in PLAYER_COLORS:
            self.window.info.set_text(color, 'turn', '')  # 手番の表示を消す

        self.window.disable_moves(possibles)  # 打てる候補のハイライトをなくす
        self.window.enable_move(*player.move)  # 打った手をハイライト
        self.window.put_stone(player.stone, *player.move)  # 石を置く
        time.sleep(0.3)
        color = 'black' if player.stone == self.window.black else 'white'
        self.window.info.set_text(color, 'move', f'({x}, {y}) に置きました')  # 打った手を表示
        self.window.turn_stone(player.stone, player.captures)  # 石をひっくり返すアニメーション
        self.window.disable_move(*player.move)

    def foul(self, player):
        """
        反則プレイヤーの表示
        """
        color = 'black' if player.stone == self.window.black else 'white'
        self.window.info.set_text(color, 'winlose', '反則')

    def win(self, player):
        """
        勝ちプレイヤーの表示
        """
        winner, loser = ('black', 'white') if player.stone == self.window.black else ('white', 'black')
        self.window.info.set_text(winner, 'winlose', '勝ち')
        self.window.info.set_text(loser,  'winlose', '負け')

    def draw(self):
        """
        引き分けの表示
        """
        for color in PLAYER_COLORS:
            self.window.info.set_text(color, 'winlose', '引き分け')


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
