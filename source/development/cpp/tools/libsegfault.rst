libSegFault.so
==================

libSegFault.so は
プロセスが Segmentation Fault で終わった際にスタックトレースを表示するライブラリ。
GDB に比べるとスタックトレースで関数名を表示するのに追加の作業が必要になって手間がかかるが、
シグナルハンドラを利用して動作するという仕組みで、
Segmentation Fault しない限りは何も処理を行わないため、
GDB 経由では発生しなくなってしまうバグも再現してスタックトレースを取ることができるという利点がある。

Ubuntu 上でのインストール
------------------------------

Ubuntu では apt のパッケージ gcc の依存パッケージの一部としてインストールされる。

.. note::

    Ubuntu 20.04 では、
    apt の gcc パッケージの依存パッケージに gcc-9 があり、
    gcc-9 の依存パッケージに libc6 があり、
    libc6 内に ``/lib/x86_64-linux-gnu/libSegFault.so`` がある。

    Ubuntu 22.04 では apt の glibc-tools パッケージ内に
    ``/usr/lib/x86_64-linux-gnu/libSegFault.so``
    がある。

実験
----------

次のような明らかに Segmentation Fault になる C++ のプログラムを用意する。

.. code-block:: cpp

    void test(int* a) {
        *a = 0;
    }

    int main() {
        test(nullptr);
    }

これをデバッグ用にビルドする。

.. code-block:: console

    $ g++ -g test.cpp -o test

これを普通に実行すると、次のようになる。

.. code-block:: console

    $ ./test
    Segmentation fault (core dumped)

libSegFault.so をロードするようにすると、次のようになる。

..
    cspell:disable

.. code-block:: console

    $ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libSegFault.so ./test
    *** signal 11
    Register dump:

     RAX: 0000000000000000   RBX: 0000000000000000   RCX: 000056489f19ddf8
     RDX: 00007ffdd6090f28   RSI: 00007ffdd6090f18   RDI: 0000000000000000
     RBP: 00007ffdd6090df0   R8 : 00007f3ed341af10   R9 : 00007f3ed3609040
     R10: 00007f3ed3603908   R11: 00007f3ed361e6c0   R12: 00007ffdd6090f18
     R13: 000056489f19b142   R14: 000056489f19ddf8   R15: 00007f3ed363d040
     RSP: 00007ffdd6090df0

     RIP: 000056489f19b139   EFLAGS: 00010246

     CS: 0033   FS: 0000   GS: 0000

     Trap: 0000000e   Error: 00000006   OldMask: 00000000   CR2: 00000000

     FPUCW: 0000037f   FPUSW: 00000000   TAG: 00000000
     RIP: 00000000   RDP: 00000000

     ST(0) 0000 0000000000000000   ST(1) 0000 0000000000000000
     ST(2) 0000 0000000000000000   ST(3) 0000 0000000000000000
     ST(4) 0000 0000000000000000   ST(5) 0000 0000000000000000
     ST(6) 0000 0000000000000000   ST(7) 0000 0000000000000000
     mxcsr: 1f80
     XMM0:  00000000000000000000000000000000 XMM1:  00000000000000000000000000000000
     XMM2:  00000000000000000000000000000000 XMM3:  00000000000000000000000000000000
     XMM4:  00000000000000000000000000000000 XMM5:  00000000000000000000000000000000
     XMM6:  00000000000000000000000000000000 XMM7:  00000000000000000000000000000000
     XMM8:  00000000000000000000000000000000 XMM9:  00000000000000000000000000000000
     XMM10: 00000000000000000000000000000000 XMM11: 00000000000000000000000000000000
     XMM12: 00000000000000000000000000000000 XMM13: 00000000000000000000000000000000
     XMM14: 00000000000000000000000000000000 XMM15: 00000000000000000000000000000000

    Backtrace:
    ./test(+0x1139)[0x56489f19b139]
    ./test(+0x1154)[0x56489f19b154]
    /lib/x86_64-linux-gnu/libc.so.6(+0x29d90)[0x7f3ed3229d90]
    /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0x80)[0x7f3ed3229e40]
    ./test(+0x1065)[0x56489f19b065]

    Memory map:

    56489f19a000-56489f19b000 r--p 00000000 08:02 7080907                    /home/user/test
    56489f19b000-56489f19c000 r-xp 00001000 08:02 7080907                    /home/user/test
    56489f19c000-56489f19d000 r--p 00002000 08:02 7080907                    /home/user/test
    56489f19d000-56489f19e000 r--p 00002000 08:02 7080907                    /home/user/test
    56489f19e000-56489f19f000 rw-p 00003000 08:02 7080907                    /home/user/test
    5648a0e4d000-5648a0e6e000 rw-p 00000000 00:00 0                          [heap]
    7f3ed3200000-7f3ed3228000 r--p 00000000 08:02 3541339                    /usr/lib/x86_64-linux-gnu/libc.so.6
    7f3ed3228000-7f3ed33bd000 r-xp 00028000 08:02 3541339                    /usr/lib/x86_64-linux-gnu/libc.so.6
    7f3ed33bd000-7f3ed3415000 r--p 001bd000 08:02 3541339                    /usr/lib/x86_64-linux-gnu/libc.so.6
    7f3ed3415000-7f3ed3419000 r--p 00214000 08:02 3541339                    /usr/lib/x86_64-linux-gnu/libc.so.6
    7f3ed3419000-7f3ed341b000 rw-p 00218000 08:02 3541339                    /usr/lib/x86_64-linux-gnu/libc.so.6
    7f3ed341b000-7f3ed3428000 rw-p 00000000 00:00 0
    7f3ed35c7000-7f3ed35ca000 r--p 00000000 08:02 3541592                    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7f3ed35ca000-7f3ed35e1000 r-xp 00003000 08:02 3541592                    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7f3ed35e1000-7f3ed35e5000 r--p 0001a000 08:02 3541592                    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7f3ed35e5000-7f3ed35e6000 r--p 0001d000 08:02 3541592                    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7f3ed35e6000-7f3ed35e7000 rw-p 0001e000 08:02 3541592                    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7f3ed35e7000-7f3ed35ea000 rw-p 00000000 00:00 0
    7f3ed35fa000-7f3ed35fb000 r--p 00000000 08:02 3540104                    /usr/lib/x86_64-linux-gnu/libSegFault.so
    7f3ed35fb000-7f3ed35fe000 r-xp 00001000 08:02 3540104                    /usr/lib/x86_64-linux-gnu/libSegFault.so
    7f3ed35fe000-7f3ed35ff000 r--p 00004000 08:02 3540104                    /usr/lib/x86_64-linux-gnu/libSegFault.so
    7f3ed35ff000-7f3ed3600000 r--p 00005000 08:02 3540104                    /usr/lib/x86_64-linux-gnu/libSegFault.so
    7f3ed3600000-7f3ed3601000 rw-p 00006000 08:02 3540104                    /usr/lib/x86_64-linux-gnu/libSegFault.so
    7f3ed3601000-7f3ed3603000 rw-p 00000000 00:00 0
    7f3ed3603000-7f3ed3605000 r--p 00000000 08:02 3541333                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7f3ed3605000-7f3ed362f000 r-xp 00002000 08:02 3541333                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7f3ed362f000-7f3ed363a000 r--p 0002c000 08:02 3541333                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7f3ed363b000-7f3ed363d000 r--p 00037000 08:02 3541333                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7f3ed363d000-7f3ed363f000 rw-p 00039000 08:02 3541333                    /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7ffdd6073000-7ffdd6094000 rw-p 00000000 00:00 0                          [stack]
    7ffdd6114000-7ffdd6118000 r--p 00000000 00:00 0                          [vvar]
    7ffdd6118000-7ffdd611a000 r-xp 00000000 00:00 0                          [vdso]
    ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0                  [vsyscall]
    Segmentation fault (core dumped)

..
    cspell:enable

Backtrace 内の ``./test(+0x1139)[0x56489f19b139]`` のような表記の内
括弧内の ``0x1139`` がバイナリ内の相対的なアドレスを示す。
次の節で相対的なアドレスから関数名を取り出す方法を説明する。

関数名の取得
------------------

関数名は ``addr2line`` というコマンドで取得できる。

..
    cspell:ignore binutils

.. note::
    Ubuntu 20.04, 22.04 で ``addr2line`` は apt の binutils パッケージにある。

例えば、前述の test.cpp のスタックトレースにある ``0x1139``, ``0x1154`` は
以下のようにして関数名とファイルの情報に変換できる。

.. code-block:: console

    $ addr2line -e test -f -C 0x1139 0x1154
    test(int*)
    /home/user/test.cpp:2
    main
    /home/user/test.cpp:7

- ``-e`` のあとにバイナリのパスを入力する。
- ``-f``, ``-C`` は関数名を表示するためのオプション。
- その他の引数が libSegFault.so で得られるアドレスで、複数並べることができる。
