Python の GUI ライブラリ Kivy
===================================

Python の GUI ライブラリ `Kivy <https://kivy.org/>`_ を使用してみた。

基本情報
-----------

- ライセンス: MIT ライセンス
- PyPI リポジトリ上の名前: Kivy

試した時の環境
-----------------

- 日付: 2020/12/31
- OS: Windows 10
- Python: CPython 3.8.6
- インストールする Kivy: Kivy 2.0.0
- リポジトリ: `test-kivy <https://gitlab.com/MusicScience37/test-kivy>`_

インストール
-------------

pip コマンドでのインストールになるが、
どこまでインストールするかは選べる。
（`Installing Kivy — Kivy 2.0.0 documentation <https://kivy.org/doc/stable/gettingstarted/installation.html#installing-kivy-s-dependencies>`_）

- ``kivy[base]``: 基本機能のみ（映像・音声の機能なし）
- ``kivy[media]``: 映像・音声の機能
- ``kivy[full]``: 上記の両方
- ``kivy[dev]``: Kivy を開発用モードで動かすための機能

  - コンパイル用のヘッダ、テストを実行したりドキュメントを生成したりするための全ての依存物。
    （Kivy 自体を開発するためのもの？）

- ``kivy[tuio]``: TUIO というのを動かせるようにする機能

.. todo:: TUIO とは？
