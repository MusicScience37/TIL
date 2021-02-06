C++ 上でデータをシリアライズする
==========================================

C++ 上でデータをシリアライズ・デシリアライズするライブラリの調査記録。

msgpack-c
--------------

`msgpack-c <https://github.com/msgpack/msgpack-c>`_
は
`MessagePack <https://msgpack.org/>`_
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

Protocol Buffers
------------------------

`Protocol Buffers <https://developers.google.com/protocol-buffers/>`_
は Google が考案したデータのシリアライズ・デシリアライズ形式で、
C++ 向けのライブラリは
`protobuf <https://github.com/protocolbuffers/protobuf>`_
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
（参考：`今さらProtocol Buffersと、手に馴染む道具の話 - Qiita <https://qiita.com/yugui/items/160737021d25d761b353>`_）

nlohmann/json
---------------------

`nlohmann/json <https://github.com/nlohmann/json>`_
は JSON のシリアライズ・デシリアライズを行うライブラリの 1 つ。
ライセンスは MIT ライセンスとなっている。

シンプルな API を持ち、
このページに挙げているライブラリの中では最も使いやすい印象。
ただし、効率は重視していないため、速度やメモリ使用量については要注意。

また、JSON は前述の msgpack-c や Protocol Buffers と異なり、
データ形式の時点で効率があまり良くない上に、
仕様上 Unicode でない文字を使用できないため注意。

RapidJSON
---------------------

`RapidJSON <https://github.com/Tencent/rapidjson/>`_
も JSON のシリアライズ・デシリアライズを行うライブラリの 1 つ。
ライセンスは MIT ライセンスとなっている。

nlohmann/json と対照的に、
効率を重視しているライブラリであり、
`Native JSON Benchmark <https://github.com/miloyip/nativejson-benchmark#parsing-time>`_
では、最速で最もメモリ使用量が少ないのが RapidJSON となっている。
ただし、API の使いやすさでは他のライブラリに負ける。

ベンチマーク
------------------

上記のライブラリについてベンチマークを行った。

環境
''''''''''''

- OS: Ubuntu 20.04
- CPU: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz （6 コア 12 スレッド）
- メモリ: 16 GB

対象データ
'''''''''''''''

- 文字列（1 文字、1024 文字、1024 × 1024 文字）
- double 型のベクトル（1 要素、1024 要素、1024 × 1024 要素）
- 次のような構造体

  .. code-block:: cpp

      struct test_struct {
          std::int32_t param_int;
          double param_double;
          std::vector<char> binary;
      };

ライブラリのバージョン
'''''''''''''''''''''''''

- msgpack-c: 3.3.0
- Protocol Buffers: 3.14.0
- nlohmann/json: 3.9.1
- RapidJSON: 1.1.0

ソースコード
'''''''''''''''''

`bench_for_cpp_serialization <https://gitlab.com/MusicScience37/bench_for_cpp_serialization>`_

結果
''''''''

- 生データ

  - 文字列:
    :download:`bench_string.xml <result_20210205_Ubuntu/bench_string.xml>`
  - double 型のベクトル:
    :download:`bench_double.xml <result_20210205_Ubuntu/bench_double.xml>`
  - 構造体:
    :download:`bench_struct.xml <result_20210205_Ubuntu/bench_struct.xml>`

- まとめたデータ

  - まとめた CSV:
    :download:`bench.csv <result_20210205_Ubuntu/bench.csv>`
  - 処理用スクリプト:
    :download:`convert_xml_to_csv.py <result_20210205_Ubuntu/convert_xml_to_csv.py>`

まず、文字列のシリアライズ・デシリアライズの処理時間から確認する。

.. jupyter-execute::

    import pandas as pd
    import plotly.express as px

    bench_results = pd.read_csv('source/development/cpp/serialization/result_20210205_Ubuntu/bench.csv')

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

    px.bar(bench_results[bench_results['data_type'] == 'string'],
           y='mean_sec', log_y=True,
           error_y_minus='error_minus_sec', error_y='error_plus_sec',
           x='procedure', color='library', barmode="group",
           facet_col='data_size',
           title='ベンチマーク結果（文字列）',
           labels=labels)

ほとんどの場合で

1. msgpack-c
2. Protocol Buffers
3. RapidJSON
4. nlohmann/json

の順に速かった。
データが 1 バイトの場合だけ Protocol Buffers が最も速かった。

double のベクトルの結果は以下の通り。
JSON は double のベクトルのシリアライズ・デシリアライズで
効率の極めて悪い少数の文字列表記を用いるため、
1024 × 1024 のデータサイズの試験を省略した。

.. jupyter-execute::

    px.bar(bench_results[bench_results['data_type'] == 'double'],
           y='mean_sec', log_y=True,
           error_y_minus='error_minus_sec', error_y='error_plus_sec',
           x='procedure', color='library', barmode="group",
           facet_col='data_size',
           title='ベンチマーク結果（double のベクトル）',
           labels=labels)

今度は

1. Protocol Buffers
2. msgpack-c
3. RapidJSON
4. nlohmann/json

の順に速かった。

最後に構造体のデータを用いた場合の結果を示す。

.. jupyter-execute::

    px.bar(bench_results[bench_results['data_type'] == 'struct'],
           y='mean_sec', log_y=True,
           error_y_minus='error_minus_sec', error_y='error_plus_sec',
           x='procedure', color='library', barmode="group",
           title='ベンチマーク結果（構造体）',
           labels=labels)

msgpack-c と Protocol Buffers はシリアライズとデシリアライズで順番が入れ替わっているが、
RapidJSON と nlohmann/JSON が時間かかるのは共通している。

ベンチマークのまとめ
'''''''''''''''''''''''

- バイナリデータを用いる msgpack-c と Protocol Buffers が
  JSON のライブラリよりも速かった。
- msgpack-c と Protocol Buffers は状況によって順位が入れ替わり、
  差は 1 桁程度までに収まっている。
- JSON のライブラリでは RapidJSON が常に速かった。

まとめ
----------------

ここでは、C++ 上でデータのシリアライズ・デシリアライズを行うライブラリをまとめた。
状況によってライブラリを使い分けていこう。

- バイナリデータ形式 vs. JSON

  - バイナリデータの方が効率は良い。
    特に少数のデータを多く扱う場合に差が出やすい。
  - JSON の方がデータを読みやすい。
  - ASCII や Unicode の範囲を超えるデータがいつでも扱えるとは限らないため、
    バイナリデータの利用には注意が必要。
    ただし、msgpack-c と Protocol Buffers はエンディアンが規定されているため、
    エンディアンが異なるシステム間でも問題なく使用できる。

- msgpack-c vs. Protocol Buffers

  - 効率の良さは状況によるため、効率だけでは選びづらい。
  - msgpack-c は動的にパースされたデータの内部を探索することができる。
  - Protocol Buffers は他言語とのデータ共有に向いている。
  - ユーザ定義のデータ型のシリアライズ・デシリアライズを行うにあたって、

    - msgpack-c ではパースされたデータ（``msgpack::object``）とユーザ定義のデータ型との間の変換の実装が必要。
    - Protocol Buffers では自動生成されたクラスとユーザ定義のデータ型との間の変換の実装が必要。

    となる。
    C++ だけでシリアライズ・デシリアライズを行うのであれば、
    C++ だけ書けば良い msgpack-c の方が簡単な印象。

- nlohmann/json vs. RapidJSON

  - 処理効率は RapidJSON が良い。
  - API は nlohmann/json が使いやすい。
    特に、STL との間の相互変換は nlohmann/json では簡単できても、
    RapidJSON では自力での実装が必要。
  - 実装時間と実行時間のバランスでどちらを利用すべきかが変わる。
