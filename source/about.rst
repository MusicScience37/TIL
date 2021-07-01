本ページについて
====================

TIL (Today I Learned) は「今日学んだこと」という名前の通り、
学んだことを書きためていくもので、GitHub 上で広がっているという。

- `Githubのリポジトリ「TIL」を使って小さなアウトプットを習慣化する - Qiita <https://qiita.com/nemui_/items/239335b4ed0c3c797add>`_
- `GithubでTILというリポジトリが流行りつつあるのかもしれない - 生涯未熟 <https://syossan.hateblo.jp/entry/2016/02/16/144305>`_

.. note::

    2021/7/1 時点で「Today I Learned」で GitHub 上を検索したところ、6145 件ヒットした。

実際に、TIL を通して自分が困って調べたことをまとめて書いておくことで、
再び同じ問題にぶつかったときに調べ直さなくて良くなる効果がある。

運用
-----------

.. uml::

    !include <logos/docker.puml>
    !include <logos/gitlab.puml>

    cloud "<$docker>\nDocker Hub" as hub {
        node "musicscience37/sphinx-doxygen image" as ci_image
    }

    cloud "<$gitlab>\nGitLab.com" as gitlab {
        database "til repository" as repo
        component "GitLab CI" as ci
        database "GitLab Pages\nhttps://musicscience37.gitlab.io/til/" as pages

        repo --> ci : 読み込み
        ci_image --> ci : 読み込み
        ci --> pages : 出力
    }

    node "DNS\nmusicscience37.com" as dns
    dns -up-> pages : til.musicscience37.com CNAME MusicScience37.gitlab.io.
    note right of dns : https://til.musicscience37.com/ \nで TIL にアクセスできるように設定

ルール
---------

- ビルドが通る状態で master にコミットする。
- sphinx の設定は一旦ブランチを切って作業して結果を確認してからマージする。

ライセンス
------------------------

.. image:: https://i.creativecommons.org/l/by/4.0/88x31.png
    :alt: クリエイティブ・コモンズ・ライセンス
    :target: http://creativecommons.org/licenses/by/4.0/

本ページは
`クリエイティブ・コモンズ 表示 4.0 国際 ライセンス <http://creativecommons.org/licenses/by/4.0/>`_
の下に提供されています。
