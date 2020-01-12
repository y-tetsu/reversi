# othello
Pythonで作るオセロゲーム

## GUI版
```
$ python othello.py
```
![gui](https://github.com/y-tetsu/othello/blob/master/image/gui.gif?raw=true)

## コンソール版
```
$ python othelloc.py
```
![console](https://github.com/y-tetsu/othello/blob/master/image/console.gif?raw=true)

## 対戦相手紹介
選択できる対戦相手の一覧。難易度は8x8サイズの場合の目安。

 | キャラクター | 説明 | 難易度 |
 |:---|:---|:---:|
 |User1, User2 |人が操作。 | ？ |
 |Unselfish |なるべく少なく取ろうとする。 | ★ |
 |Random |ランダムに手を選ぶ。 | ★ |
 |Greedy |なるべく多く取ろうとする。 | ★ |

## 動作確認環境
Windows10<br>
Python 3.7.0<br>
numpy 1.15.1<br>
pyinstaller 3.4<br>
cython 0.28.5<br>
Microsoft Visual C++ 2019<br>

## 参考書籍
- 「実践Python3」Mark Summerfield著 斎藤 康毅訳 株式会社オライリー・ジャパン ISBN978-4-87311-739-3
- 「Java言語で学ぶデザインパターン入門」結城 浩著 ソフトバンククリエイティブ株式会社 ISBN4-7973-2703-0
- 「日経ソフトウェア2019年11月号」 日経BP ISSN1347-4685

## 参考サイト
- 「オセロ･リバーシの勝ち方、必勝法」https://bassy84.net/
- 「オセロAI入門」https://qiita.com/na-o-ys/items/10d894635c2a6c07ac70
