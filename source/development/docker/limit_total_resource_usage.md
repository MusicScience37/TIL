# Docker 全体のリソース使用量を制限する

一部の Docker コンテナがホストのメモリを使用しすぎて PC 全体が固まってしまうことがあった。
そのため、Docker 全体のリソース使用量に制約をつける方法を調査した。

## 手順

1. slice の設定ファイルを作成する。

   `/etc/systemd/system/docker_limit.slice` というファイルを作成し、リソース使用量の上限を設定する。

   例えば、メモリ使用量に制約を設けるために、以下のような記述を行う。

   ```ini
   [Unit]
   Description=Slice that limits docker resources
   Before=slices.target

   [Slice]
   MemoryAccounting=true
   MemoryHigh=12G
   MemoryMax=14G
   MemoryMaxSwap=2G
   ```

2. slice のサービスを起動する。

   以下のコマンドを実行する。

   ```bash
   sudo systemctl start docker_limit.slice
   ```

3. Docker が上記の slice を使用するように設定する。

   `/etc/docker/daemon.json` ファイルに以下の設定を追加する。

   ```json
   {
     "cgroup-parent": "docker_limit.slice"
   }
   ```

4. Docker を再起動する。

   以下のコマンドを実行する。

   ```bash
   sudo systemctl restart docker
   ```

## 参考

- [rhel - How to limit Docker total resources? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/537645/how-to-limit-docker-total-resources)
