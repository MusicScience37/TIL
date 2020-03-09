別の PC に立ち上げた Docker デーモンを使いたい
===================================================

普段使いの Windows PC から別の Ubuntu PC 上の Docker デーモンを使えるようにしてみた。

なお、このメモは家のネットワーク内での利用を前提とする。
外部ネットワークを経由して使えるようにするには、相応のセキュリティ対策が必要。
（Docker を自由に使えれば簡単に root ユーザ並みの操作が可能なので…。）

環境
-------

- Ubuntu PC

  - Ubuntu 18.04
  - Docker 19.03.7

- Windows PC

  - Windows 10
  - VSCode の拡張機能 Docker から Ubuntu PC の Docker を使う。

Ubuntu PC 側の設定
------------------------

``/lib/systemd/system/docker.service`` ファイルで

.. code:: none

    ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

と書いてある行を

.. code:: none

    ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:54321 -H fd:// --containerd=/run/containerd/containerd.sock

へ変更する。

これで 54321 ポートへ Docker を公開できる。
（ポート番号は適当に決めたもの。）

VSCode の設定
--------------------

拡張機能 Docker の設定に Host という項目があるため、
その Host の欄に ``tcp://<Ubuntu PC の IP>:54321`` と入力する。

.. note::
    Docker コマンドでは ``DOCKER_HOST`` という環境変数がこの設定にあたるため、
    恐らく ``DOCKER_HOST`` を設定すれば docker コマンドも動くはず。（試してはいない。）

参考
-----------

- `Docker daemon のリファレンス <http://docs.docker.jp/engine/reference/commandline/dockerd.html>`_
