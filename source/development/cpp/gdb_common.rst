GDB でよく使っているコマンド
===================================

GDB でよく使っているコマンドをまとめておく。

全スレッドのバックトレースの確認
--------------------------------------

GDB でバックトレースを確認する際、
問題のあったスレッド以外の状況も確認したいことがある。
そのような場合は以下のコマンドを使用する。

.. code-block:: console

    (gdb) thread apply all bt

GDB 起動時に待機せずすぐ実行を開始する
-----------------------------------------

GDB を起動するとプログラムを実行せずに待機するが、
待たずに実行して欲しい場合は、次のように GDB を起動する。

.. code-block:: console

    $ gdb -ex run <command>

screen コマンド内で GDB を起動する
------------------------------------

バックグラウンドで起動するコマンドに GDB を適用する場合、
次のように起動コマンドを変更することで
screen コマンドのシェルの中で GDB を起動することができる。

.. code-block:: console

    $ screen -d -m gdb <command>

参考
------------

- `multithreading - How do I get the backtrace for all the threads in GDB? - Stack Overflow <https://stackoverflow.com/questions/18391808/how-do-i-get-the-backtrace-for-all-the-threads-in-gdb>`_
- `roslaunch/Tutorials/Roslaunch Nodes in Valgrind or GDB - ROS Wiki <http://wiki.ros.org/roslaunch/Tutorials/Roslaunch%20Nodes%20in%20Valgrind%20or%20GDB>`_
