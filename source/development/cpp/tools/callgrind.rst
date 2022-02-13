Callgrind によるプロファイリング
=====================================

Callgrind は
`Valgrind <https://valgrind.org/>`_
の一部として提供されているプロファイリングのツール。

インストール
-------------------

- Valgrind のインストール

  .. code:: bash

      sudo apt install valgrind

- kcachegrind のインストール（GUI で結果を確認する場合）

  .. code:: bash

      sudo apt install kcachegrind

測定
-----------

Callgrind によるプロファイリングの情報の測定は次のコマンドで行う。

.. code:: bash

    valgrind --tool=callgrind <command>

``<command>`` にプロファイリングするバイナリのパスとコマンドライン引数を入力する。
バイナリはデバッグ情報付きでビルドしておく。
（CMake の RelWithDebInfo とか。）

実行が完了すると、``callgrind.out.<プロセスID>`` 形式の名前のファイルが 1 つ生成される。

コンソール上での結果の確認
--------------------------------

コンソール上で次のようなコマンドで結果を確認することができる。

.. code:: bash

    callgrind_annotate callgrind.out.<プロセスID>

例
----

.. code:: console

    $ callgrind_annotate callgrind.out.84308
    --------------------------------------------------------------------------------
    Profile data file 'callgrind.out.84308' (creator: callgrind-3.15.0)
    --------------------------------------------------------------------------------
    I1 cache:
    D1 cache:
    LL cache:
    Timerange: Basic block 0 - 119895512
    Trigger: Program termination
    Profiled target:  ./bin/num_collect_ex_adaptive_diagonal_curves (PID 84308, part 1)
    Events recorded:  Ir
    Events shown:     Ir
    Event sort order: Ir
    Thresholds:       99
    Include dirs:
    User annotated:
    Auto-annotation:  off

    --------------------------------------------------------------------------------
    Ir
    --------------------------------------------------------------------------------
    614,100,382  PROGRAM TOTALS

    --------------------------------------------------------------------------------
    Ir          file:function
    --------------------------------------------------------------------------------
    96,255,222  ../../include/num_collect/opt/impl/ternary_vector.h:num_collect::opt::impl::ternary_vector::operator==(num_collect::opt::impl::ternary_vector const&) const [/home/kenta/projects/science/numerical-collection-cpp/build/RelWithDebInfo/bin/num_collect_ex_adaptive_diagonal_curves]
    52,667,246  ../../include/num_collect/opt/impl/ternary_vector.h:std::_Hashtable<num_collect::opt::impl::ternary_vector, std::pair<num_collect::opt::impl::ternary_vector const, double>, std::allocator<std::pair<num_collect::opt::impl::ternary_vector const, double> >, std::__detail::_Select1st, std::equal_to<num_collect::opt::impl::ternary_vector>, std::hash<num_collect::opt::impl::ternary_vector>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<true, false, true> >::find(num_collect::opt::impl::ternary_vector const&)
    34,880,787  ../../include/num_collect/opt/adaptive_diagonal_curves.h:num_collect::opt::impl::adc_rectangle<double>::determine_sample_points(num_collect::opt::impl::ternary_vector const&) [/home/kenta/projects/science/numerical-collection-cpp/build/RelWithDebInfo/bin/num_collect_ex_adaptive_diagonal_curves]
    31,029,712  /build/glibc-eX1tMB/glibc-2.31/malloc/malloc.c:_int_free [/usr/lib/x86_64-linux-gnu/libc-2.31.so]
    20,329,788  /build/glibc-eX1tMB/glibc-2.31/malloc/malloc.c:malloc [/usr/lib/x86_64-linux-gnu/libc-2.31.so]
    19,077,485  /build/glibc-eX1tMB/glibc-2.31/malloc/malloc.c:_int_malloc [/usr/lib/x86_64-linux-gnu/libc-2.31.so]
    14,030,352  ???:_ZZN3fmt2v86detail10vformat_toIcEEvRNS1_6bufferIT_EENS0_17basic_string_viewIS4_EENS0_17basic_format_argsINS0_20basic_format_contextINSt11conditionalIXsr3std7is_sameINS0_13type_identityIS4_E4typeEcEE5valueENS0_8appenderESt20back_insert_iteratorINS3_ISE_EEEE4typeESE_EEEENS1_10locale_refEEN14format_handler15on_format_specsEiPKcSQ_ [/home/kenta/projects/science/numerical-collection-cpp/build/RelWithDebInfo/bin/num_collect_ex_adaptive_diagonal_curves]
    13,406,838  ???:void fmt::v8::detail::for_each_codepoint<fmt::v8::detail::compute_width(fmt::v8::basic_string_view<char>)::count_code_points>(fmt::v8::basic_string_view<char>, fmt::v8::detail::compute_width(fmt::v8::basic_string_view<char>)::count_code_points)::{lambda(char const*) [/home/kenta/projects/science/numerical-collection-cpp/build/RelWithDebInfo/bin/num_collect_ex_adaptive_diagonal_curves]
    12,812,896  ???:std::_Hash_bytes(void const*, unsigned long, unsigned long) [/usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28]
    12,548,630  /build/glibc-eX1tMB/glibc-2.31/libio/fileops.c:_IO_file_xsputn@@GLIBC_2.2.5 [/usr/lib/x86_64-linux-gnu/libc-2.31.so]

    （以下省略）

kcachegrind による結果の確認
-----------------------------------

GUI で結果を確認するには、次のコマンドを実行する。

.. code:: bash

    kcachegrind callgrind.out.<プロセスID>

コマンドを実行すると、GUI の画面が起動する。

.. image:: callgrind_kcachegrind.*
