本ページについて
====================

TIL (Today I Learned) は「今日学んだこと」という名前の通り、
学んだことを書きためていくもので、GitHub 上で広がっているという。

- `Githubのリポジトリ「TIL」を使って小さなアウトプットを習慣化する - Qiita <https://qiita.com/nemui_/items/239335b4ed0c3c797add>`_
- `GithubでTILというリポジトリが流行りつつあるのかもしれない - 生涯未熟 <https://syossan.hateblo.jp/entry/2016/02/16/144305>`_

.. note::

    2021/7/1 時点で「Today I Learned」で GitHub 上を検索したところ、6145 件ヒットした。

TIL を通して自分が困って調べたことをまとめて書いておくことで、
再び同じ問題にぶつかったときに調べ直さなくて良くなる効果がある。

文書の形式としては、比較的簡単に書ける Markdown を使用することが多いようである。

運用
-----------

.. uml::

    !include <logos/docker.puml>
    !include <logos/gitlab.puml>

    cloud "<$docker>\nDocker Hub" as hub {
        node "musicscience37/sphinx-doxygen image" as ci_image
    }

    cloud "<$gitlab>\nGitLab.com" as gitlab {
        database "TIL repository" as repo
        component "GitLab CI" as ci
        database "GitLab Pages" as pages

        repo --> ci : 読み込み
        ci_image --> ci : 読み込み
        ci --> pages : 出力
    }

    note right of pages : https://musicscience37.gitlab.io/til/\nでアクセス

    node "DNS\nmusicscience37.com" as dns
    dns -up-> pages : til.musicscience37.com CNAME MusicScience37.gitlab.io.
    note right of dns : https://til.musicscience37.com/\nで TIL へアクセスできるように設定

リポジトリ
~~~~~~~~~~~~~~

- `GitLab の TIL リポジトリ <https://gitlab.com/MusicScience37/til>`_
  （作業用）
- `GitHub の TIL リポジトリ <https://github.com/MusicScience37/TIL>`_
  （ミラー）

主なツール
-----------------

- `Sphinx <https://www.sphinx-doc.org/en/master/>`_

  - Restructured Text の形式で書いた文章を HTML, CSS, Javascript へ変換する。
  - ただ Markdown を書く場合に比べて環境構築は多少手間がかかるが、
    環境構築後はテキストの文章を書くだけで見た目の整ったページを作ることができ、
    数式や UML を挿入することもできる。

- `Pipenv <https://pipenv.pypa.io/en/latest/>`_

  - Python の仮想環境を管理するツール。
  - Python パッケージのバージョンを作業環境と CI 環境で揃えるために使用する。

ルール
---------

- ビルドが通る状態で master にコミットする。
- Sphinx の設定は一旦ブランチを切って作業を行い、CI で結果を確認してからマージする。

ライセンス
------------------------

.. image:: https://i.creativecommons.org/l/by/4.0/88x31.png
    :alt: クリエイティブ・コモンズ・ライセンス
    :target: http://creativecommons.org/licenses/by/4.0/

本ページは
`クリエイティブ・コモンズ 表示 4.0 国際 ライセンス <http://creativecommons.org/licenses/by/4.0/>`_
の下に提供されています。
