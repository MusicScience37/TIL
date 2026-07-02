# 有限要素法ソフトウェア FreeFEM

[FreeFEM](https://freefem.org/) は有限要素法を用いた偏微分方程式の解法を実装するためのソフトウェア。
ライセンスは LGPL であり、[GitHub のリポジトリ](https://github.com/FreeFem/FreeFem-sources) でソースコードが公開されている。

FreeFEM は C++ に近い言語でソースコードを作成し、それを FreeFEM のコマンドで実行することで動作する。

FreeFEM は有限要素法の知識を前提としており、
ソースコード上では解きたい偏微分方程式の弱形式と境界条件を記載するほか、
メッシュの定義や有限要素空間の定義が必要となる。
このページでも FreeFEM の簡単な紹介を目的とするため、有限要素法の知識を前提とする。
有限要素法については {footcite:p}`Tabata1994` や {footcite:p}`Knabner2003` などを参照。

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

### Windows

```powershell
winget install FreeFem
```

```{note}
Windows 11 で上記のコマンドでインストールができた。
FreeFEM のバージョンは 4.15 だった。
```

## 例

今回作成して実行してみたソースコードの例の一部を以下に示す。
FreeFEM の使用方法の詳細については [FreeFEM の公式ドキュメント](https://doc.freefem.org) を参照。

### 簡単な Poisson 方程式の例

簡単な Poisson 方程式

$$
-\nabla^2 u = f
$$

の数値解を求める例を示す。
使用する弱形式は

$$
\int_\Omega \nabla u \cdot \nabla v \, d\Omega = \int_\Omega f v \, d\Omega
$$

である。

上記の弱形式をもとに、以下のように FreeFEM で実行するソースコードを作成する。
拡張子は `.edp` とすることが推奨されている。

```{code-block} freefem
:caption: poisson.edp

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
    // メッシュを square で作成した場合、境界は下が 1、右が 2、上が 3、左が 4 となる。
    + on(1, 2, 3, 4, u = 0);

// 結果の画面出力
plot(u);
```

```{note}
FreeFEM のソースコードは Sphinx （正確にはその内部で使用される pygments）が `freefem` という言語の指定で対応している。
```

上記のソースコードを `poisson.edp` という名前で保存し、以下のコマンドで実行すると、Poisson 方程式の数値解が計算され、結果が画面に表示される。

```bash
FreeFem++ poisson.edp
```

上記は Ubuntu と Windows の両方で動作することを確認している。

### 移流拡散方程式の例

2 次元の移流拡散方程式

$$
\frac{\partial u}{\partial t} + \mathbf{c} \cdot \nabla u = D \nabla^2 u
$$

については、移流項と拡散項を分離して処理する。
移流項と拡散項のそれぞれについて時間発展の更新式を作成し、2 個の更新を順番に適用することで、
1 時間ステップの更新を行う。
このような異なる種類の項を分けて処理する手法は「operator splitting」と呼ばれる {footcite:p}`Press2007`。

移流項に関する方程式（移流方程式）

$$
\frac{\partial u}{\partial t} + \mathbf{c} \cdot \nabla u = 0
$$

は特性曲線法で安定して解くことができる。
特性曲線法については、
[FreeFEM の公式ドキュメントにおける Pure Convection の例](https://doc.freefem.org/tutorials/rotatingHill.html)
や {footcite:p}`Knabner2003` を参照。
特性曲線法は FreeFEM において

```freefem
SolPrev = Sol;
Sol = convect([VelocityX, VelocityY], -TimeStepSize, SolPrev);
```

のように実現できる。

拡散項に関する方程式（拡散方程式）

$$
\frac{\partial u}{\partial t} = D \nabla^2 u
$$

については弱形式

$$
\int_\Omega \frac{\partial u}{\partial t} v \, d\Omega
+ \int_\Omega D \nabla u \cdot \nabla v \, d\Omega = 0
$$

を用いる。

拡散方程式の時間微分を陰的 Euler 法で離散化し、
移流方程式の解 $u_\text{adv}$ に拡散方程式の更新を適用するようにすると、
以下のような更新式になる。

$$
\int_\Omega \frac{u_{\text{next}} - u_{\text{adv}}}{\Delta t} v \, d\Omega
+ \int_\Omega D \nabla u_{\text{next}} \cdot \nabla v \, d\Omega = 0
$$

これを実装すると以下のようになる。

```{code-block} freefem
:caption: advection_diffusion2d.edp

// 方程式と解法の定数
real AdvectionVelocity = 0.5;
real DiffusionCoeff = 0.01;
real TimeStepSize = 0.01;
int NumSteps = 100;
int NumStepsPerPlot = 10;

// メッシュと有限要素空間
mesh Mesh = square(30, 30);
fespace FESpace(Mesh, P2);
FESpace Sol, SolPrev, Test;

// 初期条件
real CenterX = 0.2;
real CenterY = 0.5;
real Radius2 = 0.1^2;
func real SmoothBump(real xx, real yy) {
    real r2 = (xx - CenterX)^2 + (yy - CenterY)^2;
    if (r2 >= Radius2) return 0.0;
    real s = r2 / Radius2; // 0 <= s < 1
    return exp(1.0 - 1.0 / (1.0 - s));
}
Sol = SmoothBump(x, y);

// 弱形式の定義
problem AdvectionDiffusionProblem(Sol, Test) =
    int2d(Mesh)(Sol * Test / TimeStepSize)
    - int2d(Mesh)(convect([AdvectionVelocity, 0], -TimeStepSize, SolPrev) * Test / TimeStepSize)
    + int2d(Mesh)(DiffusionCoeff * (dx(Sol) * dx(Test) + dy(Sol) * dy(Test)))
    + on(1, 2, 3, 4, Sol = 0);

// プロットの設定
macro PlotSol(Step) plot(Sol, cmm = "Step: " + Step, value=true, wait=true); //
PlotSol(0);

// 解法の実行
for (int step = 1; step <= NumSteps; ++step) {
    SolPrev = Sol;
    AdvectionDiffusionProblem;

    if (step % NumStepsPerPlot == 0) {
        PlotSol(step);
    }
}
```

```{attention}
FreeFEM では変数名に `_` が使用できない。
上記のソースコードでは、その制約を回避するために PascalCase を使用している。
```

```{attention}
FreeFEM におけるマクロ（`macro` の記述）は定義の最後に `//` を付ける必要があることに注意。
知らない状態で見るとコメントの内容の書き忘れに見えるが、これで正しい。
```

上記のソースコードを実行すると、時間刻み 0.01 で時間発展をしながら、
10 回に 1 回（時間 0.1 ごと）に解を画面に出力する。
画面を選択した状態で Enter キーを押下することで次のステップの解が表示される。

## 感想

弱形式が用意できれば、それを実装して動かすのは簡単にできた。
ただし、公式ドキュメントは一部関数の仕様や言語仕様について説明が不十分な箇所があるため注意が必要。

```{footbibliography}

```
