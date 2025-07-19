---
file_format: mystnb
---

# C++ 上でデータをシリアライズする

C++ 上でデータをシリアライズ・デシリアライズするライブラリの調査記録。

## 調査したライブラリ

### msgpack-c

[msgpack-c](https://github.com/msgpack/msgpack-c)
は
[MessagePack](https://msgpack.org/)
形式でデータのシリアライズ・デシリアライズを行うライブラリ。
ライセンスは Boost Software License Version 1.0 となっている。

MessagePack はコンパクトでかつ効率的な実装がしやすいように作られた
バイナリのデータ形式で、
様々な言語のライブラリが作られている。
MessagePack 公式の GitHub グループにあるものだけでも、
Ruby, Python, PHP, Javascript, C, C++, Java, Haskell,
D, Perl, Erlang, Smalltalk, Scala, OCaml,
Go, Objective-C
といった言語のライブラリが存在する。

### Protocol Buffers

[Protocol Buffers](https://developers.google.com/protocol-buffers/)
は Google が考案したデータのシリアライズ・デシリアライズ形式で、
C++ 向けのライブラリは
[protobuf](https://github.com/protocolbuffers/protobuf)
にて公開されている。
ライセンスは 3 条項 BSD ライセンスとなっている。

MessagePack と同様にバイナリのデータ形式で、
専用の言語で書かれたメッセージの定義をもとに
各プログラミング言語向けのクラスを自動生成することができる。
公式リポジトリの README によると、
C++, Java, Python, Objective-C, C#, JavaScript, Ruby,
Go, PHP, Dart
といった言語に対応している。

インタフェースの定義を複数の言語の間で共有したいときに便利なライブラリとなっている。
（参考：[今さら Protocol Buffers と、手に馴染む道具の話 - Qiita](https://qiita.com/yugui/items/160737021d25d761b353)）

### cereal

[cereal](https://github.com/USCiLab/cereal)
はバイナリ形式、XML、JSON などでデータをシリアライズ・デシリアライズできるライブラリ。
ライセンスは BSD 3-Clause となっている。

比較的効率的なバイナリ形式でのシリアライズ・デシリアライズもできるため，今回比較に用いた。
後述のベンチマークは全てバイナリ形式で行っている。

### nlohmann/json

[nlohmann/json](https://github.com/nlohmann/json)
は JSON のシリアライズ・デシリアライズを行うライブラリの 1 つ。
ライセンスは MIT ライセンスとなっている。

シンプルな API を持ち、
このページに挙げているライブラリの中では最も使いやすい印象。
ただし、効率は重視していないため、速度やメモリ使用量については要注意。

また、JSON は前述の msgpack-c や Protocol Buffers と異なり、
データ形式の時点で効率があまり良くない上に、
仕様上 Unicode でない文字を使用できないため注意。

### RapidJSON

[RapidJSON](https://github.com/Tencent/rapidjson/)
も JSON のシリアライズ・デシリアライズを行うライブラリの 1 つ。
ライセンスは MIT ライセンスとなっている。

nlohmann/json と対照的に、
効率を重視しているライブラリであり、
[Native JSON Benchmark](https://github.com/miloyip/nativejson-benchmark#parsing-time)
では、最速で最もメモリ使用量が少ないのが RapidJSON となっている。
ただし、API の使いやすさでは他のライブラリに負ける。

### simdjson

[simdjson](https://github.com/simdjson/simdjson)
は JSON のデシリアライズを行うライブラリの 1 つ。
ライセンスは Apache 2.0 ライセンスとなっている。

SIMD 演算を用いて高速に JSON のデシリアライズを行うライブラリであり、
デシリアライズ処理だけは RapidJSON よりも速いという。
しかし、任意のデータをシリアライズする機能が実装されていないため、
デシリアライズしか行わない場合にしか使用できない。
また、API は RapidJSON 以上に使いにくく、
ライブラリの使用による実装の仕方の制約が極めて強い。

### yyjson

[yyjson](https://github.com/ibireme/yyjson)
は JSON のシリアライズ・デシリアライズを行うライブラリの 1 つ。
ライセンスは MIT ライセンスとなっている。

C 言語で書かれており、API は使いにくいが、速く動作する。
simdjson のように SIMD 演算を直接使用しているわけではないが、
simdjson と競うほどの速さを持つ。

## ベンチマーク

上記のライブラリについてベンチマークを行った。

### 環境

- OS: Ubuntu 24.04
- CPU: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz （6 コア 12 スレッド）
- メモリ: 16 GB
- コンパイラ: Clang 19.1.7

### 対象データ

- 文字列（1 文字、32 文字、1024 文字、32 × 1024 文字）
- int 型のベクトル（1 要素、32 要素、1024 要素、32 × 1024 要素）
- double 型のベクトル（1 要素、1024 要素、1024 × 1024 要素）
- 次のような構造体

  ```cpp
  struct test_struct {
      std::int32_t param_int;
      double param_double;
      std::vector<char> binary;
  };
  ```

### ライブラリのバージョン

- msgpack: 7.0.0
- Protocol Buffers: 5.29.3
- cereal 1.3.2
- nlohmann/json: 3.12.0
- RapidJSON: 2025-02-26
- simdjson: 3.13.0
- yyjson: 0.11.1

### ソースコード

[bench_for_cpp_serialization](https://gitlab.com/MusicScience37/bench_for_cpp_serialization)

### 結果

- 生データ

  - 文字列:
    {download}`bench_string.xml <result_20250719_Ubuntu/bench_string.xml>`
  - int 型のベクトル:
    {download}`bench_int.xml <result_20250719_Ubuntu/bench_int.xml>`
  - double 型のベクトル:
    {download}`bench_double.xml <result_20250719_Ubuntu/bench_double.xml>`
  - 構造体:
    {download}`bench_struct.xml <result_20250719_Ubuntu/bench_struct.xml>`

- まとめたデータ

  - まとめた CSV:
    {download}`bench.csv <result_20250719_Ubuntu/bench.csv>`

#### 文字列のベンチマーク結果

まず、文字列のシリアライズ・デシリアライズの処理時間から確認する。

```{code-cell}
:tags: [remove-input]

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

bench_results = pd.read_csv('result_20250719_Ubuntu/bench.csv')

# parse は msgpack-c でしか行っていないからグラフに入れない
bench_results = bench_results[bench_results['procedure'] != 'parse']

# 表示用データ
bench_results['error_minus_ns'] = bench_results['mean_ns'] - bench_results['lower_bound_ns']
bench_results['error_plus_ns'] = bench_results['upper_bound_ns'] - bench_results['mean_ns']
bench_results['mean_sec'] = bench_results['mean_ns'] * 1e-9
bench_results['error_minus_sec'] = bench_results['error_minus_ns'] * 1e-9
bench_results['error_plus_sec'] = bench_results['error_plus_ns'] * 1e-9
labels={
    'mean_sec': '平均処理時間 [sec.]',
}

fig = px.line(
    bench_results[bench_results["data_type"] == "string"],
    y="mean_sec",
    log_x=True,
    log_y=True,
    error_y_minus="error_minus_sec",
    error_y="error_plus_sec",
    x="data_size",
    color="library",
    facet_col="procedure",
    title='ベンチマーク結果（文字列）',
    labels=labels,
)
fig.show(renderer="notebook_connected")
```

多くの場合で

1. msgpack-c
2. Protocol Buffers
3. cereal
4. yyjson
5. simdjson
6. RapidJSON
7. nlohmann/json

の順に速かった。

特に、msgpack-c によるデシリアライズの処理では文字列のコピーをしない方法が存在しており、
その方法を用いているため、
データサイズに関係ない処理時間が実現できている。

#### int のベクトルのベンチマーク結果

int のベクトルの結果は以下の通り。
simdjson はこのデータを正常にデシリアライズできなかったため除外した。

```{code-cell}
:tags: [remove-input]

fig = px.line(
    bench_results[bench_results["data_type"] == "int"],
    y="mean_sec",
    log_x=True,
    log_y=True,
    error_y_minus="error_minus_sec",
    error_y="error_plus_sec",
    x="data_size",
    color="library",
    facet_col="procedure",
    title='ベンチマーク結果（int のベクトル）',
    labels=labels,
)
fig.show(renderer="notebook_connected")
```

今度は多くの場合で

1. cereal
2. Protocol Buffers or msgpack-c （シリアライズとデシリアライズで順位が変わる）
3. yyjson
4. RapidJSON
5. nlohmann/json

の順に速かった。

Protocol Buffers と msgpack-c はシリアライズされたデータのエンディアンが固定されている一方、
cereal はシステムのエンディアンをそのまま使用するため速い。

#### double のベクトルのベンチマーク結果

double のベクトルの結果は以下の通り。

```{code-cell}
:tags: [remove-input]

fig = px.line(
    bench_results[bench_results["data_type"] == "double"],
    y="mean_sec",
    log_x=True,
    log_y=True,
    error_y_minus="error_minus_sec",
    error_y="error_plus_sec",
    x="data_size",
    color="library",
    facet_col="procedure",
    title='ベンチマーク結果（double のベクトル）',
    labels=labels,
)
fig.show(renderer="notebook_connected")
```

今度は多くの場合で

1. Protocol Buffers
2. cereal
3. msgpack-c
4. simdjson
5. yyjson
6. RapidJSON
7. nlohmann/json

の順に速かった。

#### 構造体のベンチマーク結果

最後に構造体のデータを用いた場合の結果を示す。

```{code-cell}
:tags: [remove-input]

fig = px.bar(
    bench_results[bench_results['data_type'] == 'struct'],
    y='mean_sec', log_y=True,
    error_y_minus='error_minus_sec', error_y='error_plus_sec',
    x='procedure', color='library', barmode="group",
    title='ベンチマーク結果（構造体）',
    labels=labels,
)
fig.show(renderer="notebook_connected")
```

今度は多くの場合で

1. msgpack-c or Protocol Buffers （シリアライズとデシリアライズで順位が変わる）
2. cereal
3. yyjson
4. simdjson
5. RapidJSON
6. nlohmann/json

の順に速かった。

### ベンチマークのまとめ

- バイナリデータを用いる msgpack-c と Protocol Buffers、cereal が
  JSON のライブラリよりも速かった。
- msgpack-c と Protocol Buffers、cereal は状況によって順位が入れ替わり、
  差は文字列のデシリアライズ以外 1 桁程度までに収まっている。
- JSON のライブラリでは yyjson と simdjson が特に速く、
  RapidJSON がその次に速く、nlohmann/json が最も遅かった。

## まとめ

ここでは、C++ 上でデータのシリアライズ・デシリアライズを行うライブラリをまとめた。
状況によってライブラリを使い分けていく必要がある。

- バイナリデータ形式 vs. JSON

  - バイナリデータの方が効率は良い。
    特に小数のデータを多く扱う場合に差が出やすい。
  - JSON の方が人間にとってデータを読みやすい。
  - ASCII や Unicode の範囲を超えるデータがいつでも扱えるとは限らないため、
    バイナリデータの利用には注意が必要。
    ただし、msgpack-c と Protocol Buffers はエンディアンが規定されているため、
    エンディアンが異なるシステム間でも問題なく使用できる。

- msgpack-c vs. Protocol Buffers vs. cereal

  - 効率の良さは状況によるため、効率だけでは選びづらい。
  - msgpack-c は動的にパースされたデータの内部を探索することができる。
  - Protocol Buffers は他言語とのデータ共有に向いている。
  - cereal は C++ のみのサポートになる。
  - ユーザ定義のデータ型のシリアライズ・デシリアライズを行うにあたって、

    - msgpack-c ではパースされたデータ（`msgpack::object`）とユーザ定義のデータ型との間の変換の実装が必要。
    - Protocol Buffers では自動生成されたクラスとユーザ定義のデータ型との間の変換の実装が必要。
    - cereal ではデータ型ごとのシリアライズ・デシリアライズ用の関数の実装が必要。

    となる。
    変換処理は Protocol Buffers が書きやすい。

- nlohmann/json vs. RapidJSON vs. simdjson

  - 性能面では yyjson と simdjson が速い。
    ただし、simdjson はシリアライズができない。
  - API は nlohmann/json が使いやすい。
    特に、STL との間の相互変換は nlohmann/json では簡単にできても、
    RapidJSON, simdjson, yyjson では自力での実装が必要。
  - 実装時間と実行時間のどちらを選択するかによってどれを利用すべきかが変わる。
