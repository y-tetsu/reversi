<p align="center">
<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/reversi_v0_0_15.png" width="500px">
</p>


# reversi
[ [English](https://github.com/y-tetsu/reversi/blob/master/README.en.md) | [日本語](https://github.com/y-tetsu/reversi/blob/master/README.md)]<br>
**reversi**はリバーシ(オセロ)のPython用ライブラリです。<br>
手軽にリバーシAIをプログラミングして、アプリケーションが作れます。<br>
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Build Status](https://travis-ci.org/y-tetsu/reversi.svg?branch=master)](https://travis-ci.org/y-tetsu/reversi)
[![codecov](https://codecov.io/gh/y-tetsu/reversi/branch/master/graph/badge.svg)](https://codecov.io/gh/y-tetsu/reversi)
<br>


## 目次
- [概要](#概要)
- [動作環境](#動作環境)
- [インストール方法](#インストール方法)
- [アンインストール方法](#アンインストール方法)
- [サンプル](#サンプル)
- [ライブラリの使い方](#ライブラリの使い方)
    - [アプリケーションを起動させる](#アプリケーションを起動させる)
    - [アプリケーションにAIを追加する](#アプリケーションにAIを追加する)
    - [AIをプログラミングする](#AIをプログラミングする)
    - [AI同士の対戦をシミュレートする](#AI同士の対戦をシミュレートする)
    - [boardオブジェクトの使い方](#boardオブジェクトの使い方)
- [インストールがうまくいかない場合](#インストールがうまくいかない場合)
- [Windows版アプリケーションについて](#Windows版アプリケーションについて)
    - [ゲーム紹介](#ゲーム紹介)
    - [ダウンロード](#ダウンロード)
    - [メニュー一覧](#メニュー一覧)
    - [プレイヤー紹介](#プレイヤー紹介)
    - [プレイヤー追加機能](#プレイヤー追加機能)
- [参考書籍](#参考書籍)
- [参考サイト](#参考サイト)
- [脚注](#脚注)


## 概要
**reversi**は<a id="return1">Python</a>で作られた<sup>[[1]](#note1)</sup>Pythonで使えるリバーシのライブラリです。<br>
**reversi**をインストールすると、リバーシAIのプログラミングを手軽に試せるようになります。<br>

他にも、以下のような用途に使えます。
- リバーシAI同士の対戦シミュレート
- アプリケーションの作成

また、本ライブラリを使って作成した[Windows版アプリケーション](#Windows版アプリケーションについて)も用意しております。<br>
こちらはダウンロード後、インストール不要で、すぐにリバーシのゲームをプレイできます(無料)。

<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/tkinter_app_demo_v0_0_15.gif" width="550px">

<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/console_app_demo.gif" width="550px">

<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/simulator_demo.gif" width="550px">


## 動作環境
- Windows10 64bit<br>
- ディスプレイサイズ 1366x768 以上
- プロセッサ 1.6GHz 以上
- メモリ 4.00GB 以上
- [Python 3.7.6](https://www.python.org/downloads/release/python-376/)(ライブラリインストール時のみ必要)<br>
    - cython 0.29.15<br>
    - pyinstaller 3.6<br>
- [Microsoft Visual C++ 2019](https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc)(ライブラリ開発時のみ必要)<br>


## インストール方法
1. [Python 3.7.6](https://www.python.org/downloads/release/python-376/)をインストールしてください。<br>
2. 下記を実行して**reversi**をインストールしてください。
```
$ py -3.7 -m pip install git+https://github.com/y-tetsu/reversi
```


## アンインストール方法
**reversi**をアンインストールする場合は、下記を実行してください。
```
$ py -3.7 -m pip uninstall reversi
```


## サンプル
**reversi**をインストール後、任意のフォルダで下記コマンドを実行すると、サンプルをコピーできます。
```
$ install_reversi_examples
```

コピーされるサンプルは下記のとおりです。

- [01_tkinter_app.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/01_tkinter_app.py) - tkinterを使ったGUIアプリケーション
- [02_console_app.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/02_console_app.py) - コンソール上で遊ぶアプリケーション
- [03_create_exe.bat](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/03_create_exe.bat) - GUIアプリケーションのexeファイルを作成するバッチファイル
- [04_reversi_simulator.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/04_reversi_simulator.py) - AI同士を対戦させて結果を表示するシミュレータ
- [05_manual_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/05_manual_strategy.py) - 自作したAIを実装するサンプル
- [06_table_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/06_table_strategy.py) - テーブルによる重みづけで手を選ぶAIを実装するサンプル
- [07_minmax_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/07_minmax_strategy.py) - MinMax法で手を選ぶAIを実装するサンプル
- [08_alphabeta_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/08_alphabeta_strategy.py) - AlphaBeta法で手を選ぶAIを実装するサンプル
- [09_genetic_algorithm.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/09_genetic_algorithm.py) - 遺伝的アルゴリズムを使ってテーブルの重みを求めるサンプル

サンプルの実行方法はそれぞれ下記のとおりです。
```
$ cd reversi_examples
$ py -3.7 01_tkinter_app.py
$ py -3.7 02_console_app.py
$ 03_create_exe.bat
$ py -3.7 04_reversi_simulator.py
$ py -3.7 05_manual_strategy.py
$ py -3.7 06_table_strategy.py
$ py -3.7 07_minmax_strategy.py
$ py -3.7 08_alphabeta_strategy.py
$ py -3.7 09_genetic_algorithm.py
```


## ライブラリの使い方
本ライブラリの使い方を、コーディング例を元に説明します。

### アプリケーションを起動させる
まず最初に、リバーシのGUIアプリケーションを起動させる方法を示します。

下記のコードを実行してください。
```Python
from reversi import Reversi

Reversi().start()
```
アプリケーションが起動し、そのまま遊ぶ事ができます。<br>
ただしこの場合、選択できるプレイヤーはユーザ操作のみとなります。

### アプリケーションにAIを追加する
次に、AIをアプリケーションに追加する方法を示します。

例として、ライブラリにあらかじめ組み込まれている下記AIをアプリケーションに追加します。
- ランダムな手を打つAI : `Random`
- できるだけ多く石が取れる手を打つAI : `Greedy`
```Python
from reversi import Reversi
from reversi.strategies import Random, Greedy

Reversi(
    {
        'RANDOM': Random(),
        'GREEDY': Greedy(),
    }
).start()
```
上記を実行すると、ユーザ操作に加えて"RANDOM"と"GREEDY"をプレイヤーとして選択できるようになります。

組み込みのAIは、すべて`reversi.strategies`よりインポートすることができます。<br>
また、追加するプレイヤーの情報(以後、"プレイヤー情報")は、下記フォーマットに従ってください。
```Python
{
    'プレイヤー名1': AIクラスのオブジェクト1,
    'プレイヤー名2': AIクラスのオブジェクト2,
    'プレイヤー名3': AIクラスのオブジェクト3,
}
```

### AIをプログラミングする
続いて、本ライブラリを使って独自のAIを自作し、アプリケーションに追加する方法を示します。

#### AIクラスの作り方
下記のようにコーディングすると、AIクラスが完成します。
```Python
from reversi.strategies import AbstractStrategy

class OriginalAI(AbstractStrategy):
    def next_move(self, color, board):
        #
        # 次の一手(X, Y)を決めるロジックをコーディングして下さい。
        #

        return (X, Y)
```
`next_move`メソッドの引数は下記を参照して下さい。
 |引数|説明|
 |:---|:---|
 |`color`変数|`black`か`white`の`str`型の文字列が入り、それぞれ黒番か白番かを判別することができます。|
 |`board`オブジェクト|リバーシの盤面情報を持ったオブジェクトです。黒と白の石の配置情報のほか、リバーシのゲームを進行するために必要となる、パラメータやメソッドを持っています。|

なお、戻り値の(X, Y)座標は盤面左上を(0, 0)とした時の値となります。<br>
盤面サイズが8の場合の各マス目の座標を下図に示します。

![coordinate](https://raw.githubusercontent.com/y-tetsu/reversi/images/coordinate.png)

`board`オブジェクトについてはここでは簡単のため、
石が置ける位置を取得する`get_legal_moves`メソッドと、盤面のサイズを取得する`size`パラメータの、2つのみを取り上げます。

#### 石が置ける位置の取得方法
ある盤面の石が置ける位置(座標)は`board`オブジェクトの`get_legal_moves`メソッドで取得できます。
`get_legal_moves`呼び出し時の引数には、黒か白のどちらかの手番(`color`変数)を与えてください。

```Python
legal_moves = board.get_legal_moves(color)
```

`get_legal_moves`の戻り値"石が置ける座標のリスト"となっております。

初期状態(盤面サイズ8)での黒手番の結果は下記のとおりです。

```
[(3, 2), (2, 3), (5, 4), (4, 5)]
```

#### 盤面のサイズ
本アプリケーションは、盤面のサイズとして4～26までの偶数が選べる仕様となっております。
必要に応じて、いずれの場合でも動作するよう盤面のサイズを考慮するようにしてください。

盤面のサイズは下記で取得できます。

```Python
size = board.size
```

#### 「角が取れる時は必ず取る」AIの実装
それでは、AIの作成例として4角が取れる時は必ず取り、
そうでない時はランダムに打つ、`Corner`というAIを実装する例を示します(プレイヤー名は"CORNER"とします)。

```Python
import random

from reversi import Reversi
from reversi.strategies import AbstractStrategy

class Corner(AbstractStrategy):
    def next_move(self, color, board):
        size = board.size
        legal_moves = board.get_legal_moves(color)
        for corner in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]:
            if corner in legal_moves:
                return corner

        return random.choice(legal_moves)

Reversi({'CORNER': Corner()}).start()
```

上記を実行すると、対戦プレイヤーに"CORNER"が選択可能となります。
実際に対戦してみると、角が取れる時に必ず取ってくることが分かると思います。

### AI同士の対戦をシミュレートする
本ライブラリのシミュレータを使うと、AI同士の対戦をシミュレートし結果を確認することができます。<br>
自作したAI同士を複数回対戦させることで、AIの強さを測る事ができます。<br>
(AIの打つ手が、特定の盤面に対して固定となる場合は、別途後述のrandom_openingパラメータを設定することで、強さを測りやすくできます)

シミュレータの実行例として、
これまでに登場した"RANDOM"、"GREEDY"、"CORNER"を総当たりで対戦させ、結果を表示するまでを示します。


#### シミュレータの実行
下記を実行すると、シミュレーションを開始します。
```Python
from reversi import Simulator

if __name__ == '__main__':
    simulator = Simulator(
        {
            'RANDOM': Random(),
            'GREEDY': Greedy(),
            'CORNER': Corner(),
        },
        './simulator_setting.json',
    )
    simulator.start()
```
シミュレータは必ずメインモジュール(\_\_main\_\_)内で実行するようにしてください。<br>
シミュレータの引数には、"プレイヤー情報"と"シミュレータの設定ファイル"を指定してください。

#### シミュレータの設定ファイル
シミュレータの設定ファイル(JSON形式)の作成例は下記のとおりです。
Simulatorの第二引数に、本ファイル名(上記例では`./simulator_setting.json`ですが任意)を指定してください。

```JSON
{
    "board_size": 8,
    "board_type": "bitboard",
    "matches": 100,
    "processes": 1,
    "random_opening": 0,
    "player_names": [
        "RANDOM",
        "GREEDY",
        "CORNER"
    ]
}
```

 |パラメータ名|説明|
 |:---|:---|
 |board_size|盤面のサイズを指定してください。|
 |board_type|盤面の種類(board または bitboard)を選択してください。bitboardの方が高速で通常はこちらを使用してください。|
 |matches|AI同士の対戦回数を指定してください。100を指定した場合、AIの各組み合わせにつき先手と後手で100試合ずつ対戦する動作となります。|
 |processes|並列実行数を指定してください。AI同士の対戦組み合わせ別に並列実行します。お使いのPCのコア数に合わせて必要に応じて設定してください。|
 |random_opening|対戦開始から指定した手数までは、AI同士ランダムな手を打ち試合を進行します。指定された手数を超えるとAIはl本来の手を打ちます。対戦開始の状況をランダムに振ることで、AIの強さを測りやすくします。不要な場合は0を指定してください。|
 |player_names|対戦させたいAI名をリストアップして下さい。指定する場合は第一引数の"プレイヤー情報"に含まれるものの中から選択してください。省略すると第一引数の"プレイヤー情報"と同一と扱います。リストアップされた全てのAI同士の総当たり戦を行います。|

#### 実行結果
シミュレーション結果は下記で確認できます。
```Python
print(simulator)
```

#### 実行例
ライブラリ組み込みのAIを用いたプレイヤー"RANDOM"、"GREEDY"と、
自作のAIによる"CORNER"の、それぞれを対戦させるようシミュレータを実行して、
結果を出力するまでのコード例を下記に示します。

```Python
import random

from reversi import Simulator
from reversi.strategies import AbstractStrategy, Random, Greedy

class Corner(AbstractStrategy):
    def next_move(self, color, board):
        size = board.size
        legal_moves = board.get_legal_moves(color)
        for corner in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]:
            if corner in legal_moves:
                return corner

        return random.choice(legal_moves)

if __name__ == '__main__':
    simulator = Simulator(
        {
            'RANDOM': Random(),
            'GREEDY': Greedy(),
            'CORNER': Corner(),
        },
        './simulator_setting.json',
    )
    simulator.start()

    print(simulator)
```

"RANDOM"、"GREEDY"、"CORNER"を総当たりで、先手/後手それぞれ100回ずつ対戦したところ、下記の結果になりました。
```
Size : 8
                          | RANDOM                    GREEDY                    CORNER
---------------------------------------------------------------------------------------------------------
RANDOM                    | ------                     32.5%                     21.5%
GREEDY                    |  66.0%                    ------                     29.5%
CORNER                    |  76.0%                     68.5%                    ------
---------------------------------------------------------------------------------------------------------

                          | Total  | Win   Lose  Draw  Match
------------------------------------------------------------
RANDOM                    |  27.0% |   108   284     8   400
GREEDY                    |  47.8% |   191   202     7   400
CORNER                    |  72.2% |   289   102     9   400
------------------------------------------------------------
```

ランダムに打つよりも毎回多めに取る方が、さらにそれよりも角は必ず取る方が、より有利になりそうだという結果が得られました。

### boardオブジェクトの使い方
ここでは、リバーシの盤面を管理する`board`オブジェクトの使い方について説明します。

#### boardオブジェクトの生成
`board`オブジェクトは**reversi**より、`Board`クラスまたは`BitBoard`クラスを
インポートすることで、生成できるようになります。

`Board`クラスと`BitBoard`クラスの違いは、盤面を表現する内部データの構造のみで、使い方は同じです。
`BitBoard`クラスの方が処理速度がより高速なため、通常はこちらをご使用下さい。

`Board`クラスをインスタンス化する際の引数に、数値を入れることで盤面のサイズを指定できます。
サイズは4～26までの偶数としてください。省略時は8となります。
また、`size`プロパティにて盤面のサイズを確認することができます。

コーディング例は下記のとおりです。

```Python
from reversi import Board, BitBoard

board = Board()
print(board.size)

bitboard = BitBoard(10)
print(bitboard.size)
```

上記の実行結果は下記となります。
```
8
10
```

#### boardオブジェクトの標準出力
`board`オブジェクトを`print`すると盤面の状態が標準出力されます。

```Python
from reversi import BitBoard

board = BitBoard()
print(board)

board = BitBoard(4)
print(board)
```

上記の実行結果は下記となります。<br>
![board_print](https://raw.githubusercontent.com/y-tetsu/reversi/images/board_print.png)

#### boardオブジェクトのメソッド
`board`オブジェクトの使用可能なメソッドを紹介します。

##### get_legal_moves
黒番または白番での着手可能な位置を返します。
着手可能な位置は"XY座標のタプルのリスト"となります。
引数には`black`(黒番)または`white`(白番)の文字列(以後`color`と呼びます)を指定してください。

```Python
from reversi import BitBoard

board = BitBoard()
legal_moves = board.get_legal_moves('black')

print(legal_moves)
```

上記の実行結果は下記となります。
```
[(3, 2), (2, 3), (5, 4), (4, 5)]
```
この場合、下図の黄色のマスの位置が、着手可能な位置として返されます。<br>
![legal_moves](https://raw.githubusercontent.com/y-tetsu/reversi/images/legal_moves.png)

##### get_flippable_discs
指定位置に着手した場合の、ひっくり返せる石を返します。
ひっくり返せる石は"XY座標のタプルのリスト"となります。
第一引数に`color`、第二引数に石を置くX座標、第三引数にY座標を指定してください。

```Python
from reversi import BitBoard

board = BitBoard()
flippable_discs = board.get_flippable_discs('black', 5, 4)

print(flippable_discs)
```

上記の実行結果は下記となります。
```
[(4, 4)]
```
この場合、下図の黄色のマスの位置が、ひっくり返せる石の位置として返されます。<br>
![flippable_discs](https://raw.githubusercontent.com/y-tetsu/reversi/images/flippable_discs2.png)

##### get_board_info
盤面に置かれた石の状態を"2次元リスト"で返します。
"1"が黒、"-1"が白、"0"が空きを表します。引数はありません。

```Python
from pprint import pprint
from reversi import BitBoard

board = BitBoard()
board_info = board.get_board_info()

print(board)
pprint(board_info)
```

上記の実行結果は下記となります。<br>
![get_board_info](https://raw.githubusercontent.com/y-tetsu/reversi/images/get_board_info.png)

##### put_disc
指定位置に石を配置し、取れる石をひっくり返します。
第一引数に`color`、第二引数に石を置くX座標、第三引数にY座標を指定してください。

```Python
from reversi import BitBoard

board = BitBoard()
print(board)

board.put_disc('black', 5, 4)
print(board)
```

上記の実行結果は下記となります。<br>
![put_disc](https://raw.githubusercontent.com/y-tetsu/reversi/images/put_disc.png)

##### undo
`put_disc`メソッドで置いた石を元に戻します。引数はありません。
`put_disc`メソッドを呼び出した回数だけ、元に戻すことができます。
`put_disc`メソッドを呼び出した回数を超えて、本メソッドを呼び出さないでください。

```Python
from reversi import BitBoard

board = BitBoard()
board.put_disc('black', 5, 4)
print(board)

board.undo()
print(board)
```

上記の実行結果は下記となります。<br>
![undo](https://raw.githubusercontent.com/y-tetsu/reversi/images/undo.png)


---
## インストールがうまくいかない場合
**reversi**のインストールがうまくいかない場合は
下記の手順(1～5)に従って環境を準備して下さい。

### 1. Pythonのインストール
下記よりPythonの64bit版インストーラのexeをダウンロード後、インストールして下さい。<br>
[Python 3.7.6](https://www.python.org/downloads/release/python-376/)<br>

インストール後、コマンドプロンプトを立ち上げて下記の'$'以降を入力してEnterを押し、同じ結果が出ればOKです。
```
$ py -3.7 --version
Python 3.7.6
```

### 2. pipの更新
**reversi**をPythonから実行するためにはいくつかの外部パッケージが必要となります。<br>
正しくインストールできるようにするために下記を実行してpipをアップデートして下さい。<br>
```
$ py -3.7 -m pip install --upgrade pip
 :
Successfully installed pip-20.0.2
```
※バージョンが異なる場合は上位であれば問題ないはずです

### 3. 関連パッケージのインストール
**reversi**の実行に必要なPythonのパッケージのインストールは下記で一括して行えます。<br>
事前にコマンドプロンプトにてreversiフォルダ以下に移動しておいてください。<br>
```
$ py -3.7 -m pip install -r requirements.txt
```
もしうまくいかない場合は、以降の"(パッケージインストールの補足)"を個別に実行してください。

### 4. Visual C++のインストール
**reversi**の実行にはC言語のコンパイル環境が必要となります。<br>
下記よりVisual C++をダウンロードして下さい。<br>
[Microsoft Visual C++ 2019](https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc)<br>

### 5. 動作確認
[サンプル](https://github.com/y-tetsu/reversi/blob/master/README.md#サンプル)を参照して、サンプルが動作するか確認してください。

### (パッケージインストールの補足)
#### cythonパッケージのインストール
**reversi**を実行するためにはcythonという外部パッケージが必要となります。<br>
下記を実行してインストールして下さい。
```
$ py -3.7 -m pip install cython
 :
Successfully installed cython-0.29.15
```

#### pyinstallerパッケージのインストール
**reversi**のexeを生成するためにはpyinstallerという外部パッケージが必要となります。<br>
下記を実行してインストールして下さい。不要な場合は省略しても構いません。
```
$ py -3.7 -m pip install pyinstaller
 :
Successfully installed altgraph-0.17 future-0.18.2 pefile-2019.4.18 pyinstaller-3.6 pywin32-ctypes-0.2.0
```

うまくいかない場合は下記を実行後に、再度上記を試してみて下さい。
```
$ py -3.7 -m pip install wheel
```

インストール完了後、pyinstallerを実行できるようにするために環境変数に下記を追加して下さい。
```
C:\Users\{あなたのユーザ名}\AppData\Local\Programs\Python\Python37\Scripts
```


---
## Windows版アプリケーションについて
### ゲーム紹介
盤面のサイズや対戦プレイヤーをいろいろ選べるリバーシです。
難易度の異なる多種多様なAIがお相手いたします。<br>
おまけ要素として、お好きなプログラミング言語で作ったAIをゲームに追加して遊べる機能もございます。

### ダウンロード
下記リンクをクリックし、"reversi.zip"をダウンロードしてください。<br>
- [reversi.zip](https://github.com/y-tetsu/reversi/releases/download/0.0.18/reversi.zip)

"reversi.zip"を解凍後、reversi.exeをダブルクリックするとアプリケーションで遊ぶ事ができます。

### メニュー一覧
選択可能なメニューの一覧です。<br>

 |名前|内容|
 |:---|:---|
 |Size |盤面のサイズ(4～26までの偶数)を選択します。 |
 |Black |黒(先手)のプレイヤーを選択します。 |
 |White |白(後手)のプレイヤーを選択します。 |
 |Cputime |CPUの持ち時間を設定します。デフォルトは0.5秒となっております。 |
 |Extra |外部プログラムのAIを追加します。Cputimeの持ち時間の設定は適用されません。 |
 |Assist |打てる手の候補をハイライト表示するかどうか選びます。 |
 |Language |言語設定(English or 日本語)を選びます。 |
 |Cancel |ゲームを中断します。 |

### プレイヤー紹介
選択可能なプレイヤーの一覧です。<br>
難易度は8x8サイズの場合の目安となっております。<br>

 |名前|特徴|難易度|
 |:---|:---|:---:|
 |User1, User2 |人が操作します。 | ？ |
 |Unselfish |なるべく少なく取ろうとします。 | ★ |
 |Random |ランダムに手を選びます。 | ★ |
 |Greedy |なるべく多く取ろうとします。 | ★ |
 |SlowStarter |残り手数が15%未満の場合はUnselfish、15%以上の場合はGreedyになります。 | ★ |
 |Table |マス目の位置に重みをつけたテーブルで盤面を評価し、自身の形勢が良くなるよう手を選びます。なるべく少なく取り、角を狙い、角のそばは避けるよう心掛けます。 | ★★ |
 |MonteCarlo |モンテカルロ法で手を選びます。持ち時間の限り、すべての手の候補についてゲーム終了までランダムな手を打ちあうプレイアウトを繰り返し、最も勝率が高かった手を選びます。| ★★ |
 |MinMax |ミニマックス法で2手先を読んで手を選びます。Tableの盤面評価に加えて、着手可能数と勝敗を考慮します。自身の置ける場所は増やし、相手の置ける場所は減らし、勝ちが見えた手を優先するよう手を読みます。 | ★★ |
 |NegaMax |MinMaxの探索手法をネガマックス法に替えて、持ち時間の限り3手先を読んで手を選びます。手を読む探索効率はミニマックス法と同じです。 | ★★★ |
 |AlphaBeta |NegaMaxの探索手法をアルファベータ法(ネガアルファ法)に替えて、持ち時間の限り4手先を読んで手を選びます。αβ値の枝刈りにより、ネガマックス法より効率良く手を読みます。 | ★★★ |
 |Joseki |AlphaBetaに加えて、序盤は定石通りに手を選びます。| ★★★ |
 |FullReading |Josekiに加えて、終盤残り9手からは最終局面までの石差を読んで手を選びます。| ★★★ |
 |Iterative |FullReadingに反復深化法を適用して持ち時間の限り徐々に深く手を読みます。読む手の深さを増やす際は前回の深さで最も評価が高かった手を最初に調べます。それにより、不要な探索を枝刈りしやすくし、4手よりも深く手を読む場合があります。| ★★★★ |
 |Edge |Iterativeの盤面評価に加えて、4辺のパターンを考慮し確定石を増やすよう手を選びます。| ★★★★ |
 |Switch |Edgeの各パラメータを遺伝的アルゴリズムを使って強化し、手数に応じて5段階にパラメータを切り替えることで、よりゲームの進行に応じた手を選びます。また、探索手法をアルファベータ法からネガスカウト法に変更し、自身の着手可能数が相手より多くなる手を優先的に探索するよう候補を並び替え、探索効率を上げています。加えて終盤残り10手から石差を読みます。| ★★★★ |

### プレイヤー追加機能
#### 概要
本アプリケーションはお好きなプログラミング言語で作成したAI(追加プレイヤー)を<br>
ゲームに参加させて遊ぶことができます。<br>
また、あらかじめ用意された追加プレイヤーについても動作環境を準備する事で遊ぶ事ができます。<br>
なお、追加プレイヤーのプログラムを作成する際は入出力を後述のフォーマットに準拠させて下さい。<br>

#### 追加プレイヤー紹介
あらかじめ用意された追加プレイヤーの一覧です。<br>
動作環境を準備し、Extraメニューより登録ファイルを読み込ませると遊べるようになります。

 |名前|特徴|難易度|登録ファイル|開発言語|動作確認環境|
 |:---|:---|:---:|:---:|:---:|:---|
 |TopLeft |打てる手の中から一番上の左端を選びます。 | ★ | topleft.json | Python |Windows10 64bit<br>[Python 3.7.6](https://www.python.org/downloads/release/python-376/) |
 |BottomRight |打てる手の中から一番下の右端を選びます。 | ★ | bottomright.json | Perl |Windows10 64bit<br>[Strawberry Perl 5.30.1.1](http://strawberryperl.com/) |
 |RandomCorner |角が取れる時は必ず取ります。それ以外はランダムに手を選びます。 | ★ | randomcorner.json | VBScript |Windows10 64bit |

#### プレイヤー作成手順
プレイヤーを自作して遊ぶには、下記の手順でプレイヤーの作成と登録を行って下さい。

1. お好きなプログラミング言語の実行環境を準備する
2. [追加プレイヤー](#追加プレイヤーの実行)のプログラムを書く
3. [登録ファイル](#登録ファイル)を作成する
4. アプリケーションを起動する
5. Extraメニューより登録ファイルを読み込ませる

![extra](https://raw.githubusercontent.com/y-tetsu/reversi/images/extra_en_v0_0_15.gif)

##### 追加プレイヤーの実行
追加プレイヤーをアプリケーションに登録すると外部プログラムとして実行されるようになります。<br>
以下に処理の流れを示します。

![external](https://raw.githubusercontent.com/y-tetsu/reversi/images/external_ja.png)

1. ゲーム開始後、追加プレイヤーの手番になるとアプリケーションは対応するプログラムのコマンドを実行します。<br>その際、標準入力に盤面情報を渡し、追加プレイヤーのプログラムの応答を待ちます。

2. 追加プレイヤーは標準入力から盤面情報を受け取り、次の手を決め、その結果を標準出力します。<br>(そのようなプログラムを書いて下さい)

3. アプリケーションは追加プレイヤーの標準出力(次の手)を受け取るとゲームを再開します。<br>一定時間応答がない場合は追加プレイヤーのプログラムを強制終了し、反則負けとして扱います。

##### 標準入力フォーマット
追加プレイヤーが受け取る標準入力の盤面の情報です。
```
手番の色(黒:1、白:-1)
盤面のサイズ(4～26までの偶数)
盤面の石の2次元配置(空き:0、黒:1、白:-1をスペース区切り)
```

下記に白の手番、盤面サイズ8x8の例を示します。<br>
![stdin](https://raw.githubusercontent.com/y-tetsu/reversi/images/stdin.png)
```
-1
8
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0
0 0 0 -1 1 0 0 0
0 0 -1 -1 1 -1 0 0
0 0 0 0 1 -1 0 0
0 0 0 0 1 -1 0 0
0 0 0 0 0 0 0 0
```

##### 標準出力フォーマット
追加プレイヤーが標準出力する次の手の情報です。
```
盤面の座標(左上を起点(0,0)としてxとyをスペース区切り)
```

下記にc5へ打つ場合の例を示します。<br>
![stdout](https://raw.githubusercontent.com/y-tetsu/reversi/images/stdout.png)
```
2 4
```

##### 登録ファイル
追加プレイヤーをアプリケーションに登録するために本ファイルを作成する必要があります。<br>
登録ファイルは下記のフォーマット(JSON形式)に従って`extra/`以下に作成して下さい。<br>
作成後、Extraメニューより読み込む事でプレイヤーが追加されます。
```
{
    "name": "追加プレイヤーの名前",
    "cmd": "追加プレイヤー実行用のコマンド",
    "timeouttime": 追加プレイヤーからの応答待ち時間(秒) ※起動に時間がかかる場合があるため、余裕を持った設定を推奨します
}
```

下記に、Windows10上のPythonで動作するTopLeft(あらかじめ用意されたプレイヤー)の例を示します。
```
{
    "name": "TopLeft",
    "cmd": "py -3.7 ./extra/python/topleft/topleft.py",
    "timeouttime": 60
}
```


---
## 参考書籍
- 「実践Python3」 Mark Summerfield著 斎藤 康毅訳 株式会社オライリー・ジャパン [ISBN978-4-87311-739-3](https://www.oreilly.co.jp/books/9784873117393/)
- 「Java言語で学ぶデザインパターン入門」 結城 浩著 ソフトバンククリエイティブ株式会社 [ISBN4-7973-2703-0](https://www.hyuki.com/dp/)
- 「日経ソフトウェア2019年11月号」 日経BP [ISSN1347-4685](https://books.google.co.jp/books?id=qhCxDwAAQBAJ&pg=PA146&lpg=PA146&dq=ISSN1347-4685&source=bl&ots=_3Z0k4Y_WE&sig=ACfU3U1urxBdw_srrg62Kr5UJD1sXLEQbQ&hl=ja&sa=X&ved=2ahUKEwjlkqzArY_nAhVTc3AKHXlBA6YQ6AEwAHoECAkQAQ#v=onepage&q=ISSN1347-4685&f=false)
- 「Python計算機科学新教本」 David Kopec著 黒川 利明訳 株式会社オライリー・ジャパン [ISBN978-4-87311-881-9](https://www.oreilly.co.jp/books/9784873118819/)
- 「Cython Cとの融合によるPythonの高速化」 Krurt W. Smith著 中田 秀基監訳 長尾 高弘訳 株式会社オライリー・ジャパン [ISBN978-4-87311-727-0](https://www.oreilly.co.jp/books/9784873117270/)


## 参考サイト
- 「オセロ・リバーシプログラミング講座 ～勝ち方・考え方～」https://uguisu.skr.jp/othello/
- 「オセロ･リバーシの勝ち方、必勝法」https://bassy84.net/
- 「強いオセロプログラムの内部動作」http://www.amy.hi-ho.ne.jp/okuhara/howtoj.htm
- 「オセロAI入門」https://qiita.com/na-o-ys/items/10d894635c2a6c07ac70


## 脚注
<a id="note1">[1]</a>: 一部でCythonを使用しています。<sup>[↑](#return1)</sup>