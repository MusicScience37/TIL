Conan を用いた CMake の依存ライブラリ管理
=============================================

`Conan <https://conan.io/>`_
は C/C++ 向けのパッケージマネージャで、
プロジェクトごとの設定ファイルに書かれた通りに依存ライブラリをインストールできるほか、
パッケージを作成することもできる。

インストールしたパッケージを使用できるようにするために必要なファイルを生成する
Generator には様々な種類が存在し、
CMake, Visual Studio, QMake など様々なビルド環境で使用できる
（ `Generators — conan 1.35.2 documentation <https://docs.conan.io/en/latest/reference/generators.html>`_ ）。

ここでは、CMake で使用することを前提として導入方法について検討する。

CMake 向けの Generator
----------------------------

2021/4/25 現在、
CMake 向けの Generator には次のようなものがある
（ `CMake — conan 1.35.2 documentation <https://docs.conan.io/en/latest/integrations/build_system/cmake.html>`_ ）。

``cmake`` generator
    ``cmake`` generator を選択すると、
    conanbuildinfo.cmake というファイルが生成され、
    CMakefile.txt から次のようにインストールされたパッケージを読み込むことができる。

    .. code-block:: cmake

        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup(TARGETS)

        add_executable(timer timer.cpp)
        target_link_libraries(timer CONAN_PKG::poco)

``cmake_multi`` generator
    ``cmake_multi`` generator を選択すると、
    ``cmake`` generator と同様の CMakefile.txt で
    CMake の multi-configuration
    （Visual Studio のように Debug や Release のビルドをまとめて行うこと）
    に対応できる。

``cmake_paths`` generator
    ``cmake_paths`` generator を選択すると、
    conan_paths.cmake というファイルが生成され、
    CMakefile.txt から次のようにインストールされたパッケージを読み込むことができる。

    .. code-block:: cmake

        cmake_minimum_required(VERSION 3.0)
        project(helloworld)

        include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

        add_executable(helloworld hello.c)

        find_package(zlib)

        if(ZLIB_FOUND)
           include_directories(${ZLIB_INCLUDE_DIRS})
           target_link_libraries (helloworld ${ZLIB_LIBRARIES})
        endif()

``cmake_find_package`` generator
    ``cmake_find_package`` generator を選択すると、
    ``Find<パッケージ名>.cmake`` の形式のファイルが生成され、
    CMakefile.txt から次のようにインストールされたパッケージを読み込むことができる。

    .. code-block:: cmake

        cmake_minimum_required(VERSION 3.0)
        project(helloworld)
        # Conan が生成したファイルを正しく使用できるようにパスを追加
        list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
        list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})

        add_executable(helloworld hello.c)
        find_package(ZLIB)

        # Global approach
        if(ZLIB_FOUND)
           include_directories(${ZLIB_INCLUDE_DIRS})
           target_link_libraries (helloworld ${ZLIB_LIBRARIES})
        endif()

        # Modern CMake targets approach
        if(TARGET ZLIB::ZLIB)
           target_link_libraries(helloworld ZLIB::ZLIB)
        endif()

``cmake_find_package_multi`` generator
    ``cmake_find_package_multi`` generator は
    ``cmake_find_package`` generator を
    CMake の multi-configuration に対応させたもの。

CMakefile.txt が Conan に直接依存しない ``cmake_find_package`` generator は、
比較的容易に Conan を試すことができて良いのではないだろうか。

設定ファイル
---------------------

Conan 用の設定ファイルには次の 2 種類があり、
プロジェクトにつきいずれかの設定ファイルが必要となる。

conanfile.txt
    シンプルな設定ファイル

    .. code-block:: text

        [requires]
        poco/1.9.4
        zlib/1.2.11

        [generators]
        cmake

conanfile.py
    Python のスクリプトでクラスとして書く設定ファイル

    .. code-block:: python

        from conans import ConanFile

        class ExampleConan(ConanFile):
            requires = ("poco/1.9.4", "zlib/1.2.11")
            generators = "cmake"

conanfile.py の方が様々な設定を行うことができ、
特にパッケージを作成する場合は conanfile.py が必要となる。
conanfile.py の詳細は
`conanfile.py — conan 1.35.2 documentation <https://docs.conan.io/en/latest/reference/conanfile.html>`_
を参照。
