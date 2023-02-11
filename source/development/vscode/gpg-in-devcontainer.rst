.. _development-vscode-gpg-in-devcontainer:

GPG の鍵を Dev Container 内で使用する
===============================================

Git の gpg 鍵を使用する場合、
`Sharing GPG Keys <https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials#_sharing-gpg-keys>`_
に従って設定が必要になる。

WSL 上の Docker コンテナの場合
----------------------------------------

1. Windows 上への Gpg4win のインストール

   `Gpg4win のホームページ <https://www.gpg4win.org/>`_
   からインストーラをダウンロードして、
   インストーラに沿ってインストールする。

2. WSL 側の必要なソフトウェアのインストール

   ファイル共有元となる WSL のコンソールで、次のコマンドにより socat と gpg をインストールする。

   .. code-block:: console

       $ sudo apt update
       $ sudo apt install socat gpg

   .. note::
       最新のドキュメントでは socat のインストールが不要となっている。。

3. WSL 内の設定

   ファイル共有元となる WSL のコンソールで、次のコマンドを実行する。

   .. code-block:: console

       $ echo pinentry-program /mnt/c/Program\ Files\ \(x86\)/Gpg4win/bin/pinentry.exe > ~/.gnupg/gpg-agent.conf
       $ gpg-connect-agent reloadagent /bye

4. Dev Container のコンテナ内の設定

   使用する Dev Container の Dockerfile などで
   次のようなコマンドで gnupg2 をインストールする。

   .. code-block:: console

       $ apt-get update && apt-get install gnupg2 -y

   .. note::
       参照したドキュメントによると、gpg でなく gnupg2 であることに意味があるようだ。

SSH 接続先の Linux 上の Docker コンテナの場合
------------------------------------------------------

1. Linux ホスト上に必要なソフトウェアのインストール

   ファイル共有元となる WSL のコンソールで、次のコマンドにより gnupg2 をインストールする。

   .. code-block:: console

       $ sudo apt update
       $ sudo apt install gnupg2

2. Dev Container のコンテナ内の設定

   使用する Dev Container の Dockerfile などで
   次のようなコマンドで gnupg2 をインストールする。

   .. code-block:: console

       $ apt-get update && apt-get install gnupg2 -y

   .. note::
       参照したドキュメントによると、gpg でなく gnupg2 であることに意味があるようだ。

gpg のエラー
`````````````````````````

次のようなエラーが出てコミットができないことがあった。

.. code-block:: console

    error: gpg failed to sign the data
    fatal: failed to write commit object

WSL のコンソールを開いて以下のコマンドを実行すると何故か治った。

.. code-block:: console

    $ gpg-connect-agent killagent /bye
    $ gpg-connect-agent /bye
