libSegFault.so
==================

libSegFault.so は
プロセスが Segmentation Fault で終わった際にトレースバックを表示するライブラリ。

Ubuntu の場合
---------------

Ubuntu では apt のパッケージ gcc の依存パッケージの一部としてインストールされる。

.. note::

    Ubuntu 20.04 では、
    gcc の依存パッケージに gcc-9 があり、
    gcc-9 の依存パッケージに libc6 があり、
    libc6 内に ``/lib/x86_64-linux-gnu/libSegFault.so`` がある。

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

    $ g++ -g -O test.cpp -o test

これを普通に実行すると、次のようになる。

.. code-block:: console

    $ ./test
    Segmentation fault

libSegFault.so をロードするようにすると、次のようになる。

..
    cspell:disable

.. code-block:: console

    $ LD_PRELOAD=/lib/x86_64-linux-gnu/libSegFault.so ./test
    *** Segmentation fault
    Register dump:

     RAX: 000055fb5ddf8134   RBX: 000055fb5ddf8150   RCX: 000055fb5ddf8150
     RDX: 00007ffeb0ce2ea8   RSI: 00007ffeb0ce2e98   RDI: 0000000000000001
     RBP: 0000000000000000   R8 : 0000000000000000   R9 : 00007fc691b73d50
     R10: 0000000000000008   R11: 0000000000000246   R12: 000055fb5ddf8040
     R13: 00007ffeb0ce2e90   R14: 0000000000000000   R15: 0000000000000000
     RSP: 00007ffeb0ce2da8

     RIP: 000055fb5ddf8138   EFLAGS: 00010246

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
    ./test(+0x1138)[0x55fb5ddf8138]
    /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf3)[0x7fc6919810b3]
    ./test(+0x106e)[0x55fb5ddf806e]

    Memory map:

    55fb5ddf7000-55fb5ddf8000 r--p 00000000 08:10 100431                     /home/kenta/doc/til/test
    55fb5ddf8000-55fb5ddf9000 r-xp 00001000 08:10 100431                     /home/kenta/doc/til/test
    55fb5ddf9000-55fb5ddfa000 r--p 00002000 08:10 100431                     /home/kenta/doc/til/test
    55fb5ddfa000-55fb5ddfb000 r--p 00002000 08:10 100431                     /home/kenta/doc/til/test
    55fb5ddfb000-55fb5ddfc000 rw-p 00003000 08:10 100431                     /home/kenta/doc/til/test
    55fb5de46000-55fb5de67000 rw-p 00000000 00:00 0                          [heap]
    7fc69193c000-7fc69193f000 r--p 00000000 08:10 24385                      /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7fc69193f000-7fc691951000 r-xp 00003000 08:10 24385                      /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7fc691951000-7fc691955000 r--p 00015000 08:10 24385                      /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7fc691955000-7fc691956000 r--p 00018000 08:10 24385                      /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7fc691956000-7fc691957000 rw-p 00019000 08:10 24385                      /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
    7fc691957000-7fc69195a000 rw-p 00000000 00:00 0
    7fc69195a000-7fc69197f000 r--p 00000000 08:10 11971                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fc69197f000-7fc691af7000 r-xp 00025000 08:10 11971                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fc691af7000-7fc691b41000 r--p 0019d000 08:10 11971                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fc691b41000-7fc691b42000 ---p 001e7000 08:10 11971                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fc691b42000-7fc691b45000 r--p 001e7000 08:10 11971                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fc691b45000-7fc691b48000 rw-p 001ea000 08:10 11971                      /usr/lib/x86_64-linux-gnu/libc-2.31.so
    7fc691b48000-7fc691b4c000 rw-p 00000000 00:00 0
    7fc691b59000-7fc691b5a000 r--p 00000000 08:10 11875                      /usr/lib/x86_64-linux-gnu/libSegFault.so
    7fc691b5a000-7fc691b5d000 r-xp 00001000 08:10 11875                      /usr/lib/x86_64-linux-gnu/libSegFault.so
    7fc691b5d000-7fc691b5e000 r--p 00004000 08:10 11875                      /usr/lib/x86_64-linux-gnu/libSegFault.so
    7fc691b5e000-7fc691b5f000 r--p 00004000 08:10 11875                      /usr/lib/x86_64-linux-gnu/libSegFault.so
    7fc691b5f000-7fc691b60000 rw-p 00005000 08:10 11875                      /usr/lib/x86_64-linux-gnu/libSegFault.so
    7fc691b60000-7fc691b62000 rw-p 00000000 00:00 0
    7fc691b62000-7fc691b63000 r--p 00000000 08:10 11854                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fc691b63000-7fc691b86000 r-xp 00001000 08:10 11854                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fc691b86000-7fc691b8e000 r--p 00024000 08:10 11854                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fc691b8f000-7fc691b90000 r--p 0002c000 08:10 11854                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fc691b90000-7fc691b91000 rw-p 0002d000 08:10 11854                      /usr/lib/x86_64-linux-gnu/ld-2.31.so
    7fc691b91000-7fc691b92000 rw-p 00000000 00:00 0
    7ffeb0cc4000-7ffeb0ce6000 rw-p 00000000 00:00 0                          [stack]
    7ffeb0d5b000-7ffeb0d5e000 r--p 00000000 00:00 0                          [vvar]
    7ffeb0d5e000-7ffeb0d5f000 r-xp 00000000 00:00 0                          [vdso]
    Segmentation fault

..
    cspell:enable
