# Eigen においてメモリ確保を防ぐ

Eigen において反復法を実装するにあたって、反復ごとにメモリを確保していると性能がかなり悪くなる。
そこで、メモリ確保を防ぐ方法を調査した。

## メモリ確保しているかどうかを調査する

まず、実装した処理がメモリ確保をしているかどうかを調査する。
これには `EIGEN_RUNTIME_NO_MALLOC` マクロを定義し、`Eigen::internal::set_is_malloc_allowed` 関数を使用する。

```cpp
// Eigen のヘッダの前に EIGEN_RUNTIME_NO_MALLOC を定義する。
#define EIGEN_RUNTIME_NO_MALLOC
#include <Eigen/Core>

// 怪しい処理の前にメモリ確保を許可しないように設定する。
Eigen::internal::set_is_malloc_allowed(false);

// ここに処理が入る。

// 処理の後にメモリ確保を許可するように設定する。
Eigen::internal::set_is_malloc_allowed(true);
```

## メモリ確保を防ぐ方法

[Eigen のドキュメント内の Writing efficient matrix product expressions](https://libeigen.gitlab.io/docs/TopicWritingEfficientProductExpression.html)
によると、

- 行列積はなるべく行列積だけで 1 つの処理にすると良い。
- 代入の右辺に左辺の変数が出てこないことを明示する `noalias` 関数を使用することで、
  右辺の処理結果が一時的にメモリ領域を確保してしまうことを防げる。

以下に例を示す。
（実際、線型方程式の残差の計算で以下のような計算が必要になった。）

メモリ確保される例：

```cpp
Eigen::MatrixXd matrix1;
Eigen::VectorXd vector1, vector2, vector3;

vector1 = matrix1 * vector2 - vector3; // matrix1 * vector2 の結果について一時的にメモリ領域を確保する。
```

修正例：

```cpp
Eigen::MatrixXd matrix1;
Eigen::VectorXd vector1, vector2, vector3;

vector1.noalias() = matrix1 * vector2; // noalias を使用する上に、行列積の演算だけを行う。
vector1 -= vector3; // 行列積とは別に減算を行う。
```
