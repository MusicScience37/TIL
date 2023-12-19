# 集合の縦棒に適度にスペースを追加する

TeX の数式で集合の記述に `\left`, `\middle`, `\right` を使用する場合に、
集合の縦棒の左右に適度なスペースが入るように記述する方法をメモする。

例えば、

```{code-block} tex
S_i = \left\{ j \middle| \left|A_{ij}\right| \geq \sum_{j=1}^N \left|A_{ij}\right| \right\}
```

と入力すると、

$$
S_i = \left\{ j \middle| \left|A_{ij}\right| \geq \sum_{j=1}^N \left|A_{ij}\right| \right\}
$$

となる。
集合の中の縦棒の左右に空白がなく、少し違和感が残る。

そこで、
[\middle であり \mid であるもの - マクロツイーター](https://zrbabbler.hatenablog.com/entry/20120411/1334151482)
において以下のような書き方が提案されている。

```{code-block} tex
S_i = \left\{ j \mathrel{} \middle| \mathrel{} \left|A_{ij}\right| \geq \sum_{j=1}^N \left|A_{ij}\right| \right\}
```

これにより、以下のような表示が得られる。

$$
S_i = \left\{ j \mathrel{} \middle| \mathrel{} \left|A_{ij}\right| \geq \sum_{j=1}^N \left|A_{ij}\right| \right\}
$$

ここで、縦棒は以下により出力している。

```{code-block} tex
\mathrel{} \middle| \mathrel{}
```
