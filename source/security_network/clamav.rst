ClamAV
===========

`ClamAV <http://www.clamav.net/>`_
はフリーのアンチウイルスツールで、Unix 上でも動作する。
そこで、ここでは Ubuntu 20.04 にインストールした際のコマンドを記載する。

.. note:: 一応、Windows 上でも使えると公式ドキュメントに書いてある。

インストール
---------------

1. インストール

   .. code:: console

       $ sudo apt install clamav clamav-daemon

2. freshclam の確認

   .. code:: console

       $ sudo systemctl start clamav-freshclam.service
       $ sudo systemctl status clamav-freshclam.service
       ● clamav-freshclam.service - ClamAV virus database updater
            Loaded: loaded (/lib/systemd/system/clamav-freshclam.service; enabled; vendor preset: enabled)
            Active: active (running) since Tue 2021-12-28 03:50:41 JST; 10min ago
              Docs: man:freshclam(1)
                    man:freshclam.conf(5)
                    https://www.clamav.net/documents
          Main PID: 473570 (freshclam)
             Tasks: 1 (limit: 18928)
            Memory: 347.2M
            CGroup: /system.slice/clamav-freshclam.service
                    └─473570 /usr/bin/freshclam -d --foreground=true

3. clamd の確認

   .. code:: console

       $ sudo systemctl start clamav-daemon.service
       $ sudo systemctl status clamav-daemon.service
       ● clamav-daemon.service - Clam AntiVirus userspace daemon
            Loaded: loaded (/lib/systemd/system/clamav-daemon.service; enabled; vendor preset: enabled)
           Drop-In: /etc/systemd/system/clamav-daemon.service.d
                    └─extend.conf
            Active: active (running) since Tue 2021-12-28 03:58:08 JST; 1s ago
              Docs: man:clamd(8)
                    man:clamd.conf(5)
                    https://www.clamav.net/documents/
           Process: 477036 ExecStartPre=/bin/mkdir -p /run/clamav (code=exited, status=0/SUCCESS)
           Process: 477037 ExecStartPre=/bin/chown clamav /run/clamav (code=exited, status=0/SUCCESS)
          Main PID: 477038 (clamd)
             Tasks: 1 (limit: 18928)
            Memory: 433.2M
            CGroup: /system.slice/clamav-daemon.service
                    └─477038 /usr/sbin/clamd --foreground=true

除外パスの設定
---------------------

``/etc/clamav/clamd.conf`` に以下を書いておく。

.. code:: text

    ExcludePath ^/boot/
    ExcludePath ^/dev/
    ExcludePath ^/proc/
    ExcludePath ^/sys/

スキャンの実行
---------------------

とりあえず全てスキャンするのであれば、次のようにする。

.. code:: console

    $ sudo clamdscan --multiscan --fdpass --quiet --log="<ログファイルパス>" /

.. note::

    全てスキャンするため時間がかかる上に、
    マルチスレッド（``--multiscan``）のため、
    実行中は重くなる。
