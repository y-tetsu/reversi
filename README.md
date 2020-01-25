# reversi
Pythonで作るリバーシ

## ゲーム紹介
### GUI版
![gui](https://github.com/y-tetsu/reversi/blob/master/image/gui4.gif?raw=true)
#### 実行方法
```
$ python reversi.py
```

上記の他、Windows版は下記よりexeをダウンロード可能です。<br>
[ダウンロード](https://github.com/y-tetsu/reversi/releases)
Assetsをクリックして開き、reversi.exeをクリックしてダウンロード可能です。<br>
ダブルクリックで起動できます。

### コンソール版
![gui](https://github.com/y-tetsu/reversi/blob/master/image/console2.gif?raw=true)
#### 実行方法
```
$ python reversic.py
```

## 対戦相手紹介
選択可能な対戦相手(CPUの戦略)の一覧です。<br>
難易度は8x8サイズの場合の目安となっております。<br>
CPUの持ち時間は大体0.5秒までとしています。

 |対戦相手|特徴|難易度|
 |:---|:---|:---:|
 |User1, User2 |人が操作します。 | ？ |
 |Unselfish |なるべく少なく取ろうとします。 | ★ |
 |Random |ランダムに手を選びます。 | ★ |
 |Greedy |なるべく多く取ろうとします。 | ★ |
 |SlowStarter |残り手数が15%未満の場合はUnselfish戦略、<br>15%以上の場合はGreedy戦略を取ります。 | ★ |
 |Table |独自の評価テーブルにより盤面の形勢を判断して手を選びます。<br>なるべく少なく取り、角を狙い、角のそばは避けるよう心掛けます。 | ★★ |
 |MinMax |ミニマックス法で2手先を読んで手を選びます。<br>Table戦略に加えて、配置可能数と勝敗を考慮に入れます。 | ★★ |
 |MonteCarlo |モンテカルロ法で手を選びます。持ち時間の限りプレイアウトを繰り返します。| ★★ |
 |NegaMax |ネガマックス法で3手先を読んで手を選びます。| ★★★ |
 |AlphaBeta |アルファベータ法(ネガアルファ法)で時間の限り4手先を読もうと心掛けます。| ★★★ |
 |FullReading |AlphaBeta戦略に加えて、終盤残り9手からは最終局面の石差を読んで手を選びます。| ★★★ |
 |Joseki |FullReading戦略に加えて、序盤は定石通りに手を選びます。| ★★★ |
 |Iterative |Joseki戦略に反復深化法を適用して持ち時間の限り徐々に深く手を読みます。<br>読む手の深さを増やす際は前回の深さで最も評価が高かった手を最初に調べます。<br>それにより不要な探索をカットし局面によっては4手より深く読む場合があります。| ★★★★ |
 |NegaScout |Iterative戦略の探索手法にネガスカウト法を用いて手を読みます。<br>局面によってはアルファベータ法より深く手を読む場合があります。| ★★★★ |

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
