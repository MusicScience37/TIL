Pybind11 でラッパーを作成する際に Python の共有ライブラリが必要になった
================================================================================

Pybind11 で C++ の関数の Python ラッパーを作成しようとしたところ、
Python のインタプリタに付属するライブラリが
PIC (Position Independent Code) でコンパイルされていないことに対するリンクエラーが発生した。

Python のインストール時に ``--enable-shared`` というフラグを付加することで解決する。

pyenv を使用している場合は次のようにインストールを行う。

.. code-block:: console

    $ PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install -f 3.9.4

``-f`` オプションは元々インストールされているバージョンがあっても無視してインストールするものである。

参考
--------

..
    cspell:ignore Theano

- `TheanoをpyenvでインストールしたPython3.4.2で動かそうとしたら「PICオプションつけて再コンパイルしろよ」と怒られた時にやった対処メモ - Qiita <https://qiita.com/sobeit@github/items/74ae8eb5bfc1c445016a>`_
