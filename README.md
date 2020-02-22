# reversi
Pythonで作るリバーシ

## ゲーム紹介
盤面のサイズや対戦プレイヤーをいろいろ選べるリバーシです。<br>
自分でプログラミングしたAIをゲームに追加して遊べる特長があります。<br>

![gui](https://github.com/y-tetsu/reversi/blob/master/image/reversi2.gif?raw=true)

### 実行方法
```
$ python reversi.py
```

Windows版は下記よりexe(ダブルクリックで起動)をダウンロード可能です。<br>
[ダウンロード](https://github.com/y-tetsu/reversi/releases)

### メニュー一覧
ゲームで選べるメニューの一覧です。<br>

 |名前|内容|
 |:---|:---|
 |Size |盤面のサイズ(4～26までの偶数)を選択します。 |
 |Black |黒(先手)のプレイヤーを選択します。 |
 |White |白(後手)のプレイヤーを選択します。 |
 |Cputime |CPUの持ち時間を設定します。デフォルトは0.5秒となっております。 |
 |Extra |外部プログラムのAIを追加します。Cputimeの持ち時間の設定は適用されません。 |
 |Assist |打てる手の候補をハイライト表示するかどうか選びます。 |
 |Cancel |ゲームを中断します。 |

## プレイヤー紹介
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
 |FullReading |AlphaBetaに加えて、終盤残り9手からは最終局面までの石差を読んで手を選びます。| ★★★ |
 |Joseki |FullReadingに加えて、序盤は定石通りに手を選びます。| ★★★ |
 |Iterative |Josekiに反復深化法を適用して持ち時間の限り徐々に深く手を読みます。読む手の深さを増やす際は前回の深さで最も評価が高かった手を最初に調べます。それにより、不要な探索を枝刈りしやすくし、4手よりも深く手を読む場合があります。| ★★★★ |
 |NegaScout |Iterativeの探索手法をネガスカウト法に替えて手を読みます。Null Window Searchを行うことで、不要な探索を枝刈りしやすくし、アルファベータ法よりも多く手を読む場合があります。| ★★★★ |
 |Switch |NegaScoutの盤面評価パラメータを序盤から終盤にかけて5段階に切り替えます。手が進むにつれて、角の重みを小さくし、着手可能数の重みを大きくしていきます。それにより、パラメータ固定よりもゲームの進行状況に合った手を選ぶ場合があります。| ★★★★ |

## プレイヤー追加機能
### 概要
本プログラム(**reversi**)はお好きなプログラミング言語で作成したAI(追加プレイヤー)を<br>
ゲームに参加させて遊ぶことができます。<br>
また、あらかじめ用意された追加プレイヤーについても動作環境を準備する事で遊ぶ事ができます。<br>
なお、追加プレイヤーのプログラムを作成する際は入出力を後述のフォーマットに準拠させて下さい。<br>

### 追加プレイヤー紹介
あらかじめ用意された追加プレイヤーの一覧です。<br>
動作環境を準備し、Extraメニューより登録ファイルを読み込ませると遊べるようになります。

 |名前|特徴|難易度|登録ファイル|開発言語|動作確認環境|
 |:---|:---|:---:|:---:|:---:|:---|
 |TopLeft |打てる手の中から一番上の左端を選びます。 | ★ | topleft.json | Python |[Python 3.7.0](https://www.python.org/downloads/) |
 |BottomRight |打てる手の中から一番下の右端を選びます。 | ★ | bottomright.json | Perl |[Strawberry Perl 5.30.1.1](http://strawberryperl.com/) |
 |RandomCorner |角が取れる時は必ず取ります。それ以外はランダムに手を選びます。 | ★ | randomcorner.json | VBScript |Windows10 64bit |

### プレイヤー作成手順
プレイヤーを自作して遊ぶには、下記の手順でプレイヤーの作成と登録を行って下さい。

1. お好きなプログラミング言語の実行環境を準備する
2. [追加プレイヤー](#追加プレイヤーの実行)のプログラムを書く
3. [登録ファイル](#登録ファイル)を作成する
4. **reversi**を起動する
5. Extraメニューより登録ファイルを読み込ませる

![gui](https://github.com/y-tetsu/reversi/blob/master/image/extra.gif?raw=true)

#### 追加プレイヤーの実行
追加プレイヤーを**reversi**に登録すると外部プログラムとして実行されるようになります。<br>
以下に処理の流れを示します。

![external](https://github.com/y-tetsu/reversi/blob/master/image/external.png?raw=true)

1. ゲーム開始後、追加プレイヤーの手番になると**reversi**は対応するプログラムのコマンドを実行します。<br>その際、標準入力に盤面情報を渡し、追加プレイヤーのプログラムの応答を待ちます。

2. 追加プレイヤーは標準入力から盤面情報を受け取り、次の手を決め、その結果を標準出力します。<br>(そのようなプログラムを書いて下さい)

3. **reversi**は追加プレイヤーの標準出力(次の手)を受け取るとゲームを再開します。<br>一定時間応答がない場合は追加プレイヤーのプログラムを強制終了し、反則負けとして扱います。

#### 標準入力フォーマット
追加プレイヤーが受け取る標準入力の盤面の情報です。
```
手番の色(黒:1、白:-1)
盤面のサイズ(4～26までの偶数)
盤面の石の2次元配置(空き:0、黒:1、白:-1をスペース区切り)
```

下記に白の手番、盤面サイズ8x8の例を示します。<br>
![stdin](https://github.com/y-tetsu/reversi/blob/master/image/stdin2.png?raw=true)
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

#### 標準出力フォーマット
追加プレイヤーが標準出力する次の手の情報です。
```
盤面の座標(左上を起点(0,0)としてxとyをスペース区切り)
```

下記にc5へ打つ場合の例を示します。<br>
![stdout](https://github.com/y-tetsu/reversi/blob/master/image/stdout2.png?raw=true)
```
2 4
```

#### 登録ファイル
追加プレイヤーを**reversi**に登録するために本ファイルを作成する必要があります。<br>
登録ファイルは下記のフォーマット(JSON形式)に従って`strategies/extra/`以下に作成して下さい。<br>
作成後、Extraメニューより読み込む事でプレイヤーが追加されます。
```
{
    "name": "追加プレイヤーの名前",
    "cmd": "追加プレイヤー実行用のコマンド",
    "timeouttime": 追加プレイヤーからの応答待ち時間(秒) ※起動に時間がかかる場合があるため、余裕を持った設定を推奨します
}
```

下記に、pythonで動作するTopLeft(あらかじめ用意されたプレイヤー)の例を示します。
```
{
    "name": "TopLeft",
    "cmd": "python ./strategies/extra/python/topleft/topleft.py",
    "timeouttime": 60
}
```

## その他
### コンソール版
コマンドプロンプトなどコンソール上で遊べるタイプです。<br>

![console](https://github.com/y-tetsu/reversi/blob/master/image/console2.gif?raw=true)

#### 実行方法
```
$ python reversic.py
```

---
## 動作確認環境
- Windows10 64bit<br>
- ディスプレイサイズ 1366x768 以上
- プロセッサ 1.6GHz 以上
- メモリ 4.00GB 以上
- [Python 3.7.6](https://www.python.org/downloads/release/python-376/)<br>
    - cython 0.29.15<br>
    - numpy 1.18.1<br>
    - pyinstaller 3.6<br>
- [Microsoft Visual C++ 2019](https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc)<br>

## Windows10の環境構築方法
Pythonから直接本プログラムを実行する場合は下記の手順に従って環境を準備して下さい。

### Pythonのインストール
下記より64bit版インストーラのexeをダウンロード後、インストールして下さい。<br>
[インストーラ](https://www.python.org/downloads/release/python-376/)<br>

インストール後、コマンドプロンプトを立ち上げて下記の'$'以降を入力してEnterを押し、同じ結果が出ればOKです。
```
$ py -3.7 --version
Python 3.7.6
```

### pipの更新
下記を実行してpipをアップデートして下さい。※バージョンが異なる場合は上位であれば問題ないはずです
```
$ py -3.7 -m pip install --upgrade pip
 :
Successfully installed pip-20.0.2
```

### cythonパッケージのインストール
本プログラムをPythonから実行するためにはcythonという外部パッケージが必要となります。<br>下記を実行してインストールして下さい。※バージョンが異なる場合は上位であれば問題ないはずです
```
$ py -3.7 -m pip install cython
 :
Successfully installed cython-0.29.15
```

### numpyパッケージのインストール
本プログラムをPythonから実行するためにはnumpyという外部パッケージが必要となります。<br>下記を実行してインストールして下さい。※バージョンが異なる場合は上位であれば問題ないはずです
```
$ py -3.7 -m pip install numpy
 :
Successfully installed numpy-1.18.1
```

### pyinstallerパッケージのインストール
本プログラムのexeを生成するためにはpyinstallerという外部パッケージが必要となります。<br>下記を実行してインストールして下さい。※バージョンが異なる場合は上位であれば問題ないはずです
```
$ py -3.7 -m pip install pyinstaller
 :
Successfully installed altgraph-0.17 future-0.18.2 pefile-2019.4.18 pyinstaller-3.6 pywin32-ctypes-0.2.0
```

うまくいかない場合は下記を実行後に再度上記を試してみて下さい。
```
$ py -3.7 -m pip install wheel
```

環境変数には下記を追加しておいてください。
```
C:\Users\{あなたのユーザ名}\AppData\Local\Programs\Python\Python37\Scripts
```

### Visual C++のインストール
本プログラムの実行にはC言語のコンパイル環境が必要となります。<br>下記よりVisual C++をダウンロードして下さい。<br>
[Microsoft Visual C++ 2019](https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc)<br>

### reversiの実行
上記までの環境を構築後、コマンドプロンプトにてsrcフォルダ以下に移動し下記を実行すると本プログラムが起動します。
```
$ python reversi.py
```

## 参考書籍
- 「実践Python3」Mark Summerfield著 斎藤 康毅訳 株式会社オライリー・ジャパン [ISBN978-4-87311-739-3](https://www.oreilly.co.jp/books/9784873117393/)
- 「Java言語で学ぶデザインパターン入門」結城 浩著 ソフトバンククリエイティブ株式会社 [ISBN4-7973-2703-0](https://www.hyuki.com/dp/)
- 「日経ソフトウェア2019年11月号」 日経BP [ISSN1347-4685](https://books.google.co.jp/books?id=qhCxDwAAQBAJ&pg=PA146&lpg=PA146&dq=ISSN1347-4685&source=bl&ots=_3Z0k4Y_WE&sig=ACfU3U1urxBdw_srrg62Kr5UJD1sXLEQbQ&hl=ja&sa=X&ved=2ahUKEwjlkqzArY_nAhVTc3AKHXlBA6YQ6AEwAHoECAkQAQ#v=onepage&q=ISSN1347-4685&f=false)

## 参考サイト
- 「オセロ・リバーシプログラミング講座 ～勝ち方・考え方～」https://uguisu.skr.jp/othello/
- 「オセロ･リバーシの勝ち方、必勝法」https://bassy84.net/
- 「強いオセロプログラムの内部動作」http://www.amy.hi-ho.ne.jp/okuhara/howtoj.htm
- 「オセロAI入門」https://qiita.com/na-o-ys/items/10d894635c2a6c07ac70
