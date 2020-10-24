pyenv
=====================

pyenv で異なる Python のバージョンを自由に使用できるようにする。

環境
--------

Ubuntu 20.04 上でインストールした。

.. note:: 一部の操作は Ubuntu のバージョンによって変更が必要なため注意すること。

インストール手順
------------------

1. 必要なコマンドの準備

   pyenv のインストールや pyenv を使用した Python のインストールに必要なコマンドを準備する。

   .. code:: console

       $ sudo apt install git wget curl

2. Python のインストールに必要なパッケージをインストールするための設定

   ``/etc/apt/sources.list`` ファイルに以下を追記する。

   .. code:: none

       deb-src http://archive.ubuntu.com/ubuntu/ focal-updates main

3. Python のインストールに必要なパッケージの準備

   .. code:: console

       $ sudo apt update
       $ sudo apt build-dep python3.8

   .. note:: マイナーバージョンまで含めなければ、必要なパッケージ全てはインストールされない。

4. ソースコードのクローン

   .. code:: console

       $ git clone https://github.com/pyenv/pyenv.git ~/.pyenv

5. 環境変数の追加

   以下を ``.bashrc`` ファイルへ追記する。

   .. code:: bash

       PYENV_ROOT="${HOME}/.pyenv"
       PATH="${PYENV_ROOT}/bin:${PATH}"
       if command -v pyenv 1>/dev/null 2>&1; then
         eval "$(pyenv init -)"
       fi

   編集後はコンソールを開きなおすなどして ``.bashrc`` を再読み込みする。

使用例
--------

Python 3.9.0 をインストールしてみる。

.. code:: console

    $ pyenv install 3.9.0

Python をソースビルドでインストールする。
ここでしばらく時間がかかる上に、
ソースビルドで必要なライブラリがなければ正しくインストールできない。

インストールしたユーザ全体での python コマンドのバージョンを次のように設定する。

.. code:: console

    $ pyenv global 3.9.0

成功すると、python3 だけでなく python コマンドのバージョンが変わる。

.. code:: console

    $ python --version
    Python 3.9.0
    $ python3 --version
    Python 3.9.0
    $ pip --version
    pip 20.2.3 from /home/kenta/.pyenv/versions/3.9.0/lib/python3.9/site-packages/pip (python 3.9)

参考
------

- `pyenv/pyenv: Simple Python version management <https://github.com/pyenv/pyenv>`_

  - pyenv の公式リポジトリ

- `1. Getting Started — Python Developer's Guide <https://devguide.python.org/setup/>`_

  - Python のソースビルドの方法
