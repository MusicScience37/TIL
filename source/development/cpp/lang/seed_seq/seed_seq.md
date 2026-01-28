---
file_format: mystnb
---

# C++ 標準ライブラリの seed_seq について

C++ 標準ライブラリに `std::seed_seq` というクラスがある。
これは、疑似乱数生成器の初期化時に複数の整数をシードとして与えるためのクラスであり、
以下のように使用できる。

```cpp
// シード列（実際には std::random_device などで生成する。
std::vector<std::uint32_t> seeds = {1, 2, 3};
// seed_seq オブジェクトを生成する。
std::seed_seq seed_seq(seeds.begin(), seeds.end());
// 疑似乱数生成器に std::seed_seq オブジェクトを与えて初期化する。
std::mt19937 random_engine(seed_seq);
```

このように複数のシードを与えることができるため、

- 複数のシードを与えることで乱数列の品質向上を狙う。
- 異なる方法で生成したシードを混ぜる。
  （例：時刻やハードウェアの温度をシードに混ぜるなど）

といった使い方ができる。

## seed_seq に与える整数の個数を変化させてみる実験

`std::seed_seq` に与える整数の個数を変化させ、
それぞれシードのうち 1 ビットだけを変化させたときに
初期段階の乱数列が何ビット変化するかを実験した。

生成する乱数は 32 ビット整数とした。
そのため、理想的な乱数においては乱数列の差分が 16 ビットになる。

実験結果を以下に示す。

```{code-cell}
:tags: [remove-input]

import pandas
import plotly.express

df = pandas.read_csv("test_num_seeds.csv")

figure = plotly.express.line(
    df,
    x="pos",
    y="avg_popcount",
    color="num_seeds",
    title="シードの変化に対する乱数列の変化",
    labels={
        "pos": "乱数列のインデックス",
        "avg_popcount": "乱数列の異なるビット数の平均",
        "num_seeds": "シードの個数",
    }
)

figure.show(renderer="notebook_connected")
```

シードの個数が 1 個でも最初からほぼ 16 になっており、十分異なる乱数が生成されている。

シードの個数による違いをこの実験では確認できなかった。

```{seealso}
- 2 ～ 8 個のシードを与えておくと良いという記事：
  [How to properly seed mt19937 random number generator | Simple C++](https://simplecxx.github.io/2018/11/03/seed-mt19937.html)
```
