TeX のインストール
=======================

TeX のインストールでうまくいった手順をメモしておく。

.. caution::
    2019 年頃の古い情報のため、現在もこの方法でインストールできるかどうかは不明。
    現在は
    `Island of TeX の texlive リポジトリ <https://gitlab.com/islandoftex/images/texlive>`_
    にて管理されている Docker イメージを利用して TeXLive の環境を構築している。

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

``install-tl`` は途中で失敗すると全てやり直しになるという仕様のため、
上記のようにアップデートで主に使っている ``tlmgr`` コマンドで
全てのパッケージをダウンロードするようにした方がうまくいった。
