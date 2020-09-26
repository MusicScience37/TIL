CMake のビルドディレクトリ中での出力先
======================================

CMake のビルドディレクトリでは、
特にバイナリの出力先を指定しなければ ``CMAKE_CURRENT_BINARY_DIR`` 変数で表される
個々のディレクトリにバイナリが出力される。
しかし、そのままでは

- 生成した実行ファイルを実行するのにサブディレクトリまで行くのが面倒
- Windows 環境では別のファイルに出力された dll が見つからないというエラーで実行ができない

といった問題が発生する。

そこで、次のような記述をルートの CMakeLists.txt に書く。

.. code:: cmake

    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY $<1:${CMAKE_BINARY_DIR}/lib>)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY $<1:${CMAKE_BINARY_DIR}/lib>)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY $<1:${CMAKE_BINARY_DIR}/bin>)

すると、次のように各ファイルがビルドディレクトリ中の各サブディレクトリへ配置される。
（参考：`cmake-buildsystem(7) - CMake 3.18.3 Documentation <https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html#archive-output-artifacts>`_）

.. csv-table:: Windows 上でのビルドディレクトリ内のバイナリの配置
    :header: 種類, 拡張子, CMake における分類, ディレクトリ
    :widths: auto

    実行ファイル, exe, runtime, bin
    共有ライブラリ, dll, runtime, bin
    静的ライブラリ, lib, archive, lib

.. csv-table:: Ubuntu 上でのビルドディレクトリ内のバイナリの配置
    :header: 種類, 拡張子, CMake における分類, ディレクトリ
    :widths: auto

    実行ファイル, (なし), runtime, bin
    共有ライブラリ, so, library, lib
    静的ライブラリ, a, archive, lib

.. note::
    Windows と Ubuntu では共有ライブラリが別の分類になっている。

.. note::
    ``${CMAKE_BINARY_DIR}/bin`` と ``$<1:${CMAKE_BINARY_DIR}/bin>`` では
    一部の環境において出力先が異なる。
    ``$<1:${CMAKE_BINARY_DIR}/bin>`` のように generator expression を使用することで、
    環境に依らない一定のディレクトリ構造を保つことができる。
    （参考：`RUNTIME_OUTPUT_DIRECTORY — CMake 3.18.3 Documentation <https://cmake.org/cmake/help/latest/prop_tgt/RUNTIME_OUTPUT_DIRECTORY.html#prop_tgt:RUNTIME_OUTPUT_DIRECTORY>`_）
