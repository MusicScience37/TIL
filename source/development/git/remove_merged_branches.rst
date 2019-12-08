マージ済みのブランチを一掃する
=====================================

`A successful Git branching model <https://nvie.com/posts/a-successful-git-branching-model/>`_
を用いていると、feature ブランチが大量に増えていくため、
しばしばマージ済みのブランチを一掃したくなる。

ただし、master とかまで消されるのは（ローカルだけにしても）やめてほしいため、
`Git でマージ済みのブランチを一括削除する <https://qiita.com/kyanny/items/10a57a4f1d2806e3a3b8>`_
を参考に次のようなコマンドを実行することにした。

.. code-block:: console

    $ git branch --merged | grep -vE '^\*|master$|release$|develop$' | xargs -I % git branch -d %
    Deleted branch doc/version_of_sphinx (was ba96fad).
    Deleted branch feat/documents (was f2ce680).
    Deleted branch feat/documents_with_master_info (was f6cb737).
    Deleted branch feat/first_dockerfile (was 15d5ffa).
    Deleted branch fix/location_of_test_yml (was 304049b).

実行例はこのメモを書いた日の
`sphinx-docker <https://gitlab.com/MusicScience37/sphinx-docker>`_
のローカルリポジトリでのもの。
