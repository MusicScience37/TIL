# DevContainer を root でないユーザで起動する

VSCode の DevContainer でコンテナ上のユーザを root にしていると、
ホスト OS 上とコンテナ内とで使用するユーザ名が異なることにより、
ファイルの権限に関する問題がしばしば発生する。
そこで、コンテナ内でもホスト上と同じユーザを使用できるようにする方法が
VSCode 公式ドキュメントの
[Add a non-root user to a container](https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user)
に紹介されている。

## 概要

ファイルの権限はユーザ名でなく UID によって管理されているため、
ホスト上と UID が同じユーザを DevContainer のコンテナ上に用意し、
そのユーザで作業をするようにすれば良い。

## 手順

### 1. Docker イメージに作業用のユーザを用意する

DevContainer を root でないユーザで起動するには、
まず使用する Docker イメージ内に root でない作業用のユーザを 1 つ用意しておく必要がある。
Docker イメージの中には最初から root でないユーザが UID 1000 で用意されていることがあるため、
`cat /etc/passwd` コマンドなどでユーザの一覧を確認しておく。
例えば、Docker Hub の ubuntu の Docker イメージでは
UID 1000 の「ubuntu」ユーザが用意されている。

ユーザがない場合は以下のように追加する。

```Dockerfile
ARG USERNAME=vscode # ユーザ名。必要に応じて変更する。
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
```

### 2. Docker イメージ内に sudo コマンドを用意する

DevContainer で作業中にソフトウェアのインストールなどで root ユーザの権限が必要になる場合がある。
しかし、Docker イメージの中には sudo コマンドがインストールされていないことがよくある。
そこで、sudo コマンドを必要に応じてインストールしておく。

````{hint}
Ubuntu であれば以下のような Dockerfile の記述で sudo コマンドがインストールできる。

```Dockerfile
RUN apt-get update && \
    # sudo コマンドのインストール
    apt-get install -y sudo && \
    # 作業用のユーザで sudo コマンドが使用できるようにする。
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME
```
````

### 3. root ユーザでしか使えないツールがないか確認する

root ユーザで使用する前提でインストールしたツールが
root でないユーザでは使用できないことがあるため、
必要に応じて作業用のユーザでも使用できるように追加のインストール処理を行う。

````{note}
このサイトを作成しているリポジトリでは、
Python の環境を管理する pyenv と poetry を作業用のユーザでも使えるように
Dockerfile を調整する必要があった。

```Dockerfile
# pyenv を root ユーザ以外からでも使用できるように権限を変更
RUN chmod 0777 /root && \
    chmod -R 0777 /root/.pyenv

# poetry を作業用の ubuntu ユーザにもインストールしておく。
USER ubuntu
WORKDIR /home/ubuntu
ENV PATH="/home/ubuntu/.local/bin:$PATH"
RUN pipx install poetry

```
````

### 4. DevContainer の設定で作業用のユーザ名を指定する

DevContainer を使用するリポジトリの `.devcontainer/devcontainer.json` ファイルで
以下のようにコンテナ内で使用するユーザ名を設定する。

```json
{
  // Docker イメージ内に用意した作業用のユーザ名を指定する。
  "remoteUser": "ubuntu"
  // （その他既存の設定はそのまま）
}
```
