.. _development-cpp-clangd:

Clangd の利用
================

`Clangd <https://clangd.llvm.org/>`_ は C++ の解析を行い、
エディタにおける

- 補完
- エラー検知
- 定義への移動

などを行えるようにする言語サーバ。

インストール
----------------

Ubuntu の場合、``apt install clangd`` とすれば簡単にインストールできる。

ただし、Clangd 11 でなければ
``#include`` の補間ができないと
Issue `Better include autocomplete <https://github.com/clangd/vscode-clangd/issues/46>`_
に書いてあったため、今回は
`LLVM のダウンロードページ <https://releases.llvm.org/download.html>`_
から LLVM 11.0.0 をダウンロードしてパスを通すことで使用できるようにした。

Visual Studio Code での利用
--------------------------------

Visual Studio Code で Clangd を利用するには、
拡張機能
`clangd (llvm-vs-code-extensions.vscode-clangd) <https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.vscode-clangd>`_
をインストールする。
拡張機能
`C/C++ (ms-vscode.cpptools) <https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools>`_
をインストールしている場合は、
競合しないようにオフにしておくこと。

また、Clangd が正しく動作するためにはインクルードディレクトリが分かるようにする必要がある。
`Clangd 公式の利用方法 <https://clangd.llvm.org/installation.html>`_ では、
以下の方法が示されている。

- compile\_commands.json を使用する方法

  - compile\_commands.json は名前の通りコンパイル時に使用するコマンドを書く。
  - CMake では ``CMAKE_EXPORT_COMPILE_COMMANDS`` 変数を ON にすれば出力される。
  - 拡張機能 C/C++ や、
    `Clang-Tidy <https://clang.llvm.org/extra/clang-tidy/>`_ でも
    このファイルを利用している。

- compile\_flags.txt を使用する方法

  - compile\_flags.txt は名前の通りコンパイル時にコンパイラに使用するフラグを書く。
    インクルードディレクトリの指定（``-I``）は最低限必要。

今回は、CMake を使用しているため、
前者の compile\_commands.json を使用した。

Visual Studio Code のワーキングディレクトリの設定ファイル（``.vscode/settings.json``）に
次のような項目を追加することで、
Clangd のコマンドへ渡す引数を設定する。

.. code:: json

    {
      "clangd.arguments": [
        "--compile-commands-dir=${workspaceFolder}/build/Debug",
        "--header-insertion=never"
      ]
    }

- ``--compile-commands-dir`` で compile\_commands.json ファイルがあるディレクトリを示す。
  ワーキングディレクトリ直下に compile\_commands.json があればこのオプションは不要。
- ``--header-insertion`` は自動で ``#include`` を追加する機能の設定。
  この機能を有効にすると、外部ライブラリを使用するソースコードを実装している際に、
  ユーザがインクルードする想定ではない内部実装のヘッダを勝手にインクルードする
  （たとえユーザ向けのヘッダを既にインクルードしていても、
  その行を消してライブラリ内部のヘッダへ変更する）という問題があり、
  今のところ無効にしている。

.. note::
    ``--header-insertion`` で使用される include-what-you-use の利点については
    `Include What You Use - Fluent C++ <https://www.fluentcpp.com/2021/01/01/include-what-you-use/>`_
    などを参照。
    実装中でなく、リファクタリングのときに使うのであれば、便利なツールだと思う。

ここまで設定が終われば、あとは C++ のソースコードを開くことで自動的に Clangd が動作し始める。

初回（プロジェクトにつき 1 回）はインデックスの作成が行われるため、多少待つ必要がある。

感想
----------

- インデックスが有効なようで、ヘッダが重いプロジェクトでも結構速く動作した。
- 関数の上にポインタを持って行った時に出てくる情報で、
  パラメータや戻り値の型を教えてくれるのは便利。
- Doxygen のコメントはまだ理解してくれない模様。
  （最近作られたばかりの Issue：`Doxygen parsing missing <https://github.com/clangd/clangd/issues/529>`_）
- Clang-Tidy のチェックが素の clang-tidy コマンドよりも速く動作している印象。
  （clang-tidy コマンドでも活用できないのだろうか…。）
- `Clang-Format <https://clang.llvm.org/docs/ClangFormat.html>`_
  によるフォーマットも行ってくれる。
  （拡張機能
  `Clang-Format (xaver.clang-format) <https://marketplace.visualstudio.com/items?itemName=xaver.clang-format>`_
  よりも速い？）
