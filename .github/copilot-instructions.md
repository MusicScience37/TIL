# Copilot 向けの指示

## Python パッケージのアップデート

Python パッケージのアップデートは以下のようにします。

1. コンソールでリポジトリのルートディレクトリに移動しておきます。
2. コマンド `poetry update` を実行します。
3. ルートディレクトリの `pyproject.toml` ファイルに記載されている各パッケージについて
   コマンド `poetry add -G <group> <package>@latest` を実行します。
4. 再度 `poetry update` を実行します。
5. ビルドを確認します。

## ビルド

ビルドは以下のようにします。

1. コンソールでリポジトリのルートディレクトリに移動しておきます。
2. コマンド `./build.sh` を実行し、ビルドを行います。
   このときに警告やエラーがないかどうかチェックしておきます。

## HTML のチェック

HTML のチェックは以下のようにします。

1. コンソールでリポジトリのルートディレクトリに移動しておきます。
2. コマンド `htmltest` を実行し、HTML のチェックを実行します。
   このときに警告やエラーがないかどうかチェックしておきます。
