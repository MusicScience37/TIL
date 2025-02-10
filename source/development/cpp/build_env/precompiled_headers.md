# プリコンパイル済みヘッダの設定

プリコンパイル済みヘッダの設定をしてビルド時間を短縮する。

## CMake における設定

CMake では以下のような形式で設定を記載する。

```cmake
target_precompile_headers(<target> <PRIVATE|PUBLIC|INTERFACE> <headers>...)
```

例えば、CMake のターゲット example で
ヘッダ `<chrono>` と `<type_traits>` をコンパイル済みヘッダにすると以下のようになる。

```cmake
target_precompile_headers(example PRIVATE <chrono> <type_traits>)
```

```{note}
例のため普通の標準ライブラリのヘッダを指定しているが、
実際にはもっとビルドに影響する重いヘッダを指定する。
```

## Ccache と併用するための設定

[ccache](./ccache.rst) と併用する場合、
ccache が正しくコンパイル結果をキャッシュできるようにするため、
追加の設定が必要になる。

- 環境変数として、以下を設定する。

  ```shell
  CCACHE_SLOPPINESS=pch_defines,time_macros,include_file_mtime,include_file_ctime
  ```

- ビルド時の設定として、以下が必要となる。

  - プリコンパイル済みヘッダは `-include` オプションで指定する必要がある。

    ```{hint}
    上記の CMake の記述をしていれば `-include` オプションは自動で設定される。
    ```

  - Clang の場合、`-fno-pch-timestamp` オプションを指定する。

    CMake の場合、以下のように記載する。
    （`example` のところに CMake のターゲットの名称を記載する。）

    ```cmake
    if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        target_compile_options(example PRIVATE "$<$<COMPILE_LANGUAGE:CXX>:SHELL:-Xclang -fno-pch-timestamp>")
    endif()
    ```

## 参考

- [target_precompile_headers — CMake 3.31.5 Documentation](https://cmake.org/cmake/help/latest/command/target_precompile_headers.html)
- [ccache documentation](https://ccache.dev/manual/4.10.2.html#_precompiled_headers)
- [Ccache clang and -fno-pch-timestamp - Code - CMake Discourse](https://discourse.cmake.org/t/ccache-clang-and-fno-pch-timestamp/7253)
