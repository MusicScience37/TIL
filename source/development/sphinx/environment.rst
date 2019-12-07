環境構築
==============

このページを作成する際に pip3 でインストールした python パッケージをまとめる。

sphinx
------------

ページのビルドに必要。

sphinx-autobuild
------------------

Sphinx の自動ビルドができるパッケージ。
pip でインストールすると、
sphinx-autobuild というコマンドがインストールされる。
（ホームディレクトリの .local/bin に入った。）

使用例として、
このページを書いているリポジトリのルートには
今現在次のようなスクリプトが置いてある。

.. literalinclude:: ../../../start_auto_build.sh
    :language: bash
