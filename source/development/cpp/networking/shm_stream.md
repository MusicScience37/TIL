---
file_format: mystnb
---

# 共有メモリを用いたストリームの実験

共有メモリは UDP などの通信プロトコルに比べて速いと聞くため、
共有メモリを用いた軽いストリームを実装して性能を確認した。

## 共有メモリを用いたストリーム

今回、共有メモリを用いて以下のようなリングバッファによるストリームを
[cpp-shm-stream リポジトリ](https://gitlab.com/MusicScience37Projects/utility-libraries/cpp-shm-stream)
に用意した。

- `light_stream`:
  アトミック演算による wait free なリングバッファのストリーム

- `blocking_stream`:
  アトミック演算を主に用いつつ、
  データの待機処理がビジーループなしで行えるように実装したリングバッファのストリーム

どちらも、リングバッファ用に

- 書き込み側のインデックス
- 読み込み側のインデックス
- バッファのサイズ
- バッファ

を共有メモリ上に共有する。
2 つのインデックスについてはアトミック演算を行うため、
共有メモリ上でもアトミック演算を行うことができる
[Boost.Atomic ライブラリ](https://www.boost.org/doc/libs/1_81_0/libs/atomic/doc/html/index.html)
の `boost::atomics::ipc_atomic` クラスを用いた。

## 比較の対象とした通信方法

以下を対象に、通信時間の比較を行った。

- 共有メモリを用いたストリーム

- UDP

  - UDP による通信の実装には [Asio ライブラリ](https://think-async.com/Asio/) を用いた。
  - IPv4 と IPv6 の UDP の両方を対象とした。

## 環境

実験を行った環境は以下の通り。

- CPU：Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
- メモリ：16 GB
- OS：Ubuntu 22.04

## レイテンシの測定

各通信方法とデータサイズ（32 byte, 1 KB, 32 kB, 1 MB）ごとに
10000 回往復の通信をし、データを送受信するのにかかる時間を箱ひげ図でプロットした。

```{code-cell}
:tags: [hide-cell]
:load: shm_stream_result_parser.py
```

```{code-cell}
:tags: [hide-input]

import pandas
import plotly.express as px
import plotly.graph_objects as go

bench_results = parse_data("shm_stream_result_20230414/ping_pong.data")

fig = px.box(
    bench_results,
    x="data_size",
    y="time",
    color="protocol",
    log_y=True,
    points=False,
    labels = {
        "data_size": "データサイズ [byte]",
        "time": "レイテンシ [sec]",
        "protocol": "通信方法",
    },
    title="レイテンシの測定結果",
)
fig.update_layout(height=500)
go.FigureWidget(fig)
```

## 送信時間の測定

各通信方法とデータサイズ（32 byte, 1 KB, 32 kB, 1 MB）ごとに
10000 回データを送信し、データの送信処理にかかる時間を箱ひげ図でプロットした。

```{code-cell}
:tags: [hide-input]

bench_results = parse_data("shm_stream_result_20230414/send_messages.data")

fig = px.box(
    bench_results,
    x="data_size",
    y="time",
    color="protocol",
    log_y=True,
    points=False,
    labels = {
        "data_size": "データサイズ [byte]",
        "time": "送信時間 [sec]",
        "protocol": "通信方法",
    },
    title="送信時間の測定結果",
)
fig.update_layout(height=500)
go.FigureWidget(fig)
```

## 比較

- 共有メモリを用いた通信はどちらも UDP より速くなっている。

- IPv4 と IPv6 の UDP の両方を試したが、
  IPv4 と IPv6 では特に差が見受けられなかった。

- 共有メモリを用いた通信 2 種類では、
  アトミック演算のみを使用した `light_stream` の方が速い。
  `light_stream` ではデータの待機処理にビジーループを用いているため比較的負荷はかかるが、
  代わりに速度は速くなった。

## ソースコードなど

実験は
[cpp-shm-stream リポジトリ](https://gitlab.com/MusicScience37Projects/utility-libraries/cpp-shm-stream)
のコミット
`fa8c023d51fcf9ac9f398a11c7e548fc0539255a`
上で Release ビルドを行い、
以下のコマンドを実行することで行った。

- `./build/Release/bin/bench_send_messages --msgpack send_messages.data --samples 10000`

- `python3 ./tests/bench/ping_pong/bench.py build/Release/`
