.. _development-python-aiohttp:

aiohttp
=============

`aiohttp <https://docs.aiohttp.org/en/stable/>`_
は Python の
`asyncio <https://docs.python.org/3/library/asyncio.html>`_
の機能を利用して非同期に HTTP のクライアントとサーバを実装するためのライブラリ。

細かい説明は上記のリンクの公式ドキュメントがしっかりしているため、
どのように使えるか試してみた例を示しておく。

クライアントの例
-----------------------

.. code:: python

    import asyncio

    import aiohttp


    async def async_request() -> datetime.timedelta:
        # セッションの開始
        # セッションは同じサーバへアクセスするクライアントについて 1 つだけ用意する。
        async with aiohttp.ClientSession() as session:
            # HTTP リクエスト（他に post, put, delete, head, options, patch がある。）
            async with session.get("http://localhost:8080") as response:
                # データの取得も非同期になっており、ストリーミングで取得することもできる。
                text = await response.text()
                assert text

非同期処理を行うため ``async``, ``await`` を適切に配置する必要はあるが、簡単に書けている。

サーバの例
---------------

.. code:: python

    from aiohttp import web


    # リクエストを処理する関数を用意しておく。
    async def handle(_: web.Request) -> web.Response:
        # リクエストを引数に受け取り、レスポンスを返す。
        return web.Response(text="Hello world")


    # Application オブジェクトを構築してサーバの処理を開始させる。
    def main():
        app = web.Application()
        app.add_routes([web.get("/", handle)])
        web.run_app(app)


    if __name__ == "__main__":
        main()

HTTP 通信が目的のライブラリのため、
`Django <https://docs.djangoproject.com/>`_
のように機能が豊富なフレームワークにはなっていないが、
`Flask <https://flask.palletsprojects.com/>`_
のようにライブラリを追加していくことで機能を追加できる。
追加のライブラリについては
`Third-Party libraries — aiohttp 3.8.1 documentation <https://docs.aiohttp.org/en/stable/third_party.html>`_
を参照。

パフォーマンス
---------------

非同期処理の利点は複数のリクエストを並行して処理した際のパフォーマンスにあるため、
クライアントの数を変えながら処理時間を計測してみた。

ソースコード
...............

`bench-python-async-http リポジトリ <https://gitlab.com/MusicScience37/bench-python-async-http>`
の
`async_hello_world_server.py <https://gitlab.com/MusicScience37/bench-python-async-http/-/blob/6db276ce070c64a2052065403f7d52f71c05a115/bench_python_async_http/async_hello_world_server.py>`_
でサーバを起動し、
`mp_bench_client.py <https://gitlab.com/MusicScience37/bench-python-async-http/-/blob/6db276ce070c64a2052065403f7d52f71c05a115/bench_python_async_http/mp_bench_client.py>`_
で複数プロセスのクライアントからリクエストを行って時間を計測した。

実行結果
...............

.. csv-table:: ベンチマーク結果
    :header: クライアント数, 1000 リクエストにかかった平均時間 [sec.]
    :widths: auto

    1, 0.464
    2, 0.413
    3, 0.526
    4, 0.719
    5, 0.821
    6, 0.952
    7, 1.071
    8, 1.227

同期でリクエストを処理していれば他のクライアントを待つために
処理時間がクライアント数に比例して増えるが、
I/O が並行で行えるためクライアント数の増加に対する処理時間の増加が抑えられている。
