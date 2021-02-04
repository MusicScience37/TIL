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

結果の生データ
'''''''''''''''''

- 文字列:
  :download:`bench_string.xml <result_20210205_Ubuntu/bench_string.xml>`
- double 型のベクトル:
  :download:`bench_double.xml <result_20210205_Ubuntu/bench_double.xml>`
- 構造体:
  :download:`bench_struct.xml <result_20210205_Ubuntu/bench_struct.xml>`

結果
''''''''

.. todo:: 書く
