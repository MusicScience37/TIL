Ubuntu の apt のリポジトリ
====================================

Ubuntu の apt を使う場合は
`Ubuntu パッケージ検索 <https://packages.ubuntu.com/>`_
でパッケージ名とバージョンを確認する。

これは :ref:`docker/hadolint` の指摘に合わせて
パッケージとバージョンを指定するようにするためのもので、
`sphinx-docker <https://gitlab.com/MusicScience37/sphinx-docker>`_
では次のようにしている。

.. code-block:: Dockerfile

    RUN apt-get update && \
        apt-get install -y --no-install-recommends \
            python3-pip=9.0.1-2.3~ubuntu1.18.04.1 \
            make=4.1-9.1ubuntu1 && \
        apt-get autoremove && \
        apt-get autoclean && \
        rm -r /var/lib/apt/lists/*
