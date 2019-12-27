TeX のインストール
=======================

TeX のインストールでうまくいった手順をメモしておく。

1. インストーラのダウンロード

  .. code-block:: console

    $ wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
    $ tar -xf install-tl-unx.tar.gz
    $ cd install-tl-20191221

2. 一旦基礎的なものだけインストール

  .. code-block:: console

    $ echo "selected_scheme scheme-basic" >> texlive.profile
    $ sudo ./install-tl -profile texlive.profile

3. 全体のインストール

  .. code-block:: console

    $ sudo /usr/local/texlive/2019/bin/x86_64-linux/tlmgr update --self
    $ sudo /usr/local/texlive/2019/bin/x86_64-linux/tlmgr install scheme-full
    $ sudo /usr/local/texlive/2019/bin/x86_64-linux/tlmgr update --all

4. パスの追加

  ``/usr/local/texlive/2019/bin/x86_64-linux`` をパスに入れる。

``install-tl`` は途中で失敗すると全てやり直しになるという酷い仕様のため、
上記のようにアップデートで主に使っている ``tlmgr`` コマンドで
全てのパッケージをダウンロードするようにした方がうまくいった。

.. todo::
    全体のインストールのときに ``sudo`` にうまくパスが引き継げなかった問題の
    解決策を考える。
