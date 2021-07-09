pre-commit
==================

`pre-commit <https://pre-commit.com/>`_
は Git のコミット前に自動でチェックを行うためのフレームワーク。

インストール
------------------

.. code-block:: console

    $ pip install pre-commit

設定ファイルの作成
---------------------------------

リポジトリのルートディレクトリに ``.pre-commit-config.yaml`` というファイル名で
設定ファイルを配置しておく必要がある。

サンプルの設定ファイルを生成するには次のコマンドを実行する。

.. code-block:: console

    $ pre-commit sample-config > .pre-commit-config.yaml

コマンドを実行すると次のように設定ファイルが生成される。

.. code-block:: yaml

    # See https://pre-commit.com for more information
    # See https://pre-commit.com/hooks.html for more hooks
    repos:
    -   repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v3.2.0
        hooks:
        -   id: trailing-whitespace
        -   id: end-of-file-fixer
        -   id: check-yaml
        -   id: check-added-large-files

hooks の項目を追加していくことで様々なチェックを行うことができる。
公式の `Supported hooks <https://pre-commit.com/hooks.html>`_ のページを見ると、
かなりの数の hook が用意されいることが分かる。

Git への登録
---------------

次のコマンドを実行すると pre-commit で登録した hook がコミット前に実行されるようになる。

.. code-block:: console

    $ pre-commit install

動作例を以下に示す。

.. code-block:: console

    $ git commit -m "test"
    [WARNING] Unstaged files detected.
    [INFO] Stashing unstaged files to /home/<user>/.cache/pre-commit/patch1625801172-570995.
    Trim Trailing Whitespace.................................................Failed
    - hook id: trailing-whitespace
    - exit code: 1
    - files were modified by this hook

    Fixing NOTICE.txt

    Fix End of Files.........................................................Passed
    Check Yaml...........................................(no files to check)Skipped
    Check for added large files..............................................Passed
    [INFO] Restored changes from /home/<user>/.cache/pre-commit/patch1625801172-570995.

設定ファイルに記述したチェック項目で違反があればコミットに失敗する。

簡単に修正できるようなものについては自動で修正されるが、
Git のステージへの追加まではされない。
ユーザが問題ないか確認したあとステージし、
改めてコミットを行うという流れになる。

全てのファイルへの適用
------------------------------

設定を作成・更新したときや、CI でチェックを行いたい場合などには、
次のようなコマンドで全てのファイルに対するチェックを行うことができる。

.. code-block:: console

    $ pre-commit run --all-files

このページを書いた際に、このページを作成しているリポジトリに適用してみた結果、
以下のように自動で修正が行われた。

.. code-block:: console

    $ pre-commit run --all-files
    Trim Trailing Whitespace.................................................Failed
    - hook id: trailing-whitespace
    - exit code: 1
    - files were modified by this hook

    Fixing source/development/python/pipenv.rst

    Fix End of Files.........................................................Failed
    - hook id: end-of-file-fixer
    - exit code: 1
    - files were modified by this hook

    Fixing source/development/tools_and_libs.csv
    Fixing source/KIcon/LICENSE.txt
    Fixing NOTICE.txt
    Fixing .gitignore
    Fixing source/development/cpp/pybind11/require_python_shared.rst
    Fixing LICENSE.txt
    Fixing source/KIcon/NOTICE.txt

    Check Yaml...............................................................Passed
    Check for added large files..............................................Passed
    $ echo $?
    1

修正時は終了ステータスが 1 になるため、
上記のコマンドは CI のチェックにも使える。
