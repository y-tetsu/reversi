# reversi
Pythonで作るリバーシ

## ゲーム紹介
![gui](https://github.com/y-tetsu/reversi/blob/master/image/reversi.gif?raw=true)

### 実行方法
```
$ python reversi.py
```

上記の他、Windows版は下記よりexe(ダブルクリックで起動)をダウンロード可能です。<br>
[ダウンロード](https://github.com/y-tetsu/reversi/releases)

### メニュー一覧
 |名前|内容|
 |:---|:---|
 |Size |盤面のサイズ(4～26までの偶数)を選択できます。 |
 |Black |黒(先手)のプレイヤーを選択できます。 |
 |White |白(後手)のプレイヤーを選択できます。 |
 |Cputime |CPUの持ち時間を設定できます。デフォルトは0.5秒となっております。 |
 |Extra |外部プログラムのプレイヤーを追加できます。Cputimeの持ち時間の設定は適用されません。 |
 |Assist |打てる手の候補をハイライト表示するかどうか選べます。 |
 |Cancel |ゲームを中断できます。 |

## プレイヤー紹介
選択可能なプレイヤーの一覧です。<br>
難易度は8x8サイズの場合の目安となっております。<br>

 |名前|特徴|難易度|
 |:---|:---|:---:|
 |User1, User2 |人が操作します。 | ？ |
 |Unselfish |なるべく少なく取ろうとします。 | ★ |
 |Random |ランダムに手を選びます。 | ★ |
 |Greedy |なるべく多く取ろうとします。 | ★ |
 |SlowStarter |残り手数が15%未満の場合はUnselfish、<br>15%以上の場合はGreedyになります。 | ★ |
 |Table |マス目の位置に重みをつけた評価テーブルで盤面の形勢を判断し手を選びます。<br>なるべく少なく取り、角を狙い、角のそばは避けるよう心掛けます。 | ★★ |
 |MinMax |ミニマックス法で2手先を読んで手を選びます。<br>Tableの盤面評価に加えて、配置可能数と勝敗も考慮に入れます。 | ★★ |
 |MonteCarlo |モンテカルロ法で手を選びます。持ち時間の限りプレイアウトを繰り返し、最も勝率の高い手を選びます。| ★★ |
 |NegaMax |ネガマックス法で持ち時間の限り3手先を読んで手を選びます。| ★★★ |
 |AlphaBeta |アルファベータ法(ネガアルファ法)で持ち時間の限り4手先を読んで手を選びます。| ★★★ |
 |FullReading |AlphaBetaに加えて、終盤残り9手からは最終局面の石差を読んで手を選びます。| ★★★ |
 |Joseki |FullReadingに加えて、序盤は定石通りに手を選びます。| ★★★ |
 |Iterative |Josekiに反復深化法を適用して持ち時間の限り徐々に深く手を読みます。<br>読む手の深さを増やす際は前回の深さで最も評価が高かった手を最初に調べます。<br>それにより不要な探索をカットし、より深く手を読む場合があります。| ★★★★ |
 |NegaScout |Iterativeの探索手法にネガスカウト法を用いて手を読みます。<br>Null Window Searchを行うことで不要な探索をカットし局面によってはアルファベータ法より深く手を読む場合があります。| ★★★★ |

## プレイヤー追加機能
### 概要
本プログラム(**reversi**)はお好きなプログラミング言語で作成したAI(追加プレイヤー)を<br>ゲームに参加させて遊ぶことができます。<br>
ただし、自作した追加プレイヤーのプログラムの入出力は所定のフォーマット(後述)に準拠する必要があります。<br>
また動作環境を準備する事で、通常のプレイヤーに加えてあらかじめ用意された追加プレイヤーで遊ぶ事もできます。

### 追加プレイヤー紹介
動作環境を準備する事で対戦可能になる、あらかじめ用意された追加プレイヤーの一覧です。<br>
Extraメニューより登録ファイルを読み込ませると遊べるようになります。

 |名前|特徴|難易度|登録ファイル|開発言語|動作環境|
 |:---|:---|:---:|:---:|:---:|:---|
 |TopLeft |打てる手の中から一番上の左端を選びます。 | ★ | topleft.json | Python |Python 3.7.0 |

### プレイヤー作成手順
プレイヤーを自作して遊ぶには、下記の手順でプレイヤーの作成と登録を行って下さい。

1. お好きなプログラミング言語の実行環境を準備する
2. [追加プレイヤー](#追加プレイヤーの実行)のプログラムを書く
3. [登録ファイル](#登録ファイル)を作成する
4. **reversi**を起動する
5. Extraメニューより登録ファイルを読み込ませる

![gui](https://github.com/y-tetsu/reversi/blob/master/image/extra.gif?raw=true)

### 追加プレイヤーの実行
追加プレイヤーを**reversi**に登録すると外部プログラムとして実行されるようになります。<br>
以下に処理の流れを示します。

1. ゲーム開始後、追加プレイヤーの手番になると**reversi**は対応するプログラムの実行コマンドを叩きます。<br>その際、標準入力に盤面の情報を渡しプログラムからの応答を待ちます。
2. 追加プレイヤーは標準入力から盤面の情報を受け取り、次の手を決め、その結果を標準出力します。<br>(そのようなプログラムを書いてください)
3. **reversi**は追加プレイヤーからの標準出力(打つ手)を受け取るとゲームを再開します。<br>一定時間応答がない場合は追加プレイヤーのプログラムを強制終了し、反則負けとして扱います。

#### 標準入力フォーマット
追加プレイヤーが受け取る標準入力の情報です。
```
手番の色(黒:1、白:-1)
盤面のサイズ(4～26までの偶数)
盤面の石の2次元配置(空き:0、黒:1、白:-1をスペース区切り)
```

下記に白の手番、盤面サイズ8x8の例を示します。
![stdin](https://github.com/y-tetsu/reversi/blob/master/image/stdin.png?raw=true)
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
追加プレイヤーが標準出力する実行結果の情報です。
```
盤面の座標(左上を起点(0,0)としてxとyをスペース区切り)
![stdout](https://github.com/y-tetsu/reversi/blob/master/image/stdout.png?raw=true)
```

下記にc5へ打つ場合の例を示します。
```
2 4
```

### 登録ファイル
追加プレイヤーを**reversi**に登録するために本ファイルを作成する必要があります。<br>
登録ファイルは下記のフォーマット(JSON形式)に従って`stratgies/extra/`以下に作成してください。
```
{
    "name": "追加プレイヤーの名前",
    "cmd": "追加プレイヤーの実行コマンド",
    "timeouttime": 追加プレイヤーからの応答待ち時間(秒) ※起動に時間がかかる場合があるため、余裕を持った設定を推奨します
}
```

下記に、pythonで作ったTopLeftの例を示します。
```
{
    "name": "TopLeft",
    "cmd": "python ./strategies/extra/python/topleft/topleft.py",
    "timeouttime": 60
}
```

## その他
### コンソール版
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
- Python 3.7.0<br>
    - numpy 1.15.1<br>
    - cython 0.28.5<br>
    - pyinstaller 3.4<br>
- Microsoft Visual C++ 2019<br>

## 参考書籍
- 「実践Python3」Mark Summerfield著 斎藤 康毅訳 株式会社オライリー・ジャパン [ISBN978-4-87311-739-3](https://www.oreilly.co.jp/books/9784873117393/)
- 「Java言語で学ぶデザインパターン入門」結城 浩著 ソフトバンククリエイティブ株式会社 [ISBN4-7973-2703-0](https://www.hyuki.com/dp/)
- 「日経ソフトウェア2019年11月号」 日経BP [ISSN1347-4685](https://books.google.co.jp/books?id=qhCxDwAAQBAJ&pg=PA146&lpg=PA146&dq=ISSN1347-4685&source=bl&ots=_3Z0k4Y_WE&sig=ACfU3U1urxBdw_srrg62Kr5UJD1sXLEQbQ&hl=ja&sa=X&ved=2ahUKEwjlkqzArY_nAhVTc3AKHXlBA6YQ6AEwAHoECAkQAQ#v=onepage&q=ISSN1347-4685&f=false)

## 参考サイト
- 「オセロ・リバーシプログラミング講座 ～勝ち方・考え方～」https://uguisu.skr.jp/othello/
- 「オセロ･リバーシの勝ち方、必勝法」https://bassy84.net/
- 「強いオセロプログラムの内部動作」http://www.amy.hi-ho.ne.jp/okuhara/howtoj.htm
- 「オセロAI入門」https://qiita.com/na-o-ys/items/10d894635c2a6c07ac70
