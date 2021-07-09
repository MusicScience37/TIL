コンパイラの Sanitizer 機能で変数の使用をチェック
==================================================

コンパイラに Sanitizer という機能があり、
変数の使用に関係する様々なチェックを行うことができる。

.. note::

    Sanitize とは

        To sanitize an activity or a situation that is unpleasant or unacceptable
        means to describe it in a way
        that makes it seem more pleasant or more acceptable.

        -- from Collins COBUILD, Advanced Learner's Dictionary, 9th Edition.

    「改善する」くらいの意味合い？

GCC のオプション
------------------------

`Instrumentation Options (Using the GNU Compiler Collection (GCC)) <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>`_
によると、``-fsanitize=<type>`` のような形式で Sanitizer の指定ができる。
``<type>`` には以下のような種類の Sanitizer を指定できる。

.. list-table:: GCC の Sanitizer
    :widths: auto
    :header-rows: 1

    - - Sanitizer
      - 内容
      - 併用できない Sanitizer
    - - address
      - メモリのチェック。領域外の参照や解放後のメモリの参照など。
      - thread, hwaddress
    - - kernrl-address
      - Linux Kernel 用のメモリチェック。
      -
    - - hwaddress
      - ハードウェアによるメモリのチェック。オーバーヘッドが少ないが、AArch64 でしか利用できない。
      - thread, address
    - - kernell-hwaddress
      - ハードウェアによる Linux Kernrl のメモリのチェック。オーバーヘッドが少ないが、AArch64 でしか利用できない。
      -
    - - pointer-compare
      - ポインタの比較に処理を追加する。kernel-address, address と併用する必要がある。
        チェックを実際に動作させるには、プログラム実行時に ``ASAN_OPTIONS`` 環境変数に ``detect_invalid_pointer_pairs=2`` を追加する。
      -
    - - pointer-subtract
      - ポインタの減算に処理を追加する。kernel-address, address と併用する必要がある。
        チェックを実際に動作させるには、プログラム実行時に ``ASAN_OPTIONS`` 環境変数に ``detect_invalid_pointer_pairs=2`` を追加する。
      -
    - - thread
      - データ競合の検知。メモリへのアクセスの処理に細工をする。
      - address, leak
    - - leak
      - メモリリークの検知。リンクする ``malloc`` 関数を置き換える。
      - thread
    - - undefined
      - 未定義動作の検知。
      -

併用できない Sanitizer が存在するため、全て有効化するようなオプションは存在しない。

Clang のオプション
------------------------

`Clang Compiler User’s Manual — Clang 13 documentation <https://clang.llvm.org/docs/UsersManual.html#controlling-code-generation>`_
によると、``-fsanitize=<type1>,<type2>,...`` のような形式で Sanitizer の指定ができる。
``<type>`` には以下のような種類の Sanitizer を指定できる。

.. list-table:: Clang の Sanitizer
    :widths: auto
    :header-rows: 1

    - - Sanitizer
      - 内容
      - 併用できない Sanitizer
    - - address
      - `AddressSanitizer <https://clang.llvm.org/docs/AddressSanitizer.html>`_.
        範囲外アクセス、解放後のメモリアクセス、return 後のアクセス、スコープ外でのアクセス、
        二重解放、不正な解放、メモリリークのチェック。
      - thread, memory
    - - thread
      - `ThreadSanitizer <https://clang.llvm.org/docs/ThreadSanitizer.html>`_.
        データ競合のチェック。
      - address, memory
    - - memory
      - `MemorySanitizer <https://clang.llvm.org/docs/MemorySanitizer.html>`_.
        未初期化のメモリへのアクセスのチェック。
      - address, memory
    - - undefined
      - `UndefinedBehaviorSanitizer <https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html>`_.
        未定義動作のチェック。
      -
    - - dataflow
      - `DataFlowSanitizer <https://clang.llvm.org/docs/DataFlowSanitizer.html>`_.
        データフローの解析。ソースコード中でタグをつけたデータの流れを補足する。
      -
    - - cfi
      - `Control Flow Integrity <https://clang.llvm.org/docs/ControlFlowIntegrity.html>`_.
        制御フローを奪えるような未定義動作を検出する。
        ``-flto`` オプション（link-time optimization）を有効にする必要がある。
      -
    - - safe-stack
      - `SafeStack <https://clang.llvm.org/docs/SafeStack.html>`_.
        スタックバッファーオーバーフローによる攻撃から守る。
      -

Visual Studio のオプション
------------------------------

`/fsanitize (Enable sanitizers) | Microsoft Docs <https://docs.microsoft.com/en-us/cpp/build/reference/fsanitize?view=msvc-160>`_
によると、``/fsanitize=address`` のような形式で
`Address Sanitizer <https://docs.microsoft.com/en-us/cpp/sanitizers/asan?view=msvc-160>`_
を有効化できる。
他の Sanitizer はない。
AddressSanitizer は

- メモリの取得・解放の矛盾
- 極端に大きなメモリ取得
- calloc/alloca のオーバーフロー
- 二重解放
- 解放後のメモリ使用
- グローバル変数のオーバーフロー
- ヒープバッファーオーバーフロー
- align された変数の不正な alignment
- memcpy/strncat のオーバーラップ
- スタックバッファーオーバーフロー／アンダーフロー
- return 後のスタック使用
- スコープ外のメモリアクセス
- 不正なメモリアクセス

などをチェックする。

例
------------

Clang による範囲外アクセスの検出
``````````````````````````````````

ソースコード：`test-cpp-sanitizer <https://gitlab.com/MusicScience37/test-cpp-sanitizer>`_

次のような C++ のソースコードを準備した。

.. code-block:: c++

    #include <vector>

    int main() {
        constexpr std::size_t size = 128;
        auto vec = std::vector<double>(size);
        vec[size] = 0; // ギリギリ範囲外
        return 0;
    }

次のようにオプション付きでコンパイルした。

.. code-block:: cmake

    add_executable(test_ouf_of_bound out_of_bound.cpp)
    target_compile_options(test_ouf_of_bound PRIVATE -fsanitize=address)
    target_link_options(test_ouf_of_bound PRIVATE -fsanitize=address)

実行すると次のようになった。

.. code-block:: console

    $ ./build/Debug/bin/test_ouf_of_bound
    =================================================================
    ==589927==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x619000000480 at pc 0x0000004cb0d5 bp 0x7ffde99a1070 sp 0x7ffde99a1068
    WRITE of size 8 at 0x619000000480 thread T0
        #0 0x4cb0d4 in main /home/<user>/projects/test/test-cpp-sanitizer/build/Debug/../../out_of_bound.cpp:30:15
        #1 0x7fbef5a440b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16
        #2 0x41c30d in _start (/home/<user>/projects/test/test-cpp-sanitizer/build/Debug/bin/test_ouf_of_bound+0x41c30d)

    0x619000000480 is located 0 bytes to the right of 1024-byte region [0x619000000080,0x619000000480)
    allocated by thread T0 here:
        #0 0x4c867d in operator new(unsigned long) /home/brian/src/llvm_releases/llvm-project/llvm/utils/release/final/llvm-project/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
        #1 0x4cbe0b in __gnu_cxx::new_allocator<double>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-linux-gnu/9/../../../../include/c++/9/ext/new_allocator.h:114:27
        #2 0x4cbdb0 in std::allocator_traits<std::allocator<double> >::allocate(std::allocator<double>&, unsigned long) /usr/lib/gcc/x86_64-linux-gnu/9/../../../../include/c++/9/bits/alloc_traits.h:444:20
        #3 0x4cbd6f in std::_Vector_base<double, std::allocator<double> >::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/9/../../../../include/c++/9/bits/stl_vector.h:343:20
        #4 0x4cbb70 in std::_Vector_base<double, std::allocator<double> >::_M_create_storage(unsigned long) /usr/lib/gcc/x86_64-linux-gnu/9/../../../../include/c++/9/bits/stl_vector.h:358:33
        #5 0x4cb614 in std::_Vector_base<double, std::allocator<double> >::_Vector_base(unsigned long, std::allocator<double> const&) /usr/lib/gcc/x86_64-linux-gnu/9/../../../../include/c++/9/bits/stl_vector.h:302:9
        #6 0x4cb2b8 in std::vector<double, std::allocator<double> >::vector(unsigned long, std::allocator<double> const&) /usr/lib/gcc/x86_64-linux-gnu/9/../../../../include/c++/9/bits/stl_vector.h:508:9
        #7 0x4cb092 in main /home/<user>/projects/test/test-cpp-sanitizer/build/Debug/../../out_of_bound.cpp:29:16
        #8 0x7fbef5a440b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

    SUMMARY: AddressSanitizer: heap-buffer-overflow /home/<user>/projects/test/test-cpp-sanitizer/build/Debug/../../out_of_bound.cpp:30:15 in main
    Shadow bytes around the buggy address:
      0x0c327fff8040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      0x0c327fff8050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      0x0c327fff8060: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      0x0c327fff8070: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      0x0c327fff8080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    =>0x0c327fff8090:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
      0x0c327fff80a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
      0x0c327fff80b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
      0x0c327fff80c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
      0x0c327fff80d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
      0x0c327fff80e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
    Shadow byte legend (one shadow byte represents 8 application bytes):
      Addressable:           00
      Partially addressable: 01 02 03 04 05 06 07
      Heap left redzone:       fa
      Freed heap region:       fd
      Stack left redzone:      f1
      Stack mid redzone:       f2
      Stack right redzone:     f3
      Stack after return:      f5
      Stack use after scope:   f8
      Global redzone:          f9
      Global init order:       f6
      Poisoned by user:        f7
      Container overflow:      fc
      Array cookie:            ac
      Intra object redzone:    bb
      ASan internal:           fe
      Left alloca redzone:     ca
      Right alloca redzone:    cb
      Shadow gap:              cc
    ==589927==ABORTING

.. note::

    なお、オプションなしで実行してみたところ、
    何も表示されずに終了ステータス 0 で終了した。
    ぎりぎり範囲外くらいでは Debug ビルドでも検出してくれない場合があるということになる。
    急がない処理のときはなるべく ``at`` 関数を使用し、
    範囲外アクセスは例外を投げさせるようにしよう。
