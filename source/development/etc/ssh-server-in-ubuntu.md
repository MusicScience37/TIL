# Ubuntu への SSH サーバーの導入

## SSH サーバのインストール

```shell
sudo apt update
sudo apt install openssh-server
```

## SSH のカギの登録

1. 接続先に `~/.ssh/authorized_keys` ファイルを用意する。
2. 以下のコマンドでアクセス権を正しくしておく。

   ```shell
   chmod 600 ~/.ssh/authorized_keys
   ```

3. `~/.ssh/authorized_keys` ファイルに公開鍵を追加する。
