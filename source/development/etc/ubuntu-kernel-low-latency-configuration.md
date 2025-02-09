# Ubuntu 24.04 からのカーネルの低遅延の設定

Ubuntu 24.04 から、カーネルを低遅延にする設定が追加された。
以下のように設定することで、ある程度低遅延の設定でカーネルを実行することができる。
（本格的な低遅延の設定は PREEMPT_RT カーネルをビルドする必要がある。）

1. `/etc/default/grub` ファイルのうち、
   `GRUB_CMDLINE_LINUX_DEFAULT=` の行に
   `preempt=full` を追加する。

   例えば、試した環境では

   ```none
   GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
   ```

   を

   ```none
    GRUB_CMDLINE_LINUX_DEFAULT="quiet splash preempt=full"
   ```

   に変更した。

   ```{note}
   ここで何を追加するかにより、カーネルの遅延や電力消費が変化する。
   他のオプションの例については、
   [Fine-Tuning the Ubuntu 24.04 Kernel for low latency, throughput, and power efficiency - Kernel - Ubuntu Community Hub](https://discourse.ubuntu.com/t/fine-tuning-the-ubuntu-24-04-kernel-for-low-latency-throughput-and-power-efficiency/44834)
   を参照すること。
   上記の例はゲーミングなどの用途に適したものとして紹介されていた。
   ```

2. 設定を反映するため、以下のコマンドを実行する。

   ```shell
   sudo update-grub
   ```

3. PC を再起動する。
