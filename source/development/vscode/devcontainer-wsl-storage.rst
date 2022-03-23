Devcontainer を WSL 内のディレクトリへ適用する
=====================================================

VSCode の Devcontainer を Windows で使用する際に、
Devcontainer と共有されるソースコードは
WSL2 上に置いた方がパフォーマンスが良くなると
公式ドキュメントの
`Improve container performance <https://code.visualstudio.com/remote/advancedcontainers/improve-performance>`_
に書いてある。
しかし、WSL2 上のソースコードを用いて Devcontainer を使用すると
いくつか設定が追加で必要になるため、設定を残しておく。

Docker Desktop におけるファイル共有の設定
-----------------------------------------------------

Docker Desktop で WSL2 上のファイルを共有するには、設定が必要となる。
Docker Desktop の設定を開き、
「Resources」の「WSL INTEGRATION」を開くと、
インストールした distro ごとにファイル共有の有無を切り替えられる。
下の図の例では、Ubuntu が表示されている。

.. image:: devcontainer-wsl-storage-wsl-integration-config.png

Git の SSH 接続の設定
-----------------------

Git のリモートリポジトリを SSH 経由で使用する場合、
`Developing inside a Container using Visual Studio Code Remote Development 内 Using SSH keys <https://code.visualstudio.com/docs/remote/containers#_using-ssh-keys>`_
の内容に従って設定が必要になる。

1. Windows 上の SSH agent の設定

   Windows 上で管理者権限のコンソールを開き、次のコマンドを実行する。

   .. code-block:: console

       > Set-Service ssh-agent -StartupType Automatic
       > Start-Service ssh-agent
       > Get-Service ssh-agent

2. SSH 鍵の登録

   Windows 上のコンソールで、次の形式のコマンドを実行する。

   .. code-block:: console

       > ssh-add <SSHの秘密鍵のファイルパス>

3. WSL 側の設定

   ファイル共有元となる WSL のコンソールで、次のコマンドにより socat をインストールする。

   .. code-block:: console

       $ sudo apt update
       $ sudo apt install socat

Git の gpg 鍵の共有
----------------------------

Git の gpg 鍵を使用する場合、
`Developing inside a Container using Visual Studio Code Remote Development 内 Sharing GPG Keys <https://code.visualstudio.com/docs/remote/containers#_sharing-gpg-keys>`_
に従って設定が必要になる。

1. Windows 上への Gpg4win のインストール

   `Gpg4win のホームページ <https://www.gpg4win.org/>`_
   からインストーラをダウンロードして、
   インストーラに沿ってインストールする。

2. WSL 側の必要なソフトウェアのインストール

   ファイル共有元となる WSL のコンソールで、次のコマンドにより socat と gpg をインストールする。

   .. code-block:: console

       $ sudo apt update
       $ sudo apt install socat gpg

3. WSL 内の設定

   ファイル共有元となる WSL のコンソールで、次のコマンドを実行する。

   .. code-block:: console

       $ echo pinentry-program /mnt/c/Program\ Files\ \(x86\)/Gpg4win/bin/pinentry.exe > ~/.gnupg/gpg-agent.conf
       $ gpg-connect-agent reloadagent /bye

4. Devcontainer のコンテナ内の設定

   使用する Devcontainer の Dockerfile などで
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
