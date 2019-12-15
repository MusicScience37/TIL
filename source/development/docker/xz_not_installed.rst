xz がインストールされていない場合
====================================

Docker で使う OS は普通入っているようなものさえも入っていないため、
tar で ``.tar.xz`` 拡張子のファイルを展開すると、
次のようなエラーが表示された。

.. code-block:: console

    tar (child): xz: Cannot exec: No such file or directory

これは、
`xz-utils <https://packages.ubuntu.com/bionic/xz-utils>`_
パッケージをインストールしたら直った。
