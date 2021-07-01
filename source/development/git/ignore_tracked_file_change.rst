Git でバージョン管理の対象としたファイルの差分を無視する
=================================================================

Git でバージョン管理の対象としたファイルでも、
差分を無視したいケースがたまにある。
（そのような事態にならないようにするのが一番だが。）

ファイルの差分を無視するには次のようなコマンドを実行する。

.. code-block:: console

    $ git update-index --assume-unchanged <file>

元に戻すには次のようなコマンドを実行する。

.. code-block:: console

    $ git update-index --no-assume-unchanged <file>
