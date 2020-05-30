Asio ライブラリの io_context クラスについて
==================================================

`Asio ライブラリ <https://think-async.com/Asio/>`_
において、非同期処理を行うのに使用する io_context クラスについて、
使ってみて困った点をまとめておく。

勝手に run 関数が終了する
------------------------------

非同期処理を開始させるために、

.. code-block:: cpp

    asio::io_context context;
    // 必要に応じた初期化処理
    context.run();

のような処理を書くが、
イベント処理を行う ``context.run()`` が知らない内に終了し、
何も処理が行われなくなるケースがあった。

これは、仕事がなくなったら run 関数を抜けるという仕様によるもので、
基本的には run 関数を呼ぶ前に最初の非同期処理を初めておくものだった。

なお、何も仕事のない時間でも run 関数を動作させておきたい場合
（依頼された通信を行うクライアントクラスとか）、
run 関数が終わらないようにする ``executor_work_guard`` クラスというのがある。
`公式ドキュメント <https://think-async.com/Asio/asio-1.16.1/doc/asio/reference/io_context.html>`_
の例を参照すると、

.. code-block:: cpp

    asio::io_context io_context;
    asio::executor_work_guard<asio::io_context::executor_type> work
        = asio::make_work_guard(io_context);

のようにすると、``io_context.stop()`` か ``work.reset()`` を実行するまで
「仕事がない」という扱いにはならないと書いてある。
