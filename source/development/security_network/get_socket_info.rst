使用中のソケットの情報を見る
============================

Ubuntu の iproute2 パッケージに入っている ss コマンドを使用すると、
使用中のソケットを表示することができる。

..
    cspell:disable

.. code-block:: console

    $ ss -tlnp
    State      Recv-Q      Send-Q             Local Address:Port              Peer Address:Port
    LISTEN     0           128                      0.0.0.0:8888                   0.0.0.0:*          users:(("sphinx-autobuil",pid=17856,fd=7))

..
    cspell:enable

例はこのページを書いているリポジトリの
`start_auto_build.sh` コマンドを動作させたときのもの。

上記のコマンドのオプションはそれぞれ

- ``-t``: TCP のソケットを表示
- ``-l``: listen しているソケットのみ表示
- ``-n``: サービスの種別の名前でなくポート番号を表示
- ``-p``: 使用しているプロセスを表示

となっている。
その他のオプションは
`man ページ <https://www.man7.org/linux/man-pages//man8/ss.8.html>`_
を参照すること。
