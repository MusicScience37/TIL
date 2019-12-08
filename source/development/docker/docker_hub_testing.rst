Docker Hub でテストまで実行する時の注意点
====================================================

`Docker Hub のテスト機能 <https://docs.docker.com/docker-hub/builds/automated-testing/>`_
で少し戸惑ったポイントをまとめておく。

- テストのファイルは ``.test.yml`` という拡張子にしなければ無視される。
  （``.test.yaml`` でないことに注意。）
- テストのファイルは ``Dockerfile`` と同じディレクトリになければ無視される。
