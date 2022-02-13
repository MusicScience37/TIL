Clang の AddressSanitizer を有効にしたバイナリを valgrind でチェックしたらエラーになる
========================================================================================

Clang の
`AddressSanitizer <https://clang.llvm.org/docs/AddressSanitizer.html>`_
を適用したバイナリを
`valgrind <https://valgrind.org/>`_
でチェックしたところ、
次のようなエラーになった。

AddressSanitizer と valgrind を一緒に使用するのは良くないらしい。
（参考：`Workarounds for #837 (Shadow memory range interleaves with an existing memory mapping. ASan cannot proceed correctly. ABORTING.) · Issue #856 · google/sanitizers <https://github.com/google/sanitizers/issues/856>`_）

.. code-block:: console

    ==211==Shadow memory range interleaves with an existing memory mapping. ASan cannot proceed correctly. ABORTING.
    ==211==ASan shadow was supposed to be located in the [0x00007fff7000-0x10007fff7fff] range.
    ==211==This might be related to ELF_ET_DYN_BASE change in Linux 4.12.
    ==211==See https://github.com/google/sanitizers/issues/856 for possible workarounds.
    ==211==Process memory map follows:
        0x000000400000-0x000000423000    /builds/MusicScience37/numerical-collection-cpp/build_clang_asan/bin/num_collect_test_units_opt
        0x000000423000-0x00000096b000    /builds/MusicScience37/numerical-collection-cpp/build_clang_asan/bin/num_collect_test_units_opt
        0x00000096b000-0x000000e06000    /builds/MusicScience37/numerical-collection-cpp/build_clang_asan/bin/num_collect_test_units_opt
        0x000000e06000-0x000000e08000    /builds/MusicScience37/numerical-collection-cpp/build_clang_asan/bin/num_collect_test_units_opt
        0x000000e08000-0x000001175000    /builds/MusicScience37/numerical-collection-cpp/build_clang_asan/bin/num_collect_test_units_opt
        0x000001175000-0x000001aa4000
        0x000004000000-0x000004001000    /usr/lib/x86_64-linux-gnu/ld-2.31.so
        0x000004001000-0x000004024000    /usr/lib/x86_64-linux-gnu/ld-2.31.so
        0x000004024000-0x00000402c000    /usr/lib/x86_64-linux-gnu/ld-2.31.so
        0x00000402d000-0x00000402e000    /usr/lib/x86_64-linux-gnu/ld-2.31.so
        0x00000402e000-0x00000402f000    /usr/lib/x86_64-linux-gnu/ld-2.31.so
        0x00000402f000-0x000004030000
        0x000004030000-0x000004031000
        0x000004830000-0x000004832000
        0x000004832000-0x000004833000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_core-amd64-linux.so
        0x000004833000-0x000004834000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_core-amd64-linux.so
        0x000004834000-0x000004835000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_core-amd64-linux.so
        0x000004835000-0x000004836000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_core-amd64-linux.so
        0x000004836000-0x000004837000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_core-amd64-linux.so
        0x000004837000-0x00000483b000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so
        0x00000483b000-0x000004845000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so
        0x000004845000-0x000004848000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so
        0x000004848000-0x000004849000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so
        0x000004849000-0x00000484a000    /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so
        0x00000484a000-0x000004850000
        0x000004850000-0x00000485f000    /usr/lib/x86_64-linux-gnu/libm-2.31.so
        0x00000485f000-0x000004906000    /usr/lib/x86_64-linux-gnu/libm-2.31.so
        0x000004906000-0x00000499d000    /usr/lib/x86_64-linux-gnu/libm-2.31.so
        0x00000499d000-0x00000499e000    /usr/lib/x86_64-linux-gnu/libm-2.31.so
        0x00000499e000-0x00000499f000    /usr/lib/x86_64-linux-gnu/libm-2.31.so
        0x00000499f000-0x000004a35000    /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28
        0x000004a35000-0x000004b25000    /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28
        0x000004b25000-0x000004b6e000    /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28
        0x000004b6e000-0x000004b6f000    /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28
        0x000004b6f000-0x000004b7a000    /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28
        0x000004b7a000-0x000004b7d000    /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28
        0x000004b7d000-0x000004b80000
        0x000004b80000-0x000004b87000    /usr/lib/x86_64-linux-gnu/libpthread-2.31.so
        0x000004b87000-0x000004b98000    /usr/lib/x86_64-linux-gnu/libpthread-2.31.so
        0x000004b98000-0x000004b9d000    /usr/lib/x86_64-linux-gnu/libpthread-2.31.so
        0x000004b9d000-0x000004b9e000    /usr/lib/x86_64-linux-gnu/libpthread-2.31.so
        0x000004b9e000-0x000004b9f000    /usr/lib/x86_64-linux-gnu/libpthread-2.31.so
        0x000004b9f000-0x000004ba3000
        0x000004ba3000-0x000004ba6000    /usr/lib/x86_64-linux-gnu/librt-2.31.so
        0x000004ba6000-0x000004baa000    /usr/lib/x86_64-linux-gnu/librt-2.31.so
        0x000004baa000-0x000004bab000    /usr/lib/x86_64-linux-gnu/librt-2.31.so
        0x000004bab000-0x000004bac000    /usr/lib/x86_64-linux-gnu/librt-2.31.so
        0x000004bac000-0x000004bad000    /usr/lib/x86_64-linux-gnu/librt-2.31.so
        0x000004bad000-0x000004bae000    /usr/lib/x86_64-linux-gnu/librt-2.31.so
        0x000004bae000-0x000004bb0000
        0x000004bb0000-0x000004bb1000    /usr/lib/x86_64-linux-gnu/libdl-2.31.so
        0x000004bb1000-0x000004bb3000    /usr/lib/x86_64-linux-gnu/libdl-2.31.so
        0x000004bb3000-0x000004bb4000    /usr/lib/x86_64-linux-gnu/libdl-2.31.so
        0x000004bb4000-0x000004bb5000    /usr/lib/x86_64-linux-gnu/libdl-2.31.so
        0x000004bb5000-0x000004bb6000    /usr/lib/x86_64-linux-gnu/libdl-2.31.so
        0x000004bb6000-0x000004bb9000    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
        0x000004bb9000-0x000004bcb000    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
        0x000004bcb000-0x000004bcf000    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
        0x000004bcf000-0x000004bd0000    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
        0x000004bd0000-0x000004bd1000    /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
        0x000004bd1000-0x000004bf6000    /usr/lib/x86_64-linux-gnu/libc-2.31.so
        0x000004bf6000-0x000004d6e000    /usr/lib/x86_64-linux-gnu/libc-2.31.so
        0x000004d6e000-0x000004db8000    /usr/lib/x86_64-linux-gnu/libc-2.31.so
        0x000004db8000-0x000004db9000    /usr/lib/x86_64-linux-gnu/libc-2.31.so
        0x000004db9000-0x000004dbc000    /usr/lib/x86_64-linux-gnu/libc-2.31.so
        0x000004dbc000-0x000004dbf000    /usr/lib/x86_64-linux-gnu/libc-2.31.so
        0x000004dbf000-0x000005121000
        0x000005121000-0x000005521000
        0x000005521000-0x000005535000
        0x000058000000-0x000058001000    /usr/lib/x86_64-linux-gnu/valgrind/memcheck-amd64-linux
        0x000058001000-0x0000581f6000    /usr/lib/x86_64-linux-gnu/valgrind/memcheck-amd64-linux
        0x0000581f6000-0x000058294000    /usr/lib/x86_64-linux-gnu/valgrind/memcheck-amd64-linux
        0x000058294000-0x00005829a000    /usr/lib/x86_64-linux-gnu/valgrind/memcheck-amd64-linux
        0x00005829a000-0x000059c9d000
        0x001002001000-0x001002eb8000
        0x001002eb8000-0x001002eba000
        0x001002eba000-0x001002fba000
        0x001002fba000-0x001002fbc000
        0x001002fbc000-0x001002fbd000    /tmp/vgdb-pipe-shared-mem-vgdb-211-by-???-on-runner-0277ea0f-project-25109105-concurrent-0
        0x001002fbd000-0x0010033a4000
        0x0010033bd000-0x001003c4a000
        0x001003e4a000-0x00100404a000
        0x00100406c000-0x001005eb6000
        0x001005fb6000-0x0010060b6000
        0x0010063ab000-0x0010065eb000
        0x001ffeffc000-0x001fff001000
        0x7fffd2abc000-0x7fffd2adf000    [stack]
        0x7fffd2ae0000-0x7fffd2ae3000    [vvar]
        0xffffffffff600000-0xffffffffff601000    [vsyscall]
    ==211==End of process memory map.
