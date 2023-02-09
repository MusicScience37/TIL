Ccache によるビルド高速化
============================

`Ccache <https://ccache.dev/>`_
は、C/C++ のコンパイル時に生成されるオブジェクトファイルをキャッシュして、
同じ条件によるコンパイルの処理をなくすことにより、
リビルドの時間を短くすることができるツールである。
今回試したコンパイル時間が長い
`numerical-collection-cpp <https://gitlab.com/MusicScience37Projects/numerical-analysis/numerical-collection-cpp>`_
リポジトリでは、
リビルドを 40 倍高速化できた [#footnote-speed]_ 。

インストール方法
-------------------

Ubuntu 上では、``apt install ccache`` コマンドでインストールできる。
また、公式ホームページでは Windows 用のバイナリも用意されている。

設定
--------------

ここで、今回 ccache を使用した際に調整した設定項目を列挙しておく。
なお、いずれも環境変数で設定する。

..
    cspell:ignore COMPILERCHECK MAXSIZE

``CCACHE_DIR``
    キャッシュを保存するディレクトリ。

``CCACHE_COMPILERCHECK``
    コンパイラが同一かどうかをチェックする方法を指定する。
    デフォルトではタイムスタンプが使用されるが、
    Docker コンテナで使用する場合は
    タイムスタンプよりもコンパイラのバイナリによる比較を行う ``content`` の方が都合が良い。
    （Docker コンテナを作り直しても、コンパイラが完全に一致すれば同じコンパイラとして扱う。）

``CCACHE_MAXSIZE``
    キャッシュの合計サイズの上限。デフォルトでは 5 GB となっている。
    今回適用したリポジトリは、ビルドディレクトリが 5 GB もあったため、
    この設定項目を 10 GB に設定した。

CMake への適用
----------------------

CMake でビルドを行う場合、
``CMAKE_C_COMPILER_LAUNCHER``, ``CMAKE_CXX_COMPILER_LAUNCHER``
という 2 つの変数に ``ccache`` コマンドを指定することで、
Ccache を適用できる。

.. rubric:: Footnotes

.. [#footnote-speed]
    `numerical-collection-cpp <https://gitlab.com/MusicScience37Projects/numerical-analysis/numerical-collection-cpp>`_
    リポジトリのコミット 1ef7d5fd2be019fe142f2ffe2e939574b6d4118d 時点のソースコードに対して
    4 スレッドの Release ビルドを行ったところ、
    ビルド時間を 377 秒から 9 秒まで削減できた。
    ヘッダオンリーの重いライブラリを使用しているために 1 ファイルごとのコンパイル時間が比較的長く、
    Ccache の効果が得られやすいプロジェクトとなっている。
