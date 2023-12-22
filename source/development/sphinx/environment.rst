環境構築
==============

このサイトを作成する際に pip3 でインストールした python パッケージをまとめる。

sphinx
------------

ビルドに必要。

sphinx-autobuild
------------------

Sphinx の自動ビルドができるパッケージ。
pip でインストールすると、
sphinx-autobuild というコマンドがインストールされる。
（ホームディレクトリの .local/bin に入った。）

使用例として、
このサイトを作成しているリポジトリのルートには
今現在次のようなスクリプトが置いてある。

.. literalinclude:: ../../../start_auto_build.sh
    :language: bash
