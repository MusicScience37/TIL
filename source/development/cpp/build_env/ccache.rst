Ccache によるビルド高速化
============================

`Ccache <https://ccache.dev/>`_
は、C/C++ のコンパイル時に生成されるオブジェクトファイルをキャッシュして、
同じ条件によるコンパイルの処理をなくすことにより、
リビルドの時間を短くすることができるツールである。
ソースコードと ``#include`` で読み込まれるヘッダの内容をもとにキャッシュを作るため、
環境を作り直したりしてソースコードやヘッダのタイムスタンプが変化しても、
ファイルの内容自体が変わっていなければキャッシュが使われるようになっている。
そのため、CI における C/C++ のビルドを高速化するのに活用できる。

なお、今回試したコンパイル時間が長い
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
    Docker コンテナや CI 環境で使用する場合は
    タイムスタンプよりもコンパイラのバイナリによる比較を行う ``content`` の方が都合が良い。
    （Docker コンテナを作り直しても、コンパイラが完全に一致すれば同じコンパイラとして扱う。）

CMake への適用
----------------------

CMake でビルドを行う場合、
``CMAKE_C_COMPILER_LAUNCHER``, ``CMAKE_CXX_COMPILER_LAUNCHER``
という 2 つの変数に ``ccache`` コマンドを指定することで、
Ccache を適用できる。

Visual Studio の場合
...........................

GCC, Clang を使用する場合は上記だけで良いが、
Visual Studio を使用する場合は少し工夫が必要となる。
CMake に指定する generator として Visual Studio を指定すると
``CMAKE_C_COMPILER_LAUNCHER``, ``CMAKE_CXX_COMPILER_LAUNCHER``
の設定が無視される。
しかし、以下の例のように Visual Studio のコンパイラの情報を読み込むスクリプトを実行してから
generator として Ninja を指定して cmake コマンドを実行すると設定が反映される
[#footnote-ci-win-example]_ 。

..
    cspell:ignore vcvarsall DSTAT ctest

.. code-block:: bat
    :caption: ci_win.cmd

    call "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat" x86_x64

    cmake .. ^
        -G Ninja ^
        -DCMAKE_CXX_COMPILER_LAUNCHER=ccache ^
        -DCMAKE_TOOLCHAIN_FILE=..\vcpkg\scripts\buildsystems\vcpkg.cmake ^
        -DCMAKE_BUILD_TYPE=Release

    cmake --build . --config Release --parallel

.. caution::
    1 行目の処理は power shell でなくコマンドプロンプトを使用するバッチファイルにおいてしか実行できない。

.. seealso::
    - `GitHub Actionsでccacheを使ってCMake+Microsoft Visual C++のビルドを高速化 - 2022-10-12 - ククログ <https://www.clear-code.com/blog/2022/10/12/ccache-for-msvc-and-cmake-on-github-actions.html>`_
    - `Visual Studio 2019のプロジェクトをGitlab CI/CDで自動ビルド&Google Testでテストしてみた - 情弱の奇妙な冒険 <https://ssssssh.hatenablog.com/entry/2021/08/07/004051>`_
    - `Visual Studio (up to 2019) のコマンドラインでの C/C++ コンパイル環境 #C++ - Qiita <https://qiita.com/softgate/items/b9e04da8f8fc9f180855>`_

.. rubric:: Footnotes

.. [#footnote-speed]
    `numerical-collection-cpp <https://gitlab.com/MusicScience37Projects/numerical-analysis/numerical-collection-cpp>`_
    リポジトリのコミット 1ef7d5fd2be019fe142f2ffe2e939574b6d4118d 時点のソースコードに対して
    4 スレッドの Release ビルドを行ったところ、
    ビルド時間を 377 秒から 9 秒まで削減できた。
    ヘッダオンリーの重いライブラリを使用しているために 1 ファイルごとのコンパイル時間が比較的長く、
    Ccache の効果が得られやすいプロジェクトとなっている。

.. [#footnote-ci-win-example]
    `cpp-stat-bench リポジトリの scripts/ci_win.cmd <https://gitlab.com/MusicScience37Projects/utility-libraries/cpp-stat-bench/-/blob/0ba5074320052a6eae545a654bc63168fc111245/scripts/ci_win.cmd>`_
    より必要な部分のみ引用したもの。
    GitLab CI でこのバッチファイルを ``cmd.exe /C ..\scripts\ci_win.cmd`` のように実行している。
