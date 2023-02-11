Dev Container を WSL 内のディレクトリへ適用する
=====================================================

VSCode の Dev Container を Windows で使用する際に、
Dev Container と共有されるソースコードは
WSL2 上に置いた方がパフォーマンスが良くなると
公式ドキュメントの
`Improve container performance <https://code.visualstudio.com/remote/advancedcontainers/improve-performance>`_
に書いてある。
しかし、WSL2 上のソースコードを用いて Dev Container を使用すると
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

:ref:`development-vscode-gpg-in-devcontainer` を参照。
