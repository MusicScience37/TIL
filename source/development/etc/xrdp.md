# Ubuntu における xrdp の設定

Ubuntu 24.04 で xrdp の設定をしたときの手順を残しておく。

## 標準のリモートデスクトップを無効化

Ubuntu 24.04 では標準で GNOME Remote Desktop がインストールされており、RDP ポート (3389) を使用している。
xrdp を使用するためには、これを無効化する必要がある。
以下のコマンドを実行する。

```bash
sudo systemctl stop gnome-remote-desktop
sudo systemctl disable gnome-remote-desktop
gsettings set org.gnome.desktop.remote-desktop.rdp enable false
gsettings set org.gnome.desktop.remote-desktop.vnc enable false
```

以下のコマンドでポートが解放されていることを確認する。
解放されていれば何も出力されない。

```bash
sudo lsof -i:3389
```

## インストール

以下のコマンドで xrdp をインストールする。

```bash
sudo apt install xrdp
```

xrdp のサービスが起動していることを確認する。

```bash
sudo systemctl status xrdp
```

## Wayland の無効化

最新の Ubuntu に採用されている Wayland を無効化しないと xrdp でログインできない場合がある。
`/etc/gdm3/custom.conf` において、以下の設定を行う。

```ini
[daemon]
WaylandEnable=false
```

## GNOME の設定

xrdp で GNOME を使用するため、`/etc/xrdp/startwm.sh` の冒頭に以下の内容を追加する。

```bash
export GNOME_SHELL_SESSION_MODE=ubuntu
export XDG_CURRENT_DESKTOP=ubuntu:GNOME
```

## 証明書の設定

xrdp が TLS 接続できるようにするため、以下のコマンドで権限を追加する。

```bash
sudo adduser xrdp ssl-cert
```

## ログイン時の認証の抑制

xrdp でログインした後何度もパスワードを求められることを防ぐため、
`/etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla`
というファイルを作成し、以下の内容を記述する。

```ini
[Allow Colord all Users]
Identity=unix-user:*
Action=org.freedesktop.color-manager.create-device;org.freedesktop.color-manager.create-profile;org.freedesktop.color-manager.delete-device;org.freedesktop.color-manager.delete-profile;org.freedesktop.color-manager.modify-device;org.freedesktop.color-manager.modify-profile
ResultAny=no
ResultInactive=no
ResultActive=yes
```

最後に、ここまでの設定を反映するため、再起動しておく。

## 参考にしたページ

- [Ubuntu 20.04 に xrdp を入れてリモートデスクトップできるようにする #Linux - Qiita](https://qiita.com/hoto17296/items/0e3e5bd407351fd2e6ca)
- [開発メモ その417 Ubuntu 24.04 でXRDPを使う · A certain engineer "COMPLEX"](https://taktak.jp/2025/02/22/4524/)
