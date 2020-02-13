ファイルの多いディレクトリを開いたときのエラーについて
============================================================

`VSCode のドキュメント <https://code.visualstudio.com/docs/setup/linux#_visual-studio-code-is-unable-to-watch-for-file-changes-in-this-large-workspace-error-enospc>`_
によると、
ファイルの多いディレクトリを開いてエラーが表示される場合は、
次の操作をすれば良い。

1. ``/etc/sysctl.conf`` に

  .. code:: none

      fs.inotify.max_user_watches=524288

  と書き加える。

2. 次のコマンドを実行する。

  .. code:: bash

      sudo sysctl -p

これで、ユーザのプロセスが同時に確認できるファイルの数が増え、
EXPLORER の画面の表示の自動更新がしやすくなるという。
