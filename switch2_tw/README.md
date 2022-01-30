# switch2_tw
## 目的
Tableパラメータ(corner, c, a1, a2, b, o, x)+勝敗パラメータ(ww)をより強くするパラメータ値を求める。
かつ、ゲームの進行に合わせた5段階分のパラメータ値を求める。

## 条件
ランダムなパラメータ値の個体(wwは100000固定、それ以外は±250の範囲))から開始し、既存パラメータの個体と2手読み同士で対戦させ勝率の高いものを次の世代に入れ替える。

```JSON
{
    "max_generations": 200,
    "population_num": 24,
    "offspring_num": 12,
    "mutation_chance": 0.1,
    "mutation_value": 6,
    "large_mutation": 100,
    "large_mutation_value": 25,
    "turns": [12, 24, 36, 48, 60],
    "board_size": 8,
    "matches": 100,
    "threshold": 85,
    "random_opening": 8,
    "processes": 2
}
```

## 結果
200世代ほど繰り返すも勝率が20%からあがる気配がなく中断。<br>

![switch2_tw](https://raw.githubusercontent.com/y-tetsu/reversi/images/switch2_tw.png)

```
世代数 : 186
適応度 : 26.0%(vs既存パラメータの勝率)
corner : [   -42,     -9,    111,   -17,   218]
c      : [    -2,    -51,     57,    25,   139]
a1     : [  -141,     -3,   -134,  -144,  -166]
a2     : [   188,     46,   -123,   236,  -192]
b      : [   197,    -14,    -60,  -176,   -29]
o      : [  -202,   -136,   -207,   -23,    18]
x      : [    68,    -69,    -35,   190,  -175]
ww     : [100000, 100000, 100002, 99999, 99997]
```
