# 有限要素法ソフトウェア FreeFEM

[FreeFEM](https://freefem.org/) は有限要素法を用いた偏微分方程式の解法を実装するためのソフトウェア。
ライセンスは LGPL であり、[GitHub のリポジトリ](https://github.com/FreeFem/FreeFem-sources) でソースコードが公開されている。

FreeFEM は C++ に近い言語でソースコードを作成し、それを FreeFEM のコマンドで実行することで動作する。

## インストール

### Ubuntu

以下のように apt コマンドでインストールできる。

```bash
sudo apt install freefem++
```

```{note}
今回は Windows11 の WSL2 上にインストールした Ubuntu 24.04 でインストールし、GUI も含めて動作することを確認した。
FreeFEM のバージョンは 4.13 だった。
```

```{note}
試していないが、Windows にも対応している。
```

## 簡単な Poisson 方程式の例

簡単な Poisson 方程式の数値解を求める例を示す。

まず、以下のように FreeFEM で実行するソースコードを作成する。
拡張子は `.edp` とすることが推奨されている。

```freefem
// メッシュの定義（正方形領域）
mesh Th = square(10, 10);

// 有限要素空間の定義
fespace Vh(Th, P1);

// 解とテスト関数の定義
Vh u, v;

// ソース項の値の定義
real f = 1.0;

// 弱形式の定義と解の計算
solve Poisson(u, v) =
    // Laplacian に対応する項
    int2d(Th)(dx(u) * dx(v) + dy(u) * dy(v))
    // ソース項
    - int2d(Th)(f * v)
    // 境界条件（Dirichlet 条件）
    + on(1, 2, 3, 4, u = 0);

// 結果の画面出力
plot(u);
```

```{note}
FreeFEM のソースコードは pygments が `freefem` という指定で対応している。
```

上記のソースコードを `poisson.edp` という名前で保存し、以下のコマンドで実行すると、Poisson 方程式の数値解が計算され、結果が画面に表示される。

```bash
FreeFem++ poisson.edp
```

```{note}
上記は Ubuntu での実行例である。
```
