共有メモリを用いたストリームの実験
=======================================

共有メモリは UDP などの通信プロトコルに比べて速いと聞くため、
共有メモリを用いた軽いストリームを実装して性能を確認した。

共有メモリを用いたストリーム
---------------------------------

今回、共有メモリを用いて以下のようなリングバッファによるストリームを
`cpp-shm-stream リポジトリ <https://gitlab.com/MusicScience37Projects/utility-libraries/cpp-shm-stream>`__
に用意した。

- ``light_stream``:
  アトミック演算による wait free なリングバッファのストリーム

- ``blocking_stream``:
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
`Boost.Atomic ライブラリ <https://www.boost.org/doc/libs/1_81_0/libs/atomic/doc/html/index.html>`_
の ``boost::atomics::ipc_atomic`` クラスを用いた。

比較の対象とした通信方法
---------------------------

以下を対象に、通信時間の比較を行った。

- 共有メモリを用いたストリーム

- UDP

  - UDP による通信の実装には `Asio ライブラリ <https://think-async.com/Asio/>`_ を用いた。
  - IPv4 と IPv6 の UDP の両方を対象とした。

環境
-----------

実験を行った環境は以下の通り。

- CPU：Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
- メモリ：16 GB
- OS：Ubuntu 22.04

レイテンシの測定
-------------------

各通信方法とデータサイズ（32 byte, 1 KB, 32 kB, 1 MB）ごとに
100 回往復の通信をし、データを送受信するのにかかる時間の平均をプロットした。
エラーバーは最大と最小の時間を示している。

.. jupyter-execute::
    :hide-code:

    import pandas as pd
    import plotly.express as px

    bench_results = pd.read_csv("source/development/cpp/networking/shm_stream_result_20230326/ping_pong.csv")

    # 表示用データ
    bench_results["error_plus"] = bench_results["Max Time [sec]"] - bench_results["Mean Time [sec]"]
    bench_results["error_minus"] = bench_results["Mean Time [sec]"] - bench_results["Min Time [sec]"]

    px.line(
        bench_results,
        x="Data Size [byte]",
        y="Mean Time [sec]",
        error_y="error_plus",
        error_y_minus="error_minus",
        color="Protocol",
        log_x=True,
        log_y=True,
    )

送信時間の測定
-------------------

各通信方法とデータサイズ（32 byte, 1 KB, 32 kB, 1 MB）ごとに
100 回データを送信し、データの送信処理にかかる時間の平均をプロットした。
エラーバーは最大と最小の時間を示している。

.. jupyter-execute::
    :hide-code:

    import pandas as pd
    import plotly.express as px

    bench_results = pd.read_csv("source/development/cpp/networking/shm_stream_result_20230326/send_messages.csv")

    # 表示用データ
    bench_results["error_plus"] = bench_results["Max Time [sec]"] - bench_results["Mean Time [sec]"]
    bench_results["error_minus"] = bench_results["Mean Time [sec]"] - bench_results["Min Time [sec]"]

    px.line(
        bench_results,
        x="Data Size [byte]",
        y="Mean Time [sec]",
        error_y="error_plus",
        error_y_minus="error_minus",
        color="Protocol",
        log_x=True,
        log_y=True,
    )

比較
-----------

- 共有メモリを用いた通信はどちらも UDP より速くなっている。

- IPv4 と IPv6 の UDP の両方を試したが、
  IPv4 と IPv6 では特に差が見受けられなかった。

- 共有メモリを用いた通信 2 種類では、
  アトミック演算のみを使用した ``light_stream`` の方が速い。
  ``light_stream`` ではデータの待機処理にビジーループを用いているため比較的負荷はかかるが、
  代わりに速度は速くなった。

ソースコードなど
-------------------

実験は
`cpp-shm-stream リポジトリ <https://gitlab.com/MusicScience37Projects/utility-libraries/cpp-shm-stream>`__
のコミット
``97411b05de27074fb06123f6ff41b7e120d17980``
上で Release ビルドを行い、
以下のコマンドを実行することで行った。

- ``./build/Release/bin/bench_send_messages --json temp/bench.json``

- ``python3 ./tests/bench/ping_pong/bench.py build/Release/``
