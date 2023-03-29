vcpkg
==========

`vcpkg <https://vcpkg.io/>`_
は C++ 用のパッケージマネージャの 1 つ。
Microsoft が作成しており、
Windows、Linux、Mac で使用できる。

特徴
--------------

- Python の PyPI や Ubuntu の apt などのパッケージマネージャが
  パッケージ用の専用のサーバを持つのに対し、
  vcpkg はパッケージの情報を Git リポジトリで管理・提供する仕組みため、
  パッケージを提供する専用のサーバが不要となっている。

- vcpkg の Git リポジトリのバージョンを固定しておけば、
  ある日急にライブラリのバージョンが更新されて動作に影響が出るということはない。

- CMakeLists.txt 上ではパッケージマネージャを意識した記載をする必要がない。
  （下記の使用例を参照。）

インストール
----------------

vcpkg をインストールするには以下のようにする。

1. `vcpkg の GitHub リポジトリ <https://github.com/Microsoft/vcpkg.git>`_
   をクローンするか、
   使用する先の Git リポジトリ内に submodule で追加する。

2. 以下のコマンドで vcpkg をビルドする。

   - Linux

     .. code-block:: bash

         ./vcpkg/bootstrap-vcpkg.sh

   - Windows

     .. code-block:: bat

         .\vcpkg\bootstrap-vcpkg.bat

   vcpkg リポジトリのディレクトリ直下に ``vcpkg`` コマンドが配置される。

使用例
----------------

CMake で vcpkg を使用してみた例を記載する。

vcpkg では、以下のような形式の vcpkg.json ファイルに依存ライブラリを記載する。

.. code-block:: json

    {
      "$schema": "https://raw.githubusercontent.com/microsoft/vcpkg-tool/main/docs/vcpkg.schema.json",
      "dependencies": [
        "boost-atomic",
        "bfgroup-lyra",
        "catch2",
        "trompeloeil",
        "fmt"
      ]
    }

``cmake`` コマンドの実行時に

.. code-block:: bash

    cmake -DCMAKE_TOOLCHAIN_FILE=<vcpkgリポジトリのパス>/scripts/buildsystems/vcpkg.cmake <他のオプションやソースディレクトリなど>

のようにオプションを追加すると vcpkg.json 内のライブラリがインストールされる。
ライブラリがインストールされる際に CMakeLists.txt でどのようにライブラリを取り込むかがコンソール出力されるため、
そのコマンドを CMakeLists.txt にコピー＆ペーストする。
今回の場合は以下のようになった。

.. code-block:: cmake

    # ライブラリを探索
    find_package(lyra CONFIG REQUIRED)
    find_package(fmt REQUIRED)
    find_package(Boost REQUIRED COMPONENTS atomic)
    find_package(Catch2 CONFIG REQUIRED)
    find_package(fmt CONFIG REQUIRED)
    find_package(trompeloeil CONFIG REQUIRED)

    # ライブラリをリンク
    target_link_libraries(
        ${PROJECT_NAME} PRIVATE bfg::lyra Boost::atomic Catch2::Catch2 fmt::fmt
                                trompeloeil::trompeloeil)
