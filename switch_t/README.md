# switch_t
## 目的
Tableパラメータ(corner, c, a1, a2, b, o, x)をより強くするパラメータ値を求める。
かつ、ゲームの進行に合わせた5段階分(1～13手, 14～25手, 26～37手, 38～49手, 50～60手)のパラメータ値を求める。

## 条件
ランダムなパラメータ値(±250の範囲)の個体から開始し、既存パラメータの個体と1手読み同士で対戦させ勝率の高いものを次の世代に入れ替える。

```JSON
{
    "max_generations": 1000,
    "population_num": 24,
    "offspring_num": 12,
    "mutation_chance": 0.1,
    "mutation_value": 6,
    "large_mutation": 100,
    "large_mutation_value": 25,
    "turns": [12, 24, 36, 48, 60],
    "board_size": 8,
    "matches": 250,
    "threshold": 85,
    "random_opening": 6,
    "processes": 2
}
```

## 結果
3回目の試行の1500世代あたりで79%程度の勝率となる個体が現れたが
複数手を読む戦略にパラメータを適用したところ弱くなったため中断。<br>

![switch_t](https://raw.githubusercontent.com/y-tetsu/reversi/images/switch_t.png)

```
世代数 : 1531
適応度 : 79.4%(vs既存パラメータの勝率)
corner : [-151,   63, -104, -188,  -56]
c      : [  64,  -20,  -47, -177,  189]
a1     : [ 130,  163,   76,  -31, -121]
a2     : [ 157,   17,  145,  190,  125]
b      : [   4,   55,   39,  129,  217]
o      : [ 101,  146,   25,   -1,  -34]
x      : [-182, -186, -238,  -97,  112]
```
