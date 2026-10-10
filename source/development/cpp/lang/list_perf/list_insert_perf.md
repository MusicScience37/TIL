---
file_format: mystnb
---

# C++ 標準ライブラリの list における insert の性能調査

C++ 標準ライブラリの `std::list` は途中への要素の挿入が計算量的には効率的とされている。
実際に高速なのかベンチマークを行った。

まずは普通に `std::list` を使用して性能を確認し、
その後、C++ 17 で導入された `std::pmr::monotonic_buffer_resource` を使用した高速化を試した。

```{code-cell}
:tags: [remove-input]

import pandas
from til_utils.plot_common import load_common_config

load_common_config()
```

```{code-cell}
:tags: [remove-input]
:load: list_perf_result_parser.py
```

```{code-cell}
:tags: [remove-input]

clang_results = parse_data("bench_clang_20261011.data")
msvc_results = parse_data("bench_msvc_20261011.data")
clang_results["env"] = "Clang"
msvc_results["env"] = "MSVC"
results = pandas.concat([clang_results, msvc_results], ignore_index=True)
```

## ベンチマーク環境

2 種類の環境でベンチマークを行った。

- Clang 環境
  - CPU: Intel(R) Core(TM) Ultra 5 125H
  - OS: Ubuntu 26:04
  - コンパイラ: Clang 22.1.2
- MSVC 環境
  - CPU: Intel(R) Core(TM) i7-1195G7
  - OS: Windows 11
  - コンパイラ: Visual Studio 2026 (2026/10/11 時点の最新)

## 普通に list を使用した場合

まず、普通に `std::list` を使用してベンチマークを行った。

今回対象とした処理は以下の通り。

1. まずは `push_back` で決まった要素数の配列を用意する。
2. 用意した配列の各要素の前に新しい要素を挿入する。

これを `std::vector` および `std::list` で以下のように実装した。

- `vector` （通常の `std::vector`）

  ```cpp
  std::vector<std::uint64_t> vec;
  for (std::size_t i = 0; i < count; ++i) {
      vec.push_back(0);
  }
  for (auto iter = vec.begin(); iter != vec.end();) {
      iter = vec.insert(iter, 0);
      ++iter;
      ++iter;
  }
  ```

- `vector_reserved` （`std::vector` で `reserve` 関数でメモリを事前に確保した場合）

  ```cpp
  std::vector<std::uint64_t> vec;
  vec.reserve(count * 2);
  for (std::size_t i = 0; i < count; ++i) {
      vec.push_back(0);
  }
  for (auto iter = vec.begin(); iter != vec.end();) {
      iter = vec.insert(iter, 0);
      ++iter;
      ++iter;
  }
  ```

- `list` （通常の `std::list`）

  ```cpp
  std::list<std::uint64_t> list;
  for (std::size_t i = 0; i < count; ++i) {
      list.push_back(0);
  }
  for (auto iter = list.begin(); iter != list.end();) {
      iter = list.insert(iter, 0);
      ++iter;
      ++iter;
  }
  ```

計測結果を以下に示す。

```{code-cell}
:tags: [remove-input]

import plotly.express as px
from til_utils.plot_common import show_figure

impl_types = [
    "vector",
    "vector_reserved",
    "list",
]
labels = {
    "count": "要素数",
    "mean_time": "時間 [s]",
    "impl_type": "実装",
    "env": "環境",
}
figure_height = 800
fig = px.line(
    results[(results["bench_type"] == "insert") & (results["impl_type"].isin(impl_types))],
    x="count",
    y="mean_time",
    color="impl_type",
    line_dash="impl_type",
    facet_row="env",
    log_x=True,
    log_y=True,
    labels=labels,
)
fig.update_layout(height=figure_height)
show_figure(fig)
```

要素数が十分多ければ速いが、要素数が 1000 以内の場合はそうでもない。

今回のベンチマークの処理の場合、
要素数 `n` の場合の計算量は `std::vector` が $O(n^2)$ であるのに対し、
`std::list` は $O(n)$ であるが、
`std::list` の方が係数が大きいものと思われる。

`std::list` は以下のように `std::vector` よりも性能が悪くなりやすい要素を持っているが、
`std::list` が本来得意なはずの処理でもあまり性能を出せないことがあるようだ。

- 要素ごとにメモリを確保する仕組みのため、1 個要素を追加するごとにメモリ確保の処理が呼ばれる。
- 要素ごとにメモリを確保する仕組みのため、連続したメモリ領域を使用する `std::vector` よりもキャッシュ効率が悪い。
- 前後の要素へのポインタの格納など、`std::vector` にはない追加の処理が必要。

このように `std::list` の性能があまり良くないという話は
[C++ benchmark – std::vector VS std::list VS std::deque](https://baptiste-wicht.com/posts/2012/12/cpp-benchmark-vector-list-deque.html)
という記事にもある。

ここまでは、C++ 17 が出る前の話である。

## monotonic_buffer_resource を使用した場合

C++ 17 では、メモリ管理を改善する polymorphic memory resource（PMR）が導入された。
そのうち、 `std::pmr::monotonic_buffer_resource` ではある程度連続した領域でまとめてメモリを確保できるため、
前述の `std::list` の問題を緩和できると思われる。
ただし、メモリの解放は `std::pmr::monotonic_buffer_resource` オブジェクトが破棄されるタイミングまで行われないため、
長期間要素を追加・削除しながら使いまわすようなデータには使えないことに注意が必要である。

`std::pmr::monotonic_buffer_resource` を使用した場合の性能を確認するため、
前述の実装パターンに加えて、以下のような実装パターンを追加した。

- `list_monotonic` （`std::pmr::monotonic_buffer_resource` をそのまま使用した `std::pmr::list`）

  ```cpp
  std::pmr::monotonic_buffer_resource monotonic_buffer_resource;
  std::pmr::list<std::uint64_t> list{&monotonic_buffer_resource};
  for (std::size_t i = 0; i < count; ++i) {
      list.push_back(0);
  }
  for (auto iter = list.begin(); iter != list.end();) {
      iter = list.insert(iter, 0);
      ++iter;
      ++iter;
  }
  ```

- `list_monotonic_with_static_buffer` （あらかじめ用意した静的バッファを `std::pmr::monotonic_buffer_resource` に渡して使用した `std::pmr::list`）

  ```cpp
  const std::size_t static_buffer_size = 65536;
  std::array<char, static_buffer_size> buffer;
  std::pmr::monotonic_buffer_resource monotonic_buffer_resource{
      buffer.data(), buffer.size()};
  std::pmr::list<std::uint64_t> list{&monotonic_buffer_resource};
  for (std::size_t i = 0; i < count; ++i) {
      list.push_back(0);
  }
  for (auto iter = list.begin(); iter != list.end();) {
      iter = list.insert(iter, 0);
      ++iter;
      ++iter;
  }
  ```

処理時間の計測結果を以下に示す。

```{code-cell}
:tags: [remove-input]

impl_types = [
    "vector",
    "vector_reserved",
    "list",
    "list_monotonic",
    "list_monotonic_with_static_buffer",
]
fig = px.line(
    results[(results["bench_type"] == "insert") & (results["impl_type"].isin(impl_types))],
    x="count",
    y="mean_time",
    color="impl_type",
    line_dash="impl_type",
    facet_row="env",
    log_x=True,
    log_y=True,
    labels=labels,
)
fig.update_layout(height=figure_height)
show_figure(fig)
```

`std::list` をそのまま使用する場合よりも性能が良くなり、
要素数 100 以上なら `std::vector` よりも高速になった。
要素数が少ない場合でも `std::vector` より 2 倍程度までの処理時間で済むところまで高速化できた。
これなら利用の幅が広がりそうだ。

## まとめ

`std::list` は、そのままの利用では `std::vector` よりも性能が出にくいが、
`std::pmr::monotonic_buffer_resource` を使用するなど、
メモリ管理を工夫することで `std::vector` よりも性能を出せる場合がある。
性能のために `std::list` を使用する場合は、
計算量を見るだけでなく、実際の処理時間を計測して判断する必要がある。

## （付録）forward_list の場合

`std::list` よりも単純なデータ構造として `std::forward_list` がある。
その `std::forward_list` も試してみた。

追加した実装パターンは以下の通り。

- `forward_list` （そのまま使用した `std::forward_list`）

  ```cpp
  std::forward_list<std::uint64_t> list;
  auto iter = list.before_begin();
  for (std::size_t i = 0; i < count; ++i) {
      iter = list.insert_after(iter, 0);
  }
  iter = list.before_begin();
  for (std::size_t i = 0; i < count; ++i) {
      iter = list.insert_after(iter, 0);
      ++iter;
  }
  ```

- `forward_list_monotonic` （`std::pmr::monotonic_buffer_resource` を使用した `std::forward_list`）

  ```cpp
  std::pmr::monotonic_buffer_resource monotonic_buffer_resource;
  std::pmr::forward_list<std::uint64_t> list{&monotonic_buffer_resource};
  auto iter = list.before_begin();
  for (std::size_t i = 0; i < count; ++i) {
      iter = list.insert_after(iter, 0);
  }
  iter = list.before_begin();
  for (std::size_t i = 0; i < count; ++i) {
      iter = list.insert_after(iter, 0);
      ++iter;
  }
  ```

- `forward_list_monotonic_with_static_buffer` （`std::pmr::monotonic_buffer_resource` と静的バッファを使用した `std::forward_list`）

  ```cpp
  const std::size_t static_buffer_size = 65536;
  std::array<char, static_buffer_size> buffer;
  std::pmr::monotonic_buffer_resource monotonic_buffer_resource{
      buffer.data(), buffer.size()};
  std::pmr::forward_list<std::uint64_t> list{&monotonic_buffer_resource};
  auto iter = list.before_begin();
  for (std::size_t i = 0; i < count; ++i) {
      iter = list.insert_after(iter, 0);
  }
  iter = list.before_begin();
  for (std::size_t i = 0; i < count; ++i) {
      iter = list.insert_after(iter, 0);
      ++iter;
  }
  ```

処理時間は以下の通り。

```{code-cell}
:tags: [remove-input]

impl_types = [
    "vector",
    "vector_reserved",
    "list",
    "list_monotonic",
    "list_monotonic_with_static_buffer",
    "forward_list",
    "forward_list_monotonic",
    "forward_list_monotonic_with_static_buffer",
]
fig = px.line(
    results[(results["bench_type"] == "insert") & (results["impl_type"].isin(impl_types))],
    x="count",
    y="mean_time",
    color="impl_type",
    line_dash="impl_type",
    facet_row="env",
    log_x=True,
    log_y=True,
    labels=labels,
)
fig.update_layout(height=figure_height)
show_figure(fig)
```

`std::forward_list` は `std::list` よりも少し速かった。
ただし、 `std::vector` や `std::list` にある普通の `push_back` 関数や `insert` 関数がなく、
少し特殊な実装が要求された。

以上から、制約が強めなデータ構造でも問題がない場合は `std::forward_list` で高速化を図ることも可能である。
